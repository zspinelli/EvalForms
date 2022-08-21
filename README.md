# EvalForms
A ui compilation automator for PySide projects.

Instructions are included in comment at the top of the script. In summary:
Import EvalForms at the top of your project's entry point.
There is a couple variables in the script that need to be changed to reflect your projects directory layout.
The script in the current state favors having all the .ui files in one directory.

How it works:
All the ui's are fed into pyside-uic, their contents are hashed and the hashes are stored to detect changes every run.
So you can modify your uis without slogging the cli -uic manually.
The hash list is placed in the directory with the ui files.

-Hashes are checked each time.
-Hashes for new files are added each time.
-Hashes for nonexistent files are deleted each time.

Asides:
I use pyside so much for personal projects that I keep it as a global site package. The script design reflects this.
I have not tested it in a venv scenario.
I do not know if this script functions correctly on mac or linux.
