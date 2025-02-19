"""
keep from: adding sound
"""

import random
import sys

import pygame
from pygame.math import Vector2

CELL_NUMBER = 20
CELL_SIZE = 40  # cell size in pixels


class Fruit:
    #  Default init constructor
    def __init__(self):
        self.x = None
        self.y = None
        self.pos = None

        # image Surface object
        self.apple = pygame.image.load("Graphics/apple.png").convert_alpha()

        self.randomize()

    def draw_fruit(self):
        """
        draw the fruit with the new random position on the screen
        :return:
        """
        apple_rect = self.apple.get_rect()
        apple_rect.topleft = self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE
        root.blit(self.apple, apple_rect)

    def randomize(self):
        """
        move the fruit to a new random position
        """
        self.x = random.randint(0, CELL_NUMBER - 1)  # default value that might be changed in the future
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)  # position of the fruit on the grid


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10),
                     Vector2(7, 10)]  # each item is the position's square of the snake on the grid
        self.head_direction = Vector2(1, 0)

        self.head_up = pygame.image.load("Graphics/head_up.png").convert_alpha()  # heads
        self.head_down = pygame.image.load("Graphics/head_down.png").convert_alpha()
        self.head_right = pygame.image.load("Graphics/head_right.png").convert_alpha()
        self.head_left = pygame.image.load("Graphics/head_left.png").convert_alpha()

        self.body_horizontal = pygame.image.load("Graphics/body_horizontal.png").convert_alpha()  # bodies
        self.body_vertical = pygame.image.load("Graphics/body_vertical.png").convert_alpha()

        self.body_bl = pygame.image.load("Graphics/body_bl.png").convert_alpha()  # sides
        self.body_br = pygame.image.load("Graphics/body_br.png").convert_alpha()
        self.body_tl = pygame.image.load("Graphics/body_tl.png").convert_alpha()
        self.body_tr = pygame.image.load("Graphics/body_tr.png").convert_alpha()

        self.tail_up = pygame.image.load("Graphics/tail_up.png").convert_alpha()  # tails
        self.tail_down = pygame.image.load("Graphics/tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("Graphics/tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("Graphics/tail_left.png").convert_alpha()

        self.crunch_sound = pygame.mixer.Sound(file='crunch.wav')

    def draw_snake(self):
        """
        draw the snake body on the screen at each frame.
        """
        self.update_head_image()
        self.update_tail_image()

        for idx, square_pos in enumerate(self.body):  # run through the body segments (Vector2 objects)
            x_pos = square_pos.x * CELL_SIZE
            y_pos = square_pos.y * CELL_SIZE
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)  # Rect object

            if idx == len(self.body) - 1:  # head
                root.blit(self.head, block_rect)

            elif idx == 0:  # tail
                root.blit(self.tail, block_rect)

            else:  # body
                next_square_pos = self.body[idx + 1]
                previous_square_pos = self.body[idx - 1]

                next_direction = next_square_pos - square_pos  # unit vector
                previous_direction = square_pos - previous_square_pos  # unit vector

                if (next_direction.x == 1 and previous_direction.y == -1) or (
                        next_direction.y == 1 and previous_direction.x == -1):
                    root.blit(self.body_br, block_rect)

                elif (next_direction.x == -1 and previous_direction.y == -1) or (
                        next_direction.y == 1 and previous_direction.x == 1):
                    root.blit(self.body_bl, block_rect)

                elif (next_direction.x == -1 and previous_direction.y == 1) or (
                        next_direction.y == -1 and previous_direction.x == 1):
                    root.blit(self.body_tl, block_rect)

                elif (next_direction.x == 1 and previous_direction.y == 1) or (
                        next_direction.y == -1 and previous_direction.x == -1):
                    root.blit(self.body_tr, block_rect)

                elif next_direction.x == 1 or next_direction.x == -1:  # body
                    root.blit(self.body_horizontal, block_rect)

                elif next_direction.y == 1 or next_direction.y == -1:  # body
                    root.blit(self.body_vertical, block_rect)

    def update_head_image(self):

        if self.head_direction.x == 1:  # right
            self.head = self.head_right
        elif self.head_direction.x == -1:  # left
            self.head = self.head_left
        elif self.head_direction.y == -1:  # up
            self.head = self.head_up
        elif self.head_direction.y == 1:  # down
            self.head = self.head_down

    def update_tail_image(self):
        tail_relation = self.body[1] - self.body[0]

        if tail_relation.x == 1:
            self.tail = self.tail_left
        elif tail_relation.x == -1:
            self.tail = self.tail_right
        elif tail_relation.y == -1:
            self.tail = self.tail_down
        elif tail_relation.y == 1:
            self.tail = self.tail_up

    def move_snake(self):
        """
        update the snake body so that the block before the head gets the position where
        the head used to be, and so on.
        """
        for i in range(len(self.body[:-1])):
            self.body[i].xy = self.body[i + 1].xy  # (x,y) = (x,y)
        self.body[-1] += self.head_direction

    def add_block(self):
        """
        each time the snake eat the fruit, we add a new block at the end of the snake,
        which is the first item in the snake_body list.
        """
        new_block = self.body[0] - self.head_direction
        self.body.insert(0, new_block)

    def reset(self):
        "Reset the snake to its original body and start a new game"
        self.body = [Vector2(5, 10), Vector2(6, 10),Vector2(7, 10)]
        self.head_direction = Vector2(1,0)


