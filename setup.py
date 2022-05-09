import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="japanese-candlestick",
    version="0.1.0",
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
    install_requires=["numpy==1.22.3",
                      "pandas==1.4.2",
                      "python-binance==1.0.16",
                      "telegram-send==0.33.1",
                      "schedule==1.1.0"],
)
