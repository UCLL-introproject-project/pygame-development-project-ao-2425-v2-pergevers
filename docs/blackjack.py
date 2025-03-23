#import
import copy
import random
import pygame
import time
# cards variables

cards = [ '2','3','4','5','6','7','8','9','10','J','Q','K','A']
one_deck = 4*cards
decks = 4
game_deck = copy.deepcopy(one_deck * decks)


#variables
pygame.init()
WIDTH = 700
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Blackjack')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
active = False
records = [0,0,0]
player_score = 0
dealer_score = 0
initial_deal = True
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = 0
hand_active = False
add_score = False
results = ['', 'Player busted', 'Player WINS!','Dealer wins','The game was tied']
player_bust = False
delayBetweenDealerCards = 2
dealerScoreRect= pygame.Rect(0,0,0,0)

suit_font = pygame.font.SysFont('arial',44)

#symbols
spades = "\u2660"
hearts = "\u2665"
diamonds = "\u2666"
clubs = "\u2663"
#determine the symbol based on the number that came out of the calculations
def determine_symbol(number_of_symbol):
    if number_of_symbol == 0:
        return hearts
    if number_of_symbol == 1:
        return spades
    if number_of_symbol == 2:
        return clubs
    if number_of_symbol == 3:
        return diamonds
#determine color of symbol based on what suit it is   
def determine_color(suit):
    if suit in [hearts,diamonds]:
        return 'red'
    else:
        return 'black'

#deal cards
def deal_cards(hand,deck):
    card = []
    number = random.randint(0,len(deck)-1)
    symbol = (number%52)//13
    card.append(deck[number])
    card.append(determine_symbol(symbol))
    deck.pop(number)
    return card,deck

#draw cards on screen
def draw_cards(player,dealer,reveal):
    for i in range(len(player)):
        number_of_card = (player[i])[0]
        suit_of_card = (player[i])[1]
        pygame.draw.rect(screen,'white', [70 + (70*i),370 + (5*i),120,220],0,5)
        screen.blit(font.render(player[i][0],True,'black'),(75+ 70*i,375+5*i))
        screen.blit(font.render(player[i][0],True,'black'),(152+ 70*i,545+5*i))
        screen.blit(suit_font.render(suit_of_card,True,determine_color(suit_of_card)),(80+70*i,400+5*i))
        screen.blit(pygame.transform.flip(suit_font.render(suit_of_card,True,determine_color(suit_of_card)),False,True),(152+70*i,510+5*i))
        pygame.draw.rect(screen,'red', [70 + (70*i),370 + (5*i),120,220],5,5)

    for i in range(len(dealer)):
        number_of_card = (dealer[i])[0]
        suit_of_card = (dealer[i])[1]
        pygame.draw.rect(screen,'white', [70 + (70*i),80 + (5*i),120,220],0,5)
        if i != 0 or reveal>0:
            if i<=reveal+1:
                screen.blit(font.render(dealer[i][0],True,'black'),(77+ 70*i,85+5*i))
                screen.blit(font.render(dealer[i][0],True,'black'),(152+ 70*i,255+5*i))
            screen.blit(suit_font.render(suit_of_card,True,determine_color(suit_of_card)),(80+70*i,110+5*i))
            screen.blit(pygame.transform.flip(suit_font.render(suit_of_card,True,determine_color(suit_of_card)),False,True),(152+70*i,220+5*i))
        else:
            screen.blit(font.render('?',True,'black'),(77+ 70*i,85+5*i))
            screen.blit(font.render('?',True,'black'),(152+ 70*i,255+5*i))
        pygame.draw.rect(screen,'green', [70 + (70*i),80 + (5*i),120,220],5,5)

#draw scores
def draw_scores(player,dealer):
    screen.blit(font.render(f'Your score: {player}',True,'white'),(350,345))
    if reveal_dealer>0:
        dealerScoreRect=screen.blit(font.render(f'Dealer score: {dealer}',True,'white'),(350,50))
        pygame.draw.rect(screen,'black',dealerScoreRect)
        dealerScoreRect=screen.blit(font.render(f'Dealer score: {dealer}',True,'white'),(350,50))
        
#check endgame function
def check_endgame(hand_act,deal_score,play_score,result,totals,add):
    #check endgame scenarios
    if (not hand_act and deal_score>=17) or player_bust:
        if play_score>21:
            result=1
        elif deal_score<play_score<=21 or deal_score>21:
            result = 2
        elif play_score<deal_score<=21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
                pygame.mixer.music.load("sound_effects/sad-trombone-gaming-sound-effect-hd.mp3")
                pygame.mixer.music.play()
            elif result == 2:
                totals[0] += 1
                pygame.mixer.music.load("sound_effects/roblox-old-winning-sound-effect.mp3")
                pygame.mixer.music.play()
            else:
                totals[2] += 1
            add = False
    return result, totals,add
    
