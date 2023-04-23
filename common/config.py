# -*- coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv

if getattr(sys, 'frozen', False):
    rootdir = os.path.dirname(sys.executable)
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    rootdir = os.path.dirname(bundle_dir)

load_dotenv(os.path.join(rootdir, ".env"))

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = os.getenv("MYSQL_PORT", "6379")
