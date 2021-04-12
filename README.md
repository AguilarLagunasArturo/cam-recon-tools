# About
A computer vision toolkit focused in color detection and feature matching using OpenCV.  
It allows you to easily start the picamera in case you're using a Raspberry PI.  

# Some of the stuff you can currently do
- Color recon
	- Find HSV colorspace for a specific color
	- Find bounding boxes given a HSV colorspace
- Feature matching
	- Draw matches
	- Find bounding boxes
- Picamera
	- Easily start the picamera
- Tools
	- Draw boxes
	- Draw boxes' offset from the center of the frame
	- Stack frames in a grid

# Dependencies
| Dependency	| Installation																																|
| :- 					| :- 																																					|
| numpy				| `pip install numpy` (required by OpenCV and used to work with images)				|
| opencv			| Refer to the official [installation guide][1] (tested with version 4.5.2)		|
| picamera		| Installed by default in Raspberry PI OS (required if working with picamera)	|

# Instalation
- `pip install cv-recon`

# Usage
See examples in the [examples folder][2] or test it directly form source.   From source `cd cv_recon/recon/` once in this folder you can run:  

| Command 																	| Description 																			| Preview |
| :- 																				| :- 																								| :- 			|
| `python colorspace.py` 										| Target a single color and generate its settings 	| TODO 		|
| `python colorspace.py <path to log file>` | Load settings to detect a single color 						| TODO 		|
| `python features.py <path to an image>` 	| Perform feature detection against the given image | TODO 		|

# Examples
- TODO

# Documentation
- TODO

[1]:https://docs.opencv.org/4.5.2/da/df6/tutorial_py_table_of_contents_setup.html
[2]:https://github.com/AguilarLagunasArturo/cv-recon/tree/main/examples
