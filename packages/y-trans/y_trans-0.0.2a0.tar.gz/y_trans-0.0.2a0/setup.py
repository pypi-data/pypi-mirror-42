import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="y_trans",
    version="0.0.2a",
    author="sergey-sy",
    author_email="maiyashik@gmail.com",
    description="Machine translation with Yandex.Translate API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sergey-sy/y_trans",
    scripts=["bin/y_trans"],
    keywords=["yandex", "yandex translate", "yandex translator", "translator"],
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
