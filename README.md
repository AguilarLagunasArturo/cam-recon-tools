# About
A computer vision toolkit focused in color detection and feature matching using OpenCV. It allows you to easily start the picamera in case you're using a Raspberry PI.  

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
| python3			| Refer to the official [installation guide][3]                           		|
| opencv			| Refer to the official [installation guide][1] (tested with version 4.5.2)		|
| numpy				| `pip install numpy` (required by OpenCV and used to work with images)				|
| picamera		| Installed by default in Raspberry PI OS (required if working with picamera)	|

# Instalation
- `pip install cv-recon`

# Usage
See examples in the [examples folder][2] or test it directly form source. From source `cd cv_recon/recon/` once in this folder you can run:  

| Command 																	| Description 																			| Preview |
| :- 																				| :- 																								| :- 			|
| `python colorspace.py` 										| Generate HSV settings for an specific color 	| TODO 		|
| `python colorspace.py <path to log file>` | Load settings to detect a single color 						| TODO 		|
| `python features.py <path to an image>` 	| Perform feature detection against a given image | TODO 		|

# Documentation
## Class: Colorspace
``` python
from cv_recon import Colorspace
# load generated settings
colorspace_1 = Colorspace('settings.log')
# or set hsv lower and upper boundaries
colorspace_2 = Colorspace([ [0, 0, 0], [179, 255, 255] ])
```
### Properties
| Property | Description | Type |
| :- | :- | :- |
| Item One | Item Two | Item Three |

### Methods
| Method | Description | Returns |
| :- | :- | :- |
| Item One | Item Two | Item Three |

## Class: Features

``` python
from cv_recon import Features
```
### Properties


### Methods

## Class: PiCam

``` python
from cv_recon.picam import PiCam
```
### Properties
| Property | Description | Type |
| :- | :- | :- |
| Item One | Item Two | Item Three |

### Methods

## Module: cv_tools
``` python
from cv_recon import cv_tools
```

### Properties
| Property | Description | Type |
| :- | :- | :- |
| Item One | Item Two | Item Three |

### Methods

## Module: cv_recon
### Functions

[1]:https://docs.opencv.org/4.5.2/da/df6/tutorial_py_table_of_contents_setup.html
[2]:https://github.com/AguilarLagunasArturo/cv-recon/tree/main/examples
[3]:https://www.python.org/downloads/
