
[app]
title = Property Sharing
package.name = propertysharing
package.domain = com.realestate
source.dir = .
source.include_exts = py,png,jpg,kv,ttf
version = 0.1.0
requirements = python3,kivy,pillow,pyjnius

# Pin python-for-android to the fix for the pip BuildDependencyInstallError failure.
p4a.branch = develop
p4a.commit = d2ee8c5
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
