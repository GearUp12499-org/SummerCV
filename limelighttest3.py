import cv2 as cv
import numpy as np

path = "IMG_3996.jpg"
img = cv.imread(path)
img = cv.resize(img, (640, 480))
gse = lambda x, y: cv.getStructuringElement(cv.MORPH_ELLIPSE, (x,y))

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

yellow_upper = np.array([30, 255, 255])
yellow_lower = np.array([20, 100, 100])

mask = cv.inRange(hsv, yellow_lower, yellow_upper)

def transform(mask):
    ksize = 31
    kernel = np.ones((3,3), np.uint8)

    mask = cv.dilate(mask, kernel, iterations = 1)
    
    mask = cv.erode(mask, kernel, iterations = 1)
    mask = cv.medianBlur(mask, 5)
    mask = cv.GaussianBlur(mask, (ksize, ksize), 0)
    _, mask = cv.threshold(mask, 5, 255, cv.THRESH_BINARY)
    
    return mask

mask = transform(mask)

contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 1 else contours[0]
for cnt in contours:
    if len (cnt) < 6:
        continue
    cv.drawContours(img, cnt, -1, (255, 0, 0), 3)

def circle_coverage(mask, circle):
    cx, cy, r = circle
    cx = int(cx)
    cy = int(cy)
    r = int(r)
    circle_mask = np.zeros_like(mask)
    cv.circle(circle_mask, (cx, cy), r, 255, -1)
    circle_area = np.sum(circle_mask == 255)
    if circle_area == 0:
        return 0
    inside = np.sum((mask == 255) & (circle_mask == 255))
    return inside/circle_area

def ransac(points, max_iterations = 1000, inlier_threshhold = 5.0, min_insliers = 10):
    best_circle = None
    best_inliers = 0
    points = points.reshape(-1,2)
    n_points = len(points)
    if n_points < 3:
        return None
def circle_support(points, circle, threshold):
    cx, cy, r = circle
    points = points.reshape(-1,2).astype(np.float64)
    distances = np.sqrt(
        (points - cx) ** 2 + (points - cy) ** 2
    )
    return np.sum(np.abs(distances - r) < threshold)

def findpollen(points, max_circles = 10):
    remaining = points.reshape(-1,2).astype(np.float64)
    found = []
    for _ in range (max_circles):
        if len(remaining) < 20:
            break   
        circle = ransac(
            remaining, 
            max_iterations = 1000,
            inlier_threshhold = 3.0 
        )
        if circle == None:
            break
        cx,cy,r = circle
        support = circle_support(remaining, circle)
        if support < 20:
            break
        duplicate = False
        for old_cx, old_cy, old_r in found:
            center_distance = np.sqrt(
                (cx - old_cx) ** 2 + (cy - old_cy) ** 2
            )
        if center_distance < 0.5 * min(r, old_r):
            duplicate = True
            break
    found.append(circle)
    distances = np.sqrt(
        (remaining - cx) ** 2 + (remaining - cy) ** 2
        )
    return found

def draw_circles(p1,p2,p3):
    ax, ay = p1
    bx, by = p2
    cx_, cy_ = p3
    d = 2 * (ax * (by - cy_) + bx * (cy_ - ay) + cx_ * (ay - by))
    if abs(d) < 1e-6:
        return None
    ux = ((ax ** 2 + ay ** 2) * (by - cy_) +
           (bx ** 2 + by ** 2) * (cy_ - ay) + (cy_ ** 2 + cx_ ** 2) * (ay - by))/d
    uy = ((ax ** 2 + ay **2) * (cx_ - bx) + (bx ** 2 + by **2) * (ax - cx_)
           + (cx_ **2 + cy_ ** 2) * (bx - ax))/d
    r = np.sqrt((ux - ax) ** 2 + (uy - ay) ** 2)
    return ux, uy, r
contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
circles = []

for cnt in contours:
    if len(cnt) < 6:
        continue
    cv.drawContours(img, [cnt], -1, (255, 0, 0), 2)
    found = findpollen(cnt)
    for circle in found:
        cx, cy, r = circle
        coverage = circle_coverage(mask, circle)
    if coverage < 0.35:
        continue
    circles.append(cx, cy, r)
    cv.circle(
        img, (int(cx), int(cy)), int(r), (0, 255, 120), 2
    )
    cv.circle(
        img, (int(cx), int(cy)),3, (130, 50, 36), -1
    )
    
cv.imshow("mask", mask)
cv.imshow("img", img)
#cv.imshow("hsv", hsv)
cv.waitKey(0)
cv.destroyAllWindows()

