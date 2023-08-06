import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="smtools",
    version="0.2.0",
    author="Sy Redding",
    description="Redding Lab analysis tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/github/ReddingLab/smtools",
    packages=setuptools.find_packages(),
    package_data={'smtools': ['testdata/*.tif']},
    include_package_data=True,
    install_requires=[
          'numpy','scipy','scikit-image','matplotlib'
      ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)