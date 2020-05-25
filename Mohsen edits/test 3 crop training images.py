import pyautogui, time, cv2
import numpy as np
    
t0 = time.time()

for value_name in ['Ace','Two','Three','Four','Five','Six','Seven',
                   'Eight','Nine','Ten','Jack','Queen','King'] :

    image = cv2.imread("celeb 1th cards to crop value part/%s.png" %value_name)

    gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    croped_image = gray_image[3:23, :20] # gray_image instead of blur_image
    zoomed_croped_image = cv2.resize(croped_image, (0,0), fx=4, fy=4)

    # The best threshold level depends on the ambient lighting conditions.
    # For bright lighting, a high threshold must be used to isolate the cards
    # from the background. For dim lighting, a low threshold must be used.
    # To make the card detector independent of lighting conditions, the
    # following adaptive threshold method is used.
    #
    # A background pixel in the center top of the image is sampled to determine
    # its intensity. The adaptive threshold is set at 50 (THRESH_ADDER) higher
    # than that. This allows the threshold to adapt to the lighting conditions.
    #img_w, img_h = np.shape(image)[:2] # Mohsen: or img_w, img_h = image.shape[:2]
    BKG_THRESH = 60
    bkg_level = 125 #150#gray[int(img_h/100)][int(img_w/2)] # Mohsen: or a number 0 to 255
    thresh_level = bkg_level + BKG_THRESH

    _, final_image = cv2.threshold(zoomed_croped_image,thresh_level,255,cv2.THRESH_BINARY) 

    cv2.imwrite('celeb 1th cards croped value part/%s.png' %value_name, final_image)


print("time consumption:", time.time()-t0 )


#cv2.imshow('imagesss',final_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()