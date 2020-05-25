import pyautogui, time, cv2
import numpy as np


ZOOM = 4

t0 = time.time()

#for name in ["1 3 h", "1 3 hh"]:
image = cv2.imread("celeb cards testing/1 3 h.png")
"""Returns a grayed, blurred, and adaptively thresholded camera image."""

# Mohsen: use full path while loading image to prevent cvtColor Error
# Mohsen: Example: img = cv2.imread('C:/Users/Financial/Desktop/1.jpg')
# check: https://stackoverflow.com/questions/30506126/open-cv-error-215-scn-3-scn-4-in-function-cvtcolor 
gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#blur_image = cv2.GaussianBlur(gray_image,(5,5),0)

croped_image = gray_image[0:25, :] # gray_image instead of blur_image
zoomed_croped_image = cv2.resize(croped_image, (0,0), fx=ZOOM, fy=ZOOM)

# The best threshold level depends on the ambient lighting conditions.
# For bright lighting, a high threshold must be used to isolate the cards
# from the background. For dim lighting, a low threshold must be used.
# To make the card detector independent of lighting conditions, the
# following adaptive threshold method is used.
#
# A background pixel in the center top of the image is sampled to determine
# its intensity. The adaptive threshold is set at 50 (THRESH_ADDER) higher
# than that. This allows the threshold to adapt to the lighting conditions.
img_w, img_h = np.shape(image)[:2] # Mohsen: or img_w, img_h = image.shape[:2]
BKG_THRESH = 60
bkg_level = 150 #150#gray[int(img_h/100)][int(img_w/2)] # Mohsen: or a number 0 to 255
thresh_level = bkg_level + BKG_THRESH

retval, final_image = cv2.threshold(zoomed_croped_image,thresh_level,255,cv2.THRESH_BINARY) 


### 1 3 h , ZOOM = 1 ###
# 1 3 h :52
# 5 3 s :82
# 1 2 s :82

### 1 3 h , ZOOM = 4 ###
# 1 3 h :856, 0
# 5 3 s :1325, 510
# 1 2 s :1409, 1501

### 1 3 h , ZOOM = 20 ###
# 1 3 h :21380
# 5 3 s :32911
# 1 2 s :34849

image = cv2.imread("celeb cards testing/1 3 s.png")
gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

croped_image = gray_image[0:25, :] # gray_image instead of blur_image
zoomed_croped_image = cv2.resize(croped_image, (0,0), fx=ZOOM, fy=ZOOM)

BKG_THRESH = 60
bkg_level = 150 #150#gray[int(img_h/100)][int(img_w/2)] # Mohsen: or a number 0 to 255
thresh_level = bkg_level + BKG_THRESH
retval, final_image2 = cv2.threshold(zoomed_croped_image,thresh_level,255,cv2.THRESH_BINARY) 
"""
croped_image = gray_image[1:26, :] # gray_image instead of blur_image
zoomed_croped_image = cv2.resize(croped_image, (0,0), fx=4, fy=4)

BKG_THRESH = 60
bkg_level = 125 #150#gray[int(img_h/100)][int(img_w/2)] # Mohsen: or a number 0 to 255
thresh_level = bkg_level + BKG_THRESH
retval, final_image2 = cv2.threshold(zoomed_croped_image,thresh_level,255,cv2.THRESH_BINARY) 
"""















#test 2:
train_image = cv2.imread("testing images/game00.jpg")
query_card = cv2.imread("testing images/game1.jpg")

difference_image = cv2.absdiff(final_image, final_image2)
difference_amount = int(np.sum(difference_image)/255)

print("time consumption:", time.time()-t0 )

#cv2.imwrite('color_img.jpg', difference_image)
cv2.imshow("image", difference_image)
print(difference_amount)

cv2.waitKey()
cv2.destroyAllWindows()

