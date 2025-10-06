from tinydb import TinyDB


class FormTemplateDB:
    def __init__(self, db_path: str = 'templates.json'):
        self.db = TinyDB(db_path)
        self.templates = self.db.table('templates')

    def add_template(self, template: dict) -> None:
        self.templates.insert(template)

    def find_matching_template(self, fields: dict[str, str]) -> dict | None:
        for template in self.templates.all():
            template_fields = {k: v for k, v in template.items() if k != 'name'}
            match = True
            for field_name, field_type in template_fields.items():
                if field_name not in fields or fields[field_name] != field_type:
                    match = False
                    break
            if match:
                return template

        return None

    def get_all_templates(self) -> list[dict]:
        return self.templates.all()