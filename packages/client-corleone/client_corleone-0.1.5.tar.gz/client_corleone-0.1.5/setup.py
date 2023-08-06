from setuptools import setup, find_packages

import client_corleone

setup(
    name='client_corleone',
    version=client_corleone.__version__,
    packages=find_packages(),
    author='Luis Sieira',
    author_email='luis.sieira@spacebar.fr',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description='A python experimental client for Telegram bot API you can\'t refuse',
    long_description=open('README.md').read(),
    install_requires=['requests'],
    include_package_data=True,
    url='https://github.com/sieira/client_corleone',
    license='BSD',
)
