import time, os
import cv2, numpy as np
import pyautogui

"""
1. Set these constants the same between create_source_cards_images.py and match_card.py:
TABLE_CARD_VALUE_COORDINATE, TABLE_CARD_SUIT_COORDINATE, 
MY_CARD_VALUE_COORDINATE, MY_CARD_SUIT_COORDINATE, ZOOM

2. Functions they are used: 
create_source_cards_images.create_source_cards() 
and match_card.pre_process_query_image()

3. COORDINATE format is: TABLE_CARD_VALUE_COORDINATE = (y0,y1,x0,x1)

4. The height (y1-y0) and width (x1-x0) of COORDINATES must be same for both source cards 
(which is made by create_source_cards()) and query cards 
(which is used on pre_process_query_image()), Otherwise it will Errors.

5. The x0 and y0 of COORDINATES should be same for both source cards 
and query cards to reach the best match card result.

6. ZOOM constant must be the same for both source cards and query cards.
"""

TABLE_CARD_VALUE_COORDINATE=(3,23,0,20) #80x80
TABLE_CARD_SUIT_COORDINATE=(25,40,3,20) #68x60
MY_CARD_VALUE_COORDINATE=(0,20,0,10) #40x80
MY_CARD_SUIT_COORDINATE=(20,35,0,10) #40x60
ZOOM = 4

def pre_process_query_image(query_image, is_it_table_card ):

    """
    Operations on query image are:gray scale, crop value and suit from card,
    ×4 resize image, and threshold image.
    Note 1) while croping value and suit from card (croped_query_image);
    choose a border which remove excess pixels to get a clean an neat value or suit image
    Note 2) query image should be resized by ZOOM to reach source image sizes
    """
    #global TABLE_CARD_VALUE_COORDINATE, TABLE_CARD_SUIT_COORDINATE,\
    # MY_CARD_VALUE_COORDINATE, MY_CARD_SUIT_COORDINATE, ZOOM
    #load_variables()

    gray_query_image = cv2.cvtColor(query_image, cv2.COLOR_BGR2GRAY) 

    if is_it_table_card == True:

        value_y0, value_y1, value_x0, value_x1 = TABLE_CARD_VALUE_COORDINATE
        suit_y0, suit_y1, suit_x0, suit_x1 = TABLE_CARD_SUIT_COORDINATE

    elif is_it_table_card == False :

        value_y0, value_y1, value_x0, value_x1 = MY_CARD_VALUE_COORDINATE
        suit_y0, suit_y1, suit_x0, suit_x1 = MY_CARD_SUIT_COORDINATE

    croped_value_from_query_image = gray_query_image[value_y0:value_y1 , value_x0:value_x1]
    croped_suit_from_query_image = gray_query_image[suit_y0:suit_y1 , suit_x0:suit_x1]
    #blur operation is removed
    #×4 resize image:
    zoomed_croped_value = cv2.resize(croped_value_from_query_image, (0,0), fx=ZOOM, fy=ZOOM)
    zoomed_croped_suit = cv2.resize(croped_suit_from_query_image, (0,0), fx=ZOOM, fy=ZOOM)

    BKG_THRESH = 60
    bkg_level = 125 #or a number from 0 to 255
    thresh_level = bkg_level + BKG_THRESH

    _, threshold_zoomed_croped_value = cv2.threshold(zoomed_croped_value,thresh_level,255,cv2.THRESH_BINARY) 
    _, threshold_zoomed_croped_suit = cv2.threshold(zoomed_croped_suit,thresh_level,255,cv2.THRESH_BINARY) 
    #run line below to check if the croped_query_image contain excess pixels or not
    #cv2.imshow('threshold_zoomed_croped_value',threshold_zoomed_croped_value); cv2.waitKey(0); cv2.destroyAllWindows()

    return threshold_zoomed_croped_value, threshold_zoomed_croped_suit

