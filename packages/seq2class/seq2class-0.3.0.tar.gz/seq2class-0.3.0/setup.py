import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seq2class",
    version="0.3.0",
    author="Pranjal-Vijay",
    author_email="pranjalvijaykota@gmail.com",
    description="seq2class is developed for text classification using LSTM",
    long_description=open('README.rst', 'r').read(),
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