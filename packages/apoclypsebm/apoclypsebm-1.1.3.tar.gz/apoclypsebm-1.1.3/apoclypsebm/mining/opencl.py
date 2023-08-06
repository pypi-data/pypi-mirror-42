import pkgutil
import sys
from hashlib import md5
from queue import Empty
from struct import error, pack, unpack
from threading import Lock
from time import sleep, time

from apoclypsebm.detect import MACOSX
from apoclypsebm.log import say_line
from apoclypsebm.mining.base import Miner
from apoclypsebm.sha256 import calculateF, partial
from apoclypsebm.util import (Object, bytearray_to_uint32, bytereverse,
                              tokenize, uint32, uint32_as_bytes)

PYOPENCL = False
OPENCL = False
ADL = False

try:
    import pyopencl as cl

    PYOPENCL = True
except ImportError:
    print('\nNo PyOpenCL\n')

if PYOPENCL:
    try:
        platforms = cl.get_platforms()
        if len(platforms):
            OPENCL = True
        else:
            print('\nNo OpenCL platforms\n')
    except Exception:
        print('\nNo OpenCL\n')


def vectors_definition():
    if MACOSX:
        return '-D VECTORS'
    return '-DVECTORS'


def is_amd(platform):
    if 'amd' in platform.name.lower():
        return True
    return False


def has_amd():
    for platform in cl.get_platforms():
        if is_amd(platform):
            return True
    return False


if OPENCL:
    try:
        from adl3 import ADL_Main_Control_Create, ADL_Main_Memory_Alloc, \
            ADL_Main_Control_Destroy, \
            ADLTemperature, ADL_Overdrive5_Temperature_Get, \
            ADL_Adapter_NumberOfAdapters_Get, \
            AdapterInfo, LPAdapterInfo, ADL_Adapter_AdapterInfo_Get, \
            ADL_Adapter_ID_Get, \
            ADL_OK
        from ctypes import sizeof, byref, c_int, cast
        from collections import namedtuple

        if ADL_Main_Control_Create(ADL_Main_Memory_Alloc, 1) != ADL_OK:
            print("\nCouldn't initialize ADL interface.\n")
        else:
            ADL = True
            adl_lock = Lock()
    except ImportError:
        if has_amd():
            print('\nWARNING: no adl3 module found (github.com/mjmvisser/adl3),'
                  'temperature control is disabled\n')
    except OSError:  # if no ADL is present i.e. no AMD platform
        print('\nWARNING: ADL missing (no AMD platform?), temperature control'
              'is disabled\n')
else:
    print("\nNot using OpenCL\n")


def shutdown():
    if ADL:
        ADL_Main_Control_Destroy()


def initialize(options):
    if not OPENCL:
        options.no_ocl = True
        return []

    options.worksize = tokenize(options.worksize, 'worksize')
    options.frames = tokenize(options.frames, 'frames', [30])
    options.frameSleep = tokenize(options.frameSleep, 'frameSleep', cast=float)
    options.vectors = [True] if options.old_vectors else tokenize(
        options.vectors, 'vectors', [False], bool)

    platforms = cl.get_platforms()

    if options.platform >= len(platforms) or (
            options.platform == -1 and len(platforms) > 1):
        print('Wrong platform or more than one OpenCL platforms found, use'
              '--platform to select one of the following\n')
        for i in range(len(platforms)):
            print('[%d]\t%s' % (i, platforms[i].name))
        sys.exit()

    if options.platform == -1:
        options.platform = 0

    devices = platforms[options.platform].get_devices()

    if not options.device and devices:
        print('\nOpenCL devices:\n')
        for i in range(len(devices)):
            print('[%d]\t%s' % (i, devices[i].name))
        print('\nNo devices specified, using all GPU devices\n')

    miners = [
        OpenCLMiner(i, options)
        for i in range(len(devices))
        if ((not options.device
             and devices[i].type == cl.device_type.GPU)
             or (i in options.device))
    ]

    for i in range(len(miners)):
        miner = miners[i]
        miner.worksize = options.worksize[min(i, len(options.worksize) - 1)]
        miner.frames = options.frames[min(i, len(options.frames) - 1)]
        miner.frameSleep = options.frameSleep[
            min(i, len(options.frameSleep) - 1)]
        miner.vectors = options.vectors[min(i, len(options.vectors) - 1)]
        miner.cutoff_temp = options.cutoff_temp[
            min(i, len(options.cutoff_temp) - 1)]
        miner.cutoff_interval = options.cutoff_interval[
            min(i, len(options.cutoff_interval) - 1)]
    return miners


