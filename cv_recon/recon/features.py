import cv2 as cv
import numpy as np

#im_source = cv.imread('codes/github.png', 0)
im_source = cv.imread('book/src.jpg', 0)
#im_source = cv.resize(im_source, (0, 0), fx=0.5, fy=0.5)
corners = np.float32(
    [ [0, 0], [0, im_source.shape[0]], [im_source.shape[1], im_source.shape[0]], [im_source.shape[1], 0] ],
).reshape(-1, 1, 2)

features = 1000
orb = cv.ORB_create(nfeatures=features)

kp1, des1 = orb.detectAndCompute(im_source, None)
im_source_kp = cv.drawKeypoints(im_source.copy(), kp1, None)
cv.imshow('source kp', im_source_kp)
print('kp1', len(kp1))

cam = cv.VideoCapture(0)
bf = cv.BFMatcher()


while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    rec, frame = cam.read()
    im_target = cv.cvtColor(frame.copy(), cv.COLOR_BGR2GRAY)

    kp2, des2 = orb.detectAndCompute(im_target, None)
    im_target_kp = cv.drawKeypoints(im_target.copy(), kp2, None)
    cv.imshow('target kp', im_target_kp)

    if len(kp2) <= 1:
        cv.imshow('frame', frame)
        continue

    matches = bf.knnMatch(des1, des2, k=2) # RESEARCH

    good = []
    for m, n in matches:
        if m.distance < 0.75 *  n.distance: # Distance between matches
            good.append( m )
    print('good', len(good))

    im_matches = cv.drawMatchesKnn(im_source, kp1, im_target, kp2, [good], None, flags=2)
    cv.imshow('matches', im_matches)
    if len(good) > 20:
        src_points = np.float32( [kp1[m.queryIdx].pt for m in good] ).reshape(-1, 1, 2) # RESEARCH
        dst_points = np.float32( [kp2[m.trainIdx].pt for m in good] ).reshape(-1, 1, 2) # RESEARCH

        matrix, mask = cv.findHomography(src_points, dst_points, cv.RANSAC, 5) # RESEARCH

        if matrix is None:
            cv.imshow('frame', frame)
            continue

        des = cv.perspectiveTransform(corners, matrix)
        frame = cv.polylines(frame, [np.int32(des)], True, (0, 255, 0), 3)

    cv.imshow('frame', frame)

cam.release()
cv.destroyAllWindows()
