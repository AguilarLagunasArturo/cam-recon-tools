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
- OpenCV 4.5.2, refer to the official installation guide
- numpy, required by OpenCV and used to work with images
- picamera, required if working with Raspberry PI

# Instalation
- TODO

# Usage (add table w/ descriptions and args)
- python cv_recon/recon/colorspace.py
- python cv_recon/recon/features.py <path to reference image>
- See more examples in examples folder

# Tree
.  
├── cv_recon  
│   ├── cv_tools.py  
│   ├── __init__.py  
│   ├── picam  
│   │   ├── __init__.py  
│   │   └── picamstream.py  
│   └── recon  
│       ├── colorspace.py  
│       ├── features.py  
│       └── __init__.py  
└── examples  
    ├── color_detection  
    │   └── logs  
    │       ├── blue2.log  
    │       ├── blue.log  
    │       └── red.log  
    └── feature_matching  
        └── im  
            └── src.jpg  

# Documentation
- TODO
