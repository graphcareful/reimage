import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reimage", # Replace with your own username
    version="0.1",
    author="Robert Blafford",
    author_email="rblafford@gmail.com",
    description="Program to store and load personal configs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/graphcareful/reimage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
