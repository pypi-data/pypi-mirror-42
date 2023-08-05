from . import BaseFieldType


class FirstName(BaseFieldType):
    def generate_obfuscated_value(self, value):
        self.seed_faker(value)
        return self.faker.first_name()
