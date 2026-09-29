"""Параметры командной строки эмулятора."""

import argparse
import os

NOT_SET = "<not set>"


def parse_args(argv=None):
    """Разбирает параметры командной строки и возвращает словарь.

    Ключи словаря: vfs - путь к VFS, script - путь к стартовому
    скрипту. Незаданный параметр имеет значение None.
    """
    parser = argparse.ArgumentParser(
        prog="shell_emulator",
        description="Эмулятор командной оболочки UNIX-подобной ОС.",
    )
    parser.add_argument(
        "--vfs", metavar="PATH",
        help="путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--script", metavar="PATH",
        help="путь к стартовому скрипту",
    )
    args = parser.parse_args(argv)
    return {
        "vfs": absolute_or_none(args.vfs),
        "script": absolute_or_none(args.script),
    }


def absolute_or_none(path):
    """Преобразует путь в абсолютный, None оставляет как есть."""
    if path is None:
        return None
    return os.path.abspath(path)


def format_config(config):
    """Возвращает параметры в виде строк формата ключ=значение."""
    lines = []
    for key, value in config.items():
        shown = NOT_SET if value is None else value
        lines.append(f"{key}={shown}")
    return "\n".join(lines)
