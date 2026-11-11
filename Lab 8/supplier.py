class Supplier:
    """Supplies products. Associated with Product: neither owns the other."""

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    @staticmethod
    def is_valid(name: str, contact_email: str) -> bool:
        """A supplier needs a name and an email containing '@'."""
        return bool(name.strip()) and "@" in contact_email

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    def update_details(self, name: str, contact_email: str) -> bool:
        """Supplier decides what valid details are."""
        if not Supplier.is_valid(name, contact_email):
            print("\nName cannot be empty and the email must contain '@'. Supplier not updated.")
            return False
        self.__name = name
        self.__contact_email = contact_email
        return True

    def display_information(self) -> None:
        print(
            f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | "
            f"Email: {self.__contact_email}"
        )