import unittest

from supplier import Supplier
from product_factory import ProductFactory
from order import Order
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from percentage_discount import PercentageDiscount
from bulk_discount import BulkDiscount
from student_discount import StudentDiscount


class DoubleDiscount(DiscountStrategy):
    """A brand new strategy written only for this test. Order is never edited."""

    def apply(self, total: float) -> float:
        return total / 2


class TestDiscounts(unittest.TestCase):
    def setUp(self) -> None:
        supplier = Supplier("S1", "Test Supplier", "test@example.com")
        self.product = ProductFactory.create("physical", "P1", "Item", 125.00, 50, supplier, 1.0)

    def make_order(self, quantity: int = 2) -> Order:
        order = Order("O1")
        order.add_order_line(self.product, quantity)   # 125 x 2 = 250
        return order

    def test_default_is_no_discount(self) -> None:
        self.assertAlmostEqual(self.make_order().calculate_total(), 250.0)

    def test_no_discount_strategy(self) -> None:
        self.assertEqual(NoDiscount().apply(80.0), 80.0)

    def test_percentage_discount(self) -> None:
        self.assertAlmostEqual(PercentageDiscount(10).apply(250.0), 225.0)

    def test_bulk_discount_at_or_above_threshold(self) -> None:
        self.assertAlmostEqual(BulkDiscount(200, 20).apply(250.0), 230.0)
        self.assertAlmostEqual(BulkDiscount(200, 20).apply(200.0), 180.0)

    def test_bulk_discount_below_threshold(self) -> None:
        self.assertAlmostEqual(BulkDiscount(200, 20).apply(199.0), 199.0)

    def test_student_discount(self) -> None:
        self.assertAlmostEqual(StudentDiscount().apply(200.0), 190.0)

    def test_order_uses_strategy_given_at_creation(self) -> None:
        order = Order("O2", BulkDiscount(200, 20))
        order.add_order_line(self.product, 2)
        self.assertAlmostEqual(order.calculate_total(), 230.0)

    def test_set_discount_changes_strategy_on_existing_order(self) -> None:
        order = self.make_order()
        order.set_discount(BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_new_strategy_works_without_changing_order(self) -> None:
        order = self.make_order()
        order.set_discount(DoubleDiscount())
        self.assertAlmostEqual(order.calculate_total(), 125.0)

    def test_two_orders_can_share_one_strategy(self) -> None:
        shared = PercentageDiscount(10)
        order_1 = self.make_order()
        order_2 = self.make_order(1)
        order_1.set_discount(shared)
        order_2.set_discount(shared)
        self.assertAlmostEqual(order_1.calculate_total(), 225.0)
        self.assertAlmostEqual(order_2.calculate_total(), 112.5)

    def test_bad_discount_values_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PercentageDiscount(0)
        with self.assertRaises(ValueError):
            PercentageDiscount(150)
        with self.assertRaises(ValueError):
            BulkDiscount(0, 20)
        with self.assertRaises(ValueError):
            BulkDiscount(200, -5)


if __name__ == "__main__":
    unittest.main()