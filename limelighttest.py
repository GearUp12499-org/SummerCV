import cv2 as cv
import numpy as np

path = "C:\\Users\\Charlie\\OneDrive\\Desktop\\Robots\\pollen2.jpg"
img = cv.imread(path)
img = cv.resize(img, (640, 480))
gse = lambda x, y: cv.getStructuringElement(cv.MORPH_ELLIPSE, (x,y))

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

yellow_upper = np.array([30, 255, 255])
yellow_lower = np.array([20, 100, 100])

mask = cv.inRange(hsv, yellow_lower, yellow_upper)

def transform(mask):
    ksize = 31
    kernel = np.ones((5,5), np.uint8)

    mask = cv.dilate(mask, kernel, iterations = 1)
    mask = cv.erode(img, kernel, iterations = 1)
    mask = cv.medianBlur(mask, 5)
   

   
    mask = cv.GaussianBlur(mask, (ksize, ksize), 0)
    _, mask = cv.threshold(mask, 5, 255, cv.THRESH_BINARY)
    return mask

contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 1 else contours[0]
for cnt in contours:
    if len (cnt) < 6:
        continue
    cv.drawContours(img, cnt, -1, (255, 0, 0), 3)

def ransac(points, max_iterations = 1000, inlier_threshhold = 5.0, min_insliers = 10):
    best_circle = None
    best_inliers = 0
    points = points.reshape(-1,2)
    n_points = len(points)
    if n_points < 3:
        return None
cv.imshow("mask", mask)
cv.imshow("img", img)
cv.imshow("hsv", hsv)
cv.waitKey(0)
cv.destroyAllWindows()

