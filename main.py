import pygame
import math
import random
import os
from pygame import mixer
pygame.init()
mixer.init()

# define constants
WIDTH, HEIGHT = 700, 800
FRICTION = 0.9

# setup time
clock = pygame.time.Clock()
FPS = 60

# download images
background_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background", "background.png")), (WIDTH, HEIGHT))
player_right_img = pygame.image.load(os.path.join("assets", "player",  "playerright.png"))
player_left_img = pygame.image.load(os.path.join("assets", "player", "playerleft.png"))
player_straight_img = pygame.image.load(os.path.join("assets", "player", "playerstraight.png"))
player_imgs = [player_right_img, player_left_img, player_straight_img]
tree_1_img = pygame.image.load(os.path.join("assets", "objects", "tree1.png"))
tree_2_img = pygame.image.load(os.path.join("assets", "objects", "tree2.png"))
tree_3_img = pygame.image.load(os.path.join("assets", "objects", "tree3.png"))
hole_img = pygame.image.load(os.path.join("assets", "objects", "hole.png"))
tree_imgs = [tree_1_img, tree_2_img, tree_3_img, hole_img]


# setup screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SKI')

# classes

class Object:
    
    def __init__(self, x, y, imgs):
        self.x = x
        self.y = y
        self.imgs = imgs
        self.img = self.imgs[0]
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def new_size(self):
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        
    def draw(self):
        SCREEN.blit(self.img, (self.x, self.y))
        
    def reset(self):
        self.img = self.imgs[random.randint(0, len(self.imgs) - 1)]
        self.new_size()
        self.x = random.randint(0, WIDTH - self.width)
        self.y = HEIGHT
        
    def move(self, screen_speed):
        self.y -= screen_speed
        
        if self.y < HEIGHT * -1:
            self.reset()
    
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def collide(self, otherrect):
        
        if pygame.Rect.colliderect(self.rect, otherrect):
            return True
        
        return False
class ScrollingSurface:
    
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.speed = 6
        
    def move(self, keys):
        self.y -= self.speed
        
        if keys[pygame.K_DOWN]:
            if self.speed < 15:
                self.speed += 0.20
                
        if keys[pygame.K_UP]:
            if self.speed > 5:
                self.speed -= 0.20
                
        if self.y < HEIGHT * -1:
            self.x = 0
            self.y = HEIGHT
            
    def draw(self):
        SCREEN.blit(self.img, (self.x, self.y))

class Player:
    def __init__(self, x, y, imgs):
        self.x = x
        self.y = y
        self.dx = 3
        self.dy = 0
        self.imgs = imgs
        self.img = self.imgs[0]
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self):
        SCREEN.blit(self.img, (self.x, self.y))
    
    def move(self, keys):
        
        if keys[pygame.K_RIGHT]:
            self.dx = 3
            self.img = self.imgs[0]
            
        if keys[pygame.K_LEFT]:
            self.dx = -3
            self.img = self.imgs[1]
            
        
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.dx = 0
            self.img = self.imgs[2]
            
            
        self.x += self.dx
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        
# objects
back_1 = ScrollingSurface(0, 0, background_img)
back_2 = ScrollingSurface(0, HEIGHT, background_img)
objects = [Object(WIDTH // 2, HEIGHT, tree_imgs), Object(WIDTH // 2, HEIGHT * 1.9, tree_imgs)]
player = Player(WIDTH // 2, 20, player_imgs)

# game

def game():
    
    # variables
    run = True
    
    # game loop
    while run:
        
        # loop through all events
        for event in pygame.event.get():
            
            # if x button pressed then quit python
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                
        # draw
        back_1.draw()
        back_2.draw()
        player.draw()
    
        # move
        back_1.move(pygame.key.get_pressed())
        back_2.move(pygame.key.get_pressed())
        player.move(pygame.key.get_pressed())
        

        # loop through all objects
        for object in objects:
            object.draw()
            object.move(back_1.speed)
            
            if object.collide(player.rect):
                run = False
        
        # update
        pygame.display.update()
        clock.tick(FPS)
                
# run game

if __name__ == '__main__':
    game()