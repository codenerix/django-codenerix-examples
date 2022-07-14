#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if 'backend' in sys.argv:
        sys.argv.pop(sys.argv.index('backend'))
        mode = 'backend'
    elif 'frontend' in sys.argv:
        sys.argv.pop(sys.argv.index('frontend'))
        mode = 'frontend'
    else:
        mode = 'frontend'
    os.environ.setdefault("CODENERIX_MODE", mode)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "erp.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
