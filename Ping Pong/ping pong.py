import pygame
import os

pygame.font.init()

WID, HEIGHT = 900*1.5,600*1.5
WIN = pygame.display.set_mode(size=(WID , HEIGHT))
pygame.display.set_caption("FIRST GAME")
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (255,0,0)
YELLOW = (255,255,0)

FPS = 60
vel = 5
bullet_vel = 15
max_bullets = 5

border = pygame.Rect((WID//2)  , 0 , 5 , HEIGHT)

s_wid,s_height = 70 , 50



yellow_spaceship = pygame.image.load(os.path.join('Asset','Yellow.png'))
yellow_spaceship_ = pygame.transform.scale(yellow_spaceship,(s_wid,s_height))
green_spaceship = pygame.image.load(os.path.join('Asset','Green.png'))
green_spaceship_ = pygame.transform.scale(green_spaceship,(s_wid,s_height))
space = pygame.image.load(os.path.join('Asset' , 'space.png'))
space = pygame.transform.scale(space,(WID , HEIGHT))

yellow_hit = pygame.USEREVENT + 1
green_hit = pygame.USEREVENT + 2


health_font = pygame.font.SysFont('comicsans',40)
winner_font = pygame.font.SysFont("comicsans" , 100)

def draw_window(yellow , green , yellow_bullets , green_bullets, yellow_health , green_health):
    
    yellow_health_text = health_font.render("HEALTH : " + str(yellow_health) , 1 , WHITE)
    green_health_text = health_font.render("HEALTH : " + str(green_health) , 1 , WHITE)
    
    WIN.blit(space , (0,0))

    pygame.draw.rect(WIN , BLACK , border)
    WIN.blit(yellow_spaceship_,(yellow.x , yellow.y))
    WIN.blit(green_spaceship_,(green.x , green.y))
    WIN.blit(yellow_health_text,(10,20))
    WIN.blit(green_health_text,(WID - 250,20))

    
    for bullet in yellow_bullets :
        pygame.draw.rect(WIN , YELLOW , bullet)
    
    for bullet in green_bullets :
        pygame.draw.rect(WIN , GREEN , bullet)
    
    pygame.display.update()
    

def yellow_movement(key_pressed,yellow):
    if key_pressed[pygame.K_a] and yellow.x > 0  :
        yellow.x -= vel
    if key_pressed[pygame.K_d] and yellow.x < border.x - s_wid :
        yellow.x += vel   
    if key_pressed[pygame.K_w] and yellow.y > 0:
        yellow.y -= vel
    if key_pressed[pygame.K_s] and yellow.y < HEIGHT - s_height :
        yellow.y += vel
        
def green_movement(key_pressed,green):
    if key_pressed[pygame.K_LEFT] and green.x > (border.x+ border.width + 5) :
        green.x -= vel
    if key_pressed[pygame.K_RIGHT] and green.x < WID - s_wid:
        green.x += vel   
    if key_pressed[pygame.K_UP] and green.y > 0 :
        green.y -= vel
    if key_pressed[pygame.K_DOWN] and green.y < HEIGHT - s_height :
        green.y += vel

def bullets_movement (yellow_bullets, yellow , green_bullets , green):
            
    for (bullets)  in (yellow_bullets): 
        bullets.x += bullet_vel
        if  green.colliderect(bullets)  : 
            pygame.event.post(pygame.event.Event(green_hit))
            yellow_bullets.remove(bullets)
        elif bullets.x >WID - 10 : 
            yellow_bullets.remove(bullets)
        
    for (bullets)  in (green_bullets): 
        bullets.x -= bullet_vel
        if  yellow.colliderect(bullets):
            pygame.event.post(pygame.event.Event(yellow_hit))
            green_bullets.remove(bullets)
        if  bullets.x < 10 :
            green_bullets.remove(bullets)

def print_winner(winner):
    winner_text = winner_font.render(winner , 1 , WHITE ) 
    WIN.blit(winner_text , (300,300))
    pygame.display.update()
    pygame.time.delay(2000)
    
            
def main():

    yellow_health = 5
    green_health = 5

    yellow_bullets = []
    green_bullets = []
    
    yellow = pygame.Rect(100 , HEIGHT//2 , s_wid , s_height)
    green = pygame.Rect(WID-200,HEIGHT//2 , s_wid , s_height )
    
    clock = pygame.time.Clock()
    run = True 
    while run :
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g and len(yellow_bullets) < max_bullets :
                    bullet = pygame.Rect(yellow.x + s_wid , yellow.y + s_height//2 , 20 ,10)
                    yellow_bullets.append(bullet)
             
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l and len(green_bullets) < max_bullets :
                    bullet = pygame.Rect(green.x , green.y + s_height//2 , 20 ,10)
                    green_bullets.append(bullet)
                
            if event.type == yellow_hit:
                yellow_health -=1
                print("YH =", yellow_health)
              
            if event.type == green_hit:
                green_health -= 1
                print ("GH = ", green_health)
        
        winner = ""
        if yellow_health <= 0:
            winner = "GREEN WINS"
        elif green_health <= 0 :
            winner = "YELLOW WINS"
        

            
        key_pressed = pygame.key.get_pressed()
        
        yellow_movement(key_pressed,yellow)
        green_movement(key_pressed , green)
        bullets_movement(yellow_bullets,yellow , green_bullets , green )
        draw_window(yellow , green , yellow_bullets , green_bullets, yellow_health , green_health)
        
        if winner != "" : 
            print_winner(winner)
            break
        
        if key_pressed[pygame.K_r]:
            pygame.quit()
        
    
    main()

main()
