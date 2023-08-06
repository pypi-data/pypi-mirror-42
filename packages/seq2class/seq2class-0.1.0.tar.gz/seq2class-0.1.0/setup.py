import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seq2class",
    version="0.1.0",
    author="Pranjal-Vijay",
    author_email="pranjalvijaykota@gmail.com",
    description="seq2class is a solution for text classification. ",
    long_description="text classification using lstm is made easy via seq2class package.This package is build by harnesing the capabilities of  LSTM(Long short term Memory) model.",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License"
    ],
	install_requires=[
        'keras',
        'numpy',
		 'pandas',
		 'sklearn'
    ]
)