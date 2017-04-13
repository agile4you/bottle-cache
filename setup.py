from distutils.core import setup
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('bottle_cache/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')
    ).group(1)))


setup(
    name='bottle-cache',
    version=version,
    packages=['test', 'bottle_cache'],
    url='https://github.com/agile4you/bottle-cache',
    license='GLPv3',
    author='Papavassiliou Vassilis',
    author_email='vpapavasil@gmail.com',
    install_requires=['bottle', 'six', 'redis', 'ujson', 'hiredis'],
    description='Cache Plugins for bottle.py applications'
)
