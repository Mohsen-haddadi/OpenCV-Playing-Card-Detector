import time, cv2, os
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

def create_source_cards_directory():
    directories = ['Source Card Images for Celeb/Table Cards', 'Source Card Images for Celeb/My Cards'
                  ,'Cards to Create Source Card Images/First Table Cards'
                  ,'Cards to Create Source Card Images/My First Cards From First Seat' ]
    for directory in directories:
        if not os.path.exists( directory ):
            os.makedirs( directory )

def create_source_cards(create_table_cards = True ):
    """ 
    To create my cards set 'create_table_cards = False'.
    ×4 resize image.
    Note 1) Fill '.../First Table Cards' and '.../My First Cards From First Seat' directories with 
    16 Sample cards (12 value cards + 4 suit cards).
    Note 2) Use the same screenshoted query cards with the same screenshot coordinates to fill Sample cards.
    """

    for name in ['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King',
                 'Spade','Heart','Club','Diamond'] :

        if create_table_cards == True:
            image = cv2.imread("Cards to Create Source Card Images/First Table Cards/%s.png" %name)
            if name not in ('Spade','Heart','Club','Diamond'):
                y0, y1, x0, x1 = TABLE_CARD_VALUE_COORDINATE
            else :
                y0, y1, x0, x1 = TABLE_CARD_SUIT_COORDINATE
        elif create_table_cards == False :
            image = cv2.imread("Cards to Create Source Card Images/My First Cards From First Seat/%s.png" %name)
            if name not in ('Spade','Heart','Club','Diamond'):
                y0, y1, x0, x1 = MY_CARD_VALUE_COORDINATE
            else :
                y0, y1, x0, x1 = MY_CARD_SUIT_COORDINATE
        
        gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        #blur operation is removed
        croped_image = gray_image[y0:y1,x0:x1]
        zoomed_croped_image = cv2.resize(croped_image, (0,0), fx=ZOOM, fy=ZOOM)

        BKG_THRESH = 60
        bkg_level = 125 #or a number from 0 to 255
        thresh_level = bkg_level + BKG_THRESH

        _, final_image = cv2.threshold(zoomed_croped_image,thresh_level,255,cv2.THRESH_BINARY) 

        if create_table_cards == True:
            cv2.imwrite('Source Card Images for Celeb/Table Cards test1/%s.png' %name, final_image)
        elif create_table_cards == False :
            cv2.imwrite('Source Card Images for Celeb/My Cards test1/%s.png' %name, final_image)

def download_card_testing(COORDINATES ='not set yet'):
    """
    Use specific top left corner pixel of a card to set card COORDINATES. 
    Set table card COORDINATES the same height. 
    """
    #global coordinates
    #load_variables()

    query_image_name = "Eight spade 5th"
    query_image = cv2.imread("Cards to Create Source Card Images/First Table Cards/%s.png" %query_image_name)
    return query_image

def download_my_card(my_seat , xth_card):
    """
    Use specific top left corner pixel of a card to set card COORDINATES. 
    """
    #global my_1th_card_region, my_2th_card_region
    #load_variables()
    my_1th_card_region = { 1:(po[0]+369, po[1]+391, 10, 30) , 2:(po[0]+115, po[1]+393, 10, 30) ,
                           3:(po[0]-140, po[1]+390, 10, 30) , 4:(po[0]-171, po[1]+85, 10, 30) ,
                           5:(po[0]+399, po[1]+85, 10, 30) }
    my_2th_card_region = { 1:(po[0]+388, po[1]+391, 10, 30) , 2:(po[0]+133, po[1]+393, 10, 30) ,
                           3:(po[0]-122, po[1]+390, 10, 30) , 4:(po[0]-152, po[1]+85, 10, 30) ,
                           5:(po[0]+418, po[1]+85, 10, 30) }
    if xth_card == 1:
        pyautogui.screenshot("image.png" , my_1th_card_region[my_seat] )
    elif xth_card == 2:
        pyautogui.screenshot("image.png" , my_2th_card_region[my_seat] )
    query_image = cv2.imread("image.png")
    os.remove("image.png")
    return query_image

def download_table_card(xth_card):
    """
    Use specific top left corner pixel of a card to set card COORDINATES. 
    Set top left corner of table card regions to the same height. 
    """
    #global table_card_region
    #load_variables()
    table_card_region = { 1:(po[0]-38, po[1]+215, 20, 40) , 2:(po[0]+25, po[1]+215, 20, 40) ,
                          3:(po[0]+87, po[1]+215, 20, 40) , 4:(po[0]+150, po[1]+215, 20, 40) ,
                          5:(po[0]+212, po[1]+215, 20, 40) }

    pyautogui.screenshot("image.png" , table_card_region[xth_card] )
    query_image = cv2.imread("image.png")
    os.remove("image.png")
    return query_image

def read_my_cards(my_seat, xth_card):
    """
    Example: returns [('Eight', 'Spade') , ('Ace', 'Club')]
    my_1th_card, my_2th_card, my_3th_card, = my_cards
    """
    my_cards = []
    for xth_card in [1,2]:    
        query_image = download_my_card(my_seat , xth_card)
        value_image, suit_image = pre_process_query_image(query_image, False)
        result = match_floating_card(value_image, suit_image, False)
        my_cards.append(result[:2])
    return my_cards

def read_flop_cards():
    """
    Example: returns [('Four', 'Spade') , ('Queen', 'Club') , ('Two', 'Club')]
    table_1th_card, table_2th_card, table_3th_card, = flop_cards
    """
    flop_cards = []
    for xth_card in [1,2,3]:    
        query_image = download_table_card(xth_card)
        value_image, suit_image = pre_process_query_image(query_image, True)
        result = match_floating_card(value_image, suit_image, True)
        flop_cards.append(result[:2])
    return flop_cards

def read_turn_card():
    """
    Example: returns ('Four', 'Spade') 
    table_4th_card = turn_card
    """
    query_image = download_table_card(4)
    value_image, suit_image = pre_process_query_image(query_image, True)
    turn_card = match_floating_card(value_image, suit_image, True)
    return turn_card[:2]

def read_river_card():
    """
    Example: returns ('Four', 'Spade') 
    table_5th_card = river_card
    """
    query_image = download_table_card(5)
    value_image, suit_image = pre_process_query_image(query_image, True)
    river_card = match_floating_card(value_image, suit_image, True)
    return river_card[:2]

def pre_process_query_image(query_image, is_it_table_card ):

    """
    Operations on query image are:gray scale, crop value and suit from card,
    ×4 resize image, and threshold image.
    Note 1) while croping value and suit from card (croped_query_image);
    choose a border which remove excess pixels to get a clean an neat value or suit image
    Note 2) query image should be resized by ZOOM to reach source image sizes
    """

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

def match_card(value_image, suit_image, is_it_table_card, VALUE_DIFFERENCE_LIMIT = 1000 , SUIT_DIFFERENCE_LIMIT = 700):

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

def test():
    """
    Run test function to adjust deviation of screenshoted query image
    from source image by modifying screenshot coordinate or
    croping coordinates of suit and value of the query card.
    """
    query_image = download_card_testing(COORDINATES = 'modify screenshot coordinate here')
    value_image, suit_image = pre_process_query_image(query_image, True)
    result = match_floating_card(value_image, suit_image, True)
    print(result)

if __name__ == '__main__':
    #create_source_cards_directory()
    #create_source_cards()
    test()


