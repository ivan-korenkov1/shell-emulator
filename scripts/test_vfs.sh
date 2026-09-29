#!/bin/sh
# Задан только путь к VFS.
cd "$(dirname "$0")/.." || exit 1
echo "conf-dump" | ./run.sh --vfs vfs/minimal.zip
