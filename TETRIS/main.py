import pygame
from copy import deepcopy
from random import choice, randrange
from shapes import figures

# Constants
W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 750, 940
FPS = 60

class Figure:
    def __init__(self, figures):
        self.figures = figures
        self.reset()

    def reset(self):
        self.blocks = deepcopy(choice(self.figures))
        self.color = self.generate_color()
        self.next_blocks = deepcopy(choice(self.figures))
        self.next_color = self.generate_color()

    @staticmethod
    def generate_color():
        return randrange(30, 256), randrange(30, 256), randrange(30, 256)

    def rotate(self):
        center = self.blocks[0]
        rotated_blocks = deepcopy(self.blocks)
        for i in range(4):
            x = self.blocks[i].y - center.y
            y = self.blocks[i].x - center.x
            rotated_blocks[i].x = center.x - x
            rotated_blocks[i].y = center.y + y
        return rotated_blocks

    def update_position(self, dx, dy):
        for block in self.blocks:
            block.x += dx
            block.y += dy

class Board:
    def __init__(self):
        self.grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]
        self.field = [[0 for _ in range(W)] for _ in range(H)]

    def is_valid_position(self, figure_blocks):
        for block in figure_blocks:
            if block.x < 0 or block.x >= W or block.y >= H or (block.y >= 0 and self.field[block.y][block.x]):
                return False
        return True

    def place_figure(self, figure_blocks, color):
        for block in figure_blocks:
            self.field[block.y][block.x] = color

    def clear_lines(self):
        lines_cleared = 0
        for row in range(H - 1, -1, -1):
            if all(self.field[row]):
                lines_cleared += 1
                for y in range(row, 0, -1):
                    self.field[y] = self.field[y - 1][:]
                self.field[0] = [0 for _ in range(W)]
        return lines_cleared

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.game_screen = pygame.Surface(GAME_RES)
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.figure = Figure(figures)
        self.score = 0
        self.record = self.get_record()
        self.anim_speed, self.anim_limit = 60, 2000
        self.anim_count = 0

        # Load assets
        self.bg = pygame.image.load('img/bg.jpg').convert()
        self.game_bg = pygame.image.load('img/bg2.jpg').convert()
        self.main_font = pygame.font.Font('font/font.ttf', 65)
        self.font = pygame.font.Font('font/font.ttf', 45)
        self.title_tetris = self.main_font.render('TETRIS', True, pygame.Color('darkorange'))
        self.title_score = self.font.render('score:', True, pygame.Color('green'))
        self.title_record = self.font.render('record:', True, pygame.Color('purple'))

    def get_record(self):
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')
            return '0'

    def set_record(self):
        new_record = max(int(self.record), self.score)
        with open('record', 'w') as f:
            f.write(str(new_record))

    def check_events(self):
        dx, rotate = 0, False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.set_record()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    self.anim_limit = 100
                elif event.key == pygame.K_UP:
                    rotate = True
        return dx, rotate

    def run(self):
        while True:
            dx, rotate = self.check_events()
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.game_screen, (20, 20))
            self.game_screen.blit(self.game_bg, (0, 0))

            # Move figure horizontally
            self.figure.update_position(dx, 0)
            if not self.board.is_valid_position(self.figure.blocks):
                self.figure.update_position(-dx, 0)

            # Rotate figure
            if rotate:
                rotated_blocks = self.figure.rotate()
                if self.board.is_valid_position(rotated_blocks):
                    self.figure.blocks = rotated_blocks

            # Move figure down (gravity)
            self.anim_count += self.anim_speed
            if self.anim_count > self.anim_limit:
                self.anim_count = 0
                self.figure.update_position(0, 1)
                if not self.board.is_valid_position(self.figure.blocks):
                    self.figure.update_position(0, -1)
                    self.board.place_figure(self.figure.blocks, self.figure.color)
                    self.figure.reset()
                    lines_cleared = self.board.clear_lines()
                    self.score += {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}[lines_cleared]
                    self.anim_limit = 2000

            # Draw grid
            [pygame.draw.rect(self.game_screen, (40, 40, 40), rect, 1) for rect in self.board.grid]

            # Draw figure
            for block in self.figure.blocks:
                pygame.draw.rect(self.game_screen, self.figure.color,
                                 pygame.Rect(block.x * TILE, block.y * TILE, TILE - 2, TILE - 2))

            # Draw field
            for y, row in enumerate(self.board.field):
                for x, col in enumerate(row):
                    if col:
                        pygame.draw.rect(self.game_screen, col,
                                         pygame.Rect(x * TILE, y * TILE, TILE - 2, TILE - 2))

            # Draw next figure
            for block in self.figure.next_blocks:
                pygame.draw.rect(self.screen, self.figure.next_color,
                                 pygame.Rect(block.x * TILE + 380, block.y * TILE + 185, TILE - 2, TILE - 2))

            # Draw titles and score
            self.screen.blit(self.title_tetris, (485, -10))
            self.screen.blit(self.title_score, (535, 780))
            self.screen.blit(self.font.render(str(self.score), True, pygame.Color('white')), (550, 840))
            self.screen.blit(self.title_record, (525, 650))
            self.screen.blit(self.font.render(self.record, True, pygame.Color('gold')), (550, 710))

            # Check game over
            if any(self.board.field[0]):
                self.set_record()
                self.__init__()  # Restart the game

            pygame.display.flip()
            self.clock.tick(FPS)
if __name__ == "__main__":
    game = Game()
    game.run()
