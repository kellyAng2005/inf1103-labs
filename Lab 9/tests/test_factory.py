import unittest

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory


class TestFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S1", "Test Supplier", "test@example.com")

    def test_creates_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, self.supplier, 1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)

    def test_creates_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D1", "Editor", 49.9, 100, self.supplier, 20.0)
        self.assertIsInstance(product, DigitalProduct)

    def test_unknown_type_raises_value_error_with_clear_message(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S1", "Install", 30.0, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")

    def test_factory_returned_products_work_through_product_type(self) -> None:
        for product_type in ("physical", "digital"):
            product = ProductFactory.create(product_type, "X1", "Thing", 10.0, 3, self.supplier, 1.0)
            self.assertTrue(product.get_fulfilment_info())
            self.assertIs(product.get_supplier(), self.supplier)


if __name__ == "__main__":
    unittest.main()