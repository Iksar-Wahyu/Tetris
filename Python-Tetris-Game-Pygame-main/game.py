from grid import Grid
from blocks import *
import random
import pygame

class BaseGame:
    def __init__(self):
        self.score = 0
        self.game_over = False

    def update_score(self, lines_cleared, move_down_points):
        raise NotImplementedError("Subclasses must implement this method")

    def reset(self):
        raise NotImplementedError("Subclasses must implement this method")

    def draw(self, screen):
        raise NotImplementedError("Subclasses must implement this method")

class TetrisGame(BaseGame): #Encapsulation
    def __init__(self):
        super().__init__()
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(),
                       SBlock(), TBlock(), ZBlock()]
        self.current_block = self._get_random_block()
        self.next_block = self._get_random_block()
        self.rotate_sound = pygame.mixer.Sound("Sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("Sounds/clear.ogg")
        self.score = 0
        pygame.mixer.music.load("Sounds/background.mp3")
        pygame.mixer.music.play(-1)

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points

    def _get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(),
                           SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if not self._block_inside() or not self._block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self._block_inside() or not self._block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self._block_inside() or not self._block_fits():
            self.current_block.move(-1, 0)
            self._lock_block()

    def fall_down(self):
        while True:
            self.current_block.move(1, 0)
            if not self._block_inside() or not self._block_fits():
                self.current_block.move(-1, 0)
                self._lock_block()
                break

    def _lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self._get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if not self._block_fits():
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(),
                       SBlock(), TBlock(), ZBlock()]
        self.current_block = self._get_random_block()
        self.next_block = self._get_random_block()
        self.score = 0
        self.game_over = False

    def _block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if not self._block_inside() or not self._block_fits():
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.play()

    def _block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True
    
    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        next_block_x, next_block_y = 270, 270
        if self.next_block.id == 3:
            next_block_x, next_block_y = 255, 290
        elif self.next_block.id == 4:
            next_block_x, next_block_y = 255, 280
        self.next_block.draw(screen, next_block_x, next_block_y)

# Polymorphic usage example
class GameManager:
    def __init__(self, game_type):
        self.game = game_type

    def reset_game(self):
        self.game.reset()

    def play_move(self, move):
        if move == "left":
            self.game.move_left()
        elif move == "right":
            self.game.move_right()
        elif move == "down":
            self.game.move_down()
        elif move == "rotate":
            self.game.rotate()

    def draw(self, screen):
        self.game.draw(screen)

    def is_game_over(self):
        return self.game.game_over
