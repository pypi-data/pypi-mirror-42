import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='print_nest',
    version='1.3.0',
    py_modules=['print_nest'],
    author='GiantFurosemide',
    author_email='18640057101@163.com',
    url="https://github.com/Mokusama",
    description='a little tool for printing nested list.',
    long_description = long_description,
    long_description_content_type="text/markdown",
    ackages=setuptools.find_packages(),
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: MacOS",
        ],
)

