
[app]

# 应用程序标题
title = 双色球选号器

# 包名（只能包含字母、数字、下划线）
package.name = ballselector

# 包域名
package.domain = com.example

# 源代码目录
source.dir = .

# 包含的文件类型
source.include_exts = py,png,jpg,kv,atlas

# 应用版本
version = 1.0

# Python依赖包（指定版本避免冲突）
requirements = python3,kivy==2.1.0

# 屏幕方向
orientation = portrait

# 全屏模式
fullscreen = 0

[buildozer]

# 日志级别
log_level = 2

# 在root权限下显示警告
warn_on_root = 1

[app:android]

# Android入口点
android.entrypoint = org.kivy.android.PythonActivity

# 应用权限
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# 目标Android API（降低到更稳定的版本）
android.api = 29

# 最低API版本
android.minapi = 21

# Android NDK版本（使用稳定版本）
android.ndk = 23b

# Android SDK版本
android.sdk = 29

# 私有存储
android.private_storage = True

# 调试模式
android.debug = True

# 发布格式
android.release_artifact = apk

# logcat过滤器
android.logcat_filters = *:S python:D

# 复制库文件
android.copy_libs = 1

# 支持的架构（先只构建arm64减少时间）
android.archs = arm64-v8a

# 接受SDK许可
android.accept_sdk_license = True

# gradle依赖
android.gradle_dependencies = 

# Java构建工具
android.ant_path = /usr/bin/ant

[buildozer:global]

# 构建缓存目录
build_dir = ./.buildozer

# 输出目录
bin_dir = ./bin
