import os
import sys
from django.contrib.auth.management.commands.createsuperuser import (
    Command as CreateSuperUserCommand,
    NotRunningInTTYException
)
from django.core.management.base import CommandError
from django.contrib.auth.management import get_default_username
from django.core import exceptions
from django.utils.text import capfirst


class Command(CreateSuperUserCommand):
    def handle(self, *args, **options):
        username = options[self.UserModel.USERNAME_FIELD]
        database = options['database']
        user_data = {}
        verbose_field_name = self.username_field.verbose_name
        try:
            if options['interactive']:
                # Same as user_data but without many to many fields and with
                # foreign keys as fake model instances instead of raw IDs.
                fake_user_data = {}
                if hasattr(self.stdin, 'isatty') and not self.stdin.isatty():
                    raise NotRunningInTTYException
                default_username = get_default_username()
                if username:
                    error_msg = self._validate_username(username, verbose_field_name, database)
                    if error_msg:
                        self.stderr.write(error_msg)
                        username = None
                elif username == '':
                    raise CommandError('%s cannot be blank.' % capfirst(verbose_field_name))
                # Prompt for username.
                while username is None:
                    message = self._get_input_message(self.username_field, default_username)
                    username = self.get_input_data(self.username_field, message, default_username)
                    if username:
                        error_msg = self._validate_username(username, verbose_field_name, database)
                        if error_msg:
                            self.stderr.write(error_msg)
                            username = None
                            continue
                user_data[self.UserModel.USERNAME_FIELD] = username
                fake_user_data[self.UserModel.USERNAME_FIELD] = (
                    self.username_field.remote_field.model(username)
                    if self.username_field.remote_field else username
                )
                # Prompt for required fields.
                for field_name in self.UserModel.REQUIRED_FIELDS:
                    field = self.UserModel._meta.get_field(field_name)
                    user_data[field_name] = options[field_name]
                    while user_data[field_name] is None:
                        message = self._get_input_message(field)
                        input_value = self.get_input_data(field, message)
                        user_data[field_name] = input_value
                        if field.many_to_many and input_value:
                            if not input_value.strip():
                                user_data[field_name] = None
                                self.stderr.write('Error: This field cannot be blank.')
                                continue
                            user_data[field_name] = [pk.strip() for pk in input_value.split(',')]
                        if not field.many_to_many:
                            fake_user_data[field_name] = input_value

                        # Wrap any foreign keys in fake model instances
                        if field.many_to_one:
                            fake_user_data[field_name] = field.remote_field.model(input_value)
            else:
                # Non-interactive mode.
                # Use username from environment variable, if not provided in
                # options.
                if username is None:
                    username = os.environ.get('DJANGO_SUPERUSER_' + self.UserModel.USERNAME_FIELD.upper())
                if username is None:
                    raise CommandError('You must use --%s with --noinput.' % self.UserModel.USERNAME_FIELD)
                else:
                    error_msg = self._validate_username(username, verbose_field_name, database)
                    if error_msg:
                        raise CommandError(error_msg)

                user_data[self.UserModel.USERNAME_FIELD] = username
                for field_name in self.UserModel.REQUIRED_FIELDS:
                    env_var = 'DJANGO_SUPERUSER_' + field_name.upper()
                    value = options[field_name] or os.environ.get(env_var)
                    if not value:
                        raise CommandError('You must use --%s with --noinput.' % field_name)
                    field = self.UserModel._meta.get_field(field_name)
                    user_data[field_name] = field.clean(value, None)

            self.UserModel._default_manager.db_manager(database).create_superuser(**user_data)
            if options['verbosity'] >= 1:
                self.stdout.write("Superuser created successfully.")
        except KeyboardInterrupt:
            self.stderr.write('\nOperation cancelled.')
            sys.exit(1)
        except exceptions.ValidationError as e:
            raise CommandError('; '.join(e.messages))
        except NotRunningInTTYException:
            self.stdout.write(
                'Superuser creation skipped due to not running in a TTY. '
                'You can run `manage.py createsuperuser` in your project '
                'to create one manually.'
            )

