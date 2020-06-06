import time, os
from PIL import Image
import numpy as np, cv2
import pyautogui

"""
1.1. Set these constants the same between create_source_cards_images.py and match_card.py:
TABLE_CARD_VALUE_COORDINATE, TABLE_CARD_SUIT_COORDINATE, 
MY_CARD_VALUE_COORDINATE, MY_CARD_SUIT_COORDINATE, ZOOM

1.2. Functions they are used: 
create_source_cards_images.create_source_cards() 
and match_card.pre_process_query_image()

1.3. COORDINATE format is: TABLE_CARD_VALUE_COORDINATE = (y0,y1,x0,x1)

1.4. The height (y1-y0) and width (x1-x0) of COORDINATES must be same for both source cards 
(which is made by create_source_cards()) and query cards 
(which is used on pre_process_query_image()), Otherwise it will Errors.

1.5. The x0 and y0 of COORDINATES should be same for both source cards 
and query cards to reach the best match card result.

1.6. ZOOM constant must be the same for both source cards and query cards.

2.1. Set these constants the same between create_source_cards_images.py and read_cards.py:
my_1th_card_region, my_2th_card_region, and table_card_region

2.2. Functions they are used: 
create_source_cards_images.crop_raw_card_image() 
and read_card.download_my_card() read_card.download_table_card()
"""
TABLE_CARD_VALUE_COORDINATE=(3,23,0,20) #80x80
TABLE_CARD_SUIT_COORDINATE=(25,40,3,20) #68x60
MY_CARD_VALUE_COORDINATE=(0,20,0,10) #40x80
MY_CARD_SUIT_COORDINATE=(20,35,0,10) #40x60
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

def crop_raw_card_image(create_table_cards = True):
    """ 
    croping 14(+4 suits) table card from 1th card poitsion on the table. 
    croping 14(+4 suits) card from my 1th card position on first seat.
    Note 1: Before runing this function, first fill 'Raw Images/First Table Cards Raw Images' 
    and 'Raw Images/My First Cards From First Seat Raw Images' directories with 
    17 Sample cards (13 value cards + 4 suit cards).
    Note 2: Variables table_card_region and my_1th_card_region should contain 
    same coordinates used in read_card file too!
    """
    #global table_card_region, my_1th_card_region
    #load_variables()

    for name in ['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King',
                 'Spade','Heart','Club','Diamond']: 

        GAME_POSITION = find_game_reference_point_from_image_file(name)
        if GAME_POSITION == None:
            print("Can not find game reference point at %s.png image" %name)
            continue
        table_card_region = { 1:(GAME_POSITION[0]-38, GAME_POSITION[1]+215, 20, 40) , 
                              2:(GAME_POSITION[0]+25, GAME_POSITION[1]+215, 20, 40) ,
                              3:(GAME_POSITION[0]+87, GAME_POSITION[1]+215, 20, 40) ,
                              4:(GAME_POSITION[0]+150, GAME_POSITION[1]+215, 20, 40) ,
                              5:(GAME_POSITION[0]+212, GAME_POSITION[1]+215, 20, 40) }
        my_1th_card_region = { 1:(GAME_POSITION[0]+369, GAME_POSITION[1]+391, 10, 40) ,
                               2:(GAME_POSITION[0]+115, GAME_POSITION[1]+393, 10, 40) ,
                               3:(GAME_POSITION[0]-140, GAME_POSITION[1]+390, 10, 40) ,
                               4:(GAME_POSITION[0]-171, GAME_POSITION[1]+85, 10, 40) ,
                               5:(GAME_POSITION[0]+399, GAME_POSITION[1]+85, 10, 40) }

        if create_table_cards == True:
            image = cv2.imread("Raw Images/First Table Cards Raw Images/%s.png" %name )
            x0, y0, x1, y1 = (table_card_region[1][0], table_card_region[1][1],
                              table_card_region[1][0] + table_card_region[1][2],
                              table_card_region[1][1] + table_card_region[1][3])

            if isinstance(image, type(None)):
                raise Exception("Unable to read %s.png image" %name)
            croped_image = image[y0:y1,x0:x1]
            cv2.imwrite('Raw Images/First Table Cards/%s.png' %name, croped_image)

        elif create_table_cards == False :
            image = cv2.imread("Raw Images/My First Cards From First Seat Raw Images/%s.png" %name )
            x0, y0, x1, y1 = (my_1th_card_region[1][0], my_1th_card_region[1][1],
                              my_1th_card_region[1][0] + my_1th_card_region[1][2],
                              my_1th_card_region[1][1] + my_1th_card_region[1][3])

            if isinstance(image, type(None)):
                raise Exception("Unable to read %s.png image" %name)
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
    #global TABLE_CARD_VALUE_COORDINATE, TABLE_CARD_SUIT_COORDINATE,\
    # MY_CARD_VALUE_COORDINATE, MY_CARD_SUIT_COORDINATE, ZOOM
    #load_variables()

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
        if isinstance(image, type(None)):
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
            cv2.imwrite('Source Card Images for Celeb/Table Cards/%s.png' %name, final_image)
        elif create_table_cards == False :
            cv2.imwrite('Source Card Images for Celeb/My Cards/%s.png' %name, final_image)

def find_game_reference_point_from_image_file(file_name):
    """
    https://stackoverflow.com/questions/38473952/find-location-of-image-inside-bigger-image
    it will set GAME_POSITION to (x,y) position
    there is no need to open image on top screen to sreen shot from it.
    """
    t0 = time.time()
    here = Image.open(r"reference image.png")
    big  = Image.open(r"Raw Images/First Table Cards Raw Images/%s.png" %file_name)

    herear = np.asarray(here)
    bigar  = np.asarray(big)

    hereary, herearx = herear.shape[:2]
    bigary,  bigarx  = bigar.shape[:2]

    stopx = bigarx - herearx + 1
    stopy = bigary - hereary + 1


    for y in range(0, stopy): 
        for x in range(0, stopx):
            x2 = x + herearx
            y2 = y + hereary
            pic = bigar[y:y2, x:x2]
            test = (pic == herear)
            if test.all():
                print("game reference point for image '%s' is founded"%file_name)
                #print(time.time()-t0)
                GAME_POSITION = (x,y)
                return GAME_POSITION
    print("###Unable to find game reference point for image file %s###"%file_name)
    return None
"""
def find_game_reference_point_from_image_file():
    #If exact same pixel to pixel sub image is not existed, 
    #It will find the most look like sub image position.

    global GAME_POSITION
    t0 = time.time()
    image = cv2.imread("Raw Images/First Table Cards Raw Images/%s.png" %'Nine')  
    template = cv2.imread("reference image.png")  
    result = cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED)  
    print(result)
    print(result.argmax())
    print (np.unravel_index(result.argmax(),result.shape))
    print(time.time() - t0)
"""

def main():
    create_directories_for_cards()
    
    crop_raw_card_image()
    create_source_cards()
    crop_raw_card_image(create_table_cards = False)
    create_source_cards(create_table_cards = False)

if __name__ == '__main__':
	main()

