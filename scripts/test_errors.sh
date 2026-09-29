#!/bin/sh
# Ошибочные ситуации: скрипт с ошибкой, exit в скрипте,
# несуществующий скрипт, неизвестный параметр.
cd "$(dirname "$0")/.." || exit 1

echo "=== Скрипт с ошибкой (остановка на первой ошибке)"
./run.sh --script examples/error.txt
echo "код выхода: $?"

echo "=== Скрипт с exit 3"
./run.sh --script examples/exit.txt
echo "код выхода: $?"

echo "=== Несуществующий скрипт"
./run.sh --script examples/no_such_file.txt
echo "код выхода: $?"

echo "=== Неизвестный параметр"
./run.sh --foo
echo "код выхода: $?"
