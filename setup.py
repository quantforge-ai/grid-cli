from setuptools import setup, find_packages

setup(
    name="grid-cli",
    version="1.0.0",
    author="QuantGrid Team",
    description="The Universal Interface for Financial Intelligence",
    packages=find_packages(),
    install_requires=[
        "click",
        "rich",
        "prompt_toolkit",
        "requests",
        "pyyaml",
        "loguru",
        "psutil",
        "huggingface_hub"
    ],
    entry_points={
        "console_scripts": [
            "grid=grid.main:main",
        ],
    },
    python_requires=">=3.9",
)
