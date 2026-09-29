"""Тесты этапа 2: параметры, conf-dump и стартовый скрипт."""

import io
import os
import tempfile
import unittest

from shell_emulator.commands import CommandError
from shell_emulator.config import format_config, parse_args
from shell_emulator.shell import Shell


class ParseArgsTest(unittest.TestCase):
    """Тесты разбора параметров командной строки."""

    def test_no_args(self):
        """Без параметров оба значения не заданы."""
        self.assertEqual(parse_args([]), {"vfs": None, "script": None})

    def test_all_args(self):
        """Пути преобразуются в абсолютные."""
        config = parse_args(["--vfs", "a.zip", "--script", "s.txt"])
        self.assertEqual(config["vfs"], os.path.abspath("a.zip"))
        self.assertEqual(config["script"], os.path.abspath("s.txt"))

    def test_format(self):
        """Параметры выводятся в формате ключ=значение."""
        text = format_config({"vfs": "/a.zip", "script": None})
        self.assertEqual(text, "vfs=/a.zip\nscript=<not set>")


class ScriptTest(unittest.TestCase):
    """Тесты conf-dump и выполнения стартового скрипта."""

    def setUp(self):
        """Создает эмулятор с перехваченным выводом."""
        self.out = io.StringIO()
        self.err = io.StringIO()
        config = {"vfs": "/v.zip", "script": None}
        self.shell = Shell(config, out=self.out, err=self.err)

    def run_script_text(self, text):
        """Записывает текст во временный файл и выполняет его."""
        with tempfile.NamedTemporaryFile(
            "w", suffix=".txt", delete=False, encoding="utf-8"
        ) as file:
            file.write(text)
        self.addCleanup(os.remove, file.name)
        return self.shell.run_script(file.name)

    def test_conf_dump(self):
        """conf-dump выводит все параметры."""
        output = self.shell.execute("conf-dump")
        self.assertEqual(output, "vfs=/v.zip\nscript=<not set>")

    def test_conf_dump_args(self):
        """conf-dump не принимает аргументов."""
        with self.assertRaises(CommandError):
            self.shell.execute("conf-dump x")

    def test_script_shows_input_and_output(self):
        """Скрипт показывает и команды, и их вывод."""
        result = self.run_script_text("# comment\n\nls a\n")
        self.assertIsNone(result)
        output = self.out.getvalue()
        self.assertIn("$ ls a\n", output)
        self.assertIn("ls: args=['a']", output)
        self.assertNotIn("comment", output)

    def test_script_stops_on_error(self):
        """Скрипт останавливается на первой ошибке."""
        result = self.run_script_text("ls\nfoo\nls never\n")
        self.assertEqual(result, 1)
        self.assertNotIn("never", self.out.getvalue())
        self.assertIn("stopped at line 2", self.err.getvalue())

    def test_script_exit(self):
        """exit в скрипте завершает работу с кодом."""
        self.assertEqual(self.run_script_text("exit 5\nls\n"), 5)

    def test_missing_script(self):
        """Несуществующий скрипт - ошибка с кодом 1."""
        self.assertEqual(self.shell.run_script("/no/such/file"), 1)
        self.assertIn("script:", self.err.getvalue())


if __name__ == "__main__":
    unittest.main()
