import pygame
import math
import random
import os
import time
from pygame import mixer
pygame.init()
mixer.init()

# define constants
WIDTH, HEIGHT = 700, 800
FRICTION = 0.9
player_size = 2



# setup font
font = pygame.font.SysFont(None, 50)
title_font = pygame.font.SysFont(None, 100)

# setup time
clock = pygame.time.Clock()
FPS = 60

# download images
background_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background", "background.png")), (WIDTH, HEIGHT))
player_right_img = pygame.image.load(os.path.join("assets", "player",  "playerright.png"))
player_left_img = pygame.image.load(os.path.join("assets", "player", "playerleft.png"))
player_straight_img = pygame.image.load(os.path.join("assets", "player", "playerstraight.png"))
player_imgs = [player_left_img, player_straight_img, player_right_img]
tree_1_img = pygame.image.load(os.path.join("assets", "objects", "tree1.png"))
tree_2_img = pygame.image.load(os.path.join("assets", "objects", "tree2.png"))
hole_img = pygame.image.load(os.path.join("assets", "objects", "hole.png"))
tree_imgs = [tree_1_img, tree_2_img, hole_img]
red_flag_img = pygame.image.load(os.path.join("assets", "collectables", "redflag.png"))

# download music
hover_sfx = pygame.mixer.Sound(os.path.join("sfx", "hover.wav"))
click_sfx = pygame.mixer.Sound(os.path.join("sfx", "click.wav"))
hit_sfx = pygame.mixer.Sound(os.path.join("sfx", "hit.wav"))
ski_sfx = pygame.mixer.Sound(os.path.join("sfx", "ski.wav"))
slowdown_sfx = pygame.mixer.Sound(os.path.join("sfx", "slowdown.wav"))
speed_sfx = pygame.mixer.Sound(os.path.join("sfx", "speed.wav"))
skiing_sfx = pygame.mixer.Sound(os.path.join("sfx", "ski.wav"))
title_sfx = pygame.mixer.Sound(os.path.join("sfx", "title.wav"))

# button images
titlenormalimg = pygame.image.load(os.path.join("assets", "buttons", "titlenormal.png"))
titlehoverimg = pygame.image.load(os.path.join("assets", "buttons", "titlehover.png"))
playnormalimg = pygame.image.load(os.path.join("assets", "buttons", "playnormal.png"))
playhoverimg = pygame.image.load(os.path.join("assets", "buttons", "playhover.png"))

# setup screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SKI HOP')

# classes

class Object:
    
    def __init__(self, x, y, imgs):
        self.x = x
        self.y = y
        self.imgs = imgs
        self.img = self.imgs[0]
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.mask = pygame.mask.from_surface(self.img)
        self.mask_img = self.mask.to_surface()
        
    def new_size(self):
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        
    def draw(self):
        # pygame.draw.rect(SCREEN, (0, 0, 0), self.rect)
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
    
        self.mask = pygame.mask.from_surface(self.img)
        
    def collide(self, othermask, otherx, othery):
        
        if self.mask.overlap(othermask, (otherx - self.x, othery - self.y)):
            return True
        
        return False
    
class Button:
    
    def __init__(self, x, y, normalimg, hoverimg):
        self.x = x
        self.y = y
        self.normalimg = normalimg
        self.hoverimg = hoverimg
        self.shouldsound = True
        self.img = self.normalimg
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self):
        SCREEN.blit(self.img, (self.x, self.y))
        
    def is_hover(self):
        
        pos = pygame.mouse.get_pos()
        collide = pygame.Rect.collidepoint(self.rect, pos)
        
        if collide:
            if self.shouldsound:
                hover_sfx.play()
                self.shouldsound = False
                
            self.img = self.hoverimg

        else:
            self.img = self.normalimg
            self.shouldsound = True
            
    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        collide = pygame.Rect.collidepoint(self.rect, pos)
        
        if collide:
            
            if pygame.mouse.get_pressed()[0] == 1:
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
                
                
        if self.y < HEIGHT * -1:
            self.x = 0
            self.y = HEIGHT
            
    def draw(self):
        SCREEN.blit(self.img, (self.x, self.y))

class Player:
    def __init__(self, x, y, imgs):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.imgs = imgs
        self.state = 1
        self.state_timer = 0
        self.img = self.imgs[0]
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.mask = pygame.mask.from_surface(self.img)
        self.mask_img = self.mask.to_surface()
        
    def draw(self):
        SCREEN.blit(self.img, (self.x, self.y))
    
    def move(self, keys):
        
        
        # change state number
        
        if self.state_timer > 0.50:
            if keys[pygame.K_RIGHT]:
                if self.state < 2:
                    self.state += 1
                
            if keys[pygame.K_LEFT]:
                if self.state > 0:
                    self.state -=1
            self.state_timer = 0
        
        # change image and direction
        
        if self.state == 0:
            self.dx = -3
            self.img = self.imgs[self.state]
            
        if self.state == 2:
            self.dx = 3
            self.img = self.imgs[self.state]
            
        if self.state == 1:
            self.dx = 0
            self.img = self.imgs[self.state]
            
            
        self.x += self.dx
        self.state_timer += 0.10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        
