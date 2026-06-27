"""Application configuration."""

import os
import sys

# In PyInstaller single-file mode, use the exe's directory for data persistence
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'finance_data.json')
SECRET_KEY = os.environ.get('SECRET_KEY', 'family_finance_default_key')
