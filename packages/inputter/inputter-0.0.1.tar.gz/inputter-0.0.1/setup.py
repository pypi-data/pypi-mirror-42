import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="inputter",
	version="0.0.1",
	author="mat",
	author_email="fake@email.lol",
	description="Input detector",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://repl.it/@mat1/inputter",
	packages=setuptools.find_packages(),
	install_requires=[],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)