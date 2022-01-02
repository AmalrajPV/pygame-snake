import pygame
import sys
import os
from pygame.locals import *
from random import randint
import shelve


# initialization
pygame.init()
pygame.font.init()
FONT = pygame.font.Font('freesansbold.ttf', 32)


class Block(object):
    def __init__(self, surface, position:tuple, size:int=25, color:tuple=(0, 0, 255)):
        self.color = color
        self.surface = surface
        self.block = pygame.Rect(position[0], position[1], size, size)
    

    def move(self, position):
        self.block.x = position[0]
        self.block.y = position[1]


    def draw(self, img=None,  pic=False):
        if pic:
            # pygame.draw.ellipse(self.surface, self.color, self.block)
            self.surface.blit(img, self.block)
        else:
            pygame.draw.rect(self.surface, self.color, self.block)

    def pos(self):
        return self.block.x, self.block.y


class Food:
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1)
    try:
        food_tone = pygame.mixer.Sound(os.path.join('ASSETS/AUDIO', 'food.wav'))
        PIC = pygame.image.load(os.path.join('ASSETS/IMAGES', 'download.png'))
        PIC = pygame.transform.scale(PIC, (25, 25))


    except FileNotFoundError:
        pass
    def __init__(self, surface, color, x_range:tuple, y_range:tuple, size=25):
        self.x_range = x_range
        self.y_range = y_range
        self.size =size
        pos = (
            randint((self.x_range[0]//self.size), (self.x_range[1]//self.size))*self.size, 
            randint((self.y_range[0]//self.size), (self.y_range[1]//self.size))*self.size
            )
        self.food = Block(surface, pos, color=color)


    def draw(self):
        self.food.draw(self.PIC, pic=True)

    def eat(self):
        pos = (
            randint((self.x_range[0]//self.size), (self.x_range[1]//self.size))*self.size, 
            randint((self.y_range[0]//self.size), (self.y_range[1]//self.size))*self.size
            )
        try:
            pygame.mixer.Sound.play(self.food_tone)
        except AttributeError:
            pass
        self.food.move(pos)


class Snake(object):
    body = []
    def __init__(self,surface, start:tuple):
        self.surface = surface
        self.pos = start
        head = Block(surface, self.pos, color=(58, 156, 64))
        self.body.append(head)


    def draw(self):
        for part in self.body:
            part.draw()

    def move(self, direction:tuple):
        if direction == (-1, 0):    # left
            self.pos = (self.pos[0] - 25, self.pos[1])
        
        elif direction == (1, 0):    # right
            self.pos = (self.pos[0] + 25, self.pos[1])
        
        if direction == (0, 1):    # down
            self.pos = (self.pos[0], self.pos[1] + 25)
        
        if direction == (0, -1):    # up
            self.pos = (self.pos[0], self.pos[1] - 25)
        
        for i in range(len(self.body)-1, 0, -1):
            self.body[i].move((self.body[i-1].pos()[0], self.body[i-1].pos()[1]))
        self.body[0].move(self.pos)

        
    def grow(self):
        if len(self.body) % 2 == 0:
            self.body.append(Block(self.surface, self.pos, color=(58, 156, 64)))
        else:
            self.body.append(Block(self.surface, self.pos, color=(0, 200, 0)))



    def self_collision(self):
        for i in range(1, len(self.body)):
            if self.body[0].pos() == self.body[i].pos():
                return True

    def borderCollision(self, boundary):    # boundary = (left, right, up, down)
        x = self.body[0].pos()[0]
        y = self.body[0].pos()[1]
        if x < boundary[0] or x > boundary[1] or y < boundary[2] or y > boundary[3]:
            return True

def drawBoard(surface, start:tuple, width:int, height:int, color:tuple=(0, 0, 0), borderwidth=25, border=0):
    for i in range(start[0], start[0]+width+(borderwidth*2), borderwidth):
        for j in range(start[1], start[1]+height+(borderwidth*2), borderwidth):
            if i in range(start[0]+borderwidth, start[0]+width+borderwidth) and j in range(start[1]+borderwidth, start[1]+height+borderwidth):
                # pygame.draw.rect(surface, color, (i, j, borderwidth, borderwidth))
                continue
            else:   # border
                pygame.draw.rect(surface, color, (i, j, borderwidth, borderwidth))
                pygame.draw.rect(surface, (0, 0, 0), (i, j, borderwidth, borderwidth), border)


#game texts
def renderOthers(surface, score, highscore):
    TITLE = FONT.render('SNAKE', True, (0, 100, 0))
    try:
        TITLE_PIC = pygame.image.load(os.path.join('ASSETS/IMAGES', 'snake-title-pic.png'))
        TITLE_PIC = pygame.transform.scale(TITLE_PIC, (100, 100))
        surface.blit(TITLE_PIC, (120, 110))
    except FileNotFoundError:
        pass
    SCORE_TEXT = FONT.render(f'Score         : {score}', True, (0, 0, 0))
    HIGHSCORE_TEXT = FONT.render(f'High Score : {highscore}', True, (0, 0, 0))
    titleRect = TITLE.get_rect()
    titleRect.center = (170, 80)
    scoreRect = SCORE_TEXT.get_rect()
    scoreRect.center = (170, 350)
    highScoreRect = HIGHSCORE_TEXT.get_rect()
    highScoreRect.center = (170, 450)
    surface.blit(TITLE, titleRect)
    surface.blit(SCORE_TEXT, scoreRect)
    surface.blit(HIGHSCORE_TEXT, highScoreRect)


def main():
    
    # variables
    GAMEON = True
    FPS = 10
    WIDTH, HEIGHT = 1200, 600
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BRICK = (214, 105, 54)
    BLACK = (0, 0, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    STOP = (0, 0)
    DIRECTION = STOP
    BOARD_WIDTH, BOARD_HEIGHT = 800, 550
    BOARD_START = (350, 0)
    BOARD_CENTER = (BOARD_START[0]+(BOARD_WIDTH//2), BOARD_START[1]+(BOARD_HEIGHT//2))
    SCORE = 0
    HIGHSCORE = 0
    f = shelve.open('hs')
    try:
        HIGHSCORE = f['score']
    except KeyError:
        f['score'] = 0
    f.close()


    # setup
    ROOT = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    snake =Snake(ROOT, BOARD_CENTER)
    food = Food(ROOT, RED, x_range=(375, 1150), y_range=(25, 550))

    pygame.mixer.init()
    pygame.mixer.music.set_volume(1)
    try:
        bong = pygame.mixer.Sound(os.path.join('ASSETS/AUDIO', 'gameover.mp3'))
    except FileNotFoundError:
        pass

    while GAMEON:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and DIRECTION != RIGHT:
                    DIRECTION = LEFT
                elif event.key == pygame.K_RIGHT  and DIRECTION != LEFT:
                    DIRECTION = RIGHT
                elif event.key == pygame.K_UP  and DIRECTION != DOWN:
                    DIRECTION = UP
                elif event.key == pygame.K_DOWN and DIRECTION != UP:
                    DIRECTION = DOWN
                elif event.key == pygame.K_SPACE:
                    DIRECTION = STOP
        if snake.borderCollision((375, 1150, 25, 550)) or snake.self_collision():
            DIRECTION = (0, 0)
            try:
                pygame.mixer.Sound.play(bong)
            except UnboundLocalError:
                pass
            pygame.time.delay(2000)
            GAMEON = False

        if food.food.pos() == snake.body[0].pos():
            food.eat()
            snake.grow()
            SCORE += 1

        if SCORE > HIGHSCORE:
            HIGHSCORE = SCORE
            f = shelve.open('hs')
            f['score'] = HIGHSCORE
            f.close()

   
        ROOT.fill(WHITE)
        drawBoard(ROOT, BOARD_START, BOARD_WIDTH, BOARD_HEIGHT, color=BRICK, border=1)
        pygame.draw.rect(ROOT, (255, 219, 136), (BOARD_START[0]+25, BOARD_START[1]+25, BOARD_WIDTH, BOARD_START[1]+BOARD_HEIGHT))
        food.draw()
        snake.draw()
        snake.move(DIRECTION)
        renderOthers(ROOT, SCORE, HIGHSCORE)
        
        pygame.display.update()


if __name__ == '__main__':
    main()
