from distutils.core import setup

with open('README.txt') as file:
    readme = file.read()


setup(
    name='stsun_first_wargame',
    version='2.0.0',
    package=['wargame'],
    url='https://testpypi.python.org/pypi/stsun_first_wargame/',
    license='LICENSE.txt',
    description='text pkg ignore',
    long_description=readme,
    author='stsun',
    author_email='stsun@leqee.com',
)