
[app]

# (str) 应用程序标题
title = 双色球选号器

# (str) 包名
package.name = ballselector

# (str) 包域名
package.domain = com.example

# (str) 应用程序的源代码目录
source.dir = .

# (list) 应用程序的源文件（留空则包含所有文件）
source.include_exts = py,png,jpg,kv,atlas

# (str) 应用程序版本
version = 1.0

# (list) 应用程序要求
requirements = python3,kivy

# (str) 应用程序预安装图标
#icon.filename = %(source.dir)s/data/icon.png

# (str) 支持的方向 (landscape, sensorLandscape, portrait, sensorPortrait, all)
orientation = portrait

# (bool) 指示应用程序是否应在全屏模式下运行
fullscreen = 0

[buildozer]

# (int) 日志级别 (0 = 错误, 1 = 信息, 2 = 调试)
log_level = 2

# (int) 显示警告
warn_on_root = 1

[app:android]

# (str) Android入口点
android.entrypoint = org.kivy.android.PythonActivity

# (list) 应用程序权限
android.permissions = INTERNET

# (int) Target Android API
android.api = 30

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK版本
android.ndk = 25b

# (str) Android SDK版本
android.sdk = 33

# (bool) 使用--private数据存储
android.private_storage = True

# (str) Android额外的Java .jar文件路径
#android.add_jars = foo.jar,bar.jar

# (str) Android额外的Java源文件路径
#android.add_src = java

# (str) ANT路径
#android.ant_path = /usr/bin/ant

# (bool) 如果为True，那么创建一个调试版本
android.debug = False

# (str) The format used to package the app for release mode (aab or apk)
android.release_artifact = apk

# (str) Android logcat过滤器
android.logcat_filters = *:S python:D

# (bool) 复制库而不是重新编译
android.copy_libs = 1

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

[buildozer:global]

# (str) 构建缓存目录路径
build_dir = ./.buildozer

# (str) 构建输出目录路径  
bin_dir = ./bin
