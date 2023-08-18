# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    scripts      = ['scripts/update_detail.py', 'scripts/demo.py'],
    entry_points = {'scrapy': ['settings = tutorial.settings']},
)
