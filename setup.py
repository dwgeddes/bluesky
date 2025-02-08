from setuptools import setup, find_packages

setup(
    name="bluesky_social",
    version="0.1.0",
    description="A Python module for BlueSky social networking",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "atproto",
        "Pillow",
        "keyring",
        # ...other dependencies...
    ],
    entry_points={
        "console_scripts": [
            "bluesky-social=bluesky_social.cli:main"
        ]
    },
)
