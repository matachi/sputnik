from os import path
import fileinput

from django.utils.crypto import get_random_string

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
secret_key = get_random_string(50, chars)

current_file_dir = path.dirname(path.abspath(__file__))
settings_file_name = path.join(current_file_dir, 'hydra', 'settings.py')

# Solution found on http://stackoverflow.com/a/2962828/595990
for line in fileinput.input(settings_file_name, inplace=True):
    print(line.replace('INSERT_SECRET_KEY_HERE', secret_key), end='')
