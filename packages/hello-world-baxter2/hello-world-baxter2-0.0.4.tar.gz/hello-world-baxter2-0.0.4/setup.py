import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hello-world-baxter2",
    version="0.0.4",
    author="Baxter Callan",
    author_email="baxcallan@gmail.com",
    py_modules=["hello_world"],
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/baxter2/hello-world-baxter2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
