from setuptools import setup, find_packages

setup(
    name="ghostme",
    version="1.0.0",
    description="Change your iPhone's GPS location over USB",
    packages=find_packages(),
    include_package_data=True,
    package_data={"ghostme": ["templates/*", "static/*"]},
    install_requires=[
        "pymobiledevice3>=4.0.0",
        "flask>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ghostme=ghostme.__main__:main",
        ],
    },
    python_requires=">=3.9",
)
