[app]
title = Hemel Study AI
package.name = hemelstudyai
package.domain = com.hemel
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0
requirements = python3,kivy,kivymd,requests,pillow,cryptography,pyjnius,aiohttp
orientations = portrait
fullscreen = 0
android.permissions = INTERNET,RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA,VIBRATE,POST_NOTIFICATIONS
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.arch = arm64-v8a
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1,androidx.legacy:legacy-support-v4:1.0.0
android.features = android.hardware.microphone
android.logcat_filters = *:S python:D
p4a.source_dir = 
p4a.local_recipes = recipes
[buildozer]
log_level = 2
warn_on_root = 1