def match_floating_card(value_image, suit_image, is_it_table_card, BORDER_WIDTH = 4):
    """ 
    To optimize time_consumption change the BORDER_WIDTH value 
    Set BORDER_WIDTH to a Coefficient of ZOOM.
    Query image float within (BORDER_WIDTH ÷ ZOOM) pixels
    """

    #All calculated diffrences amounts are lower than this large number.
    best_value_difference_amount = 1000000 
    best_suit_difference_amount = 1000000
    best_value_match_name = "Unknown"
    best_suit_match_name = "Unknown"

    t0 = time.time()


    value_image_h, value_image_w = value_image.shape[:2]
    extended_value_image = cv2.copyMakeBorder(value_image, BORDER_WIDTH, BORDER_WIDTH,
                                                 BORDER_WIDTH, BORDER_WIDTH, cv2.BORDER_CONSTANT, value=255)
    suit_image_h, suit_image_w = suit_image.shape[:2]
    extended_suit_image = cv2.copyMakeBorder(suit_image, BORDER_WIDTH, BORDER_WIDTH,
                                                 BORDER_WIDTH, BORDER_WIDTH, cv2.BORDER_CONSTANT, value=255)
    #float the image, and find best possible position:
    for i in range(2*BORDER_WIDTH):
        for j in range(2*BORDER_WIDTH):
            floating_value_image = extended_value_image[j:value_image_h+j, i:value_image_w+i]
            floating_suit_image = extended_suit_image[j:suit_image_h+j, i:suit_image_w+i]
            value_name, suit_name, value_difference_amount, suit_difference_amount = \
            match_card(floating_value_image, floating_suit_image, is_it_table_card)
            if value_difference_amount < best_value_difference_amount:
                #print line below to find probable mistakes and set VALUE_DIFFERENCE_LIMIT
                #print(value_name ,value_difference_amount) 
                best_value_difference_amount = value_difference_amount
                best_value_match_name = value_name
                best_floating_value_image = floating_value_image
                deviation_from_center_x = i - BORDER_WIDTH
                deviation_from_center_y = j - BORDER_WIDTH

            if suit_difference_amount < best_suit_difference_amount:
                #print line below to find probable mistakes and set suit_DIFFERENCE_LIMIT
                #print(suit_name ,suit_difference_amount) 
                best_suit_difference_amount = suit_difference_amount
                best_suit_match_name = suit_name

    #cv2.imshow('best_floating_query_image',best_floating_query_image); cv2.waitKey(0); cv2.destroyAllWindows()
    time_consumption = time.time()-t0

    return(best_value_match_name, best_suit_match_name, best_value_difference_amount, best_suit_difference_amount, 
           "time consumption:%s"%round(time_consumption, 4),
           "deviation from center:%s,%s"%(deviation_from_center_x,deviation_from_center_y))#, best_suit_match_diff)

def match_card(value_image, suit_image, is_it_table_card, VALUE_DIFFERENCE_LIMIT = 1000 , SUIT_DIFFERENCE_LIMIT = 400):

    #All calculated diffrences amounts are lower than this large number.
    best_value_difference_amount = 1000000 
    best_suit_difference_amount = 1000000
    best_value_match_name = "Unknown"
    best_suit_match_name = "Unknown"

    for value_name in ['Ace','Two','Three','Four','Five','Six','Seven',
                       'Eight','Nine','Ten','Jack','Queen','King'] :

        if is_it_table_card == True:
            value_source_image = cv2.imread("Source Card Images for Celeb/Table Cards/%s.png"%value_name, cv2.IMREAD_GRAYSCALE)
        elif is_it_table_card == False:
            value_source_image = cv2.imread("Source Card Images for Celeb/My Cards/%s.png"%value_name, cv2.IMREAD_GRAYSCALE)

        if isinstance(value_source_image, type(None)):
            raise Exception("Unable to read %s.png value source image" %value_name)
        #comparing 2 images. value_image and value_source_image sizes should be equal otherwise it errors
        difference_image = cv2.absdiff(value_image, value_source_image)
        difference_amount = int(np.sum(difference_image)/255)

        if difference_amount < best_value_difference_amount:
            #best_value_difference_image = difference_image
            best_value_difference_amount = difference_amount
            best_value_name = value_name

    for suit_name in ['Spade','Heart','Club','Diamond'] :

        if is_it_table_card == True:
            suit_source_image = cv2.imread("Source Card Images for Celeb/Table Cards/%s.png"%suit_name, cv2.IMREAD_GRAYSCALE)
        elif is_it_table_card == False:
            suit_source_image = cv2.imread("Source Card Images for Celeb/My Cards/%s.png"%suit_name, cv2.IMREAD_GRAYSCALE)

        if isinstance(suit_source_image, type(None)):
            raise Exception("Unable to read %s.png suit source image" %suit_name)
        #comparing 2 images. value_image and value_source_image sizes should be equal otherwise it errors
        difference_image = cv2.absdiff(suit_image, suit_source_image)
        difference_amount = int(np.sum(difference_image)/255)

        if difference_amount < best_suit_difference_amount:
            #best_suit_difference_image = difference_image
            best_suit_difference_amount = difference_amount
            best_suit_name = suit_name


    if (best_value_difference_amount < VALUE_DIFFERENCE_LIMIT):
        best_value_match_name = best_value_name
    if (best_suit_difference_amount < SUIT_DIFFERENCE_LIMIT):
        best_suit_match_name = best_suit_name    

    return best_value_match_name, best_suit_match_name, best_value_difference_amount, best_suit_difference_amount



#Excesses functions to run testing:
def test():
    """
    Run test function to adjust deviation of screenshoted query image
    from source image by modifying screenshot coordinate or
    croping coordinates of suit and value of the query card.
    """

    def download_cropped_card_for_testing():
        """
        Use specific top left corner pixel of a card to set card COORDINATES. 
        """
        query_image_name = "Ace"
        query_image = cv2.imread("Raw Images/First Table Cards/%s.png" %query_image_name)
        if isinstance(query_image, type(None)):
            raise Exception("Unable to read %s.png image" %query_image_name)
        return query_image

    query_image = download_cropped_card_for_testing()
    value_image, suit_image = pre_process_query_image(query_image, True)
    result = match_floating_card(value_image, suit_image, True)
    print(result)

if __name__ == '__main__':

    test()


