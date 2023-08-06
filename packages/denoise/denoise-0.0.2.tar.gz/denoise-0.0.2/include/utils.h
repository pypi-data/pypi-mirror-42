#ifndef __UTILS_H__
#define __UTILS_H__

void drwav_f32_to_s16(int16_t* pOut, const float* pIn, size_t sampleCount);

void drwav_s16_to_f32(float* pOut, const int16_t* pIn, size_t sampleCount);

void drwav_clamp_f32(float* pOut, float* pIn, size_t sampleCount);

void denoise_proc(DenoiseState **sts, float *frameBuffer, float *input, uint64_t sampleCount, uint32_t sampleRate, uint32_t channels);

#endif
