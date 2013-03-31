from distutils.core import setup

setup(
    name='Gritty',
    version='0.1.2',
    author='Joe Cross',
    author_email='joe.mcross@gmail.com',
    packages=['gritty', 'gritty.demos'],
    url='http://pypi.python.org/pypi/Gritty/',
    license='LGPL.txt',
    description='A basic module for rendering a grid using pygame',
    long_description=open('README.rst').read(),
    install_requires=[
        "pygame >= 1.8.0",
    ],
)
