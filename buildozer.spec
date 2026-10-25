
[app]
title = Property Sharing
package.name = propertysharing
package.domain = com.realestate
source.dir = .
source.include_exts = py,png,jpg,kv,ttf
version = 0.1.0
requirements = python3,kivy,pillow,pyjnius

# Use the stable python-for-android branch compatible with the Python 3.11 CI environment.
p4a.branch = master
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
