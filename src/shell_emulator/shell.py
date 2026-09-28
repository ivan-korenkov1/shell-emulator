"""Ядро эмулятора: приглашение, парсер и цикл REPL."""

import getpass
import shlex
import socket
import sys

from shell_emulator.commands import COMMANDS, CommandError, ExitRequest


def parse_line(line):
    """Разбивает строку на команду и аргументы по пробелам.

    Поддерживаются кавычки: 'a b' считается одним аргументом.
    Возвращает кортеж (команда, список аргументов) или (None, [])
    для пустой строки.
    """
    try:
        tokens = shlex.split(line)
    except ValueError as error:
        raise CommandError(f"syntax error: {error}") from None
    if not tokens:
        return None, []
    return tokens[0], tokens[1:]


class Shell:
    """Состояние эмулятора и выполнение команд."""

    def __init__(self, out=sys.stdout, err=sys.stderr):
        """Берет имя пользователя и хоста из реальной ОС."""
        self.user = getpass.getuser()
        self.host = socket.gethostname().split(".")[0]
        self.cwd = "~"
        self.out = out
        self.err = err

    def prompt(self):
        """Возвращает приглашение вида user@host:~$."""
        return f"{self.user}@{self.host}:{self.cwd}$ "

    def execute(self, line):
        """Выполняет одну строку и возвращает вывод команды.

        Бросает CommandError при ошибке и ExitRequest при exit.
        """
        name, args = parse_line(line)
        if name is None:
            return ""
        command = COMMANDS.get(name)
        if command is None:
            raise CommandError(f"{name}: command not found")
        return command(self, args)

    def run_line(self, line):
        """Выполняет строку и печатает результат или ошибку.

        Возвращает True, если команда выполнена без ошибок.
        """
        try:
            output = self.execute(line)
        except CommandError as error:
            print(error, file=self.err)
            return False
        if output:
            print(output, file=self.out)
        return True

    def run_interactive(self):
        """Запускает интерактивный цикл REPL. Возвращает код выхода."""
        while True:
            try:
                line = input(self.prompt())
            except EOFError:
                print(file=self.out)
                return 0
            except KeyboardInterrupt:
                print(file=self.out)
                continue
            try:
                self.run_line(line)
            except ExitRequest as request:
                return request.code
