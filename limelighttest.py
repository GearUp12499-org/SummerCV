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



def ransac(points, max_iterations = 1000, inlier_threshhold = 5.0, min_insliers = 10):
    best_circle = None
    best_inliers = 0
    points = points.reshape(-1,2)
    n_points = len(points)
    if n_points < 3:
        return None

    for _ in range(max_iterations):
        sample_points = np.random.choice(n_points, 3, replace=False)
        p1, p2, p3 = points[sample_points]

        a = np.array([p1, p2, p3])
        try:
            midpoint_1 = (p1 + p2)/2
            midpoint_2 = (p2 + p3)/2

            if p1[1] == p2[1]:
                perpendicular_slope_1 = np.inf

            else:
                perpendicular_slope_1 = -1*((p1[0] - p2[0])/(p1[1] - p2[1]))

            if p2[1] == p3[1]:
                perpendicular_slope_2 = np.inf
            else:
                perpendicular_slope_2 = -1*((p2[0] - p3[0])/(p2[1] - p3[1]))
            if np.isinf(perpendicular_slope_1) and np.isinf(perpendicular_slope_2) or abs(perpendicular_slope_1 - perpendicular_slope_2) < 1e-6:
                continue


            if perpendicular_slope_1 == np.inf:
                x_intersection = midpoint_1[0]
                y_intersection = perpendicular_slope_2 * (midpoint_1[0] - x_intersection) + midpoint_2[1]

            elif perpendicular_slope_2 == np.inf:
                x_intersection = midpoint_2[0]
                y_intersection = perpendicular_slope_1 * (midpoint_1[0] - x_intersection) + midpoint_2[1]

            else:
                x_intersection = ((perpendicular_slope_1 * midpoint_1[0]) - (perpendicular_slope_2 * midpoint_2[0]) + (midpoint_2[1] - midpoint_1[1]))/(perpendicular_slope_1 - perpendicular_slope_2)
                y_intersection = perpendicular_slope_1 * (midpoint_1[0] - x_intersection) + midpoint_2[1]
            radius = np.sqrt(((x_intersection - p1[0]) ** 2) + ((y_intersection - p1[1]) ** 2)) 

            distances = np.sqrt(((x_intersection - points[:,0]) ** 2) + ((y_intersection - points[:,1]) ** 2))

            num_of_inliers = np.sum(np.abs(distances - radius) < inlier_threshhold) 
            if inliers > best_inliers and inliers >= min_insliers:
                best_inliers = inliers
                best_circle = (x_intersection, y_intersection, radius)
        except Exception:
            continue
        
        return best_circle


contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 1 else contours[0]

circles = []
i = 0

for cnt in contours:
    if len (cnt) < 6:
        continue
    cv.drawContours(img, cnt, -1, (255, 0, 0), 3)
    circle = ransac(cnt, max_iterations = 1000, inlier_threshhold = 5.0, min_insliers = 10)

    if circle == None:
        continue
    
    x_intersection, y_intersection, radius = circle

    circles.append([x_intersection, y_intersection, radius])
    cv.circle(image, [int(x_intersection), int(y_intersection), int(radius), (0, 255, 0), 2])
    cv.circle(image, [int(x_intersection), int(y_intersection), int(3), (0, 0, 255), -1])



cv.imshow("mask", mask)
cv.imshow("img", img)
cv.imshow("hsv", hsv)
cv.waitKey(0)
cv.destroyAllWindows()

