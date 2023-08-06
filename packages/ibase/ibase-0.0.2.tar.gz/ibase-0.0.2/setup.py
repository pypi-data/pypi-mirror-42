import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ibase",
    version="0.0.2",
    install_requires=[
        "requests"
    ],
    author="Hanz",
    author_email="wanghan0406@autohome.com.cn",
    description="interface testcase script basefunc",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yangeren/ibase",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)