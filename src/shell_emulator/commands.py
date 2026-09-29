"""Команды эмулятора и исключения, которые они используют."""

from shell_emulator.config import format_config

MAX_CD_ARGS = 1
MAX_EXIT_ARGS = 1


class CommandError(Exception):
    """Ошибка выполнения команды (неверные аргументы и т.п.)."""


class ExitRequest(Exception):
    """Запрос на завершение работы эмулятора с кодом возврата."""

    def __init__(self, code):
        """Сохраняет код возврата."""
        super().__init__(code)
        self.code = code


def format_stub(name, args):
    """Формирует вывод команды-заглушки: имя и список аргументов."""
    return f"{name}: args={args}"


def cmd_ls(shell, args):
    """Заглушка ls: выводит свое имя и аргументы."""
    return format_stub("ls", args)


def cmd_cd(shell, args):
    """Заглушка cd: принимает не более одного аргумента."""
    if len(args) > MAX_CD_ARGS:
        raise CommandError("cd: too many arguments")
    return format_stub("cd", args)


def cmd_exit(shell, args):
    """Завершает работу эмулятора. Необязательный аргумент - код."""
    if len(args) > MAX_EXIT_ARGS:
        raise CommandError("exit: too many arguments")
    code = 0
    if args:
        try:
            code = int(args[0])
        except ValueError:
            raise CommandError(
                f"exit: {args[0]}: numeric argument required"
            ) from None
    raise ExitRequest(code)


def cmd_conf_dump(shell, args):
    """Служебная команда: выводит параметры эмулятора."""
    if args:
        raise CommandError("conf-dump: too many arguments")
    return format_config(shell.config)


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
    "conf-dump": cmd_conf_dump,
}
