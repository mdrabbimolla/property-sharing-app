[app]
title = Property Sharing
package.name = propertysharing
package.domain = com.realestate
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,svg
version = 0.1.0
requirements = python3,kivy,pillow,pyjnius

# Custom launcher icon generated from icon.svg in the workflow.
icon.filename = %(source.dir)s/icon.png

# Use a stable p4a release to avoid the Python 3.14 / pip wheel mismatch.
p4a.branch = v2024.01.21
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
