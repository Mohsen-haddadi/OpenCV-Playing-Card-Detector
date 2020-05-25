import time, cv2
import numpy as np
import pyautogui

#Global constant below are used in create_source_cards() and pre_process_query_image() functions.
#These COORDINATES should be same for both source cards and query cards to get the best match card result.
#ZOOM constant must be the same for both source cards and query cards.
TABLE_CARD_VALUE_COORDINATE=(3,23,0,20)
TABLE_CARD_SUIT_COORDINATE=(25,40,3,20)
MY_CARD_VALUE_COORDINATE=(3,23,0,20)
MY_CARD_SUIT_COORDINATE=(25,40,3,20)
ZOOM = 4

def create_source_cards(create_table_cards = True ):
    """ 
    To create my cards set 'create_table_cards = False'.
    Resize 20×20 value image to 80×80, and threshold image.
    Note 1) Fill '.../First Table Cards' and '.../My First Cards From First Seat' directories with 
    16 Sample cards (12 value cards + 4 suit cards).
    Note 2) Use the same screenshoted query cards with the same screenshot coordinates to fill Sample cards.
    """

    for name in ['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King',
                 'Spade','Heart','Club','Diamond'] :

        if create_table_cards == True:
            image = cv2.imread("Cards to Create Source Card Images/First Table Cards/%s.png" %name)
            gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            if name not in ('Spade','Heart','Club','Diamond'):
                y0, y1, x0, x1 = TABLE_CARD_VALUE_COORDINATE
            else :
                y0, y1, x0, x1 = TABLE_CARD_SUIT_COORDINATE
        elif create_table_cards == False :
            image = cv2.imread("Cards to Create Source Card Images/My First Cards From First Seat/%s.png" %name)
            gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            if name not in ('Spade','Heart','Club','Diamond'):
                y0, y1, x0, x1 = MY_CARD_VALUE_COORDINATE
            else :
                y0, y1, x0, x1 = MY_CARD_SUIT_COORDINATE
        
        #blur operation is removed
        croped_image = gray_image[y0:y1,x0:x1]
        zoomed_croped_image = cv2.resize(croped_image, (0,0), fx=ZOOM, fy=ZOOM)

        BKG_THRESH = 60
        bkg_level = 125 #150#gray[int(img_h/100)][int(img_w/2)] # Mohsen: or a number 0 to 255
        thresh_level = bkg_level + BKG_THRESH

        _, final_image = cv2.threshold(zoomed_croped_image,thresh_level,255,cv2.THRESH_BINARY) 

        if create_table_cards == True:
            cv2.imwrite('Source Card Images for Celeb/Table Cards test1/%s.png' %name, final_image)
        elif create_table_cards == False :
            cv2.imwrite('Source Card Images for Celeb/My Cards test1/%s.png' %name, final_image)

def screenshot_and_read_query_image(COORDINATES ='not set yet'):
    """
    Use specific top left corner pixel of a card to set card COORDINATES. 
    Set table card COORDINATES the same height. 
    """
    query_image_name = "4h"
    query_image = cv2.imread("Cards to Create Source Card Images/First Table Cards/%s.png" %query_image_name)
    return query_image

