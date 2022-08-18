import os

if os.environ.get("CODENERIX_MODE", "backend") == "backend":
    print("Starting Backend...")
    from erp.settings_backend import *
else:
    print("Starting Frontend...")
    from erp.settings_frontend import *
