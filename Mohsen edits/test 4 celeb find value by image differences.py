import time, cv2
import numpy as np
import pyautogui

def screenshot_and_read_query_image():
    query_image_name = "Four"
    query_image = cv2.imread("celeb 1th cards to crop value part/%s.png" %query_image_name)
    return query_image

def pre_process_query_image(query_image):
    """
    Operations on query image are:gray scale, crop value and suit from card,
    resize value image to 80×80, and threshold image.
    Note 1: while croping value and suit from card (croped_query_image);
    choose a border which remove excess pixels to get a clean an neat value or suit image
    Note 2:query image should resize by ZOOM to reach trainig image source sizes
    """
    ZOOM = 4
    
    gray_query_image = cv2.cvtColor(query_image, cv2.COLOR_BGR2GRAY)
    #blur operation is removed
    croped_query_image = gray_query_image[3:23, 0:20] 
    #resize 20×20 value image to 80×80 image:
    zoomed_croped_query_image = cv2.resize(croped_query_image, (0,0), fx=ZOOM, fy=ZOOM)

    BKG_THRESH = 60
    bkg_level = 125 #gray[int(img_h/100)][int(img_w/2)] # Mohsen: or a number 0 to 255
    thresh_level = bkg_level + BKG_THRESH

    _, threshold_zoomed_croped_query_image = cv2.threshold(zoomed_croped_query_image,thresh_level,255,cv2.THRESH_BINARY) 
    #run line below to check if the croped_query_image contain excess pixels or not
    cv2.imshow('threshold_zoomed_croped_query_image',threshold_zoomed_croped_query_image); cv2.waitKey(0); cv2.destroyAllWindows()

    return threshold_zoomed_croped_query_image

def match_floating_card(query_image, BORDER_WIDTH = 4):
    """ To optimize time_consumption change the BORDER_WIDTH value """

    best_value_difference_amount = 1000000
    #best_suit_match_diff = 1000000
    best_value_match_name = "Unknown"
    best_suit_match_name = "Unknown"

    img_w, img_h = query_image.shape[:2]
    extended_query_image = cv2.copyMakeBorder(query_image, BORDER_WIDTH, BORDER_WIDTH,
                                                 BORDER_WIDTH, BORDER_WIDTH, cv2.BORDER_CONSTANT, value=255)

    t0 = time.time()
    #float the image, and find best possible position:
    for i in range(2*BORDER_WIDTH):
        for j in range(2*BORDER_WIDTH):
            floating_query_image = extended_query_image[i:img_w+i, j:img_h+j]
            value_name, suit_name, difference_amount = match_card(floating_query_image)
            if difference_amount < best_value_difference_amount:
                best_value_difference_amount = difference_amount
                best_value_match_name = value_name
                best_floating_query_image = floating_query_image
                deviation_from_center_x = i - BORDER_WIDTH
                deviation_from_center_y = j - BORDER_WIDTH

    #cv2.imshow('best_floating_query_image',best_floating_query_image); cv2.waitKey(0); cv2.destroyAllWindows()
    time_consumption = time.time()-t0

    return(best_value_match_name, best_suit_match_name, best_value_difference_amount,
           "time consumption:%s"%round(time_consumption, 4),
           "deviation from center:%s,%s"%(deviation_from_center_x,deviation_from_center_y))#, best_suit_match_diff)

def match_card(query_image):
    VALUE_DIFFERENCE_LIMIT = 2000
    SUIT_DIFF_MAX = 700
    best_value_difference_amount = 1000000 #All calculated diffrences amounts are lower than this large number.
    best_suit_match_diff = 1000000
    best_value_match_name = "Unknown"
    best_suit_match_name = "Unknown"

    for value_name in ['Ace','Two','Three','Four','Five','Six','Seven',
                       'Eight','Nine','Ten','Jack','Queen','King'] :


        train_image = cv2.imread("celeb 1th cards croped value part/%s.png"%value_name, cv2.IMREAD_GRAYSCALE)

        difference_image = cv2.absdiff(query_image, train_image)
        difference_amount = int(np.sum(difference_image)/255)

        if difference_amount < best_value_difference_amount:
            #best_rank_diff_img = difference_amount
            best_value_difference_amount = difference_amount
            best_value_name = value_name

    if (best_value_difference_amount < VALUE_DIFFERENCE_LIMIT):
        best_value_match_name = best_value_name

    return best_value_match_name, best_suit_match_name, best_value_difference_amount#, best_suit_match_diff

def test():
    query_image = screenshot_and_read_query_image()
    threshold_zoomed_croped_query_image = pre_process_query_image(query_image)
    result = match_floating_card(threshold_zoomed_croped_query_image)
    print(result)

if __name__ == '__main__':
    test()

