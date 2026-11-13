import unittest

from supplier import Supplier
from product import Product
from product_factory import ProductFactory
from order import Order
from order_line import OrderLine


class TestValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S1", "Test Supplier", "test@example.com")
        self.product: Product = ProductFactory.create(
            "physical", "P1", "Lamp", 25.0, 10, self.supplier, 1.0)

    def test_price_must_be_greater_than_zero(self) -> None:
        for bad_price in (0.0, -5.0):
            with self.assertRaises(ValueError):
                ProductFactory.create("physical", "P2", "Bad", bad_price, 1, self.supplier, 1.0)

    def test_starting_stock_cannot_be_negative(self) -> None:
        for product_type in ("physical", "digital"):
            with self.assertRaises(ValueError):
                ProductFactory.create(product_type, "P2", "Bad", 5.0, -1, self.supplier, 1.0)

    def test_zero_stock_is_allowed(self) -> None:
        product = ProductFactory.create("digital", "D1", "Ok", 5.0, 0, self.supplier, 1.0)
        self.assertEqual(product.get_stock(), 0)

    def test_update_stock_rejects_negative_and_keeps_old_value(self) -> None:
        with self.assertRaises(ValueError):
            self.product.update_stock(-3)
        self.assertEqual(self.product.get_stock(), 10)

    def test_update_stock_accepts_valid_value_for_every_product_type(self) -> None:
        digital = ProductFactory.create("digital", "D1", "Ok", 5.0, 5, self.supplier, 1.0)
        for product in (self.product, digital):
            product.update_stock(7)
            self.assertEqual(product.get_stock(), 7)

    def test_order_line_quantity_must_be_greater_than_zero(self) -> None:
        for bad_quantity in (0, -2):
            with self.assertRaises(ValueError):
                OrderLine(self.product, bad_quantity)

    def test_order_line_update_rejects_bad_quantity(self) -> None:
        line = OrderLine(self.product, 2)
        with self.assertRaises(ValueError):
            line.update_quantity(0)
        self.assertEqual(line.get_quantity(), 2)

    def test_order_rejects_bad_quantities_and_stays_empty(self) -> None:
        order = Order("O1")
        with self.assertRaises(ValueError):
            order.add_order_line(self.product, 0)
        self.assertEqual(order.get_order_lines(), [])

    def test_order_rejects_bad_quantity_for_existing_line(self) -> None:
        order = Order("O1")
        order.add_order_line(self.product, 2)
        with self.assertRaises(ValueError):
            order.add_order_line(self.product, -1)
        self.assertEqual(order.get_order_lines()[0].get_quantity(), 2)

    def test_adding_same_product_twice_adds_quantities(self) -> None:
        order = Order("O1")
        order.add_order_line(self.product, 2)
        order.add_order_line(self.product, 3)
        self.assertEqual(len(order.get_order_lines()), 1)
        self.assertEqual(order.get_order_lines()[0].get_quantity(), 5)


if __name__ == "__main__":
    unittest.main()