import os

env = os.environ.get('APP_ENV', 'development')

if env in ('development', 'staging', 'production'):
    exec(f'from .{env} import *')
