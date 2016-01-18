#!/usr/bin/env python

from multiprocessing import Process
import pygame
from pygame.locals import (QUIT, KEYUP, MOUSEBUTTONUP)
# import getch

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

APP_QUIT = 'Q'
APP_ESCAPE = '\x1b'
FPS = 30
SPACING = 20
PADDING = 10

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


# def runGameSameProcess(game_key):
#     global GAMES
#
#     for keys, fn, desc in GAMES:
#         if game_key in keys and fn is not None:
#             fn()
#             break


def runGameExternalProcess(game_key):
    global GAMES

    for keys, fn, desc in GAMES:
        if game_key in keys and fn is not None:
            p = Process(target=fn)  # , args=('bob',))
            p.start()
            p.join()
            break


def getTextRect(txt, font):
    global BLACK

    return font.render("{0}".format(txt), 1, BLACK).get_rect()


def getMaxTextSize(font):
    global GAMES

    h = 0
    w = 0
    for txt in GAMES:
        rect = getTextRect(txt, font)
        if rect.height > h:
            h = rect.height
        if rect.width > w:
            w = rect.width

    return w, h


def drawText(txt, color, left, top, font):
    global DISPLAYSURF

    textImg = font.render("{0}".format(txt), 1, color)
    textRect = textImg.get_rect()
    textRect.left = left
    textRect.top = top
    DISPLAYSURF.blit(textImg, textRect)


def getButtonRect(col, row):
    global SPACING, BTN_WIDTH, BTN_HEIGHT, TOPMARGIN

    x = SPACING + col * (BTN_WIDTH + SPACING)
    y = TOPMARGIN + SPACING + row * (BTN_HEIGHT + SPACING)

    return pygame.Rect(x, y, BTN_WIDTH, BTN_HEIGHT)


def drawButton(txt, col, row, txt_color, btn_fill_color, btn_border_color,
               font):

    btn_rect = getButtonRect(col, row)
    border = pygame.Rect(btn_rect.left - 2, btn_rect.top - 2,
                         btn_rect.width + 4, btn_rect.height + 4)
    pygame.draw.rect(DISPLAYSURF, btn_fill_color, btn_rect)
    pygame.draw.rect(DISPLAYSURF, btn_border_color, border, 2)
    txt_rect = getTextRect(txt, font)
    drawText(txt,
             txt_color,
             btn_rect.left + (btn_rect.width - txt_rect.width) // 2,
             btn_rect.top + (btn_rect.height - txt_rect.height) // 2,
             font)


def showGamesGUI(font):
    global GAMES, SPACING, PADDING, BTN_WIDTH, BTN_HEIGHT, \
        WINDOWHEIGHT, WINDOWWIDTH, COLS

    txt_width, txt_height = getMaxTextSize(font)
    BTN_WIDTH = txt_width + (PADDING * 2)
    BTN_HEIGHT = txt_height + (PADDING * 2)

    COLS = (WINDOWWIDTH - SPACING) // (BTN_WIDTH + SPACING)

    for idx, game in enumerate(GAMES):
        row, col = divmod(idx, COLS)
        drawButton("{0} - {1}".format("/".join(game[0]), game[-1]),
                   col, row, BLACK, LIGHTBLUE, WHITE, font)


def getButtonAt(x, y):
    global COLS

    for idx, game in enumerate(GAMES):
        row, col = divmod(idx, COLS)
        rect = getButtonRect(col, row)
        if rect.collidepoint(x, y):
            return game[0][0]

    return None


def getInputGUI():
    global GAMES

    keys = []
    for a in map(lambda x: x[0], GAMES):
        keys.extend(a)
    keys = map(lambda s: s.upper() if s is not 'ESC' else APP_ESCAPE, keys)

    # event handling loop
    for event in pygame.event.get((KEYUP, MOUSEBUTTONUP, QUIT)):
        if (event.type == QUIT):
            return APP_QUIT
        elif (event.type == KEYUP):
            if chr(event.key).upper() in keys:
                return chr(event.key).upper()
        else:  # type is MOUSEBUTTONUP
            mousex, mousey = event.pos
            # check if a button was clicked
            btn = getButtonAt(mousex, mousey)
            if btn is not None:
                if btn is 'ESC':
                    return APP_ESCAPE
                else:
                    return btn
    return None


def runLauncherGUI():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, TITLEFONT, GAMES, BLUE, \
        WINDOWHEIGHT, WINDOWWIDTH, TOPMARGIN

    try:
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        WINDOWHEIGHT = DISPLAYSURF.get_height()
        WINDOWWIDTH = DISPLAYSURF.get_width()
        title = 'Python Games Launcher'
        pygame.display.set_caption(title)

        BASICFONT = pygame.font.Font(pygame.font.get_default_font(), 18)

        TITLEFONT = pygame.font.Font(pygame.font.get_default_font(), 72)
        titleRect = getTextRect(title, TITLEFONT)
        titleRect.top = 20
        titleRect.left = (WINDOWWIDTH - titleRect.width) // 2
        TOPMARGIN = titleRect.height + 40

        pygame.event.set_allowed([KEYUP, MOUSEBUTTONUP, QUIT])

        while True:  # main game loop
            # Draw the screen.
            DISPLAYSURF.fill(BLUE)

            drawText(title, LIGHTBLUE, titleRect.left, titleRect.top,
                     TITLEFONT)

            showGamesGUI(BASICFONT)

            from_user = getInputGUI()
            if from_user is not None:
                # respond to events
                if (from_user == APP_QUIT) or (from_user == APP_ESCAPE):
                    return
                else:
                    DISPLAYSURF = pygame.display.set_mode((200, 200))
                    pygame.display.flip()
                    runGameExternalProcess(from_user)
                    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,
                                                           WINDOWHEIGHT),
                                                          pygame.FULLSCREEN)
                    pygame.display.flip()
                    pygame.event.clear()
                    pygame.event.set_allowed([KEYUP, MOUSEBUTTONUP, QUIT])

            pygame.display.update()
            FPSCLOCK.tick(FPS)
    finally:
        pygame.quit()


# def getGameConsole():
#     global GAMES
#
#     keys = []
#     for a in map(lambda x: x[0], GAMES):
#         keys.extend(a)
#     keys = map(lambda s: s.upper() if s is not 'ESC' else APP_ESCAPE, keys)
#
#     x = None
#     while x is None:
#         print('Enter a number: ')
#         key = getch.getch().upper()
#         if key in keys:
#             x = key
#
#     return x
#
#
# def showGamesConsole():
#     global GAMES
#
#     for keys, fn, desc in GAMES:
#         print("{0} - {1}".format("/".join(keys), desc))
#
#
# def runLauncherConsole():
#     while True:
#         showGamesConsole()
#         game = getGameConsole()
#         if game == APP_QUIT or game == APP_ESCAPE:  # q or ESC
#             return
#         runGameExternalProcess(game)


if __name__ == '__main__':
    # runLauncherConsole()
    runLauncherGUI()
