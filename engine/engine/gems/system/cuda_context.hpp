/*
Copyright (c) 2018, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.
*/
#pragma once

#include <cuda.h>

namespace isaac {
namespace cuda {

// Return the current CUDA context bound to the calling CPU thread. If no
// context is bound then one is created.
CUcontext GetOrCreateCudaContext(int device_id = 0);

}  // namespace cuda
}  // namespace isaac
