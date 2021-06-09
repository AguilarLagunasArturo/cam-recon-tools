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
| python3			| Refer to the official [website][3]                           		|
| opencv			| Refer to the official [installation guide][1] (tested with version 4.5.2)		|
| numpy				| `pip install numpy`			|
| picamera		| Installed by default in Raspberry PI OS (required only if working with a picamera)	|

# Instalation
- `pip install cv-recon`

# Usage
See examples in the [examples folder][2] or test it directly form source. Change directory `cd cv_recon/recon/` once in this folder you can run:  

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
| Property | Description | Type | Default |
| :- | :- | :- | :- |
| lower | Lower HSV boundary | np.array | None |
| upper | Upper HSV boundary | np.array | None |
| im_mask | Mask obtained from the HSV boundaries | np.array | None |
| im_cut | Portions of the frame containing the color boundaries | np.array | None |
| im_edges | Canny edge detection applied to _im_mask_ | np.array | None |
| im_contours | Contours of the detected objects drawn on the current frame | np.array | None |

### Methods
##### loadSettings(settings)
Loads HSV settings from a generated .log file.  

| Args | Description | Default |
| :- | :- | :- |
| settings | Path to .log file with generated HSV settings | None |

__returns:__ _None_

#### dumpSettings(output='last.log')
Generates a .log file with the current HSV settings.

| Args | Description | Default |
| :- | :- | :- |
| output | Path in witch the file is gonna be written | 'last.log' |

__returns:__ _None_

#### createSliders()
Creates a window with sliders in order to adjust the HSV settings.  
__returns:__ _None_

#### updateHSV()
Updates the current HSV settings with the slider values.  
__returns:__ _None_

#### getMaskBoxes(im_base, im_hsv, min_area=20, scale=0.1)
Generates a list containing the bounding box (x, y, w, h) of the object.

| Args | Description | Default |
| :- | :- | :- |
| im_base | Base image in bgr format | None |
| im_hsv | Base image in hsv format | None |
| min_area | Minimum area to generate the coordinates | 20 |
| scale | Scale of the bounding box | 0.1 |

__returns:__ bounding_boxes

#### getMaskBoxesArea(im_base, im_hsv, min_area=20, scale=0.1)
Generates two lists containing the bounding box (x, y, w, h) and the estimated area of each object.

| Args | Description | Default |
| :- | :- | :- |
| im_base | Base image in bgr format | None |
| im_hsv | Base image in hsv format | None |
| min_area | Minimum area to generate the coordinates | 20 |
| scale | Scale of the bounding box | 0.1 |

__returns:__ bounding_boxes, areas

## Class: Features

``` python
from cv_recon import Features
import cv2 as cv

# load source image
im_source = cv.imread('image.jpg')
# create Features object (detects 1000 matching features)
my_feature = Features(im_source, 1000)
```

### Properties

| Property | Description | Type | Default |
| :- | :- | :- | :- |
| im_source | Image containing the source image | np.array | _im_source_ |
| im_source_kp | Image containing the source image keypoints | np.array | _im_source_ keypoints |
| im_target | Image containing the target image | np.array | None |
| im_target_kp | Image containing the target image keypoints | np.array | None |

### Methods

#### loadTarget(im)

| Args | Description | Default |
| :- | :- | :- |
| output | Path in witch the file is gonna be written | 'last.log' |

__returns:__ None
#### getMatches(distance)

| Args | Description | Default |
| :- | :- | :- |
| output | Path in witch the file is gonna be written | 'last.log' |

__returns:__ None
#### matchPoints(matches)

| Args | Description | Default |
| :- | :- | :- |
| output | Path in witch the file is gonna be written | 'last.log' |

__returns:__ None
#### getBoxes(matches, min_matches)

| Args | Description | Default |
| :- | :- | :- |
| output | Path in witch the file is gonna be written | 'last.log' |

__returns:__ None

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