def pre_process_query_image(query_image):

        if create_table_cards == True:
            image = cv2.imread("Cards to Create Source Card Images/First Table Cards/%s.png" %name)
            gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            if name not in ('Spade','Heart','Club','Diamond'):
                y0, y1, x0, x1 = TABLE_CARD_VALUE_COORDINATE
            else :
                y0, y1, x0, x1 = TABLE_CARD_SUIT_COORDINATE
        elif create_table_cards == False :
            image = cv2.imread("Cards to Create Source Card Images/My First Cards From First Seat/%s.png" %name)
            gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            if name not in ('Spade','Heart','Club','Diamond'):
                y0, y1, x0, x1 = MY_CARD_VALUE_COORDINATE
            else :
                y0, y1, x0, x1 = MY_CARD_SUIT_COORDINATE
    """
    Operations on query image are:gray scale, crop value and suit from card,
    Resize 20×20 value image to 80×80, and threshold image.
    Note 1) while croping value and suit from card (croped_query_image);
    choose a border which remove excess pixels to get a clean an neat value or suit image
    Note 2) query image should be resized by ZOOM to reach source image sizes
    """
    
    gray_query_image = cv2.cvtColor(query_image, cv2.COLOR_BGR2GRAY)
    #blur operation is removed
    y0, y1, x0, x1 = TABLE_CARD_VALUE_COORDINATE
    croped_query_image = gray_query_image[y0:y1,x0:x1]
    #resize 20×20 value image to 80×80 image:
    zoomed_croped_query_image = cv2.resize(croped_query_image, (0,0), fx=ZOOM, fy=ZOOM)

    BKG_THRESH = 60
    bkg_level = 125 #gray[int(img_h/100)][int(img_w/2)] # Mohsen: or a number 0 to 255
    thresh_level = bkg_level + BKG_THRESH

    _, threshold_zoomed_croped_query_image = cv2.threshold(zoomed_croped_query_image,thresh_level,255,cv2.THRESH_BINARY) 
    #run line below to check if the croped_query_image contain excess pixels or not
    #cv2.imshow('threshold_zoomed_croped_query_image',threshold_zoomed_croped_query_image); cv2.waitKey(0); cv2.destroyAllWindows()

    return threshold_zoomed_croped_query_image

def match_floating_card(threshold_zoomed_query_image, BORDER_WIDTH = 4):
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

    img_h, img_w = threshold_zoomed_query_image.shape[:2]
    extended_query_image = cv2.copyMakeBorder(threshold_zoomed_query_image, BORDER_WIDTH, BORDER_WIDTH,
                                                 BORDER_WIDTH, BORDER_WIDTH, cv2.BORDER_CONSTANT, value=255)

    t0 = time.time()
    #float the image, and find best possible position:
    for i in range(2*BORDER_WIDTH):
        for j in range(2*BORDER_WIDTH):
            floating_query_image = extended_query_image[j:img_h+j, i:img_w+i]
            value_name, suit_name, difference_amount = match_card(floating_query_image)
            if difference_amount < best_value_difference_amount:
                #print line below to find probable mistakes and set VALUE_DIFFERENCE_LIMIT
                #print(value_name ,difference_amount) 
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

def match_card(threshold_zoomed_query_image, VALUE_DIFFERENCE_LIMIT = 1000 , SUIT_DIFFERENCE_LIMIT = 700):

    #All calculated diffrences amounts are lower than this large number.
    best_value_difference_amount = 1000000 
    best_suit_difference_amount = 1000000
    best_value_match_name = "Unknown"
    best_suit_match_name = "Unknown"

    for value_name in ['Ace','Two','Three','Four','Five','Six','Seven',
                       'Eight','Nine','Ten','Jack','Queen','King'] :


        train_image = cv2.imread("Source Card Images for Celeb/Table Cards/%s.png"%value_name, cv2.IMREAD_GRAYSCALE)

        difference_image = cv2.absdiff(threshold_zoomed_query_image, train_image)
        difference_amount = int(np.sum(difference_image)/255)

        if difference_amount < best_value_difference_amount:
            #best_value_difference_image = difference_image
            best_value_difference_amount = difference_amount
            best_value_name = value_name

    if (best_value_difference_amount < VALUE_DIFFERENCE_LIMIT):
        best_value_match_name = best_value_name

    return best_value_match_name, best_suit_match_name, best_value_difference_amount#, best_suit_match_diff

def test():
    """
    Run test function to adjust deviation of screenshoted query image
    from source image by modifying screenshot coordinate or
    croping coordinates of suit and value of the query card.
    """
    query_image = screenshot_and_read_query_image(COORDINATES= 'modify screenshot coordinate here')
    threshold_zoomed_croped_query_image = pre_process_query_image(query_image)
    result = match_floating_card(threshold_zoomed_croped_query_image)
    print(result)

if __name__ == '__main__':
    #create_source_cards()
    test()

