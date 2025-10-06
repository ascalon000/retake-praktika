import unittest
import json
import os
import tempfile
from database import FormTemplateDB
from form_validator import FormValidator


class TestFormTemplates(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        with open(self.db_path, 'w') as f:
            json.dump({'_default': {}}, f)
        self.db = FormTemplateDB(self.db_path)
        self.test_templates = [
            {
                "name": "Данные пользователя",
                "login": "email",
                "tel": "phone"
            },
            {
                "name": "Форма заказа",
                "customer": "text",
                "order_id": "text",
                "дата_заказа": "date",
                "contact": "phone"
            },
            {
                "name": "Проба",
                "f_name1": "email",
                "f_name2": "date"
            }
        ]
        for template in self.test_templates:
            self.db.add_template(template)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_add_and_retrieve_templates(self):
        templates = self.db.get_all_templates()
        self.assertEqual(len(templates), 3)
        template_names = [t['name'] for t in templates]
        self.assertIn("Данные пользователя", template_names)
        self.assertIn("Форма заказа", template_names)
        self.assertIn("Проба", template_names)

    def test_find_matching_template_exact_match_form_order(self):
        fields = {
            "customer": "text",
            "order_id": "text",
            "дата_заказа": "date",
            "contact": "phone"
        }
        template = self.db.find_matching_template(fields)
        self.assertIsNotNone(template)
        self.assertEqual(template['name'], "Форма заказа")

    def test_find_matching_template_exact_match_user_data(self):
        fields = {
            "login": "email",
            "tel": "phone"
        }
        template = self.db.find_matching_template(fields)
        self.assertIsNotNone(template)
        self.assertEqual(template['name'], "Данные пользователя")

    def test_find_matching_template_exact_match_proba(self):
        fields = {
            "f_name1": "email",
            "f_name2": "date"
        }
        template = self.db.find_matching_template(fields)
        self.assertIsNotNone(template)
        self.assertEqual(template['name'], "Проба")

    def test_find_matching_template_extra_fields(self):
        fields = {
            "login": "email",
            "tel": "phone",
            "extra_field": "text",
            "another_extra": "date"
        }
        template = self.db.find_matching_template(fields)
        self.assertIsNotNone(template)
        self.assertEqual(template['name'], "Данные пользователя")

    def test_find_matching_template_no_match_missing_fields(self):
        fields = {
            "customer": "text"
        }

        template = self.db.find_matching_template(fields)
        self.assertIsNone(template)

    def test_find_matching_template_no_match_wrong_field_types(self):
        fields = {
            "login": "text",
            "tel": "phone"
        }
        template = self.db.find_matching_template(fields)
        self.assertIsNone(template)

    def test_find_matching_template_no_match_unknown_fields(self):
        fields = {
            "unknown_field": "text",
            "another_unknown": "date"
        }
        template = self.db.find_matching_template(fields)
        self.assertIsNone(template)

    def test_find_matching_template_partial_match_proba(self):
        fields = {
            "f_name1": "email"
        }
        template = self.db.find_matching_template(fields)
        self.assertIsNone(template)

    def test_validate_phone(self):
        validator = FormValidator()
        valid_phones = [
            "+7 903 123 45 67",
            "+7 999 888 77 66"
        ]
        invalid_phones = [
            "89031234567",
            "+79031234567",
            "7 903 123 45 67",
            "+7 903 123 45 6",
            "+7 903 123 45 678",
            "телефон"
        ]
        for phone in valid_phones:
            self.assertTrue(validator.validate_phone(phone), f"Phone {phone} should be valid")
        for phone in invalid_phones:
            self.assertFalse(validator.validate_phone(phone), f"Phone {phone} should be invalid")

    def test_validate_date(self):
        validator = FormValidator()
        valid_dates = [
            "27.05.2025",
            "01.01.2020",
            "2025-05-27",
            "2020-01-01"
        ]
        invalid_dates = [
            "27/05/2025",
            "2025/05/27",
            "32.05.2025",  # Неверный день
            "27.13.2025",  # Неверный месяц
            "27.05.25",  # Неверный год
            "not-a-date"
        ]
        for date in valid_dates:
            self.assertTrue(validator.validate_date(date), f"Date {date} should be valid")
        for date in invalid_dates:
            self.assertFalse(validator.validate_date(date), f"Date {date} should be invalid")

    def test_validate_email(self):
        validator = FormValidator()
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org"
        ]
        invalid_emails = [
            "invalid",
            "invalid@",
            "@domain.com",
            "invalid@domain",
            "no-at-sign"
        ]
        for email in valid_emails:
            self.assertTrue(validator.validate_email(email), f"Email {email} should be valid")
        for email in invalid_emails:
            self.assertFalse(validator.validate_email(email), f"Email {email} should be invalid")

    def test_detect_field_type(self):
        validator = FormValidator()
        test_cases = [
            ("27.05.2025", "date"),
            ("2025-05-27", "date"),
            ("+7 903 123 45 67", "phone"),
            ("test@example.com", "email"),
            ("plain text", "text"),
            ("12345", "text"),
            ("", "text")
        ]
        for value, expected_type in test_cases:
            actual_type = validator.detect_field_type(value)
            self.assertEqual(actual_type, expected_type,
                             f"Value '{value}' should be detected as '{expected_type}', but got '{actual_type}'")

    def test_detect_field_types(self):
        validator = FormValidator()
        fields = {
            "field1": "27.05.2025",
            "field2": "+7 903 123 45 67",
            "field3": "test@example.com",
            "field4": "plain text",
            "field5": "2024-01-15"
        }
        expected_types = {
            "field1": "date",
            "field2": "phone",
            "field3": "email",
            "field4": "text",
            "field5": "date"
        }
        result = validator.detect_field_types(fields)
        self.assertEqual(result, expected_types)


if __name__ == '__main__':
    unittest.main()