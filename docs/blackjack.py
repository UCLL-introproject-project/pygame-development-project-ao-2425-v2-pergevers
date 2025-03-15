#import
import copy
import random
import pygame

# cards variables

cards = [ '2','3','4','5','6','7','8','9','10','J','Q','K','A']
one_deck = 4*cards
decks = 4
game_deck = copy.deepcopy(one_deck * decks)


#variables
pygame.init()
WIDTH = 700
HEIGHT = 900
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
reveal_dealer = False
hand_active = False
add_score = False
results = ['', 'Player busted', 'Player WINS!','Dealer wins','The game was tied']

#deal cards
def deal_cards(hand,deck):
    card = random.randint(0,len(deck))
    hand.append(deck[card-1])
    deck.pop(card-1)
    return hand,deck

#draw cards on screen
def draw_cards(player,dealer,reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen,'white', [70 + (70*i),420 + (5*i),120,220],0,5)
        screen.blit(font.render(player[i],True,'black'),(75+ 70*i,425+5*i))
        screen.blit(font.render(player[i],True,'black'),(152+ 70*i,595+5*i))
        pygame.draw.rect(screen,'red', [70 + (70*i),420 + (5*i),120,220],5,5)

    for i in range(len(dealer)):
        pygame.draw.rect(screen,'white', [70 + (70*i),120 + (5*i),120,220],0,5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i],True,'black'),(75+ 70*i,125+5*i))
            screen.blit(font.render(dealer[i],True,'black'),(152+ 70*i,295+5*i))
        else:
            screen.blit(font.render('?',True,'black'),(75+ 70*i,125+5*i))
            screen.blit(font.render('?',True,'black'),(152+ 70*i,295+5*i))
        pygame.draw.rect(screen,'green', [70 + (70*i),120 + (5*i),120,220],5,5)

#draw scores
def draw_scores(player,dealer):
    screen.blit(font.render(f'Your score: {player}',True,'white'),(350,400))
    if reveal_dealer:
        screen.blit(font.render(f'Dealer score: {dealer}',True,'white'),(350,100))
        
#check endgame function
def check_endgame(hand_act,deal_score,play_score,result,totals,add):
    #check endgame scenarios
    if not hand_act and deal_score>=17:
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
            elif result == 2:
                totals[0] += 1
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
        #hit
        hit = pygame.draw.rect(screen, 'white', [0,700,350,100],0,5)
        pygame.draw.rect(screen, 'blue', [0,700 ,350,100],3,5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (100,735))
        button_list.append(hit)
        #stand
        stand = pygame.draw.rect(screen, 'white', [350,700 ,350,100],0,5)
        pygame.draw.rect(screen, 'blue', [350,700 ,350,100],3,5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (450,735))
        button_list.append(stand)
        #score
        score_text = font.render(f'Wins: {record[0]}    Losses: {record[1]}     Draws: {record[2]}',True, 'white')
        screen.blit(score_text,(15,840))
    #if there is an outcome for the hand that was played then we display restart button
    if result != 0:
        screen.blit(font.render(results[result],True,'white'),(15,25))
        deal = pygame.draw.rect(screen, 'white', [175,220 ,350,100],0,5)
        pygame.draw.rect(screen, 'blue', [175,220 ,350,100],3,5)
        pygame.draw.rect(screen, 'black', [178,223 ,344,94],3,5)
        deal_text = font.render('NEW HAND', True, 'black')
        screen.blit(deal_text, (220,250))
        button_list.append(deal)
    return button_list

#calculate the score of a hand
def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        if hand[i] in ['10','J','Q','K']:
            hand_score+=10
        elif hand[i] == 'A':
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
            my_hand,game_deck = deal_cards(my_hand,game_deck)
            dealer_hand,game_deck = deal_cards(dealer_hand,game_deck)
        initial_deal = False
        print(my_hand,dealer_hand)
    

    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand,dealer_hand,reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            while dealer_score<17:
                dealer_hand,game_deck = deal_cards(dealer_hand,game_deck)
                dealer_score = calculate_score(dealer_hand)
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
                    reveal_dealer = False
            else:
                if buttons[0].collidepoint(event.pos) and player_score<21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand,game_deck)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
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
                        reveal_dealer = False
    if hand_active and player_score>21:
        hand_active = False
        reveal_dealer = True                
    outcome, records, add_score = check_endgame(hand_active,dealer_score,player_score,outcome,records,add_score)
    pygame.display.flip()

pygame.quit()