class GameManager:
    """
    manage the game and the game's logic.
    make the actual game by using all the classes together.
    """

    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update_elements(self):
        """
        update the positions of the elements and set their behavior.:
        snake - move the snake to next position.
        fruit - move the fruit to new random position.
        check the behavior - collision with the fruit or the walls.
        """
        self.snake.move_snake()
        self.check_eat_fruit()
        self.check_fail()

    def draw_elements(self):
        """
        draw the elements on the screen after the update
        """
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_eat_fruit(self):
        """
        whenever the snake position equal to fruit position, it means
        we eat the fruit. in that case we add a new block to the snake's body, and
        move the fruit to a new random position.

        """
        if self.snake.body[-1].xy == self.fruit.pos:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.crunch_sound.play()

            # to ensure our fruit will never be on top of the snake body.
            while self.fruit.pos in self.snake.body[:-1]:
                self.fruit.randomize()



    def check_fail(self):
        """
        check the snake collision with each side of the screen or with each part of
        his body.
        """

        if self.snake.body[-1].x > CELL_NUMBER - 1 or self.snake.body[-1].x < 0:  # horizontal
            self.game_over()
        elif self.snake.body[-1].y > CELL_NUMBER - 1 or self.snake.body[-1].y < 0:  # vertical
            self.game_over()

        for segment in self.snake.body[:-1]:  # collision with body
            if self.snake.body[-1] == segment:
                self.game_over()

    def draw_grass(self):
        """
        draw grass pattern on the screen
        """
        block_color1 = (156, 210, 54)
        block_color2 = (147, 203, 57)

        for row in range(CELL_NUMBER):
            for column in range(CELL_NUMBER):
                block = pygame.Rect(column * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if column % 2 == 0:
                    pygame.draw.rect(root, block_color1, block)
                else:
                    pygame.draw.rect(root, block_color2, block)

            temp = block_color1
            block_color1 = block_color2
            block_color2 = temp

    def draw_score(self):
        """
        draw the score on the screen each time the snake eat the fruit.
        """

        snake_score = str(len(self.snake.body) - 3)  # initial value = 0

        # apply the font to our score text and create a score surface:
        score_surface = game_font.render(snake_score, True, "black") # antialiasing make the text a bit smoother
        apple_surface = pygame.image.load("Graphics/apple.png").convert_alpha()


        score_rect = score_surface.get_rect(midleft=(CELL_SIZE, CELL_SIZE - 20))
        apple_rect = apple_surface.get_rect(midright=(score_rect.left, score_rect.centery))

        bg_rect = pygame.Rect(apple_rect.topleft,(apple_rect.width + score_rect.width + 5,apple_rect.height))
        pygame.draw.rect(root,(147, 203, 57),bg_rect)

        root.blit(score_surface, score_rect)
        root.blit(apple_surface, apple_rect)

        pygame.draw.rect(root,"darkgreen",bg_rect,2)


    def game_over(self):
        self.snake.reset()

# set up
pygame.mixer.pre_init()
pygame.init()
grid = CELL_NUMBER * CELL_SIZE  # 800 x 800
root = pygame.display.set_mode(size=(grid, grid))
clock = pygame.time.Clock()
game_manager = GameManager()
game_font = pygame.font.Font("PoetsenOne-Regular.ttf", 25)

# custom event:
SCREEN_UPDATE = pygame.USEREVENT  # custom event
pygame.time.set_timer(SCREEN_UPDATE, 120)

while True:  # game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            game_manager.update_elements()
        if event.type == pygame.KEYDOWN:  # user events:
            if event.key == pygame.K_UP:
                if game_manager.snake.head_direction.y != 1:
                    game_manager.snake.head_direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if game_manager.snake.head_direction.y != -1:
                    game_manager.snake.head_direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if game_manager.snake.head_direction.x != 1:
                    game_manager.snake.head_direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if game_manager.snake.head_direction.x != -1:
                    game_manager.snake.head_direction = Vector2(1, 0)

    game_manager.draw_elements()

    pygame.display.update()
    clock.tick(120)  # frame rate
