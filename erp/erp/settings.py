import os

if os.environ.get("CODENERIX_MODE", "frontend") == "backend":
    from erp.settings_backend import *
else:
    from erp.settings_frontend import *
