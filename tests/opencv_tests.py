import numpy as np
import cv2

candy = cv2.imread('antnestcv/img_src/food/food.png')
candy_bw = cv2.cvtColor(candy, cv2.COLOR_BGR2GRAY)
candy_contour = cv2.Canny(image = candy_bw, threshold1 = 0, threshold2 = 50)

#contours
_ , thresh = cv2.threshold(candy_bw, 0, 255, 0)
all_contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


#Estamos interessados apenas no contorno mais longo
candy_contours = []
for array in all_contours:
    
    if len(array) > 50:
        candy_contours.append(array)       
        

contour_len = len(candy_contours)
num_pts = int(0.5*contour_len)

some_contour_pts = candy_contour[::10]

candy_contours_array = np.array(candy_contours).squeeze()


cv2.drawContours(
    image = candy_bw,
    contours = candy_contours,
    contourIdx = -1,
    color = (255, 0, 0),
    thickness = 3)

def show_img(image):
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    
    
    show_img(candy_bw)
    
    
    
      
    