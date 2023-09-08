import pygame
from random import randint
import math

pygame.init()

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dunk Shot")
clock = pygame.time.Clock()
icon = pygame.image.load("Images/basketball.png")
pygame.display.set_icon(icon)
gray = (200, 200, 200)
gravity = 0.5
bounce_stop = 1
friction = 0.02
active_select = False
immunity = 0
x_push = 0
y_push = 0
scroll_threshold = 300
scroll_floor = 550
counter = 0
canScore = False
scored = False
score = 0
counter2 = 0
multiplier = 1
lives = 2
newLife = False
stuckCounter = 0
buttonPressed = False

def gameReset():
    global ball1
    global basket1
    global basket2
    global score
    global canScore
    global scored
    global counter
    global counter2
    global multiplier
    global lives
    ball1 = Ball(100, 360, 100, .7, 0, 0, 40)
    basket1 = Basket(100, 460, False)
    basket2 = Basket(300, 300, False)
    score = 0
    canScore = False
    scored = False
    score = 0
    counter = 0
    counter2 = 0
    multiplier = 1
    lives = 2
    stuckCounter = 0

class Ball:
    def __init__(self, x_pos, y_pos, mass, retention, y_speed, x_speed, radius):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.mass = mass
        self.retention = retention
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.radius = radius
        temp = pygame.image.load("Images/ball.png").convert_alpha()
        self.basketball = pygame.transform.smoothscale(temp, (self.radius, self.radius))
        self.selected = False
        self.circle = ''
        self.mask = pygame.mask.from_surface(self.basketball)
        self.rect = self.basketball.get_rect()
        self.rect.topleft = (self.x_pos, self.y_pos)
        self.active_shooter = False
    
    def update_circle(self):
        surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
        self.circle = pygame.draw.circle(surface, (0, 0, 0, 0), (self.x_pos, self.y_pos), self.radius/2)
    
    def check_gravity(self):
        global lives
        global newLife
        if not self.selected and self.active_shooter == False:
            if self.y_pos < SCREEN_HEIGHT - self.radius/2:
                self.y_speed += gravity
            else:
                if lives > 0:
                    newLife = True
                    lives -= 1
                    if basket1.isShooter:
                        ball1.x_speed = 0
                        ball1.y_speed = 0
                        ball1.x_pos = basket1.x_pos
                        ball1.y_pos = basket1.y_pos - 100
                    elif basket2.isShooter:
                        ball1.x_speed = 0
                        ball1.y_speed = 0
                        ball1.x_pos = basket2.x_pos
                        ball1.y_pos = basket2.y_pos - 100
                else:
                    gameReset()
            if (self.x_pos < self.radius/2 and self.x_speed < 0) or (self.x_pos > SCREEN_WIDTH - self.radius/2 and self.x_speed > 0):
                self.x_speed *= -1*self.retention
                if abs(self.x_speed) <= bounce_stop:
                    self.x_speed = 0
            if abs(self.x_speed) > 0 and self.y_speed == 0:
                self.x_speed -= self.x_speed*friction
        else:
            self.x_speed = x_push
            self.y_speed = y_push
        return self.y_speed
    
    def update_pos(self, mouse):
        global counter
        screen_scroll = 0
        self.update_circle()
        self.x_pos += self.x_speed
        if ball1.y_pos < scroll_threshold and ball1.y_speed < 0:
            screen_scroll = self.y_speed
            basket1.y_pos -= screen_scroll
            basket2.y_pos -= screen_scroll
            counter += 1
        elif counter > 0 and ball1.y_speed > 0:
            screen_scroll = self.y_speed
            basket1.y_pos -= screen_scroll
            basket2.y_pos -= screen_scroll
            counter -= 1
        else:
            self.y_pos += self.y_speed

    def check_select(self, pos):
        self.selected = False
        if self.circle.collidepoint(pos):
            self.selected = True
        return self.selected
    
    def shoot(self):
        global active_select
        active_select = False
        self.selected = False
        self.active_shooter = True
        if fullBasket(basket1, basket2) != False:
            fullBasket(basket1, basket2).isFull == False
     
