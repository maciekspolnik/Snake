import random
import sys

import pygame
from gamedata import *

pygame.init()
clock = pygame.time.Clock()


class GameObject:
    """
    Class representing an object on two dimensional axis and managing it.
    """
    def __init__(self):
        self.x = None
        self.y = None

    def reset(self, param):
        """
        Method resetting object to its initial location.
        """
        if param != 0:
            self.__init__(param)
        else:
            self.__init__()

    def randomize_values(self, snake) -> tuple:
        """
        Method that generates random point on two dimensional axis
        :returns: tuple of x,y coordinates
        """
        while True:
            x = round(random.randrange(BOARD_START, SCREEN_WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            if [x, y] not in snake.body:
                self.x = x
                self.y = y
                break
        return x, y


class Snake(GameObject):
    """
    Class representing an object of snake
    """
    def __init__(self):
        super().__init__()
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.x_movement = self.y_movement = STOP
        self.body = []
        self.length = 1
        self.speed = INITIAL_SPEED

    def grow(self):
        """
        Method that makes snake grow after eating food
        """
        self.length += 1
        if self.length > 1 and self.length % 5 == 1:
            self.speed += 1

    def collision_check(self):
        """
        Method checking if a collision of snake and terrain/his body happened.
        :return: bool value
        """

        if (self.x >= BOARD_START + BOARD_SIZE or self.x < BOARD_START
                or self.y >= SCREEN_HEIGHT or self.y < 0):
            self.x_movement = self.y_movement = STOP
            return True
        for i in self.body[:-1]:
            if i == [self.x, self.y]:
                return True
        return False

    def turn(self, direction: str):
        """
        Method that makes snake turn to the given direction.
        :param direction: Direction, that snake should turn to.
        """
        if direction == "LEFT":
            self.x_movement = LEFT
            self.y_movement = STOP
        elif direction == "RIGHT":
            self.x_movement = RIGHT
            self.y_movement = STOP
        elif direction == "UP":
            self.x_movement = STOP
            self.y_movement = UP
        elif direction == "DOWN":
            self.x_movement = STOP
            self.y_movement = DOWN

    def move(self):
        """
        Method that makes snake move one block farther.
        """
        self.x += self.x_movement
        self.y += self.y_movement
        self.body.append([self.x, self.y])
        if len(self.body) > self.length:
            del self.body[0]


class Food(GameObject):
    """
    Class representing food object
    """

    def __init__(self, snake):
        super().__init__()
        self.randomize_values(snake)

    def eaten_check(self, snake):
        """
        Method that checks if food has been eaten by a snake
        :param snake: object representing a snake
        """
        if snake.x == self.x and snake.y == self.y:
            self.reset(snake)
            snake.grow()


class Screen:
    """
    Class representing and controlling the display of the game.
    """
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_icon(pygame.image.load(ICON))
        pygame.display.set_caption('SNAKE GAME')
        self.font_normal = pygame.font.SysFont("segoeui", FONT_SIZE)
        self.font_big = pygame.font.SysFont("segoeui", FONT_SIZE_LARGE)
        self.mouse_coords = STARTER_MOUSE_COORDS

    def draw_framed_rect(self, coords, color):
        """
        Method that prints a rectangle with a gray frame around it.
        :param coords: coordinates of the rectangle [x,y,width,height]
        :param color: RGB tuple representing color
        """
        pygame.draw.rect(self.screen, GRAY, coords)
        pygame.draw.rect(self.screen, color, [coords[0] + 1, coords[1] + 1, coords[2] - 2, coords[3] - 2])

    def render_text(self, text, coords, font, color=GRAY):
        """
        Method rendering and printing given text on the screen.
        :param text: String to be printed
        :param coords: coordinates of the text [x,y,width,height]
        :param font: pygame.font object
        :param color: RGB tuple representing color
        """
        self.screen.blit(font.render(text, True, color), coords)

    def render_image(self, image, coords):
        """
        Method rendering image on the screen
        :param image: image path (string)
        :param coords: coordinates of the image [x,y]
        """
        self.screen.blit(pygame.image.load(image), coords)

    def render_score(self, score):
        """
        Method rendering score during game screen phase
        :param score: score number to be shown
        """
        self.render_text("SCORE: " + str(score - 1), SCORE, self.font_normal)

    def draw_snake(self, snake_list):
        """
        Method that renders snake on the screen
        :param snake_list: list of snake body parts (its positions)
        :return:
        """

        for i in snake_list:
            self.draw_framed_rect([i[0], i[1], SNAKE_SIZE, SNAKE_SIZE], GREEN)

    def draw_food(self, food):
        """
        Method that renders food on the screen.
        :param food: object representing food.
        """
        self.draw_framed_rect([int(food.x), int(food.y), SNAKE_SIZE, SNAKE_SIZE], RED)

    def draw_game_screen(self, snake, food):
        """
        Method that prints the main game screen.
        :param snake: object representing snake.
        :param food: object representing food.
        """
        self.draw_framed_rect(BOARD, YELLOW)
        self.draw_framed_rect(BACKGROUND, LIGHT_BLUE)
        self.draw_framed_rect(SCOREBOARD, BLUE)
        self.render_image(LOGO_IMG_SMALL, GAME_LOGO)
        self.draw_food(food)
        self.draw_snake(snake.body)
        self.render_score(snake.length)
        screen_update()

    def draw_start_screen(self):
        """
        Method that prints the starting game screen.
        """
        self.draw_framed_rect(WINDOW, LIGHT_BLUE)
        self.draw_framed_rect(START_BUTTON, BLUE)
        self.draw_framed_rect(EXIT_BUTTON, BLUE)
        self.render_image(LOGO_IMG_LARGE, START_LOGO)
        self.render_text("SNAKE", START_TITLE, self.font_big)
        self.render_text("START", START_START, self.font_normal)
        self.render_text("EXIT", START_EXIT, self.font_normal)
        screen_update()

    def draw_final_screen(self, snake):
        """
        Method that prints the starting game screen.
        :param snake: object representing snake.
        """
        self.render_score(snake.length)
        self.draw_framed_rect(BOX_FINAL_UPPER, BLUE)
        self.draw_framed_rect(BOX_FINAL_LOWER, BLUE)
        self.render_text("GAME OVER", FINAL_OVER, self.font_big)
        self.render_text("TO PLAY AGAIN, PRESS RETURN", FINAL_AGAIN, self.font_normal)
        self.render_text("TO QUIT, PRESS ESC", FINAL_EXIT, self.font_normal)
        screen_update()


def screen_update():
    """
    A function that refreshes the game screen
    """
    pygame.display.update()


def button(coords, button_coords):
    """
    A function checking if a certain button was clicked.
    :param coords: mouse click coords
    :param button_coords: button coords tuple
    :return: bool value
    """
    if (button_coords[0] <= coords[0] <= button_coords[0] + button_coords[2] and
            button_coords[1] <= coords[1] <= button_coords[1] + button_coords[3]):
        return True
    else:
        return False


def starting_events_check(screen: Screen):
    """
    Function checking pygame events in the starting screen
    :param screen: object representing screen
    :return: bool value
    """
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return False
        if (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1):
            screen.mouse_coords = pygame.mouse.get_pos()
            if button(screen.mouse_coords, START_BUTTON):
                return False
        if ((event.type == pygame.KEYDOWN
             and event.key == pygame.K_ESCAPE)
                or button(screen.mouse_coords, EXIT_BUTTON)
                or event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
    return True


def game_events_check(snake: Snake):
    """
    Function checking pygame events in the game screen
    :param snake: object representing snake
    """
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a) and snake.x_movement != RIGHT:
                snake.turn("LEFT")
            elif event.key in (pygame.K_RIGHT, pygame.K_d) and snake.x_movement != LEFT:
                snake.turn("RIGHT")
            elif event.key in (pygame.K_UP, pygame.K_w) and snake.y_movement != DOWN:
                snake.turn("UP")
            elif event.key in (pygame.K_DOWN, pygame.K_s) and snake.y_movement != UP:
                snake.turn("DOWN")
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def events_final_check(snake: Snake, food: Food):
    """
    Function checking pygame events in the final screen
    :param snake: object representing snake
    :param food: object representing food
    :return: bool value
    """
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                snake.reset(0)
                food.reset(snake)
                return False
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
    return True


def starting_screen(screen: Screen):
    """
    Function managing the starting screen
    :param screen: object representing the screen
    """
    screen.draw_start_screen()
    starting = True
    while starting:
        starting = starting_events_check(screen)


def game_screen(screen, snake, food):
    """
    Function managing the game screen
    :param screen: object representing the screen
    :param snake: object representing the snake
    :param food: object representing the food
    """
    while True:
        game_events_check(snake)
        snake.move()
        if snake.collision_check():
            break
        food.eaten_check(snake)
        screen.draw_game_screen(snake, food)
        clock.tick(snake.speed)


def final_screen(screen, snake, food):
    """
    Function managing the final screen
    :param screen: object representing the screen
    :param snake: object representing the snake
    :param food: object representing the food
    """
    screen.draw_final_screen(snake)
    final = True
    while final:
        final = events_final_check(snake, food)
