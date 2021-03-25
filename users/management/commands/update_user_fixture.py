import os
import json
from django.core.management import BaseCommand, CommandError


def update_fixture_data(fixture_data):
    print('fixture_data', fixture_data)
    if fixture_data['model'] == 'auth.user':
        fixture_data['model'] = 'users.authuser'
        del fixture_data['fields']['username']

    return fixture_data


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--file', '-f', type=str, default=None)

    def handle(self, *args, **options):
        file = options.get('file')

        if not file:
            raise CommandError('File not provided.')

        if not file.endswith('.json'):
            raise CommandError('Only .json file supported.')

        try:
            with open(file) as json_file:
                fixture_data = json.load(json_file)
        except FileNotFoundError:
            raise CommandError('File not found.')

        fixture_data_map = map(update_fixture_data, fixture_data)
        fixture_data = list(fixture_data_map)

        with open(file, 'w') as json_file:
            json.dump(fixture_data, json_file)
