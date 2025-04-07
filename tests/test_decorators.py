import pytest

from src.decorators import log


# Тест для логирования в консоль
def test_log_to_console(capsys):
    @log()
    def add(a, b):
        return a + b

    result = add(2, 3)

    assert result == 5

    captured = capsys.readouterr()
    output = captured.out

    assert "Function: 'add'" in output
    assert "result: 5" in output
    assert "Time start:" in output
    assert "Time end:" in output
    assert "Time execution:" in output


def test_log_error(capsys):
    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    # Захватываем вывод в консоль
    captured = capsys.readouterr()
    output = captured.out

    # Проверяем, что вывод содержит информацию об ошибке
    assert "Function 'divide' raised an error: ZeroDivisionError" in output
    assert "Args: (10, 0)" in output
