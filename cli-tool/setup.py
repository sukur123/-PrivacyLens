"""
Setup script for PrivacyLens CLI Tool
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="privacylens",
    version="1.0.0",
    author="PrivacyLens Team",
    author_email="contact@privacylens.org",
    description="A command-line tool for analyzing website privacy and security",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/PrivacyLens",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "privacylens=privacylens.__main__:cli",
        ],
    },
    keywords="privacy security web analysis cli tool",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/PrivacyLens/issues",
        "Source": "https://github.com/yourusername/PrivacyLens",
        "Documentation": "https://github.com/yourusername/PrivacyLens/blob/main/README.md",
    },
)
