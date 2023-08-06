import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FastSent",
    version="0.1.0",
    author="Pranjal-Vijay",
    author_email="pranjalvijaykota@gmail.com",
    description="FastSent is one of the solution for Sentiment classification using Recurrent Neural Networks. ",
    long_description="FastSent is a sentiment classification package for the input text.FastSent enables sequential model capabilities to enhance the sentiment classification of input text.",
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