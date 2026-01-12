

---
description: 'C++ 项目配置和包管理'
applyTo: '**/*.cmake, **/CMakeLists.txt, **/*.cpp, **/*.h, **/*.hpp'
---

此项目使用 vcpkg 的清单模式。在提供 vcpkg 建议时请注意这一点。请不要提供诸如 `vcpkg install library` 这样的建议，因为它们可能不会按预期工作。
如果可能，请优先通过 CMakePresets.json 设置缓存变量和其他内容。
请提供有关任何可能影响建议或提及的 CMake 变量的 CMake 策略信息。
此项目需要跨平台和多编译器支持，包括 MSVC、Clang 和 GCC。
在提供使用文件系统读取文件的 OpenCV 示例时，请始终使用绝对文件路径而不是文件名或相对文件路径。例如，使用 `video.open("C:/project/file.mp4")`，而不是 `video.open("file.mp4")`。
---