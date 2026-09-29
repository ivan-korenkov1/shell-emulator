#!/bin/sh
# Запуск без параметров: оба параметра не заданы.
cd "$(dirname "$0")/.." || exit 1
echo "conf-dump" | ./run.sh
