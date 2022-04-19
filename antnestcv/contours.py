import numpy as np
import cv2

img = cv2.imread('antnestcv/img_src/food/food.png')
img_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_ , thresh = cv2.threshold(img_bw, 0, 255, 0)

def find_food_contours(food_bw: np.array) -> list:
    '''
        Find the edges of the food (target).
        Only contours with more than 50 points will be considered.

        -> _contours: list(np.array)
        -> self.food_contours: list(np.array), we can consider each array as 
        the contour of a food object.
        
        https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html             
    '''
    _ , thresh = cv2.threshold(food_bw, 0, 255, 0)
    _contours, _ = cv2.findContours(
                    thresh,
                    cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_NONE)
    
    food_contours = []
    for contour in _contours:
        if len(contour) > 50:
            food_contours.append(contour)
    
    x_pts, y_pts = [], []
    for pt in food_contours[0].squeeze():
        x_pts.append(pt[0])
        y_pts.append(pt[1])

    return x_pts, y_pts
   
x, y = find_food_contours(img_bw)


def some_pts_in_contour(x_contour: list, y_contour: list, percent: float) -> list:
    
    assert len(x_contour) == len(y_contour)
    
    
    length = len(x_contour)
    n_pts = min(length, int(length * percent))

    '''
        length = n_pts * q + r
        q = length//n_pts
        r = length%n_pts
    
    '''
    r = length%n_pts
    q = length//n_pts
    new_length = length - r

    x_of_interest = x_contour[:new_length:q]
    y_of_interest = y_contour[:new_length:q]
    return x_of_interest, y_of_interest


x_interest, y_interest = some_pts_in_contour(x_contour = x, y_contour = y, percent = 0.02)

# print(lista)
# cv2.drawContours(
#                 image = img,
#                 contours = lista,
#                 contourIdx = -1,
#                 color = (0,255,255),
#                 thickness = 2)


# # xy = [i**2 for i in range(10)]

img[np.nonzero(thresh)[0], np.nonzero(thresh)[1]] = [0, 255, 255]

cv2.namedWindow('Image', cv2.WINDOW_GUI_EXPANDED)
cv2.imshow('Image', img)
cv2.waitKey(0)