#draw buttons
def draw_game(act,record,result):
    button_list = []
    #on start up
    if not act:
        deal = pygame.draw.rect(screen, 'white', [175,20 ,350,100],0,5)
        pygame.draw.rect(screen, 'blue', [175,20 ,350,100],3,5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (220,50))
        button_list.append(deal)
    #game started
    else:
        #score
        score_text = font.render(f'Wins: {record[0]}    Losses: {record[1]}     Draws: {record[2]}',True, 'white')
        screen.blit(score_text,(15,740))
    #if there is an outcome for the hand that was played then we display restart button
        if result != 0:
            screen.blit(font.render(results[result],True,'white'),(15,25))
            newHand = pygame.draw.rect(screen, 'white', [175,610 ,350,100],0,5)
            pygame.draw.rect(screen, 'blue', [175,610 ,350,100],3,5)
            pygame.draw.rect(screen, 'black', [178,613 ,344,94],3,5)
            deal_text = font.render('NEW HAND', True, 'black')
            screen.blit(deal_text, (225,640))
            button_list.append(pygame.Rect(0,0,0,0))
            button_list.append(pygame.Rect(0,0,0,0))
            button_list.append(newHand)
        else:
            #hit
            hit = pygame.draw.rect(screen, 'white', [0,640,350,80],0,5)
            pygame.draw.rect(screen, 'blue', [0,640 ,350,80],3,5)
            hit_text = font.render('HIT ME', True, 'black')
            screen.blit(hit_text, (100,663))
            button_list.append(hit)
            #stand
            stand = pygame.draw.rect(screen, 'white', [350,640 ,350,80],0,5)
            pygame.draw.rect(screen, 'blue', [350,640 ,350,80],3,5)
            stand_text = font.render('STAND', True, 'black')
            screen.blit(stand_text, (450,663))
            button_list.append(stand)

    return button_list

#calculate the score of a hand
def calculate_score(hand):
    hand_score = 0
    hand_with_numbers = []
    for card in hand:
        hand_with_numbers.append(card[0])
    aces_count = hand_with_numbers.count('A')
    for i in range(len(hand_with_numbers)):
        for j in range(8):
            if hand_with_numbers[i] == cards[j]:
                hand_score += int(hand_with_numbers[i])
        if hand_with_numbers[i] in ['10','J','Q','K']:
            hand_score+=10
        elif hand_with_numbers[i] == 'A':
            hand_score += 11
    while hand_score > 21 and aces_count >0:
        if hand_score>21:
            hand_score-=10
            aces_count-=1
    return hand_score
#main loop
run = True

while run:
    timer.tick(fps)
    screen.fill('black')

    if initial_deal:
        for i in range(2):
            new_card,game_deck = deal_cards(my_hand,game_deck)
            my_hand.append(new_card)
            new_card,game_deck = deal_cards(dealer_hand,game_deck)
            dealer_hand.append(new_card)
        initial_deal = False
    

    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand,dealer_hand,reveal_dealer)
        if reveal_dealer>0:
            dealer_score = calculate_score(dealer_hand)
            while dealer_score<17:
                reveal_dealer= reveal_dealer + 1
                draw_cards(my_hand,dealer_hand,reveal_dealer)
                draw_scores(player_score,dealer_score)
                pygame.display.flip()
                new_card,game_deck = deal_cards(dealer_hand,game_deck)
                dealer_hand.append(new_card)
                dealer_score = calculate_score(dealer_hand)
                time.sleep(delayBetweenDealerCards)
        draw_scores(player_score,dealer_score)
    buttons = draw_game(active,records,outcome)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    add_score = True
                    dealer_score = 0
                    player_score = 0
                    reveal_dealer = 0
                    player_bust = False
            else:
                if buttons[0].collidepoint(event.pos) and player_score<21 and hand_active:
                    new_card, game_deck = deal_cards(my_hand,game_deck)
                    my_hand.append(new_card)
                elif buttons[1].collidepoint(event.pos) and reveal_dealer==0:
                    reveal_dealer= reveal_dealer+1
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        add_score = True
                        dealer_score = 0
                        player_score = 0
                        reveal_dealer = 0
                        player_bust = False
    if hand_active and player_score>21:
        hand_active = False
        reveal_dealer = False
        player_bust = True                
    outcome, records, add_score = check_endgame(hand_active,dealer_score,player_score,outcome,records,add_score)
    pygame.display.flip()

pygame.quit()