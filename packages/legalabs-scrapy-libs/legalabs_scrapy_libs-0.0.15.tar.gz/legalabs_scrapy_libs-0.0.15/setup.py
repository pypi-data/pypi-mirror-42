import setuptools
import os

root_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(root_path, "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="legalabs_scrapy_libs",
    version="0.0.15",
    author="Legal Labs",
    author_email="inteligencia@legalabs.com.br",
    description="Library with support functions for building scrapers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/LegalLabs/crawlers/scrapy_libs",
    packages=setuptools.find_packages(),
    package_dir={'legalabs_scrapy_libs':'legalabs_scrapy_libs'},
    package_data={'legalabs_scrapy_libs':['./schemas/*.yaml']},
    install_requires=[
        'CMRESHandler'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
