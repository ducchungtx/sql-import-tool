from setuptools import setup, find_packages

setup(
    name='sql-import-tool',
    version='0.1.0',
    author='Chung Nguyen',
    author_email='zrmedia9@gmail.com',
    description='A tool to import SQL databases into MySQL with file splitting capabilities.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'PyMySQL>=1.1.0',
        'PyYAML>=6.0.1',
        'tqdm>=4.66.1',
        'click>=8.1.7',
    ],
    entry_points={
        'console_scripts': [
            'sql-import=main:cli',
        ],
    },
)