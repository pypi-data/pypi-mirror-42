from setuptools import setup, find_packages

import client_corleone

setup(
    name='client_corleone',
    version=client_corleone.__version__,
    packages=find_packages(),
    author='Luis Sieira',
    author_email='luis.sieira@spacebar.fr',
    description='A python experimental client for Telegram bot API you can\'t refuse',
    long_description=open('README.md').read(),
    install_requires=['requests'],
    include_package_data=True,
    url='https://github.com/sieira/client_corleone',
    license='BSD',
)