class Basket():
    def __init__(self, x_pos, y_pos, isFull):
        temp = pygame.image.load("Images/hoop (1).png").convert_alpha()
        self.basket = pygame.transform.smoothscale(temp, (100, 64))
        self.basket_width = 100
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.isFull = isFull
        temp = pygame.image.load("Images/rim_hitbox.png").convert_alpha()
        temp = pygame.transform.smoothscale(temp, (100, 64))
        self.rimLeftMask = pygame.mask.from_surface(temp)
        temp = pygame.image.load("Images/goalmask.png").convert_alpha()
        temp = pygame.transform.smoothscale(temp, (100, 64))
        self.rimRightMask = pygame.mask.from_surface(temp)
        temp = pygame.image.load("Images/pixil-frame-0.png").convert_alpha()
        temp = pygame.transform.smoothscale(temp, (100, 64))
        self.netMask = pygame.mask.from_surface(temp)
        self.rotate = pygame.transform.rotate(self.basket, 0)
        self.rotate_rect = self.rotate.get_rect(center = (self.x_pos, self.y_pos))
        self.isShooter = False

    def shootingPos(self):
        if self.isFull == True:
            ball1.x_pos = self.x_pos 
            ball1.y_pos = self.y_pos
            ball1.x_speed = 0
            ball1.y_speed = 0 
        
class Button():
    def __init__(self, x, y, img):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)
    
    def drawButton(self):
        screen.blit(self.img, (self.rect.x, self.rect.y)) 

    def check_select(self, pos):
        self.selected = False
        if self.rect.collidepoint(pos):
            self.selected = True
        return self.selected

ball1 = Ball(100, 360, 100, .7, 0, 0, 40)
basket1 = Basket(100, 460, False)
basket2 = Basket(300, 300, False)
temp = pygame.image.load("Images/reload.png").convert_alpha()
temp = pygame.transform.smoothscale(temp, (64, 64))
restartButton = Button(208, 500, temp)

def show_images():
    screen.blit(ball1.basketball, (ball1.x_pos - ball1.radius/2, ball1.y_pos - ball1.radius/2))
    font = pygame.font.SysFont("Railway", 100)
    score_string = str(score)
    img = font.render(score_string, True, (169, 169, 169, 0.6))
    screen.blit(img, (220, 130))
    if basket1.isShooter == True:
        temp = pygame.image.load("Images/hoop (2).png").convert_alpha()
        basket1.basket = pygame.transform.smoothscale(temp, (100, 64))
    if basket2.isShooter == True:
        temp = pygame.image.load("Images/hoop (2).png").convert_alpha()
        basket2.basket = pygame.transform.smoothscale(temp, (100, 64))
    if basket1.isShooter == False:
        temp = pygame.image.load("Images/hoop (1).png").convert_alpha()
        basket1.basket = pygame.transform.smoothscale(temp, (100, 64))
    if basket2.isShooter == False:
        temp = pygame.image.load("Images/hoop (1).png").convert_alpha()
        basket2.basket = pygame.transform.smoothscale(temp, (100, 64))
    font = pygame.font.SysFont("Railway", 40)
    lives_string = "Lives: " + str(lives + 1)
    img = font.render(lives_string, True, (169, 169, 169, 0.6))
    screen.blit(img, (25, 25))
    #screen.blit(ball1.mask.to_surface(unsetcolor=(0,0,0,0), setcolor= (255,255,255,255)), (ball1.x_pos - ball1.radius/2, ball1.y_pos - ball1.radius/2))
    #screen.blit(basket1.netMask.to_surface(unsetcolor=(0,0,0,0), setcolor= (255,255,255,255)), (basket1.x_pos - 50, basket1.y_pos - 32))
    #screen.blit(basket1.rimLeftMask.to_surface(unsetcolor=(0,0,0,0), setcolor= (255,255,255,255)), (basket1.x_pos - 50, basket1.y_pos - 32))
    #screen.blit(basket1.rimRightMask.to_surface(unsetcolor=(0,0,0,0), setcolor= (255,255,255,255)), (basket1.x_pos - 50, basket1.y_pos - 32))
    if basket1.isFull == True and active_select == True:
        screen.blit(basket1.rotate, (basket1.rotate_rect))
        screen.blit(basket2.basket, (basket2.x_pos - 50, basket2.y_pos - 32))
    elif basket2.isFull == True and active_select == True:
        screen.blit(basket1.basket, (basket1.x_pos - 50, basket1.y_pos - 32))
        screen.blit(basket2.rotate, (basket2.rotate_rect))
    else:
        screen.blit(basket1.basket, (basket1.x_pos - 50, basket1.y_pos - 32))
        screen.blit(basket2.basket, (basket2.x_pos - 50, basket2.y_pos - 32))

