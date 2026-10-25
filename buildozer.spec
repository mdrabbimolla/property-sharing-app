
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
p4a.commit = 725804ad06527fbfacb514add9a67ea7e7ee8683
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
