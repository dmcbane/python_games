#!/usr/bin/env python

from multiprocessing import Process
import pygame
from pygame.locals import (QUIT, KEYUP, K_ESCAPE, MOUSEBUTTONUP, K_q)
import getch

import flippy
import fourinarow
import gemgem
import inkspill
import marcelmemory
import pentomino
import simulate
import slidepuzzle
import squirrel
import starpusher
import tetromino
import tetrominoforidiots
import wormy

# [[keys to press for button], function to execute, "Label for button"]
GAMES = [[["1"], gemgem.main, "Like Bejeweled"],
         [["2"], fourinarow.main, "Like Connect Four"],
         [["3"], inkspill.main, "Like Flood-It!"],
         [["4"], flippy.main, "Like Reversi"],
         [["5"], simulate.main, "Like Simon"],
         [["6"], wormy.main, "Like Snake"],
         [["7"], starpusher.main, "Like Sokoban"],
         [["8"], tetromino.main, "Like Tetris"],
         [["9"], tetrominoforidiots.main, "Tetris for Idiots"],
         [["A"], pentomino.main, "5 block Tetris"],
         [["B"], squirrel.main, "Eat the smaller squirrels"],
         [["C"], marcelmemory.main, "Memory puzzle"],
         [["D"], slidepuzzle.main, "Traditional slide puzzle"],
         [["ESC", "Q"], None, "Quit"]]

APP_QUIT = 'quit'
FPS = 30
SPACING = 10
PADDING = 5

# R, G, B
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
RED = (173, 82, 74)
CYAN = (115, 247, 247)
PURPLE = (189, 107, 189)
GREEN = (115, 231, 115)
BLUE = (24, 16, 144)
YELLOW = 255, 255, 123
ORANGE = (200, 142, 47)
BROWN = (132, 99, 57)
LIGHTRED = (255, 156, 156)
DARKGRAY = (123, 123, 123)
GRAY = (148, 148, 148)
LIGHTGREEN = (165, 255, 165)
LIGHTBLUE = (156, 156, 247)
LIGHTGRAY = (206, 206, 206)


def getTextRect(txt):
    global BASICFONT, BLACK

    return BASICFONT.render("{0}".format(txt), 1, BLACK).get_rect()


def getMaxTextSize():
    global GAMES

    h = 0
    w = 0
    for txt in GAMES:
        rect = getTextRect(txt)
        if rect.height > h:
            h = rect.height
        if rect.width > w:
            w = rect.width

    return w, h


def drawText(txt, color, left, top):
    global BASICFONT, DISPLAYSURF

    textImg = BASICFONT.render("{0}".format(txt), 1, color)
    textRect = textImg.get_rect()
    textRect.left = left
    textRect.top = top
    DISPLAYSURF.blit(textImg, textRect)


def getButtonRect(col, row):
    global SPACING, BTN_WIDTH, BTN_HEIGHT

    x = SPACING + col * (BTN_WIDTH + SPACING)
    y = SPACING + row * (BTN_HEIGHT + SPACING)

    return pygame.Rect(x, y, BTN_WIDTH, BTN_HEIGHT)


def drawButton(txt, col, row, txt_color, btn_fill_color, btn_border_color):

    btn_rect = getButtonRect(col, row)
    border = pygame.Rect(btn_rect.left - 2, btn_rect.top - 2,
                         btn_rect.width + 4, btn_rect.height + 4)
    pygame.draw.rect(DISPLAYSURF, btn_fill_color, btn_rect)
    pygame.draw.rect(DISPLAYSURF, btn_border_color, border, 2)
    txt_rect = getTextRect(txt)
    drawText(txt,
             txt_color,
             btn_rect.left + (btn_rect.width - txt_rect.width) // 2,
             btn_rect.top + (btn_rect.height - txt_rect.height) // 2)


def showGamesGUI():
    global GAMES, SPACING, PADDING, BTN_WIDTH, BTN_HEIGHT, \
        WINDOWHEIGHT, WINDOWWIDTH

    txt_width, txt_height = getMaxTextSize()
    BTN_WIDTH = txt_width + (PADDING * 2)
    BTN_HEIGHT = txt_height + (PADDING * 2)

    cols = (WINDOWWIDTH - SPACING) // (BTN_WIDTH + SPACING)

    for idx, game in enumerate(GAMES):
        row, col = divmod(idx, cols)
        drawButton("{0} - {1}".format("/".join(game[0]), game[-1]),
                   col, row, BLACK, LIGHTBLUE, WHITE)


def getKeyboardInputGUI():
    for event in pygame.event.get((KEYUP)):  # event handling loop
        if (event.key == K_ESCAPE or event.key == K_q):
            return APP_QUIT
        else:
            try:
                key = int(event.unicode)
            except:
                key = None

            if (key is not None and key > 0 and key <= 9):
                number * 10 + key
    return None


def getMouseInputGUI():
    # event handling loop
    for event in pygame.event.get((QUIT, MOUSEBUTTONUP)):
        if (event.type == QUIT):
            return APP_QUIT
        else:  # type is MOUSEBUTTONUP
            mousex, mousey = event.pos
            # check if a button was clicked
            btn = getButtonAt(mousex, mousey)
            if btn is not None:
                return btn
    return None


def runLauncherGUI():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, GAMES, BLUE, WINDOWHEIGHT, \
        WINDOWWIDTH

    try:
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        WINDOWHEIGHT = DISPLAYSURF.get_height()
        WINDOWWIDTH = DISPLAYSURF.get_width()
        pygame.display.set_caption('Python Games Launcher')
        BASICFONT = pygame.font.Font(pygame.font.get_default_font(), 18)

        # Draw the screen.
        DISPLAYSURF.fill(BLUE)

        while True:  # main game loop
            showGamesGUI()

            from_user = [elem
                         for elem
                         in [getKeyboardInputGUI(), getMouseInputGUI()]
                         if elem is not None]
            for item in from_user:
                # respond to events
                if item is APP_QUIT:
                    return
                else:
                    runGameExternalProcess(item)

            pygame.display.update()
            FPSCLOCK.tick(FPS)
    finally:
        pygame.quit()


def runGameSameProcess(game_key):
    global GAMES

    for keys, fn, desc in GAMES:
        if game_key in keys and fn is not None:
            fn()
            break


def runGameExternalProcess(game_key):
    global GAMES

    for keys, fn, desc in GAMES:
        if game_key in keys and fn is not None:
            p = Process(target=fn)  # , args=('bob',))
            p.start()
            p.join()
            break


def getGame():
    global GAMES

    keys = []
    for a in map(lambda x: x[0], GAMES):
        keys.extend(a)
    keys = map(lambda s: s.upper() if s is not 'ESC' else '\x1b', keys)

    x = None
    while x is None:
        print 'Enter a number: '
        key = getch.getch().upper()
        if key in keys:
            x = key

    return x


def showGames():
    global GAMES

    for keys, fn, desc in GAMES:
        print "{0} - {1}".format("/".join(keys), desc)


def launch():
    while True:
        showGames()
        game = getGame()
        if game == 'Q' or game == '\x1b':  # q or ESC
            return
        runGameExternalProcess(game)


if __name__ == '__main__':
    # launch()
    runLauncherGUI()