def check_event():
    global run
    global active_select
    global buttonPressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if ball1.check_select(event.pos):
                    active_select = True
                if restartButton.check_select(event.pos):
                    buttonPressed = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if ball1.selected == True and (abs(x_push) > 3 or abs(y_push) > 3):
                    ball1.shoot()
                ball1.check_select((-1000, -1000))
                basket1.rotate = pygame.transform.rotate(basket1.basket, 0)
                basket2.rotate = pygame.transform.rotate(basket1.basket, 0)
                active_select = False
                if buttonPressed == True:
                    buttonPressed = False
                    gameReset()

def calc_motion_vector(mouseX, mouseY, basket):
    x_speed = 0
    y_speed = 0 
    x_speed = (ball1.x_pos - mouseX)*0.1
    y_speed = (ball1.y_pos - mouseY)*0.15
    if y_speed != 0:
        if abs(y_speed) > 20:
            if y_speed > 0:
                y_speed = 20
            else:
                y_speed = -20
        elif abs(y_speed) > 2 and abs(y_speed) < 3:
            y_speed *= 1.2
    if x_speed != 0:
        if abs(x_speed) > 20:
            if x_speed > 0:
                x_speed = 20
            else:
                x_speed = -20
        elif abs(x_speed) > 2 and abs(x_speed) < 3:
            x_speed *= 1.2
    if active_select == True and basket.isFull == True:
        angle_of_rotation = math.degrees(math.atan2(-(basket.y_pos - mouseY),basket.x_pos - mouseX))
        basket.rotate_rect = basket.rotate.get_rect(center = (basket.x_pos, basket.y_pos))
        basket.rotate = pygame.transform.rotate(basket.basket, angle_of_rotation - 90)
    if (abs(x_speed) > 3 or abs(y_speed) > 3) and active_select == True:
        draw_tracer(x_speed, y_speed)
    return x_speed, y_speed
    
def draw_circle(x, y):
    surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(screen, (105,105,105,0.8), (x, y), 5)

def draw_tracer(x_speed, y_speed):
    tracerPos = calc_future_position(x_speed, y_speed)
    for i in range(len(tracerPos)):
        draw_circle(tracerPos[i][0], tracerPos[i][1])

def calc_future_position(x_speed, y_speed):
    tracerList = [[None for x in range(2)] for y in range(9)]
    xSpeed = x_speed*1.5
    ySpeed = y_speed*1.5
    futureX = ball1.x_pos
    futureY = ball1.y_pos
    for i in range(len(tracerList)):
        if (futureX < ball1.radius/2 and xSpeed < 0) or (futureX > SCREEN_WIDTH - ball1.radius/2 and xSpeed > 0):
                xSpeed *= -1*ball1.retention
        futureX += xSpeed
        futureY += ySpeed + gravity
        tracerList[i][0] = futureX
        tracerList[i][1] = futureY
    return tracerList

