import argparse
import sys
from database import FormTemplateDB
from form_validator import FormValidator
import json


def main():
    parser = argparse.ArgumentParser(description='Form Template Matcher')
    parser.add_argument('command', choices=['get_tpl'], help='Command to execute')
    args_list = sys.argv[1:]
    field_args = [arg for arg in args_list if arg.startswith('--') and '=' in arg]
    for arg in field_args:
        field_name = arg[2:].split('=')[0]
        parser.add_argument(f'--{field_name}', dest=field_name)
    args = parser.parse_args()
    if args.command == 'get_tpl':
        fields = {}
        for field_name in dir(args):
            if not field_name.startswith('_') and field_name not in ['command']:
                value = getattr(args, field_name)
                if value is not None:
                    fields[field_name] = value
        db = FormTemplateDB('templates.json')
        matching_template = db.find_matching_template(fields)
        if matching_template:
            print(matching_template['name'])
        else:
            field_types = FormValidator.detect_field_types(fields)
            print(json.dumps(field_types, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()