from setuptools import setup, find_packages

setup(
    name="duckdns-updater",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "pystray",
        "Pillow",
    ],
    entry_points={
        "gui_scripts": [
            "duckdns-updater = duckdns_updater.__init__:main",
        ],
    },
    author="Jose Porcel",
    description="A DuckDNS IP updater application.",
    long_description=open('README.md').read(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
