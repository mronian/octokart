#!/usr/bin/env python
import os
import sys
from django.conf import settings

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "octokart.settings")

	from django.core.management import execute_from_command_line

	if sys.argv[1] == 'runserver':
		settings.SERVER_IP, settings.SERVER_PORT = sys.argv[2].split(":")
		settings.DATABASES['default']['NAME'] += settings.SERVER_PORT
		execute_from_command_line(sys.argv)
	else:
		settings.SERVER_PORT = sys.argv[len(sys.argv) - 1]
		settings.DATABASES['default']['NAME'] += settings.SERVER_PORT
		execute_from_command_line(sys.argv[:-1])
