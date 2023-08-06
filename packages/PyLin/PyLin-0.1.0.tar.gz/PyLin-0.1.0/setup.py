from distutils.core import setup

setup(
    name='PyLin',
    version='0.1.0',
    author='Jan Offermann',
    author_email='jano@uchicago.edu',
    packages=['pylin'],
    url='http://pypi.python.org/pypi/PyLin/',
    license='LICENSE.txt',
    description='Lin Engineering step motor driver software.',
    long_description=open('README.md').read(),
    install_requires=[
	'serial'
    ],
)
