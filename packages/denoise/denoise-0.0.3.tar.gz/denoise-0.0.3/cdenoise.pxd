from libc.stdint cimport int16_t, uint32_t, uint64_t

cdef extern from "include/rnnoise.h":
    ctypedef struct DenoiseState:
        pass
    DenoiseState* rnnoise_create();
    void rnnoise_destroy(DenoiseState *st);

cdef extern from "include/utils.h":
    void drwav_f32_to_s16(int16_t* pOut, const float* pIn, size_t sampleCount);
    void drwav_s16_to_f32(float* pOut, const int16_t* pIn, size_t sampleCount);
    void drwav_clamp_f32(float* pOut, float* pIn, size_t sampleCount);
    void denoise_proc(DenoiseState **sts, float *frameBuffer, float *input, uint64_t sampleCount, uint32_t sampleRate, uint32_t channels);
