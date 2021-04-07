from cv_recon import Colorspace
from cv_recon import cv_tools
import cv2 as cv

colorspace = Colorspace( 'examples/color_detection/logs/blue-0.log' )
cam = cv.VideoCapture(0)

while True:
    rec, frame = cam.read()

    if not rec:
        raise Exception('Cam is not recording')

    frame_blur = cv.GaussianBlur(frame, (9, 9), 150) 		# smoothes the noise
    frame_hsv = cv.cvtColor(frame_blur, cv.COLOR_BGR2HSV)	# convert BGR to HSV

    boxes = colorspace.getBoxes(frame, frame_hsv, 150)	     # get boxes (x, y, w, h)

    offsets = cv_tools.getBoxesOffset(frame, boxes)			# get boxes offset from the center of the frame
    for i, offset in enumerate(offsets):
        print(i, offset)                                    # print offset (x_off, y_off)

    frame_out = cv_tools.drawBoxes(frame.copy(), boxes)     # draw boxes
    frame_out = cv_tools.drawBoxesPos(frame_out, boxes)     # draw offsets

    frame_grid = cv_tools.grid(frame, (2, 3),[              # generate grid
        frame_hsv, frame_out, colorspace.im_contours,
        colorspace.im_cut, colorspace.im_mask, colorspace.im_edges
    ])

    cv.imshow('grid', frame_grid)                           # show grid

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
