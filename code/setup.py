#!/usr/bin/env python3
"""Setup script for AI-Textpad."""

from setuptools import setup, find_packages

VERSION = "0.1.0"

setup(
    name="ai-textpad",
    version=VERSION,
    description="LLM-powered text transformation utility for Linux desktop",
    author="Daniel Rosehill",
    author_email="public@danielrosehill.com",
    url="https://github.com/danielrosehill/AI-Textpad",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyQt6>=6.6.0",
        "httpx>=0.25.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-textpad=ai_textpad.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
)
