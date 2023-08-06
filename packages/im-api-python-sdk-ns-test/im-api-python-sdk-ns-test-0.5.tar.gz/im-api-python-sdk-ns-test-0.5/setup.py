import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name='im-api-python-sdk-ns-test',
	version='0.5',
	author="Voximplant",
	description="Voximplant IM-API python SDK",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://voximplant.com/docs/references/messagingapi",
	packages=setuptools.find_packages(),
	install_requires=[
		"grpcio-tools",
		"PyJWT",
		"cryptography",
	],
	classifiers=[
		"Programming Language :: Python :: 2.7",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
