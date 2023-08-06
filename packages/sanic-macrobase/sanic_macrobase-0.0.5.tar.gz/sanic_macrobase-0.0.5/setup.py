from setuptools import setup, find_packages

setup(
    name='sanic_macrobase',
    version='0.0.5',
    packages=find_packages(),
    url='https://github.com/mbcores/sanic-macrobase',
    license='MIT',
    author='Alexey Shagaleev',
    author_email='alexey.shagaleev@yandex.ru',
    description='Sanic driver for macrobase framework',
    install_requires=[
        'macrobase-driver>=0.0.5',
        'sanic==18.12.0',
        'structlog==19.1.0'
    ]
)
