import unittest
import gameplay
from gamedata import *


class SnakeTest(unittest.TestCase):
    def setUp(self):
        self.snake = gameplay.Snake()

    def test_grow(self):
        self.snake.grow()
        self.assertEqual(self.snake.length, 2)

    def test_turn(self):
        self.snake.turn("DOWN")
        self.assertEqual([self.snake.x_movement, self.snake.y_movement], [STOP, DOWN])

    def test_collision(self):
        self.snake.x, self.snake.y = 100, 100
        self.assertTrue(self.snake.collision_check())


class FoodTest(unittest.TestCase):
    def setUp(self):
        self.coordinates = [100, 97]

    def test_button(self):
        self.assertFalse(gameplay.button(self.coordinates, START_BUTTON))
