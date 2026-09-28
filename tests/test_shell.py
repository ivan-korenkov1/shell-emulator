"""Тесты этапа 1: парсер, приглашение и команды-заглушки."""

import io
import unittest

from shell_emulator.commands import CommandError, ExitRequest
from shell_emulator.shell import Shell, parse_line


class ParseLineTest(unittest.TestCase):
    """Тесты парсера командной строки."""

    def test_splits_by_spaces(self):
        """Команда и аргументы разделяются пробелами."""
        self.assertEqual(parse_line("ls -l  /home"), ("ls", ["-l", "/home"]))

    def test_empty_line(self):
        """Пустая строка не содержит команды."""
        self.assertEqual(parse_line("   "), (None, []))

    def test_quotes(self):
        """Аргумент в кавычках не разбивается."""
        self.assertEqual(parse_line("cd 'my dir'"), ("cd", ["my dir"]))

    def test_unclosed_quote(self):
        """Незакрытая кавычка - синтаксическая ошибка."""
        with self.assertRaises(CommandError):
            parse_line("cd 'abc")


class ShellTest(unittest.TestCase):
    """Тесты выполнения команд."""

    def setUp(self):
        """Создает эмулятор с перехваченным выводом."""
        self.out = io.StringIO()
        self.err = io.StringIO()
        self.shell = Shell(out=self.out, err=self.err)

    def test_prompt(self):
        """Приглашение строится из реальных данных ОС."""
        prompt = self.shell.prompt()
        self.assertTrue(prompt.startswith(f"{self.shell.user}@"))
        self.assertTrue(prompt.endswith(":~$ "))

    def test_ls_stub(self):
        """ls выводит свое имя и аргументы."""
        self.assertEqual(self.shell.execute("ls -a b"), "ls: args=['-a', 'b']")

    def test_cd_stub(self):
        """cd выводит свое имя и аргументы."""
        self.assertEqual(self.shell.execute("cd /tmp"), "cd: args=['/tmp']")

    def test_cd_too_many_args(self):
        """cd с двумя аргументами - ошибка."""
        with self.assertRaises(CommandError):
            self.shell.execute("cd a b")

    def test_unknown_command(self):
        """Неизвестная команда сообщает об ошибке."""
        self.assertFalse(self.shell.run_line("foo"))
        self.assertIn("foo: command not found", self.err.getvalue())

    def test_exit_code(self):
        """exit передает код возврата."""
        with self.assertRaises(ExitRequest) as ctx:
            self.shell.execute("exit 3")
        self.assertEqual(ctx.exception.code, 3)

    def test_exit_bad_arg(self):
        """exit с нечисловым аргументом - ошибка."""
        with self.assertRaises(CommandError):
            self.shell.execute("exit abc")


if __name__ == "__main__":
    unittest.main()
