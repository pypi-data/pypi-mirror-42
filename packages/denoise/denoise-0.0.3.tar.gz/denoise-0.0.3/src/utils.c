#include <stdint.h>
#include <stdio.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include "include/rnnoise.h"

#define drwav_min(a, b)                    (((a) < (b)) ? (a) : (b))
#define drwav_max(a, b)                    (((a) > (b)) ? (a) : (b))
#define drwav_clamp(x, lo, hi)             (drwav_max((lo), drwav_min((hi), (x))))


void drwav_f32_to_s16(int16_t * pOut, const float* pIn, size_t sampleCount){
    for (size_t i = 0; i < sampleCount; ++i){
        pOut[i] = (short)drwav_clamp(pIn[i], -32768, 32768);
    }
}

void drwav_s16_to_f32(float* pOut, const int16_t* pIn, size_t sampleCount){
    if (pOut == NULL || pIn == NULL){
        return ;
    }

    for (size_t i = 0; i < sampleCount; ++i){
        *pOut++ = pIn[i] / 1.0f;
    }
}

void drwav_clamp_f32(float *pOut, float *pIn, size_t sampleCount){
    if (pOut == NULL || pIn == NULL){
        return ;
    }
    for (size_t i = 0; i < sampleCount; ++i){
        pOut[i] = drwav_clamp(pIn[i], -32768, 32767) * (1.0f / 32768.0f);
    }
}

uint64_t Resample_f32(const float *input, float *output, int inSampleRate, int outSampleRate, uint64_t inputSize,
                      uint32_t channels
) {
    if (input == NULL)
        return 0;
    uint64_t outputSize = inputSize * outSampleRate / inSampleRate;
    if (output == NULL)
        return outputSize;
    double stepDist = ((double) inSampleRate / (double) outSampleRate);
    const uint64_t fixedFraction = (1LL << 32);
    const double normFixed = (1.0 / (1LL << 32));
    uint64_t step = ((uint64_t) (stepDist * fixedFraction + 0.5));
    uint64_t curOffset = 0;
    for (uint32_t i = 0; i < outputSize; i += 1) {
        for (uint32_t c = 0; c < channels; c += 1) {
            *output++ = (float) (input[c] + (input[c + channels] - input[c]) * (
                    (double) (curOffset >> 32) + ((curOffset & (fixedFraction - 1)) * normFixed)
            )
            );
        }
        curOffset += step;
        input += (curOffset >> 32) * channels;
        curOffset &= (fixedFraction - 1);
    }
    return outputSize;
}

void denoise_proc(DenoiseState **sts, float *frameBuffer, float *input, uint64_t sampleCount, uint32_t sampleRate, uint32_t channels) {
    uint32_t targetFrameSize = 480;
    uint32_t targetSampleRate = 48000;
    uint32_t perFrameSize = sampleRate / 100;
    float *processBuffer = frameBuffer + targetFrameSize * channels;

    size_t frameStep = channels * perFrameSize;
    uint64_t frames = sampleCount / frameStep;
    uint64_t lastFrameSize = (sampleCount % frameStep) / channels;
    for (uint64_t i = 0; i < frames; ++i) {
        Resample_f32(input, frameBuffer, sampleRate, targetSampleRate,
                     perFrameSize, channels);
        for (uint32_t c = 0; c < channels; c++) {
            for (uint32_t k = 0; k < targetFrameSize; k++)
                processBuffer[k] = frameBuffer[k * channels + c];
            rnnoise_process_frame(sts[c], processBuffer, processBuffer);
            for (uint32_t k = 0; k < targetFrameSize; k++)
                frameBuffer[k * channels + c] = processBuffer[k];
        }
        Resample_f32(frameBuffer, input, targetSampleRate, sampleRate, targetFrameSize, channels);
        input += frameStep;
    }
    if (lastFrameSize != 0) {
        memset(frameBuffer, 0, targetFrameSize * channels * sizeof(float));
        uint64_t lastReasmpleSize = Resample_f32(input, frameBuffer, sampleRate,
                                                 targetSampleRate,
                                                 lastFrameSize, channels);
        for (uint32_t c = 0; c < channels; c++) {
            for (uint32_t k = 0; k < targetFrameSize; k++)
                processBuffer[k] = frameBuffer[k * channels + c];
            rnnoise_process_frame(sts[c], processBuffer, processBuffer);
            for (uint32_t k = 0; k < targetFrameSize; k++)
                frameBuffer[k * channels + c] = processBuffer[k];
        }
        Resample_f32(frameBuffer, input, targetSampleRate, sampleRate, lastReasmpleSize,
                     channels);
    }
}
