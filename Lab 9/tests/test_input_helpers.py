import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from input_helpers import get_positive_float, get_non_negative_int


class TestInputHelpers(unittest.TestCase):
    def test_keeps_asking_until_valid_price(self) -> None:
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with redirect_stdout(output):
                value = get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(
            output.getvalue().splitlines(),
            ["Please enter a valid number, e.g. 12.50",
             "Please enter a number greater than zero."],
        )

    def test_zero_is_not_a_positive_price(self) -> None:
        with patch("builtins.input", side_effect=["0", "3"]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(get_positive_float("Price: "), 3.0)

    def test_stock_rejects_text_decimals_and_negatives(self) -> None:
        with patch("builtins.input", side_effect=["ten", "2.5", "-1", "0"]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(get_non_negative_int("Stock: "), 0)


if __name__ == "__main__":
    unittest.main()