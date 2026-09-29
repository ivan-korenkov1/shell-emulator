#!/bin/sh
# Задан только стартовый скрипт. После скрипта - интерактивный режим,
# в который через echo передается команда exit.
cd "$(dirname "$0")/.." || exit 1
echo "exit" | ./run.sh --script examples/start.txt
