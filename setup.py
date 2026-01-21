from setuptools import setup, find_packages

setup(
    name='grid-cli',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'rich',
        'urllib3',
    ],
    entry_points={
        'console_scripts': [
            'grid = grid.main:main',
        ],
    },
    author='QuantForge AI',
    description='A sentient developer companion that judges your code.',
)