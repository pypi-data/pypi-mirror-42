import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="persis",
    version="0.0.6",
    author="Martin Skarzynski",
    author_email="marskar@gmail.com",
    description=".",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/marskar/persis",
    packages=setuptools.find_packages('src'),
    package_dir={"": "src"},
    package_data={'persis': ['data/*', 'models/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
