import pygame,sys
import os
import time
from random import choice
from player import Player
from alien import Alien
from laser import laser
import obstacle

class Game:
    def __init__(self):  #all sprite groups in it
        running = True
        # Player Setup
        player_sprite = Player((width/2,height),width,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)  # creating a player

        # Health Setup
        self.lives = 3
        self.live_surf = pygame.image.load(os.path.join("graphics", "player.png")).convert_alpha()
        self.live_x_start_pos = width - (self.live_surf.get_size()[0] * 2 + 20)

        # Obstacle Setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions,x_start = width/15,y_start = 680)

        # Alien setup
        self.aliens = pygame.sprite.Group() # creating all aliens
        self.alien_setup(rows=1,cols=2)  # size of alien wave
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group() # creating alien lasers (different from player lasers!)

        # Score setup
        self.score = 0
        self.font = pygame.font.Font(os.path.join("font", "Pixeled.ttf"),20)
    
    # Alien wave spawn
    def alien_setup(self,rows,cols,x_distance = 80,y_distance= 64,x_offset = 70,y_offset = 50):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset # spread aliens over the screen
                y = row_index * y_distance + y_offset
                if row_index <= 1: alien_sprite = Alien('yellow',x,y)
                elif row_index == 2: alien_sprite = Alien('green',x,y)
                else: alien_sprite = Alien('red',x,y)
                self.aliens.add(alien_sprite)
    
    # Alien movement
    def alien_position_check(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            #change movement direction if alien touches side of screen and move down slightly
            if alien.rect.right >= width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)
    
    # Alien movement down
    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    # Aliens shooting back
    def aliens_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites()) # pick random alien to shoot
            laser_sprite = laser(random_alien.rect.center, speed = -4)
            self.alien_lasers.add(laser_sprite)

    # Obstacle Setup
    def create_obtsacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size,(102, 102, 255),x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.create_obtsacle(x_start, y_start,offset_x)
    
    def collision_check(self):
        #player laser checks
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                #obstacle check
                #if set to true, object is destroyed
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                #alien check
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True) #list of aliens
                if aliens_hit:
                    for aliens in aliens_hit:
                        self.score+= aliens.value #adding score #increasing score based on the score of aliens hit
                    laser.kill()
        #alien laser checks
        if self.alien_lasers:
            for laser in self.alien_lasers:
                #obstacle check
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                #player check
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    
        #alien obstacle check
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    self.lives -=1

    def display_score(self):
        score_surface = self.font.render(f'score: {self.score}', False, 'white') #for score font
        score_rectangle = score_surface.get_rect(topleft = (10,-10)) # for score rectangle, 10-10 is padding
        screen.blit(score_surface, score_rectangle)

    def display_lives(self):
        for live in range(self.lives-1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf,(x, 8))
    
    def victory_message(self):
        if not self.aliens.sprites():
            for laser in self.player.sprite.lasers:
                laser.kill()
            for laser in self.alien_lasers:
                laser.kill()
            victory_surf = self.font.render('You won !!', False, 'white')
            victory_rect = victory_surf.get_rect(center = (width / 2, height / 2) )
            screen.blit(victory_surf, victory_rect)

    def game_over_message(self):
        if self.lives <= 0 :
            pygame.time.set_timer(alien_laser_timer, 100000)
            for laser in self.player.sprite.lasers:
                laser.kill()
            for laser in self.alien_lasers:
                laser.kill()
            for alien in self.aliens:
                self.alien_direction = 0

            game_over_surf = self.font.render('Game Over!!', False, 'white')
            game_over_rect = game_over_surf.get_rect(center = (width / 2, height / 2) )
            screen.blit(game_over_surf, game_over_rect)
            
    def quit(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    # Run
    def run(self):   # update all sprite groups , and draw, main framework for game
        self.player.sprite.lasers.draw(screen) # show laser on screen
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_position_check()
        self.alien_lasers.update()
        self.collision_check()
    
        self.player.draw(screen) # to see the player on screen    
        self.blocks.draw(screen) # draw obstacle on the screen
        self.aliens.draw(screen) # draw aliens on screen
        self.alien_lasers.draw(screen) # show alien lasers on screen
        self.display_score() 
        self.display_lives()
        self.victory_message()
        self.game_over_message()
        self.quit()


if __name__ == '__main__': #for safeguarding
    pygame.init()      # inital screen 
    width = 800
    height = 800
    screen = pygame.display.set_mode((width,height))
    clock= pygame.time.Clock()
    game = Game()

    alien_laser_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(alien_laser_timer, 1000) # set cooldown on aliens attacking

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == alien_laser_timer:
                game.aliens_shoot()
        
        screen.fill((30,30,30))
        game.run()

        pygame.display.flip()
        clock.tick(60)