from . import BaseFieldType


class StreetAddress(BaseFieldType):
    def generate_obfuscated_value(self, value):
        self.seed_faker(value)
        return self.faker.street_address()
