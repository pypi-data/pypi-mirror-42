from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="waterbend",
    version="0.0.0",
    author="Bulat Bochkariov",
    author_email="bulat+pypi@bochkariov.com",
    description="High-level Python library for DigitalOcean's REST API (v2)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["waterbend"],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
)
