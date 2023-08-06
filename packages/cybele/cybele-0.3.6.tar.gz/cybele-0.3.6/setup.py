from setuptools import setup, find_packages


from cybele import __version__


with open("README.md", encoding="utf8") as f:
    readme = f.read()

setup(
    name="cybele",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    description="cli password manager",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=[
        "Click==7.0",
        "pycrypto==2.6.1",
        "pyperclip==1.7.0",
        "terminaltables==3.1.0",
        "tqdm==4.31.1"
    ],
    url="https://gitlab.com/dithyrambe/cybele",
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
    license="MIT",
    entry_points={
        'console_scripts': [
            "cybele = cybele.cli:cybele"
        ]
    }
)
