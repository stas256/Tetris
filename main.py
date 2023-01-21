import pygame
import random
from copy import deepcopy

class Board:
    # creating board
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # default values
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # customisation the appearance
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        # vertical lines
        start = self.left
        end = self.top + self.height * self.cell_size
        for i in range(self.width + 1):
            pygame.draw.line(
                screen,
                (255, 255, 255),
                (start, self.top),
                (start, end),
                1
            )
            start += self.cell_size
        
        # horizontal lines
        start = self.top
        end = self.left + self.width * self.cell_size
        for i in range(self.height + 1):
            pygame.draw.line(
                screen,
                (255, 255, 255),
                (self.left, start),
                (end, start),
                1
            )
            start += self.cell_size


class Figure:
    def __init__(self, board, body):
        self.board = board
        self.base = deepcopy(body) # first values
        self.body = deepcopy(body) # changing values
        # moving to center
        for i in range(4):
            self.body[i][0] += 5
        self.color = random.randrange(1, 13)
    
    def render(self):
        for i in range(4):
            x = self.board.left + self.body[i][0] * self.board.cell_size
            y = self.board.top + self.body[i][1] * self.board.cell_size
            rect = (x, y, self.board.cell_size, self.board.cell_size)
            screen.fill(colors[self.color], rect)
    
    # rendering next figure next to the board
    def next_render(self):
        for i in range(4):
            x = self.board.left + (self.body[i][0] + 9) * self.board.cell_size
            y = self.board.top + (self.body[i][1] + 4) * self.board.cell_size
            rect = (x, y, self.board.cell_size, self.board.cell_size)
            screen.fill(colors[self.color], rect)


def isInAir(board, figure):
    for i in range(4):
        x = figure.body[i][0]
        y = figure.body[i][1]
        if y >= board.height - 1:
            return False
        if board.board[y + 1][x] != 0:
            return False
    return True

def rightCheck(board, figure):
    for i in range(4):
        x = figure.body[i][0]
        y = figure.body[i][1]
        if x >= board.width - 1:
            return False
        if board.board[y][x + 1] != 0:
            return False
    return True

def leftCheck(board, figure):
    for i in range(4):
        x = figure.body[i][0]
        y = figure.body[i][1]
        if x <= 0:
            return False
        if board.board[y][x - 1] != 0:
            return False
    return True

def check(board, figure):
    for i in range(4):
        x = figure.body[i][0]
        y = figure.body[i][1]
        if x < 0 or x >= board.width:
            return False
        if board.board[y][x] != 0:
            return False
        if y >= board.height - 1:
            return False
        if board.board[y][x] != 0:
            return False
    return True

pygame.init()

size = (600, 650)
screen = pygame.display.set_mode(size)
board = Board(10, 20)
board.set_view(0, 0, 30)

score, lines = 0, 0
scores = {
    0: 0,
    1: 100, 
    2: 300,
    3: 700,
    4: 1500
}
colors = {
    1: pygame.Color(255, 255, 255),
    2: pygame.Color(0, 255, 255),
    3: pygame.Color(0, 0, 255),
    4: pygame.Color(255, 0, 255),
    5: pygame.Color(128, 0, 128),
    6: pygame.Color(0, 128, 0),
    7: pygame.Color(0, 255, 0),
    8: pygame.Color(128, 0, 0),
    9: pygame.Color(255, 0, 0),
    10: pygame.Color(255, 255, 0),
    11: pygame.Color(128, 128, 0),
    12: pygame.Color(0, 128, 128),
}
main_font = pygame.font.Font('font/font.ttf', 65)
font = pygame.font.Font('font/font.ttf', 45)

title = main_font.render("TETRIS", True, pygame.Color('darkorange'))
title_score = font.render("SCORE:", True, pygame.Color('white'))
gameOver = font.render("GAME OVER", True, pygame.Color('darkorange'))
title_restart = font.render("Restarting...:", True, pygame.Color('white'))

figures = [
    [[0, 0], [-1, 0], [1, 0], [2, 0]], # I
    [[0, 0], [-1, 0], [0, 1], [1, 1]], # S
    [[0, 0], [-1, 0], [-1, 1], [0, 1]], # O
    [[0, 0], [0, 1], [1, 1], [2, 1]], # L
    [[0, 0], [0, 1], [1, 0], [2, 0]], # J
    [[0, 0], [0, 1], [-1, 0], [1, 0]], # Z
    [[0, 0], [-1, 0], [0, 1], [1, 0]] # T 
    
]
figure = Figure(board, random.choice(figures))
next_figure = Figure(board, random.choice(figures))

anim_count = 0
anim_speed = 60
anim_a = 0.25
anim_limit = 2000

destroyed = False
clock = pygame.time.Clock()
running = True
isGame = True
after_game = 0
after_game_limit = 20000
while running:
    if isGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # move left
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    new = deepcopy(figure.body)
                    flag = True
                    for i in range(4):
                        new[i][0] -= 1
                        if leftCheck(board, figure):
                            figure.body = new
                # move right
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    new = deepcopy(figure.body)
                    flag = True
                    for i in range(4):
                        new[i][0] += 1
                        if rightCheck(board, figure):
                            figure.body = new
                elif event.key in [pygame.K_DOWN, pygame.K_s, pygame.K_SPACE]:
                    anim_limit = 100
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    center = figure.body[0]
                    old = deepcopy(figure.body)
                    for i in range(4):
                        x = figure.body[i][1] - center[1]
                        y = figure.body[i][0] - center[0]
                        figure.body[i][0] = center[0] - x
                        figure.body[i][1] = center[1] + y
                    if not check(board, figure):
                        figure.body = old
        # move down
        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            anim_speed += anim_a
            flag = True
            if not isInAir(board, figure):
                flag = False
                for i in range(4):
                    board.board[figure.body[i][1]][figure.body[i][0]] = figure.color
                anim_limit = 2000
                if check(board, next_figure):
                    figure = next_figure
                    next_figure = Figure(board, random.choice(figures))
                else:
                    isGame = False
            if flag:
                for i in range(4):
                    figure.body[i][1] += 1
        # destroy the line
        line = board.height - 1
        lines = 0
        for row in range(board.height - 1, -1, -1):    
            count = 0
            cell_in_line = len(board.board[0])
            for i in range(cell_in_line):
                if board.board[row][i]:
                    count += 1
                board.board[line][i] = board.board[row][i]
            if count < board.width:
                line -= 1
            else:
                anim_speed += anim_a
                lines += 1
        score += scores[lines]
        if lines != 0: print(lines, 'hm')
        # rendering static figures on the board
        screen.fill((0, 0, 0))
        board.render(screen)
        for line in range(len(board.board)):    
            for cell in range(len(board.board[0])):
                color = board.board[line][cell]
                if color != 0:
                    x = board.left + cell * board.cell_size
                    y = board.top + line * board.cell_size
                    rect = (x, y, board.cell_size, board.cell_size)
                    screen.fill(colors[color], rect)
        figure.render()
        next_figure.next_render()

        screen.blit(title, (325, -10))
        screen.blit(title_score, (325, 200))
        score_count = font.render(str(score), True, pygame.Color('white'))
        screen.blit(score_count, (325, 260))

        pygame.display.flip()
        clock.tick(60)
    else:
        if after_game < after_game_limit:
            after_game += 2
            screen.blit(gameOver, (325, 300))
            screen.blit(title_restart, (325, 360))
        else:
            anim_speed = 60
            score = 0
            board.board = [[0] * board.width for _ in range(board.height)]
            isGame = True