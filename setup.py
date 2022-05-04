import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    INSTALL_REQUIRES = [l.split('#')[0].strip() for l in fh if not l.strip().startswith('#')]

setuptools.setup(
    name="japanese-candlestick",
    version="0.0.1",
    author="Vincent Vandenbussche",
    author_email="vandenbussche.vincent@gmail.com",
    license="MIT",
    description="Japanese candlestick pattern",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vincent-vdb/japanese-candlestick-pattern",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    keywords="trading candlestick analysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    install_requires=INSTALL_REQUIRES,
)
