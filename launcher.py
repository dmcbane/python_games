#!/usr/bin/env python

import blankpygame
import catanimation
import flippy
import fourinarow
import gemgem
import inkspill
import marcelmemory
import memorypuzzle
import pentomino
import simulate
import slidepuzzle
import squirrel
import starpusher
import tetromino
import tetrominoforidiots
# import wordguess
import wormy

games = [[blankpygame.main, "Blank Game Template"],
         [catanimation.main, "Animation Example"],
         [gemgem.main, "A game like Bejeweled"],
         [fourinarow.main, "A game like Connect Four"],
         [flippy.main, "A game like Reversi"],
         [simulate.main, "A game like Simon"],
         [wormy.main, "A game like Snake"],
         [starpusher.main, "A game like Sokoban"],
         [tetromino.main, "A game like Tetris"],
         [tetrominoforidiots.main, "Tetris for Idiots"],
         [pentomino.main, "5 block Tetris"],
         [squirrel.main, "Eat the smaller squirrels"],
         [inkspill.main, "Flood the screen with pixels"],
         [memorypuzzle.main, "Large memory puzzle"],
         [marcelmemory.main, "Memory puzzle with Marcel settings"],
         [slidepuzzle.main, "Traditional slide puzzle"]]  # ,
# [wordguess.main, "New word game"]]


def showGames():
    global games

    i = 1
    for fn, desc in games:
        print str(i) + ' - ' + desc
        i += 1
    print 'q - Quit'


def getGame():
    global games

    x = None
    while x is None:
        try:
            raw = raw_input('Enter a number: ')
            if raw == 'q' or raw == 'Q':
                return -1
            x = int(raw)
            if x < 1 or x > len(games):
                x = None
        except ValueError:
            print "Invalid Number!"
            showGames()

    return (x - 1)


def runGame(ndx):
    global games

    fn, desc = games[ndx]
    fn()


def launch():
    while True:
        showGames()
        game = getGame()
        if game < 0:
            return
        runGame(game)


if __name__ == '__main__':
    launch()
