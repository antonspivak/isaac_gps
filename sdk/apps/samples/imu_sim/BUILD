"""
Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.
"""
package(default_visibility = ["//visibility:public"])
load("//bzl:module.bzl", "isaac_app")

isaac_app(
    name = "imu_sim",
    app_json_file = "imu_sim.app.json",
    data = [
        "imu_calib.json",
    ],
    modules = [
        "engine_tcp_udp",
        "flatsim",
        "imu",
        "navigation",
        "sensors:joystick",
        "sight",
    ],
)


py_binary(
    name = "ping_python",
    srcs = [
        "__init__.py",
        "ping_python.py",
    ],
    data = [
        "ping_python.app.json",
        "//apps:py_init",
        "//apps/tutorials:py_init",
        "//packages/sight:libsight_module.so",
        "//packages/navigation:libnavigation_module.so",
        "//apps/samples/imu_sim"
    ],
    deps = [
        "//packages/pyalice",
    ],
)
