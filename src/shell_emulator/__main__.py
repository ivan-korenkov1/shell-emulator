"""Точка входа: python -m shell_emulator."""

import sys

from shell_emulator.shell import Shell


def main():
    """Запускает эмулятор в интерактивном режиме."""
    return Shell().run_interactive()


if __name__ == "__main__":
    sys.exit(main())
