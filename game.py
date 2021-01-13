import gameplay
import gamedata

if __name__ == '__main__':
    screen = gameplay.Screen(gamedata.SCREEN_WIDTH, gamedata.SCREEN_HEIGHT)
    snake = gameplay.Snake()
    food = gameplay.Food(snake)

    gameplay.starting_screen(screen)
    while True:
        gameplay.game_screen(screen, snake, food)
        gameplay.final_screen(screen, snake, food)