class OpenCLMiner(Miner):
    def __init__(self, device_index, options):
        super(OpenCLMiner, self).__init__(device_index, options)
        self.output_size = 0x100

        self.device = (
            cl.get_platforms()[options.platform].get_devices()[device_index]
        )
        self.device_name = self.device.name.strip('\r\n \x00\t')
        self.frames = 30

        self.worksize = self.frameSleep = self.rate = self.estimated_rate = 0
        self.vectors = False

        self.adapterIndex = None
        if (ADL and
                is_amd(self.device.platform)
                and self.device.type == cl.device_type.GPU):
            with adl_lock:
                self.adapterIndex = self.get_adapter_info()
                if self.adapterIndex:
                    self.adapterIndex = (self.adapterIndex[self.device_index].
                                         iAdapterIndex)

    def id(self):
        return str(self.options.platform) + ':' + str(
            self.device_index) + ':' + self.device_name

    def nonce_generator(self, nonces):
        for i in range(0, len(nonces) - 4, 4):
            nonce = bytearray_to_uint32(nonces[i:i + 4])
            if nonce:
                yield nonce

    def mining_thread(self):
        say_line('started OpenCL miner on platform %d, device %d (%s)',
                 (self.options.platform, self.device_index, self.device_name))

        (self.defines, rate_divisor, hashspace) = (
        vectors_definition(), 500, 0x7FFFFFFF) if self.vectors else (
        '', 1000, 0xFFFFFFFF)
        self.defines += (' -DOUTPUT_SIZE=' + str(self.output_size))
        self.defines += (' -DOUTPUT_MASK=' + str(self.output_size - 1))

        self.load_kernel()
        frame = 1.0 / max(self.frames, 3)
        unit = self.worksize * 256
        global_threads = unit * 10

        queue = cl.CommandQueue(self.context)

        last_rated_pace = last_rated = last_n_time = last_temperature = time()
        base = last_hash_rate = threads_run_pace = threads_run = 0
        output = bytearray((self.output_size + 1) * 4)
        output_buffer = cl.Buffer(self.context,
                                  cl.mem_flags.WRITE_ONLY |
                                  cl.mem_flags.USE_HOST_PTR,
                                  hostbuf=output)
        self.kernel.set_arg(20, output_buffer)

        work = None
        temperature = 0
        while True:
            if self.should_stop:
                return

            sleep(self.frameSleep)

            if (not work) or (not self.work_queue.empty()):
                try:
                    work = self.work_queue.get(True, 1)
                except Empty:
                    continue
                else:
                    if not work:
                        continue
                    nonces_left = hashspace
                    state = work.state
                    f = [0] * 8
                    state2 = partial(state, work.merkle_end, work.time,
                                     work.difficulty, f)
                    calculateF(state, work.merkle_end, work.time,
                               work.difficulty, f, state2)

                    set_arg = self.kernel.set_arg
                    set_arg(0, uint32_as_bytes(state[0]))
                    set_arg(1, uint32_as_bytes(state[1]))
                    set_arg(2, uint32_as_bytes(state[2]))
                    set_arg(3, uint32_as_bytes(state[3]))
                    set_arg(4, uint32_as_bytes(state[4]))
                    set_arg(5, uint32_as_bytes(state[5]))
                    set_arg(6, uint32_as_bytes(state[6]))
                    set_arg(7, uint32_as_bytes(state[7]))

                    set_arg(8, uint32_as_bytes(state2[1]))
                    set_arg(9, uint32_as_bytes(state2[2]))
                    set_arg(10, uint32_as_bytes(state2[3]))
                    set_arg(11, uint32_as_bytes(state2[5]))
                    set_arg(12, uint32_as_bytes(state2[6]))
                    set_arg(13, uint32_as_bytes(state2[7]))

                    set_arg(15, uint32_as_bytes(f[0]))
                    set_arg(16, uint32_as_bytes(f[1]))
                    set_arg(17, uint32_as_bytes(f[2]))
                    set_arg(18, uint32_as_bytes(f[3]))
                    set_arg(19, uint32_as_bytes(f[4]))

            if temperature < self.cutoff_temp:
                self.kernel.set_arg(14, uint32_as_bytes(base))
                cl.enqueue_nd_range_kernel(queue, self.kernel,
                                           (global_threads,), (self.worksize,))

                nonces_left -= global_threads
                threads_run_pace += global_threads
                threads_run += global_threads
                base = uint32(base + global_threads)
            else:
                threads_run_pace = 0
                last_rated_pace = time()
                sleep(self.cutoff_interval)

            now = time()
            if self.adapterIndex != None:
                t = now - last_temperature
                if temperature >= self.cutoff_temp or t > 1:
                    last_temperature = now
                    with adl_lock:
                        temperature = self.get_temperature()

            t = now - last_rated_pace
            if t > 1:
                rate = (threads_run_pace / t) / rate_divisor
                last_rated_pace = now
                threads_run_pace = 0
                r = last_hash_rate / rate
                if r < 0.9 or r > 1.1:
                    global_threads = max(
                        unit * int((rate * frame * rate_divisor) / unit), unit)
                    last_hash_rate = rate

            t = now - last_rated
            if t > self.options.rate:
                self.update_rate(now, threads_run, t, work.targetQ,
                                 rate_divisor)
                last_rated = now
                threads_run = 0

            queue.finish()
            cl.enqueue_copy(queue, output_buffer, output)
            queue.finish()

            if output[-1]:
                result = Object()
                result.header = work.header
                result.merkle_end = work.merkle_end
                result.time = work.time
                result.difficulty = work.difficulty
                result.target = work.target
                result.state = list(state)
                result.nonces = output[:]
                result.job_id = work.job_id
                result.extranonce2 = work.extranonce2
                result.transactions = work.transactions
                result.server = work.server
                result.miner = self
                self.switch.put(result)
                output[:] = b'\x00' * len(output)
                cl.enqueue_copy(queue, output, output_buffer)

            if not self.switch.update_time:
                if nonces_left < 3 * global_threads * self.frames:
                    self.update = True
                    nonces_left += 0xFFFFFFFFFFFF
                elif 0xFFFFFFFFFFF < nonces_left < 0xFFFFFFFFFFFF:
                    say_line('warning: job finished, %s is idle', self.id())
                    work = None
            elif now - last_n_time > 1:
                work.time = bytereverse(bytereverse(work.time) + 1)
                state2 = partial(state, work.merkle_end, work.time,
                                 work.difficulty, f)
                calculateF(state, work.merkle_end, work.time, work.difficulty,
                           f, state2)
                set_arg = self.kernel.set_arg
                set_arg(8, uint32_as_bytes(state2[1]))
                set_arg(9, uint32_as_bytes(state2[2]))
                set_arg(10, uint32_as_bytes(state2[3]))
                set_arg(11, uint32_as_bytes(state2[5]))
                set_arg(12, uint32_as_bytes(state2[6]))
                set_arg(13, uint32_as_bytes(state2[7]))
                set_arg(15, uint32_as_bytes(f[0]))
                set_arg(16, uint32_as_bytes(f[1]))
                set_arg(17, uint32_as_bytes(f[2]))
                set_arg(18, uint32_as_bytes(f[3]))
                set_arg(19, uint32_as_bytes(f[4]))
                last_n_time = now
                self.update_time_counter += 1
                if self.update_time_counter >= self.switch.max_update_time:
                    self.update = True
                    self.update_time_counter = 1

    def load_kernel(self):
        self.context = cl.Context([self.device], None, None)
        if self.device.extensions.find('cl_amd_media_ops') != -1:
            self.defines += ' -DBITALIGN'
            if self.device_name in ('Cedar', 'Redwood', 'Juniper', 'Cypress',
                                    'Hemlock', 'Caicos', 'Turks', 'Barts',
                                    'Cayman', 'Antilles', 'Wrestler',
                                    'Zacate', 'WinterPark', 'BeaverCreek'):
                self.defines += ' -DBFI_INT'

        kernel = pkgutil.get_data('apoclypsebm', 'apoclypse0.cl')
        m = md5(
            b''.join(
                (
                    self.device.platform.name.encode('utf-8'),
                    self.device.platform.version.encode('utf-8'),
                    self.device.name.encode('utf-8'),
                    self.defines.encode('utf-8'),
                    kernel
                )
            )
        )
        cache_name = '%s.elf' % m.hexdigest()
        binary = None
        try:
            binary = open(cache_name, 'rb')
            self.program = cl.Program(self.context, [self.device],
                                      [binary.read()]).build(self.defines)
        except (IOError, cl.LogicError):
            kernel = kernel.decode('ascii')
            self.program = cl.Program(self.context, kernel).build(self.defines)
            if self.defines.find('-DBFI_INT') != -1:
                patched_binary = self.patch(self.program.binaries[0])
                self.program = cl.Program(self.context,
                                          [self.device],
                                          [patched_binary]).build(self.defines)
            with open(cache_name, 'wb') as binary_w:
                binary_w.write(self.program.binaries[0])
        finally:
            if binary:
                binary.close()

        self.kernel = self.program.search

        if not self.worksize:
            self.worksize = self.kernel.get_work_group_info(
                cl.kernel_work_group_info.WORK_GROUP_SIZE, self.device)

    def get_temperature(self):
        temperature = ADLTemperature()
        temperature.iSize = sizeof(temperature)

        if ADL_Overdrive5_Temperature_Get(self.adapterIndex, 0,
                                          byref(temperature)) == ADL_OK:
            return temperature.iTemperature / 1000.0
        return 0

    def get_adapter_info(self):
        adapter_info = []
        num_adapters = c_int(-1)
        if ADL_Adapter_NumberOfAdapters_Get(byref(num_adapters)) != ADL_OK:
            say_line(
                "ADL_Adapter_NumberOfAdapters_Get failed, cutoff temperature"
                "disabled for %s",
                self.id()
            )
            return

        AdapterInfoArray = (AdapterInfo * num_adapters.value)()

        if ADL_Adapter_AdapterInfo_Get(cast(AdapterInfoArray, LPAdapterInfo),
                                       sizeof(AdapterInfoArray)) != ADL_OK:
            say_line(
                "ADL_Adapter_AdapterInfo_Get failed, "
                "cutoff temperature disabled for %s",
                self.id()
            )
            return

        deviceAdapter = namedtuple(
            'DeviceAdapter',
            ('AdapterIndex', 'AdapterID', 'BusNumber', 'UDID'))

        devices = []
        for adapter in AdapterInfoArray:
            index = adapter.iAdapterIndex
            busNum = adapter.iBusNumber
            udid = adapter.strUDID

            adapterID = c_int(-1)

            if ADL_Adapter_ID_Get(index, byref(adapterID)) != ADL_OK:
                say_line(
                    "ADL_Adapter_ID_Get failed, "
                    "cutoff temperature disabled for %s",
                    self.id()
                )
                return

            found = False
            for device in devices:
                if device.AdapterID.value == adapterID.value:
                    found = True
                    break

            if found is False:
                devices.append(deviceAdapter(index, adapterID, busNum, udid))

        for device in devices:
            adapter_info.append(AdapterInfoArray[device.AdapterIndex])

        return adapter_info

    def patch(self, data):
        pos = data.find('\x7fELF', 1)
        if pos != -1 and data.find('\x7fELF', pos + 1) == -1:
            data2 = data[pos:]
            try:
                (id, a, b, c, d, e, f, offset, g, h, i, j, entrySize, count,
                 index) = unpack('QQHHIIIIIHHHHHH', data2[:52])
                if id == 0x64010101464c457f and offset != 0:
                    (a, b, c, d, nameTableOffset, size, e, f, g, h) = unpack(
                        'IIIIIIIIII',
                        data2[offset + index * entrySize:
                              offset + (index + 1) * entrySize]
                    )
                    header = data2[offset:offset + count * entrySize]
                    first_text = True
                    for i in range(count):
                        entry = header[i * entrySize:(i + 1) * entrySize]
                        (nameIndex, a, b, c, offset, size, d, e, f, g) = unpack(
                            'IIIIIIIIII', entry)
                        name_offset = nameTableOffset + nameIndex
                        name = data2[name_offset:
                                     data2.find('\x00', name_offset)]
                        if name == '.text':
                            if first_text:
                                first_text = False
                            else:
                                data2 = data2[offset:offset + size]
                                patched = ''
                                for j in range(len(data2) // 8):
                                    instruction, = unpack('Q',
                                                          data2[j * 8:
                                                                j * 8 + 8])
                                    if ((instruction & 0x9003f00002001000) ==
                                            0x0001a00000000000):
                                        instruction ^= (0x0001a00000000000
                                                        ^
                                                        0x0000c00000000000)
                                    patched += pack('Q', instruction)
                                return ''.join([data[:pos + offset], patched,
                                                data[pos + offset + size:]])
            except error:
                pass
        return data
