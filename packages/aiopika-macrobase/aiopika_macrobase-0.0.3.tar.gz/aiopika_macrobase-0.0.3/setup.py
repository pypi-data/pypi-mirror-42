from setuptools import setup, find_packages

setup(
    name='aiopika_macrobase',
    version='0.0.3',
    packages=find_packages(),
    url='https://github.com/mbcores/aiopika-macrobase',
    license='MIT',
    author='Alexey Shagaleev',
    author_email='alexey.shagaleev@yandex.ru',
    description='Aio-pika driver for macrobase framework',
    install_requires=[
        'macrobase-driver>=0.0.5',
        'aio-pika==5.2.2',
        'python-rapidjson==0.7.0',
        'structlog==19.1.0'
    ]
)
