
from cv_recon import Features
from cv_recon import cv_tools
import cv2 as cv

im_source = cv.imread('im/src.jpg')
my_feature = Features(im_source, 1000)

cam = cv.VideoCapture(0)
while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    rec, frame = cam.read()
    my_feature.loadTarget(frame)
    frame_matches = None
    boxes = []

    try:
        matches = my_feature.getMatches(0.75)
        frame_matches = my_feature.matchPoints(matches)
        boxes = my_feature.getBoxes(matches, 20)
    except Exception as e:
        print(e)
        continue

    offsets = cv_tools.getBoxesOffset(frame, boxes)
    for i, offset in enumerate(offsets):
        print(i, offset)

    frame_boxes = cv_tools.drawBoxes(frame.copy(), boxes)
    cv_tools.drawBoxesPos(frame_boxes, boxes)
    frame_grid = cv_tools.grid(frame, (1, 3), [
        frame, my_feature.im_poly, frame_boxes
    ])
    if frame_matches is not None:
        cv.imshow('image matches', frame_matches)
    cv.imshow('grid', frame_grid)

cam.release()
cv.destroyAllWindows()
