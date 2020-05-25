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

def create_directories_for_cards():
    directories = ['Source Card Images for Celeb/Table Cards'
                  ,'Source Card Images for Celeb/My Cards'
                  ,'Raw Images/First Table Cards'
                  ,'Raw Images/First Table Cards Raw Images'
                  ,'Raw Images/My First Cards From First Seat'
                  ,'Raw Images/My First Cards From First Seat Raw Images']
    for directory in directories:
        if not os.path.exists( directory ):
            os.makedirs( directory )

def find_game_reference_point():
    global GAME_POSITION

    print('searching for game region on screen...')
    GAME_POSITION = pyautogui.locateOnScreen('reference image for celeb game.png')
    if GAME_POSITION == None:
        raise Exception("can not find game region on screen")
    else:
        print('game reference point is set')

def crop_raw_card_image(create_table_cards = True):
    """ 
    croping 14(+4 suits) table card from 1th card poitsion on the table. 
    croping 14(+4 suits) card from my 1th card position on first seat.
    Note: Before runing this function, first fill 'Raw Images/First Table Cards Raw Images' 
    and 'Raw Images/My First Cards From First Seat Raw Images' directories with 
    16 Sample cards (12 value cards + 4 suit cards).
    """
    #global table_card_region, my_1th_card_region, my_2th_card_region
    #load_variables()
    table_card_region = { 1:(GAME_POISTION[0]-38, GAME_POISTION[1]+215, 20, 40) , 
                          2:(GAME_POISTION[0]+25, GAME_POISTION[1]+215, 20, 40) ,
                          3:(GAME_POISTION[0]+87, GAME_POISTION[1]+215, 20, 40) ,
                          4:(GAME_POISTION[0]+150, GAME_POISTION[1]+215, 20, 40) ,
                          5:(GAME_POISTION[0]+212, GAME_POISTION[1]+215, 20, 40) }
    my_1th_card_region = { 1:(GAME_POISTION[0]+369, GAME_POISTION[1]+391, 10, 30) ,
                           2:(GAME_POISTION[0]+115, GAME_POISTION[1]+393, 10, 30) ,
                           3:(GAME_POISTION[0]-140, GAME_POISTION[1]+390, 10, 30) ,
                           4:(GAME_POISTION[0]-171, GAME_POISTION[1]+85, 10, 30) ,
                           5:(GAME_POISTION[0]+399, GAME_POISTION[1]+85, 10, 30) }


#    for name in ['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King',
#                 'Spade','Heart','Club','Diamond']:
    for name in ['Three']:
        if create_table_cards == True:
            image = cv2.imread("Raw Images/First Table Cards Raw Images/%s.png" %name )
            x0, y0, x1, y1 = (table_card_region[1][0], table_card_region[1][1],
                              table_card_region[1][0] + table_card_region[1][2],
                              table_card_region[1][1] + table_card_region[1][3])
            croped_image = image[y0:y1,x0:x1]
            cv2.imwrite('Raw Images/First Table Cards/%s.png' %name, croped_image)

        elif create_table_cards == False :
            image = cv2.imread("Raw Images/My First Cards From First Seat Raw Images/%s.png" %name )
            x0, y0, x1, y1 = (my_1th_card_region[1][0], my_1th_card_region[1][1],
                              my_1th_card_region[1][0] + my_1th_card_region[1][2],
                              my_1th_card_region[1][1] + my_1th_card_region[1][3])
            croped_image = image[y0:y1,x0:x1]
            cv2.imwrite('Raw Images/My First Cards From First Seat/%s.png' %name, croped_image)

def create_source_cards(create_table_cards = True ):
    """ 
    To create my cards set 'create_table_cards = False'.
    ×4 resize image.
    Note 1: Run crop_raw_card_image() before this function to fill 'Raw Images/First Table Cards'
    and 'Raw Images/My First Cards From First Seat' directories.
    Note 2: Use the same screenshoted query cards with the same screenshot coordinates to fill Sample cards.
    """

    for name in ['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King',
                 'Spade','Heart','Club','Diamond'] :

        if create_table_cards == True:
            image = cv2.imread("Raw Images/First Table Cards/%s.png" %name)
            if name not in ('Spade','Heart','Club','Diamond'):
                y0, y1, x0, x1 = TABLE_CARD_VALUE_COORDINATE
            else :
                y0, y1, x0, x1 = TABLE_CARD_SUIT_COORDINATE
        elif create_table_cards == False :
            image = cv2.imread("Raw Images/My First Cards From First Seat/%s.png" %name)
            if name not in ('Spade','Heart','Club','Diamond'):
                y0, y1, x0, x1 = MY_CARD_VALUE_COORDINATE
            else :
                y0, y1, x0, x1 = MY_CARD_SUIT_COORDINATE
        
        if image == None:
            raise Exception("Unable to read %s.png image" %name)
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


def main():
    create_directories_for_cards()
    find_game_reference_point()
    crop_raw_card_image()
    create_source_cards()

if __name__ == '__main__':
	main()



