import setuptools

with open("README.md", "r") as fh:
	readme = fh.read()

setuptools.setup(
	name="cv-recon",
	version="0.0.4",
	author="Arturo Aguilar Lagunas",
	author_email="aguilar.lagunas.arturo@gmail.com",
	description="A computer vision toolkit focused in color detection and feature matching using OpenCV. It allows you to easily start the picamera in case you're using a Raspberry PI.",
	long_description=readme,
	long_description_content_type="text/markdown",
	url="https://github.com/AguilarLagunasArturo/cv-recon",
	packages=setuptools.find_packages(),
	keywords='opencv color-detection feature-matching computer-vision picamera',
	classifiers=[
		"Development Status :: 4 - Beta",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
