from setuptools import setup

setup(
    name='conform',
    version='0.1.0',
    description='A simple config generator',
    url='https://bitbucket.org/jonsul/cfgen',
    author='Jon Sully',
    author_email='jon@sul.ly',
    license='MIT',
    packages=['conform'],
    entry_points={
        'console_scripts': ['conform=conform.cli:cli'],
    },
    install_requires=[
        'aiofiles',
        'aiohttp',
        'Click',
        'colorama',
        'graphviz',
        'Jinja2',
        'paramiko',
        'pydantic',
        'PyYAML',
        'toml',
    ],
    zip_safe=False)