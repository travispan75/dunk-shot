import pygame
from random import randint
import math

pygame.init()

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 680
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dunk Shot")
clock = pygame.time.Clock()
icon = pygame.image.load("Images/basketball.png")
pygame.display.set_icon(icon)
gray = (200, 200, 200)
gravity = 0.5
bounce_stop = 1
mouse_trajectory = []
friction = 0.02
active_select = False
immunity = 0

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
        if not self.selected:
            if self.y_pos < SCREEN_HEIGHT - self.radius/2:
                self.y_speed += gravity
            else:
                if self.y_speed > bounce_stop:
                    self.y_speed *= self.retention*-1
                else:
                    if abs(self.y_speed) <= bounce_stop:
                        self.y_speed = 0
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
        if not self.selected:
            self.y_pos += self.y_speed
            self.x_pos += self.x_speed
            self.update_circle()

    def check_select(self, pos):
        self.selected = False
        if self.circle.collidepoint(pos):
            self.selected = True
        return self.selected
    
    def shoot(self):
        global active_select
        active_select = False
        basket1.isFull = False
        basket2.isFull = False
        self.selected = False
        self.active_shooter = True
     
class Basket():
    def __init__(self, x_pos, y_pos, isFull):
        temp = pygame.image.load("Images/hoop (1).png").convert_alpha()
        self.basket = pygame.transform.smoothscale(temp, (100, 64))
        self.basket_width = 100
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.isFull = isFull
        temp = pygame.image.load("Images/rimleft.png").convert_alpha()
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
        
    def shootingPos(self):
        if self.isFull == True:
            ball1.x_pos = self.x_pos 
            ball1.y_pos = self.y_pos
            ball1.x_speed = 0
            ball1.y_speed = 0

ball1 = Ball(100, 360, 100, .7, 0, 0, 40)
basket1 = Basket(100, 460, False)
basket2 = Basket(100, 100, False)

def show_images():
    screen.blit(ball1.basketball, (ball1.x_pos - ball1.radius/2, ball1.y_pos - ball1.radius/2))
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if ball1.check_select(event.pos):
                    active_select = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if ball1.selected == True:
                    ball1.shoot()
                basket1.rotate = pygame.transform.rotate(basket1.basket, 0)
                basket2.rotate = pygame.transform.rotate(basket1.basket, 0)
                ball1.check_select((-1000, -1000))

def calc_motion_vector(mouseX, mouseY, basket):
    x_speed = 0
    y_speed = 0 
    if active_select == True and basket.isFull == True:
        angle_of_rotation = math.degrees(math.atan2(-(basket.y_pos - mouseY),basket.x_pos - mouseX))
        basket.rotate_rect = basket.rotate.get_rect(center = (basket.x_pos, basket.y_pos))
        basket.rotate = pygame.transform.rotate(basket.basket, angle_of_rotation - 90)
    return x_speed, y_speed

def check_collision():
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
    
    if basket2.rimLeftMask.overlap(ball1.mask, ((ball1.x_pos - ball1.radius/2) - (basket2.x_pos - 50), (ball1.y_pos - ball1.radius/2) - (basket2.y_pos - 32))) != None:
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
        if len(mouse_trajectory) > 20:
            mouse_trajectory.pop(0)
        ball1.update_pos(mouse_coords)
    elif basket1.isFull == True or basket2.isFull == True:
        ball1.update_pos(mouse_coords)
        if basket1.isFull == True:
            basket1.shootingPos()
            x_push, y_push = calc_motion_vector(mouseX, mouseY, basket1)
        if basket2.isFull == True:
            basket2.shootingPos()
            x_push, y_push = calc_motion_vector(mouseX, mouseY, basket2)
    show_images()
    pygame.display.flip()

pygame.quit()
