from settings import *
import pygame
import random

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tetris')

clock = pygame.time.Clock()

class Block:

    blocks = []

    def __init__(self):
        self.falling = True
        self.state = 0
        self.x = 4
        self.y = -1
        self.speed = 0
        block = random.randint(1, 7)

        # I
        if block == 1:
            self.states = [[4, 5, 6, 7], [2, 6, 10, 14], [8, 9, 10, 11], [1, 5, 9, 13]]
            self.color = LIGHT_BLUE

        # L
        elif block == 2:
            self.states = [[0, 4, 5, 6], [2, 1, 5, 9], [10, 6, 5, 4], [8, 9, 5, 1]]
            self.color = ORANGE

        # rL
        elif block == 3:
            self.states = [[2, 6, 5, 4], [10, 9, 5, 1], [8, 4, 5, 6], [0, 1, 5, 9]]
            self.color = BLUE

        # #
        elif block == 4:
            self.states = [[1, 2, 5, 6]]
            self.color = YELLOW

        # Z
        elif block == 5:
            self.states = [[0, 1, 5, 6], [2, 6, 5, 9], [4, 5, 9, 10], [1, 5, 4, 8]]
            self.color = RED

        # rZ
        elif block == 6:
            self.states = [[4, 5, 1, 2], [1, 5, 6, 10], [6, 5, 9, 8], [0, 4, 5, 9]]
            self.color = GREEN

        # T
        else:
            self.states = [[1, 4, 5, 6], [6, 1, 5, 9], [9, 6, 5, 4], [4, 9, 5, 1]]
            self.color = PURPLE

    def draw(self):
        if len(self.states):
            for state in self.states[self.state]:
                pygame.draw.rect(win, self.color, (((self.x + state % 4) * SQUARE_SIZE_X, (self.y + state // 4) * SQUARE_SIZE_Y), (SQUARE_SIZE_X, SQUARE_SIZE_Y)))

    def move_x(self, direction):
        self.speed += 1
        if self.speed >= BLOCK_SPEED:
            self.speed = 0
            self.x += direction
            for state in self.states[self.state]:
                for block in Block.blocks:
                    for state2 in block.states[block.state]:
                        if self.x + state % 4 == block.x + state2 % 4 and self.y + state // 4 == block.y + state2 // 4 and self != block:
                            self.x -= direction
                            return False
                if (self.x + state % 4) * SQUARE_SIZE_X < 0 or (self.x + state % 4) * SQUARE_SIZE_X >= WIDTH:
                    self.x -= direction
                    return False
            return True

    def rotate(self, direction):
        if direction > 0:
            if self.state >= len(self.states) - 1:
                self.state = 0
            else:
                self.state += direction
        if direction < 0:
            if self.state < 1:
                self.state = len(self.states) - 1
            else:
                self.state += direction
        for state in self.states[self.state]:
            for block in Block.blocks:
                for state2 in block.states[block.state]:
                    if self.x + state % 4 == block.x + state2 % 4 and self.y + state // 4 == block.y + state2 // 4 and self != block:
                        if self.state % 4 < 2:
                            if state % 4 == 1 or state % 4 == 2:
                                move = self.move_x(2)
                            else:
                                move = self.move_x(1)
                            if not move:
                                self.state -= direction
                                return
                        else:
                            move = self.move_x(-1)
                            if not move:
                                self.state -= direction
                                return
            if (self.x + state % 4) * SQUARE_SIZE_X < 0 or (self.x + state % 4) * SQUARE_SIZE_X >= WIDTH :
                        if self.state % 4 < 2:
                            if state % 4 == 1 or state % 4 == 2:
                                move = self.move_x(2)
                            else:
                                move = self.move_x(1)
                            if not move:
                                self.state -= direction
                                return
                        else:
                            move = self.move_x(-1)
                            if not move:
                                self.state -= direction
                                return

    def touch(self):
        pass

    def fall(self):
        if self.falling:
            self.y += 1 
            for state in self.states[self.state]:
                for block in Block.blocks:
                    for state2 in block.states[block.state]:
                        if (self.x + state % 4) == (block.x + state2 % 4) and (self.y + state // 4) == (block.y + state2 // 4) and self != block:
                            self.attach()
                            return
                if (self.y + state // 4) * SQUARE_SIZE_Y >= HEIGHT:
                    self.attach()
                    return

    def attach(self):
        self.y -= 1
        self.falling = False
        Block.blocks.append(Block())


def loss():
    for block in Block.blocks:
        if not block.falling:
            for state in block.states[block.state]:
                if (block.y + state // 4) * SQUARE_SIZE_Y <= 0:
                    return True
    return False

def clear_lines():
    for i in range(20):
        squares = 0
        for block in Block.blocks:
            if not block.falling:
                for state in block.states[block.state]:
                    if block.y + state // 4 == i:
                        squares += 1

        if squares >= 10:
            for block in Block.blocks:
                if not block.falling:
                    for state in list(block.states[block.state]):
                        if block.y + state // 4 == i:
                            block.states[block.state].remove(state)
                        elif block.y + state // 4 < i:
                            block.states[block.state][block.states[block.state].index(state)] += 4

def update_display():

    win.fill(BLACK)

    for block in Block.blocks:
        block.draw()

    pygame.display.update()

interrupted = False

Block.blocks.append(Block())
fall = 0
buttons = [False] * 3

while not interrupted:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            interrupted = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                buttons[0] = True
            if event.key == pygame.K_LEFT:
                buttons[1] = True
            if event.key == pygame.K_DOWN:
                buttons[2] = True
            if event.key == pygame.K_UP:
                Block.blocks[len(Block.blocks) - 1].rotate(1)
            if event.key == pygame.K_z:
                Block.blocks[len(Block.blocks) - 1].rotate(-1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                buttons[0] = False
            if event.key == pygame.K_LEFT:
                buttons[1] = False
            if event.key == pygame.K_DOWN:
                buttons[2] = False
    
    if buttons[0]:
        Block.blocks[len(Block.blocks) - 1].move_x(1)
    if buttons[1]:
        Block.blocks[len(Block.blocks) - 1].move_x(-1)

    if buttons[2]:
        fall += 3
    else:
        fall += 1
    if fall >= GAME_SPEED:
        fall = 0
        Block.blocks[len(Block.blocks) - 1].fall()
    clear_lines()
    if not interrupted:
        interrupted = loss()

    update_display()

pygame.quit()