def check_still_in_basket():
    if basket1.rimLeftMask.overlap(ball1.mask, ((ball1.x_pos - ball1.radius/2) - (basket1.x_pos - 50), (ball1.y_pos - ball1.radius/2) - (basket1.y_pos - 32))) != None:
        return True
    elif basket1.rimRightMask.overlap(ball1.mask, ((ball1.x_pos - ball1.radius/2) - (basket1.x_pos - 50), (ball1.y_pos - ball1.radius/2) - (basket1.y_pos - 32))) != None:
        return True
    elif basket1.netMask.overlap(ball1.mask, ((ball1.x_pos - ball1.radius/2) - (basket1.x_pos - 50), (ball1.y_pos - ball1.radius/2) - (basket1.y_pos - 32))) != None:
        return True
    elif basket2.rimLeftMask.overlap(ball1.mask, ((ball1.x_pos - ball1.radius/2) - (basket2.x_pos - 50), (ball1.y_pos - ball1.radius/2) - (basket2.y_pos - 32))) != None:
        return True
    elif basket2.rimRightMask.overlap(ball1.mask, ((ball1.x_pos - ball1.radius/2) - (basket2.x_pos - 50), (ball1.y_pos - ball1.radius/2) - (basket2.y_pos - 32))) != None:
        return True
    elif basket2.netMask.overlap(ball1.mask, ((ball1.x_pos - ball1.radius/2) - (basket2.x_pos - 50), (ball1.y_pos - ball1.radius/2) - (basket2.y_pos - 32))) != None:
        return True
    else:
        basket1.isFull = False
        basket2.isFull = False
        return False

def check_collision():
    global score
    global canScore
    global scored
    if basket1.rimLeftMask.overlap(ball1.mask, ((ball1.x_pos - ball1.radius/2) - (basket1.x_pos - 50), (ball1.y_pos - ball1.radius/2) - (basket1.y_pos - 32))) != None:
        if abs(ball1.x_speed) > bounce_stop:
            ball1.x_pos -= ball1.x_speed
            ball1.x_speed *= 0.5*-1
        else:
            ball1.x_pos -= ball1.x_speed
            ball1.x_speed = 0
        if abs(ball1.y_speed) > bounce_stop:
            ball1.y_pos -= ball1.y_speed
            ball1.y_speed *= 0.5*-1
        else:
            ball1.y_pos -= ball1.y_speed
            ball1.y_speed = 0
        return True
    elif basket1.rimRightMask.overlap(ball1.mask, ((ball1.x_pos - ball1.radius/2) - (basket1.x_pos - 50), (ball1.y_pos - ball1.radius/2) - (basket1.y_pos - 32))) != None:
        basket1.isFull = True
        if canScore == True and basket1.isShooter == False:
            canScore = False
            score += 1
            scored = True
        basket1.isShooter = True
        basket2.isShooter = False
        return False
    elif basket1.netMask.overlap(ball1.mask, ((ball1.x_pos - ball1.radius/2) - (basket1.x_pos - 50), (ball1.y_pos - ball1.radius/2) - (basket1.y_pos - 32))) != None:
        if abs(ball1.x_speed) > bounce_stop:
            ball1.x_pos -= ball1.x_speed
            ball1.x_speed *= 0.2*-1
        else:
            ball1.x_pos -= ball1.x_speed
            ball1.x_speed = 0
        if abs(ball1.y_speed) > bounce_stop:
            ball1.y_pos -= ball1.y_speed
            ball1.y_speed *= 0.2*-1
        else:
            ball1.y_pos -= ball1.y_speed
            ball1.y_speed = 0
        return True
    elif basket2.rimLeftMask.overlap(ball1.mask, ((ball1.x_pos - ball1.radius/2) - (basket2.x_pos - 50), (ball1.y_pos - ball1.radius/2) - (basket2.y_pos - 32))) != None:
        if abs(ball1.x_speed) > bounce_stop:
            ball1.x_pos -= ball1.x_speed
            ball1.x_speed *= 0.5*-1
        else:
            ball1.x_pos -= ball1.x_speed
            ball1.x_speed = 0
        if abs(ball1.y_speed) > bounce_stop:
            ball1.y_pos -= ball1.y_speed
            ball1.y_speed *= 0.5*-1
        else:
            ball1.y_pos -= ball1.y_speed
            ball1.y_speed = 0
        return True
    elif basket2.rimRightMask.overlap(ball1.mask, ((ball1.x_pos - ball1.radius/2) - (basket2.x_pos - 50), (ball1.y_pos - ball1.radius/2) - (basket2.y_pos - 32))) != None:
        basket2.isFull = True
        if canScore == True and basket2.isShooter == False:
            canScore = False
            score += 1
            scored = True
        basket2.isShooter = True
        basket1.isShooter = False
        return False
    elif basket2.netMask.overlap(ball1.mask, ((ball1.x_pos - ball1.radius/2) - (basket2.x_pos - 50), (ball1.y_pos - ball1.radius/2) - (basket2.y_pos - 32))) != None:
        if abs(ball1.x_speed) > bounce_stop:
            ball1.x_pos -= ball1.x_speed
            ball1.x_speed *= 0.2*-1
        else:
            ball1.x_pos -= ball1.x_speed
            ball1.x_speed = 0
        if abs(ball1.y_speed) > bounce_stop:
            ball1.y_pos -= ball1.y_speed
            ball1.y_speed *= 0.2*-1
        else:
            ball1.y_pos -= ball1.y_speed
            ball1.y_speed = 0
        return True
    else:
        basket1.isFull = False
        basket2.isFull = False
        return False

