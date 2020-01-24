import pyautogui, time, cv2
import numpy as np

def preprocess_image(image):
    """Returns a grayed, blurred, and adaptively thresholded camera image."""
    BKG_THRESH = 0
    # Mohsen: use full path while loading image to prevent cvtColor Error
    # Mohsen: Example: img = cv2.imread('C:/Users/Financial/Desktop/1.jpg')
    # check: https://stackoverflow.com/questions/30506126/open-cv-error-215-scn-3-scn-4-in-function-cvtcolor 
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)

    # The best threshold level depends on the ambient lighting conditions.
    # For bright lighting, a high threshold must be used to isolate the cards
    # from the background. For dim lighting, a low threshold must be used.
    # To make the card detector independent of lighting conditions, the
    # following adaptive threshold method is used.
    #
    # A background pixel in the center top of the image is sampled to determine
    # its intensity. The adaptive threshold is set at 50 (THRESH_ADDER) higher
    # than that. This allows the threshold to adapt to the lighting conditions.
    img_w, img_h = np.shape(image)[:2]
    bkg_level = gray[int(img_h/100)][int(img_w/2)] # Mohsen: or a number 0 to 255
    thresh_level = bkg_level + BKG_THRESH

    retval, thresh = cv2.threshold(blur,thresh_level,255,cv2.THRESH_BINARY)
    
    return thresh


"""
img = cv2.imread('C:/Users/Financial/Desktop/1.jpg')
img = preprocess_image(img)
cv2.imshow('imagesss',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

image = cv2.imread('C:/Users/Financial/Desktop/2.jpg')
"""Returns a grayed, blurred, and adaptively thresholded camera image."""
BKG_THRESH = 60
# Mohsen: use full path while loading image to prevent cvtColor Error
# Mohsen: Example: img = cv2.imread('C:/Users/Financial/Desktop/1.jpg')
# check: https://stackoverflow.com/questions/30506126/open-cv-error-215-scn-3-scn-4-in-function-cvtcolor 
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)

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
bkg_level = 150#gray[int(img_h/100)][int(img_w/2)] # Mohsen: or a number 0 to 255
thresh_level = bkg_level + BKG_THRESH

retval, thresh = cv2.threshold(blur,thresh_level,255,cv2.THRESH_BINARY)


cv2.imshow('imagesss',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()