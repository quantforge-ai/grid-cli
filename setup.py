from setuptools import setup, find_packages

setup(
    name='grid-cli',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'rich',
        'requests',
        'praw',
        # 'tree-sitter', # Uncomment if/when you use C++ support
    ],
    entry_points={
        'console_scripts': [
            # TARGET: module 'grid.main', function 'run_cli'
            'grid = grid.main:main',  
        ],
    },
)