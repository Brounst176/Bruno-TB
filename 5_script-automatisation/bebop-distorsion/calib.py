import cv2
import numpy as np

assert float(cv2.__version__.rsplit('.', 1)[0]) >= 3, 'OpenCV version 3 or newer required.'

K = np.array([[  1400,     0.  ,  1695.56],
              [    0.  ,   1100,   1750],
              [    0.  ,     0.  ,     0.8  ]])

# zero distortion coefficients work well for this image
D = np.array([0., 0., 0., 0.])

# use Knew to scale the output
Knew = K.copy()
Knew[(0,1), (0,1)] = 0.7 * Knew[(0,1), (0,1)]


img = cv2.imread('bebop_0022.jpg')
img_undistorted = cv2.fisheye.undistortImage(img, K, D=D, Knew=Knew)
cv2.imwrite('fisheye_sample_undistorted.jpg', img_undistorted)
cv2.waitKey()