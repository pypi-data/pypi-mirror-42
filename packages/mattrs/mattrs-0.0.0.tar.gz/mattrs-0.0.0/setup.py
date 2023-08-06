from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="mattrs",
    version="0.0.0",
    author="Bulat Bochkariov",
    author_email="bulat+pypi@bochkariov.com",
    description="Use Marshmallow schemas with attrs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["mattrs"],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
)