def fullBasket(basket1, basket2):
    if basket1.isFull == True:
        return basket1
    elif basket2.isFull == True:
        return basket2
    else:
        return False

def emptyBasket(basket1, basket2):
    if basket1.isFull == False:
        return basket1
    elif basket2.isFull == False:
        return basket2
    else:
        return False

def scroll_screen(basket1, basket2):
    global canScore
    global scored
    still_scrolling = False
    full_basket = fullBasket(basket1, basket2)
    if full_basket != False and canScore == False:
        if full_basket.y_pos < 460:
            full_basket.y_pos += 3
            still_scrolling = True
    if scored == True and canScore == False and still_scrolling == False:
        scored = False
        newBasket(emptyBasket(basket1, basket2))

def newBasket(basket):
    basket.y_pos = randint(200, SCREEN_HEIGHT - 425)
    basket.x_pos = randint(100, SCREEN_WIDTH - 100)
            
run = True

while run == True:
    clock.tick(60)
    check_event()
    screen.fill(gray)
    mouse_coords = pygame.mouse.get_pos()
    mouseX = mouse_coords[0]
    mouseY = mouse_coords[1]
    if basket1.isFull == False and basket2.isFull == False:
        if check_collision() == False:
            ball1.y_speed = ball1.check_gravity()
        ball1.update_pos(mouse_coords)
    elif basket1.isFull == True or basket2.isFull == True:
        if ball1.active_shooter == False:
            ball1.update_pos(mouse_coords)
            if basket1.isFull == True:
                basket1.shootingPos()
                x_push, y_push = calc_motion_vector(mouseX, mouseY, basket1)
            if basket2.isFull == True:
                basket2.shootingPos()
                x_push, y_push = calc_motion_vector(mouseX, mouseY, basket2)
        else:
            canScore = True
            ball1.y_speed = ball1.check_gravity()
            ball1.update_pos(mouse_coords)
            if check_still_in_basket() == False:
                ball1.active_shooter = False
    if fullBasket(basket1, basket2) == False:
        stuckCounter += 0.1
        if stuckCounter > 30:
            restartButton.drawButton()
    else:
        stuckCounter = 0
    show_images()
    scroll_screen(basket1, basket2)
    pygame.display.flip()
pygame.quit()