# objects
back_1 = ScrollingSurface(0, 0, background_img)
back_2 = ScrollingSurface(0, HEIGHT, background_img)
objects = [Object(WIDTH // 2, HEIGHT, tree_imgs), Object(WIDTH // 2, HEIGHT * 1.9, tree_imgs)]
player = Player(WIDTH // 2, 20, player_imgs)
title_btn = Button(WIDTH // 2 - titlenormalimg.get_width() // 2, 100, titlenormalimg, titlehoverimg)
play_btn = Button(WIDTH // 2 - playnormalimg.get_width() // 2, HEIGHT // 2, playnormalimg, playhoverimg)

# game

def title_def():
    
    # variables
    title = True

    # title music
    title_sfx.play(-1)
    
    # objects
    title_btn = Button(WIDTH // 2 - titlenormalimg.get_width() // 2, 100, titlenormalimg, titlehoverimg)
    play_btn = Button(WIDTH // 2 - playnormalimg.get_width() // 2, HEIGHT // 2, playnormalimg, playhoverimg)

    # title loop
    
    while title:
        
        # loop trough all events
        
        for event in pygame.event.get():
            
            # if x button pressed then quit python
            
            if event.type == pygame.QUIT:
                title = False
                pygame.quit()
                quit()

        
        # if mouse tapped then begin the game!
        
        if play_btn.is_clicked():
            title = False
            title_sfx.stop()
            click_sfx.play()
            
            break
        
        # draw
        
        SCREEN.blit(background_img, (0, 0))
        title_btn.draw()
        title_btn.is_hover()
        play_btn.draw()
        play_btn.is_hover()

        pygame.display.update()
        clock.tick(FPS)
        
def game():
    
    # variables
    run = True
    score = 0
    speed_timer = 0
    hit = False
    hit_sound = False
    
    # highscore
    highscore = 0

    # objects
    back_1 = ScrollingSurface(0, 0, background_img)
    back_2 = ScrollingSurface(0, HEIGHT, background_img)
    objects = [Object(WIDTH // 2, HEIGHT, tree_imgs), Object(WIDTH // 2, HEIGHT * 1.9, tree_imgs)]
    player = Player(WIDTH // 2, 20, player_imgs)

    # reset and init everything
    back_1.__init__(0, 0, background_img)
    back_2.__init__(0, HEIGHT, background_img)
    player.__init__(WIDTH // 2, 20, player_imgs)
    
    objects[0].y = HEIGHT
    objects[1].y = HEIGHT * 1.9
    
    # music
    skiing_sfx.play(-1)
    
    # game loop
    while run:
        
        # loop through all events
        for event in pygame.event.get():
            
            # if x button pressed then quit python
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
           
        # render text
        
        score_txt = title_font.render(f'{math.ceil(score)}', True, (0, 0, 0))  
        feet_txt = font.render('feet', True, (0, 0, 0))     
        
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
            
            if object.collide(player.mask, player.x, player.y):
                hit = True
                
                if hit_sound == False:
                    hit_sfx.play()
                    slowdown_sfx.play()
                    skiing_sfx.stop()
                    hit_sound = True
                    objects.remove(object)

        
        # draw score after trees
        SCREEN.blit(score_txt, (WIDTH // 2 - score_txt.get_width() // 2, HEIGHT - 100))
        SCREEN.blit(feet_txt, (WIDTH // 2 - feet_txt.get_width() // 2, HEIGHT - 45))
        
        # change score
        
        score += 0.10
        
        # speed timer check
        
        if speed_timer > 300:
            
            if back_1.speed < 15:
                back_1.speed += 1
                back_2.speed += 1
                speed_sfx.play()
                speed_timer = 0
            
        speed_timer += 1
        
        # if hit then slowly stop game
        
        if hit:
            if back_1.speed > 0:
                back_1.speed -= 0.07
                back_2.speed -= 0.07
                
            if back_1.speed < 1:
                back_1.speed = 0
                back_2.speed = 0
                time.sleep(1)
                run = False
            
            
        # update
        pygame.display.update()
        clock.tick(FPS)
                
# run game

if __name__ == '__main__':
    
    while True:
        title_def()
        game()
        