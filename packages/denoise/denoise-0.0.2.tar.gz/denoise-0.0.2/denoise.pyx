# cython: language_level=3
# distutils: include_dirs=./src

from libc.stdint cimport int16_t, uint32_t, uint64_t
cimport cdenoise
from struct import unpack, pack
from libc.stdlib cimport malloc, free
from libc.string cimport memcpy

cdef class denoise:
    VERSION = '0.0.2'
    cdef uint32_t _sampleRate
    cdef uint64_t _sampleCount
    cdef uint32_t _channels
    cdef uint32_t _targetFrameSize
    cdef uint32_t _targetSampleRate
    cdef uint32_t _perFrameSize

    cdef float *_frameBuffer
    cdef float *_processBuffer

    cdef cdenoise.DenoiseState** _sts

    def __cinit__(self, sampleRate=16000, channels=1, pcm_type='S16LE'):
        print('set up denoise')
        self._targetFrameSize = 480
        self._targetSampleRate = 48000
        self._sampleRate = sampleRate
        self._channels = channels
        self._perFrameSize = sampleRate / 100;
        if pcm_type is not 'S16LE':
            raise Exception("Unacceptable pcm types")
        if channels != 1:
            raise Exception("Unacceptable channels")
        # 申请内存
        self._frameBuffer = <float *>malloc(sizeof(float) * (channels + 1) * self._targetSampleRate)
        self._sts = <cdenoise.DenoiseState**>malloc(channels * sizeof(cdenoise.DenoiseState*))
        if not self._frameBuffer or not self._sts:
            raise MemoryError()

        cdef uint32_t i = 0;
        for i in range(channels):
            self._sts[i] = cdenoise.rnnoise_create()
            if self._sts[i] is NULL:
                raise Exception("sts is NULL")

    def __dealloc__(self):
        free(self._frameBuffer)
        free(self._sts)
        cdef uint32_t i = 0;
        for i  in range(self._channels):
            if self._sts[i] is not NULL:
                cdenoise.rnnoise_destroy(self._sts[i])


    def proc(self, bytes data):
        self._sampleCount = len(data) // 2
        print('sampleCount = ', self._sampleCount)
        # 先将数据从s16转换为f32
        # 1. 申请缓冲区
        cdef int16_t* int16_buffer = <int16_t *>malloc(self._sampleCount * sizeof(int16_t))
        cdef float* float_buffer = <float *>malloc(self._sampleCount * sizeof(float))
        if not int16_buffer or not float_buffer:
            raise MemoryError()
        try:
            # 2. 复制数据
            memcpy(int16_buffer, <char*>data, self._sampleCount * sizeof(int16_t))
            #print(data[:100])
            # 3. 转换数据
            cdenoise.drwav_s16_to_f32(float_buffer, int16_buffer, self._sampleCount)
            # 调用函数进行降噪处理
            #print((<char*>float_buffer)[:200])
            #cdenoise.denoise_proc(float_buffer, self._sampleCount, self._sampleRate, self._channels)
            print('before proc')
            cdenoise.denoise_proc(self._sts, self._frameBuffer, float_buffer, self._sampleCount, self._sampleRate, self._channels)
            print('after proc')
            #cdenoise.drwav_clamp_f32(float_buffer, float_buffer, self._sampleCount);
            #print((<char*>float_buffer)[:200])
            # 转换后的数据重新转为s16
            #return (<char*>float_buffer)[:self._sampleCount*sizeof(float)]
            cdenoise.drwav_f32_to_s16(int16_buffer, float_buffer, self._sampleCount)
            return (<char*>int16_buffer)[:self._sampleCount*sizeof(int16_t)]
        finally:
            free(float_buffer)
            free(int16_buffer)


    @staticmethod
    def f32_to_s16(bytes data):
        cdef int num = len(data)
        cdef float* float_buffer = <float *>malloc(num // 4 * sizeof(float))
        cdef int16_t* int16_buffer = <int16_t *>malloc(num // 4 * sizeof(int16_t))
        if not float_buffer or not int16_buffer:
            raise MemoryError()
        try:
            memcpy(float_buffer, <char *>data, num)
            cdenoise.drwav_f32_to_s16(int16_buffer, float_buffer, num//4)
            return (<char*>int16_buffer)[:num//2]
        finally:
            free(float_buffer)
            free(int16_buffer)

    @staticmethod
    def s16_to_f32(bytes data):
        cdef int num = len(data)
        cdef int16_t* int16_buffer = <int16_t *>malloc(num // 2 * sizeof(int16_t))
        cdef float* float_buffer = <float *>malloc(num // 2 * sizeof(float))
        if not int16_buffer or not float_buffer:
            raise MemoryError()
        try:
            memcpy(int16_buffer, <char *>data, num)
            cdenoise.drwav_s16_to_f32(float_buffer, int16_buffer, num//2)
            return (<char*>float_buffer)[:num*2]
        finally:
            free(float_buffer)
            free(int16_buffer)
