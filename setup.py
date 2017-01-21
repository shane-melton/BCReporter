from setuptools import setup, find_packages

with open('README') as f:
    readme = f.read()

setup(
    name='BCReporter',
    version='0.1.0',
    #description='',
    #long_description=readme,
    #author='',
    #author_email='',
    #url='',
    #license=None,
    packages=find_packages(exclude=('tests'))
)

