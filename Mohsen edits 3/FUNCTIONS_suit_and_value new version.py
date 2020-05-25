def s(card) :
    """ returns suit of a card in string format"""
    if card[1] == 'Spade':
        return 's'
    elif card[1] == 'Heart':
        return 'h'
    elif card[1] == 'Club':
        return 'c'
    elif card[1] == 'Diamond':
        return 'd'

def n(card) :
    """ returns value of a card by numbering them from 2 to 14"""
    if isinstance(card, int) and 2 <= card <= 14:
        return card 
    else:
    if Card[0] == 'Two':
        return 2
    if Card[0] == 'Three':
        return 3
    if Card[0] == 'Four':
        return 4
    if Card[0] == 'Five':
        return 5
    if Card[0] == 'Six':
        return 6
    if Card[0] == 'Seven':
        return 7
    if Card[0] == 'Eight':
        return 8
    if Card[0] == 'Nine':
        return 9
    if Card[0] == 'Ten':
        return 10
    if Card[0] == 'Jack':
        return 11
    if Card[0] == 'Queen':
        return 12
    if Card[0] == 'King':
        return 13
    if Card[0] == 'Ace':
        return 14
