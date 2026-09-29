#!/bin/sh
# Заданы оба параметра.
cd "$(dirname "$0")/.." || exit 1
echo "exit" | ./run.sh --vfs vfs/minimal.zip --script examples/start.txt
