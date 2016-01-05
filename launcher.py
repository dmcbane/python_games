#!/usr/bin/env python

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
import wordguess
import wormy

games = [[flippy.main, "A game like Reversi"],
         [fourinarow.main, "A game like Connect Four"],
         [gemgem.main, "A game like Bejeweled"],
         [starpusher.main, "A game like Sokoban"],
         [simulate.main, "A game like Simon"],
         [wormy.main, "A game like Snake"],
         [tetromino.main, "A game like Tetris"],
         [tetrominoforidiots.main, "Tetris for Idiots"],
         [pentomino.main, "5 block Tetris"],
         [inkspill.main, "Flood the screen with pixels"],
         [memorypuzzle.main, "Large memory puzzle"],
         [marcelmemory.main, "Memory puzzle with Marcel settings"],
         [slidepuzzle.main, "Traditional slide puzzle"],
         [squirrel.main, "Eat the smaller squirrels"],
         [wordguess.main, "New word game"]]


def showGames():
    global games

    i = 1
    for fn, desc in games:
        print str(i) + ' - ' + desc
        i += 1


def getGame():
    global games

    x = None
    while x is None:
        try:
            x = int(raw_input('Enter a number: '))
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
    showGames()
    runGame(getGame())


if __name__ == '__main__':
    launch()
