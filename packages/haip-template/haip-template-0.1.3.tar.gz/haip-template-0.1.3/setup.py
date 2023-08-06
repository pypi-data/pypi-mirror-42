import setuptools

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="haip-template",
    version="0.1.3",
    author="Reinhard Hainz",
    author_email="reinhard.hainz@gmail.com",
    description="Jinja2 based template module.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haipdev/template",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "haip_config>=0.1.7",
        "jinja2>=2.10"
    ]
)
