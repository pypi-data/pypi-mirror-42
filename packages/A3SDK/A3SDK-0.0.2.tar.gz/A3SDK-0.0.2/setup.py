from setuptools import setup

setup(
    name='A3SDK',
    version='0.0.2',
    author='Vyacheslav Anzhiganov',
    author_email='vanzhiganov@ya.ru',
    packages=[
        'A3SDK'
    ],
    install_requires=[
        'requests',
        'zeep',
    ]
)
