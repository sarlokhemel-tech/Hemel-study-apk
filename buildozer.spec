[app]
title = Hemel Study AI
package.name = hemelstudyai
package.domain = com.hemel.studyai
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json,db
version = 1.0.0
requirements = python3,kivy,kivymd,requests,pillow,cryptography,pyjnius,aiohttp,openssl,sqlite3
orientations = portrait
fullscreen = 0

android.permissions = INTERNET,RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA,VIBRATE,POST_NOTIFICATIONS,MODIFY_AUDIO_SETTINGS
android.features = android.hardware.microphone,android.hardware.camera
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.arch = arm64-v8a

android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1,androidx.legacy:legacy-support-v4:1.0.0,androidx.constraintlayout:constraintlayout:2.1.4,com.google.android.material:material:1.9.0

android.logcat_filters = *:S python:D
android.entrypoint = org.kivy.android.PythonActivity
android.bootstrap = sdl2
android.activity_class_name = PythonActivity
android.service_class_name = PythonService

android.presplash_lottie_loop = true
android.release_artifact = apk
android.wakelock = true

p4a.source_dir = 
p4a.local_recipes = recipes

android.gradle_options = org.gradle.jvmargs=-Xmx4096m

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = .buildozer
bin_dir = ./bin
