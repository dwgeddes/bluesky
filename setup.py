from setuptools import setup, find_packages

setup(
    name="bluesky-social",
    version="0.1.0",  # update version as needed
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Pillow",
        "keyring",
        "atproto",  # adjust if needed
    ],
    entry_points={
        "console_scripts": [
            "bluesky=bluesky_social.cli:main",
        ],
    },
    author="David Geddes",
    author_email="dwgeddes@gmail.com",
    description="A CLI and API for interacting with BlueSky.",
    url="https://github.com/dwgeddes/bluesky-social",  # update URL if applicable
)
