"""
Setup script for the BlueSky social media client package.
"""
from setuptools import setup, find_packages

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bluesky-social",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    
    # Core dependencies
    install_requires=[
        "atproto>=0.1.0,<0.2.0",
        "Pillow>=9.0.0,<10.0.0",
        "keyring>=23.0.0,<25.0.0",
        "colorama",  # Add colorama as a dependency
    ],
    
    # Development dependencies
    extras_require={
        "dev": [
            "pytest>=7.0.0,<8.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ]
    },
    
    # Command-line entry point
    entry_points={
        "console_scripts": [
            "bluesky=bluesky_social.cli:main",
        ],
    },
    
    # Metadata
    author="David Geddes",
    author_email="dwgeddes@gmail.com",
    description="A CLI and API for interacting with BlueSky social network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dwgeddes/bluesky-social",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications",
        "Topic :: Internet",
    ],
    python_requires=">=3.9",
)
