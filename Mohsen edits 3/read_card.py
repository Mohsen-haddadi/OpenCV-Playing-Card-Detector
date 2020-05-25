import time, os
import numpy as np , cv2
import pyautogui
import match_card

def download_my_card(my_seat , xth_card):
    """
    Use specific top left corner pixel of a card to set card region. 
    """
    #global my_1th_card_region, my_2th_card_region
    #load_variables()
    my_1th_card_region = { 1:(GAME_POISTION[0]+369, GAME_POISTION[1]+391, 10, 30) ,
                           2:(GAME_POISTION[0]+115, GAME_POISTION[1]+393, 10, 30) ,
                           3:(GAME_POISTION[0]-140, GAME_POISTION[1]+390, 10, 30) ,
                           4:(GAME_POISTION[0]-171, GAME_POISTION[1]+85, 10, 30) ,
                           5:(GAME_POISTION[0]+399, GAME_POISTION[1]+85, 10, 30) }
    my_2th_card_region = { 1:(GAME_POISTION[0]+388, GAME_POISTION[1]+391, 10, 30) ,
                           2:(GAME_POISTION[0]+133, GAME_POISTION[1]+393, 10, 30) ,
                           3:(GAME_POISTION[0]-122, GAME_POISTION[1]+390, 10, 30) ,
                           4:(GAME_POISTION[0]-152, GAME_POISTION[1]+85, 10, 30) ,
                           5:(GAME_POISTION[0]+418, GAME_POISTION[1]+85, 10, 30) }
    if xth_card == 1:
        pyautogui.screenshot("image.png" , my_1th_card_region[my_seat] )
    elif xth_card == 2:
        pyautogui.screenshot("image.png" , my_2th_card_region[my_seat] )
    query_image = cv2.imread("image.png")
    os.remove("image.png")
    return query_image

def download_table_card(xth_card):
    """
    Use specific top left corner pixel of a card to set card region. 
    Set top left corner of table card regions to the same height. 
    """
    #global table_card_region
    #load_variables()
    table_card_region = { 1:(GAME_POISTION[0]-38, GAME_POISTION[1]+215, 20, 40) , 
                          2:(GAME_POISTION[0]+25, GAME_POISTION[1]+215, 20, 40) ,
                          3:(GAME_POISTION[0]+87, GAME_POISTION[1]+215, 20, 40) ,
                          4:(GAME_POISTION[0]+150, GAME_POISTION[1]+215, 20, 40) ,
                          5:(GAME_POISTION[0]+212, GAME_POISTION[1]+215, 20, 40) }

    pyautogui.screenshot("image.png" , table_card_region[xth_card] )
    query_image = cv2.imread("image.png")
    os.remove("image.png")
    return query_image

def read_my_cards(my_seat):
    """
    Example: returns [('Eight', 'Spade') , ('Ace', 'Club')]
    my_1th_card, my_2th_card = my_cards
    """
    my_cards = []
    for xth_card in [1,2]:    
        query_image = download_my_card(my_seat , xth_card)
        value_image, suit_image = match_card.pre_process_query_image(query_image, False)
        result = match_card.match_floating_card(value_image, suit_image, False)
        my_cards.append(result[:2])
    return my_cards

def read_flop_cards():
    """
    Example: returns [('Unknown', 'Spade') , ('Queen', 'Club') , ('Two', 'Club')]
    table_1th_card, table_2th_card, table_3th_card = flop_cards
    """
    flop_cards = []
    for xth_card in [1,2,3]:    
        query_image = download_table_card(xth_card)
        value_image, suit_image = match_card.pre_process_query_image(query_image, True)
        result = match_card.match_floating_card(value_image, suit_image, True)
        flop_cards.append(result[:2])
    return flop_cards

def read_turn_card():
    """
    Example: returns ('Four', 'Spade') 
    table_4th_card = turn_card
    """
    query_image = download_table_card(4)
    value_image, suit_image = match_card.pre_process_query_image(query_image, True)
    turn_card = match_card.match_floating_card(value_image, suit_image, True)
    return turn_card[:2]

def read_river_card():
    """
    Example: returns ('Four', 'Spade') 
    table_5th_card = river_card
    """
    query_image = download_table_card(5)
    value_image, suit_image = match_card.pre_process_query_image(query_image, True)
    river_card = match_card.match_floating_card(value_image, suit_image, True)
    return river_card[:2]


def test():
    my_1th_card, my_2th_card = read_my_cards(1)
    table_1th_card, table_2th_card, table_3th_card = read_flop_cards()
    table_4th_card = read_turn_card()
    table_5th_card = read_river_card()

    print('my cards are:%s , %s'%(my_1th_card, my_2th_card))
    print('table cards are:%s, %s, %s, %s, %s'
          %(table_1th_card, table_2th_card, table_3th_card, table_4th_card, table_5th_card))

if __name__ == '__main__':
    pass
    #test()


