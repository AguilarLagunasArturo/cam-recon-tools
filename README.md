# About
A computer vision toolkit focused on color detection and feature matching using OpenCV. It allows you to easily start the picamera in case you're using a Raspberry PI.

# Some of the stuff you can currently do
- Color detection
	- Detect a range of colors in an image using HSV boundaries.
	- Find bounding boxes.
- Feature matching
	- Draw matches between a source and target image.
	- Find bounding boxes.
- Picamera
	- Easily start the picamera.
- Tools
	- Draw boxes.
	- Draw boxes' offset from the center of the frame.
	- Stack frames in a grid.

# Dependencies
| Dependency | Installation |
| :- | :- |
| python3	| Refer to the official [website][3] |
| opencv	| Refer to the official [installation guide][1] (tested with version 4.5.2) |
| numpy	| `pip install numpy` |
| picamera | Installed by default in Raspberry PI OS (required only if working with a picamera)	|

# Installation
``` bash
pip install cv-recon
```

# Usage
See examples in the [examples folder][2] or test it directly form source. Change directory `cd cv_recon/recon/` once in this folder you can run:  

| Command | Description | Preview |
| :- | :- | :- 			|
| `python colorspace.py` | Generates HSV settings to detect a specific color | ![Colorspace example 1](https://raw.githubusercontent.com/AguilarLagunasArturo/cv-recon/main/preview/colorspace-1.png) |
| `python colorspace.py <path to .log file>` | Loads HSV settings to detect a specific color | ![Colorspace example 2](https://raw.githubusercontent.com/AguilarLagunasArturo/cv-recon/main/preview/colorspace-2.png) |
| `python features.py <path to an image>` | Performs feature detection against a given image | ![Feature matching example](https://raw.githubusercontent.com/AguilarLagunasArturo/cv-recon/main/preview/feature-matching.png) |

# Documentation
## Class: Colorspace(hsv_settings=None)
This class allows you to detect a range of colors using HSV boundaries. You can generate the settings or set them directly. See examples [here][4].

| Args | Description | Default |
| :- | :- | :- |
| hsv_settings | Path to .log file containing the HSV settings or list containing lower and upper HSV boundaries | None |

### Import example
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
| lower | Lower HSV boundary | list | None |
| upper | Upper HSV boundary | list | None |
| im_mask | Mask obtained from the HSV boundaries | np.array | None |
| im_cut | Portions of the frame containing the color boundaries | np.array | None |
| im_edges | Canny edge detection applied to _im_mask_ | np.array | None |
| im_contours | Contours of the detected objects drawn on the current frame | np.array | None |

### Methods
#### `loadSettings(settings)`
Loads HSV settings from a generated .log file.  

| Args | Description | Default |
| :- | :- | :- |
| settings | Path to .log file with generated HSV settings | None |

__returns:__ _None_

#### `dumpSettings(output='last.log')`
Generates a .log file with the current HSV settings.

| Args | Description | Default |
| :- | :- | :- |
| output | Path in which the file is gonna be written | 'last.log' |

__returns:__ _None_

#### `createSliders()`
Creates a window with sliders in order to adjust the HSV settings.  
__returns:__ _None_

#### `updateHSV()`
Updates the current HSV settings with the current slider values.  
__returns:__ _None_

#### `getMaskBoxes(im_base, im_hsv, min_area=20, scale=0.1)`
Generates a list containing the bounding boxes (x, y, w, h) of the objects.

| Args | Description | Default |
| :- | :- | :- |
| im_base | Base image in bgr format | None |
| im_hsv | Base image in hsv format | None |
| min_area | Minimum area to generate the coordinates | 20 |
| scale | Scale of the bounding box | 0.1 |

__returns:__ bounding_boxes

#### `getMaskBoxesArea(im_base, im_hsv, min_area=20, scale=0.1)`
Generates two lists containing the bounding boxes (x, y, w, h) and the estimated area of each object.

| Args | Description | Default |
| :- | :- | :- |
| im_base | Base image in bgr format | None |
| im_hsv | Base image in hsv format | None |
| min_area | Minimum area to generate the coordinates | 20 |
| scale | Scale of the bounding box | 0.1 |

__returns:__ bounding_boxes, areas

## Class: Features(im_source=None, features=500)
This class allows you to easily perform feature matching detection. See examples [here][5].

| Args | Description | Default |
| :- | :- | :- |
| im_source | Source image | None |
| features | Amount of features in _im_source_ | 500 |

### Import example
``` python
from cv_recon import Features
import cv2 as cv

# load source image (the image you want to detect)
im_source = cv.imread('image.jpg')
# create Features object (detects 1000 features from the source image)
my_feature = Features(im_source, 1000)
```

### Properties
| Property | Description | Type | Default |
| :- | :- | :- | :- |
| im_source | Source image (the image you want to detect) | np.array | _im_source_ |
| im_source_kp | Source image keypoints | np.array | _im_source_ keypoints |
| im_target | Target image | np.array | None |
| im_target_kp | Target image keypoints | np.array | None |
| im_poly | Image containing a polygon around the best matches | np.array | None |

### Methods

#### `loadTarget(im)`
Loads the target image to perform the feature matching detection.

| Args | Description | Default |
| :- | :- | :- |
| im | Target image in which the feature matching is gonna be perform | None |

__returns:__ None

#### `getMatches(distance=0.75)`
Generates a list with the good matches found in the target image.

| Args | Description | Default |
| :- | :- | :- |
| distance | Threshold which decides if it is a good match | 0.75 |

__returns:__ good_matches

#### `matchPoints(matches)`
Returns an image containing the matches between _im_target_ and _im_source_.

| Args | Description | Default |
| :- | :- | :- |
| matches | List containing the good matches | None |

__returns:__ image

#### `getBoxes(matches, min_matches=20)`
Generates a list containing the bounding box (x, y, w, h) of the object.

| Args | Description | Default |
| :- | :- | :- |
| matches | Good matches | None |
| min_matches | Minimum amount of matches to generate the bounding box | 20 |

__returns:__ bounding_box

## Class: PiCam(resolution=(320, 240), framerate=32, **kargs)
This class allows you to easily interact with the picamera. See examples [here][6].

| Args | Description | Default |
| :- | :- | :- |
| resolution | Camera resolution | (320, 240) |
| framerate | Framerate | 32 |
| **kargs | Assign default picamera settings. See a list of the settings [here][7] | None |

### Import example
``` python
from cv_recon.picam import PiCam

# cam settings
res = (320, 240)
fps = 24

# initialize the camera
camera = PiCam(res, fps, brightness=55, contrast=10)
```
### Properties
| Property | Description | Type |
| :- | :- | :- |
| current_frame | Current frame | np.array |

### Methods
#### `videoCapture()`
Creates a thread which updates the property _current_frame_ .  
__returns:__ None

#### `release()`
Stops updating the property _current_frame_ .  
__returns:__ None

#### `effects()`
Prints the list of image effects.  
__returns:__ None

#### `exposureModes()`
Prints the list of exposure modes.  
__returns:__ None

#### `awbModes()`
Prints the list of automatic withe balance modes.  
__returns:__ None

## Module: cv_tools
This module allows you generate a grid of images, draw bounding boxes and its offset from the center of the frame.

### Import example
``` python
from cv_recon import cv_tools
```

### Functions
#### `grid(base, dimensions, images, scale=0.5)`
Generates a _numpy.array_ containing a grid of images with the given dimensions and scale.  

| Args | Description | Default |
| :- | :- | :- |
| base | Image with the base dimensions for the rest of the images | None |
| dimensions | Tupla containing the dimensions of the grid | None |
| images | List of images not larger than _`dimensions[0] * dimensions[1]`_, each image must have the same dimensions as _base_ | None |
| scale | Scale of the output image | 0.5 |

__Returns:__ image

#### `getBoxesOffset(im, boxes)`
Generates a list containing the offset of each box from the center of the frame.

| Args | Description | Default |
| :- | :- | :- |
| im | Image with the size of the frame | None |
| boxes | List of bounding boxes | None |

__Returns:__ [x_offset, y_offset]

#### `drawBoxes(im, boxes)`
Draw the bounding boxes over an image.

| Args | Description | Default |
| :- | :- | :- |
| im | Image in which the bounding boxes are going to be drawn | None |
| boxes | List of bounding boxes | None |

__Returns:__ image

#### `drawBoxesPos(im, boxes)`
Draw the offset from the center of the frame of each bounding box.

| Args | Description | Default |
| :- | :- | :- |
| im | Image in which the offsets are going to be drawn | None |
| boxes | List of bounding boxes | None |

__Returns:__ image

[1]:https://docs.opencv.org/4.5.2/da/df6/tutorial_py_table_of_contents_setup.html
[2]:https://github.com/AguilarLagunasArturo/cv-recon/tree/main/examples
[3]:https://www.python.org/downloads/
[4]:https://github.com/AguilarLagunasArturo/cv-recon/tree/main/examples/color_detection
[5]:https://github.com/AguilarLagunasArturo/cv-recon/tree/main/examples/feature_matching
[6]:https://github.com/AguilarLagunasArturo/cv-recon/tree/main/examples/picamera
[7]:https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/7
