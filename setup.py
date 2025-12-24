"""
setup.py for IntentLang
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="intentlang",
    version="1.0.0",
    author="IntentLang Contributors",
    description="A natural language programming language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/intentlang/intentlang",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Interpreters",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "networkx>=3.0",
        "rich>=13.0",
    ],
    extras_require={
        "viz": ["matplotlib>=3.5", "pygraphviz>=1.9"],
        "dev": ["pytest>=7.0", "black>=23.0", "flake8>=6.0"],
    },
    entry_points={
        "console_scripts": [
            "intentlang=intentlang.__main__:main",
        ],
    },
)
