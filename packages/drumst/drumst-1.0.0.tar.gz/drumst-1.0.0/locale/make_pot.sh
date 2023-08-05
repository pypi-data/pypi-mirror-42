#!/bin/bash
# Make a file po/pot with the current state of files

CWD=$(pwd)

xgettext -d drumst "../drumsT/DrumsT.py" "../drumsT/drumsT_FRAMES/mainwindow.py" \
"../drumsT/drumsT_FRAMES/lessons.py" "../drumsT/drumsT_PANELS/add_lesson.py" \
"../drumsT/drumsT_PANELS/lessons_prospective.py" "../drumsT/drumsT_DIALOGS/infoprg.py" \
"../drumsT/drumsT_DIALOGS/first_time_start.py" "../drumsT/drumsT_DIALOGS/add_student.py" \
"../drumsT/drumsT_DIALOGS/add_school.py" "../drumsT/drumsT_DIALOGS/add_newyear.py" \
"../drumsT/drumsT_SYS/os_filesystem.py" "../drumsT/drumsT_SYS/SQLite_lib.py"
