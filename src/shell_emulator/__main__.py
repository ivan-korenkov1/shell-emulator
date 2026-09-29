"""Точка входа: python -m shell_emulator [--vfs PATH] [--script PATH]."""

import sys

from shell_emulator.config import format_config, parse_args
from shell_emulator.shell import Shell


def print_debug(config):
    """Отладочный вывод всех заданных параметров при запуске."""
    for line in format_config(config).splitlines():
        print(f"[debug] {line}", flush=True)


def main(argv=None):
    """Запускает эмулятор: сначала стартовый скрипт, затем REPL."""
    config = parse_args(argv)
    print_debug(config)
    shell = Shell(config)
    if config["script"] is not None:
        code = shell.run_script(config["script"])
        if code is not None:
            return code
    return shell.run_interactive()


if __name__ == "__main__":
    sys.exit(main())
