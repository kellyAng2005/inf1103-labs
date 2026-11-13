import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from supplier import Supplier
from inventory import Inventory
from product_loader import load_products

CSV_TEXT = (
    "product_type,product_id,name,price,stock_quantity\n"
    "physical,P001,Desk Lamp,25.00,10\n"
    "digital,D001,Photo Editor,49.90,100\n"
    "service,S001,Installation,30.00,5\n"
    "physical,P002,Office Chair,abc,3\n"
    "physical,P003,Monitor Stand,39.50,7\n"
)


class TestProductLoader(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S1", "Test Supplier", "test@example.com")
        self.inventory = Inventory()
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)

    def write_csv(self, text: str) -> str:
        path = os.path.join(self.folder.name, "products.csv")
        with open(path, "w", newline="") as f:
            f.write(text)
        return path

    def run_loader(self, path: str) -> list[str]:
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(path, self.inventory, self.supplier)
        return output.getvalue().splitlines()

    def test_bad_rows_skipped_and_valid_rows_load(self) -> None:
        lines = self.run_loader(self.write_csv(CSV_TEXT))
        self.assertEqual(len(self.inventory.get_all_products()), 3)
        self.assertIsNotNone(self.inventory.find_product("P001"))
        self.assertIsNotNone(self.inventory.find_product("D001"))
        self.assertIsNotNone(self.inventory.find_product("P003"))
        self.assertIsNone(self.inventory.find_product("S001"))
        self.assertIsNone(self.inventory.find_product("P002"))
        self.assertIn("Row 4 skipped: Unknown product type: service", lines)
        self.assertEqual(lines[-2:], ["3 products loaded.", "Load attempt finished."])

    def test_missing_file_is_handled_without_crashing(self) -> None:
        missing = os.path.join(self.folder.name, "nope.csv")
        lines = self.run_loader(missing)
        self.assertEqual(lines, [f"Products file not found: {missing}",
                                 "Load attempt finished."])
        self.assertEqual(self.inventory.get_all_products(), [])

    def test_invalid_price_and_stock_values_are_reported(self) -> None:
        text = ("product_type,product_id,name,price,stock_quantity\n"
                "physical,P1,Free Thing,0,5\n"
                "physical,P2,Negative Stock,5.00,-2\n"
                "physical,P3,Short Row,5.00\n")
        lines = self.run_loader(self.write_csv(text))
        self.assertEqual(self.inventory.get_all_products(), [])
        self.assertEqual(sum(1 for line in lines if "skipped" in line), 3)
        self.assertEqual(lines[-2:], ["0 products loaded.", "Load attempt finished."])

    def test_duplicate_id_is_reported_and_skipped(self) -> None:
        text = ("product_type,product_id,name,price,stock_quantity\n"
                "physical,P1,First,5.00,1\n"
                "physical,P1,Second,6.00,2\n")
        lines = self.run_loader(self.write_csv(text))
        self.assertEqual(len(self.inventory.get_all_products()), 1)
        self.assertIn("Row 3 skipped: ID P1 already exists.", lines)


if __name__ == "__main__":
    unittest.main()