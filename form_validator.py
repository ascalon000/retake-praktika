import re


class FormValidator:
    @staticmethod
    def validate_phone(value):
        pattern = r'^\+7\s\d{3}\s\d{3}\s\d{2}\s\d{2}$'
        return bool(re.match(pattern, value))

    @staticmethod
    def validate_date(value):
        date_pattern1 = r'^\d{2}\.\d{2}\.\d{4}$'
        date_pattern2 = r'^\d{4}-\d{2}-\d{2}$'

        if re.match(date_pattern1, value):
            try:
                day, month, year = map(int, value.split('.'))
                if 1 <= month <= 12 and 1 <= day <= 31 and year >= 1900:
                    return True
            except ValueError:
                return False

        elif re.match(date_pattern2, value):
            try:
                year, month, day = map(int, value.split('-'))
                if 1 <= month <= 12 and 1 <= day <= 31 and year >= 1900:
                    return True
            except ValueError:
                return False

        return False

    @staticmethod
    def validate_email(value):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, value))

    @staticmethod
    def detect_field_type(value):
        if FormValidator.validate_date(value):
            return 'date'
        elif FormValidator.validate_phone(value):
            return 'phone'
        elif FormValidator.validate_email(value):
            return 'email'
        else:
            return 'text'

    @staticmethod
    def detect_field_types(fields):
        return {field_name: FormValidator.detect_field_type(value)
                for field_name, value in fields.items()}