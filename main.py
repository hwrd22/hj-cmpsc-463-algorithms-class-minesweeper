# Howard Jiang
# CMPSC 463
# Final Project
import tkinter
import tkinter.ttk

import pygame
import random
import sys
import time
import copy
from tkinter import *
from tkinter import messagebox

# List of colors for number use.
colorList = ((0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 0, 128), (175, 0, 0), (0, 255, 255), (0, 0, 0), (128, 128, 128))
bonus = (1000, 5000, 10000)
difficulty = -1
minesweeper_grid = []
adjacent_bombs = []
bomb_counts = (10, 40, 99)
grid_sizes = ((10, 10), (16, 16), (16, 30))


class Cell:
    def __init__(self, mine):
        self.clicked = False
        self.mine = mine
        self.marked = False


def setup(option):
    global minesweeper_grid
    global adjacent_bombs
    global difficulty
    difficulty = option
    global bomb_counts
    global grid_sizes
    # 16 x 30 grid, 99 bombs
    remaining_bombs = bomb_counts[option]
    if option == 0:
        minesweeper_grid = [[], [], [], [], [], [], [], [], [], []]
        adjacent_bombs = [[], [], [], [], [], [], [], [], [], []]
    else:
        minesweeper_grid = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
        adjacent_bombs = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    for each in minesweeper_grid:
        while len(each) < grid_sizes[option][1]:
            each.append(0)
    while remaining_bombs > 0:
        for y in range(grid_sizes[option][0]):
            for x in range(grid_sizes[option][1]):
                if minesweeper_grid[y][x] == 0:
                    chance = random.randint(0, grid_sizes[option][0] * grid_sizes[option][1])
                    if chance == random.randint(0, grid_sizes[option][0] * grid_sizes[option][1]):
                        minesweeper_grid[y][x] = 1
                        remaining_bombs -= 1
                        if remaining_bombs == 0:
                            break
            if remaining_bombs == 0:
                break

    for row in range(len(adjacent_bombs)):
        for col in range(len(minesweeper_grid[row])):
            if minesweeper_grid[row][col] == 1:
                adjacent_bombs[row].append(-1)
            else:
                adjacents = 0
                if row == 0:
                    if col == 0:
                        if minesweeper_grid[0][1] == 1:
                            adjacents += 1
                        if minesweeper_grid[1][0] == 1:
                            adjacents += 1
                        if minesweeper_grid[1][1] == 1:
                            adjacents += 1
                        adjacent_bombs[row].append(adjacents)
                    elif col + 1 == len(minesweeper_grid[row]):
                        if minesweeper_grid[0][col - 1] == 1:
                            adjacents += 1
                        if minesweeper_grid[1][col] == 1:
                            adjacents += 1
                        if minesweeper_grid[1][col - 1] == 1:
                            adjacents += 1
                        adjacent_bombs[row].append(adjacents)
                    else:
                        if minesweeper_grid[row][col - 1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row][col + 1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row + 1][col - 1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row + 1][col] == 1:
                            adjacents += 1
                        if minesweeper_grid[row + 1][col + 1] == 1:
                            adjacents += 1
                        adjacent_bombs[row].append(adjacents)
                elif row + 1 == len(adjacent_bombs):
                    if col == 0:
                        if minesweeper_grid[row][1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row - 1][0] == 1:
                            adjacents += 1
                        if minesweeper_grid[row - 1][1] == 1:
                            adjacents += 1
                        adjacent_bombs[row].append(adjacents)
                    elif col + 1 == len(minesweeper_grid[row]):
                        if minesweeper_grid[row][col - 1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row - 1][col] == 1:
                            adjacents += 1
                        if minesweeper_grid[row - 1][col - 1] == 1:
                            adjacents += 1
                        adjacent_bombs[row].append(adjacents)
                    else:
                        if minesweeper_grid[row][col - 1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row][col + 1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row - 1][col - 1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row - 1][col] == 1:
                            adjacents += 1
                        if minesweeper_grid[row - 1][col + 1] == 1:
                            adjacents += 1
                        adjacent_bombs[row].append(adjacents)
                else:
                    if col == 0:
                        if minesweeper_grid[row - 1][0] == 1:
                            adjacents += 1
                        if minesweeper_grid[row - 1][1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row][1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row + 1][0] == 1:
                            adjacents += 1
                        if minesweeper_grid[row + 1][1] == 1:
                            adjacents += 1
                        adjacent_bombs[row].append(adjacents)
                    elif col + 1 == len(minesweeper_grid[row]):
                        if minesweeper_grid[row - 1][col] == 1:
                            adjacents += 1
                        if minesweeper_grid[row - 1][col - 1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row][col - 1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row + 1][col] == 1:
                            adjacents += 1
                        if minesweeper_grid[row + 1][col - 1] == 1:
                            adjacents += 1
                        adjacent_bombs[row].append(adjacents)
                    else:
                        if minesweeper_grid[row - 1][col - 1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row - 1][col] == 1:
                            adjacents += 1
                        if minesweeper_grid[row - 1][col + 1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row][col - 1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row][col + 1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row + 1][col - 1] == 1:
                            adjacents += 1
                        if minesweeper_grid[row + 1][col] == 1:
                            adjacents += 1
                        if minesweeper_grid[row + 1][col + 1] == 1:
                            adjacents += 1
                        adjacent_bombs[row].append(adjacents)
    menu.destroy()


menu = Tk()
menu.title("Minesweeper - Menu")
menu.minsize(215, 137)
menu.maxsize(215, 137)
label = tkinter.Label(menu, text="Select a difficulty level.")
label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
beginnerButton = tkinter.ttk.Button(menu, text="Beginner", command=(lambda: setup(0)))
beginnerLabel = tkinter.ttk.Label(menu, text="10x10 grid, 10 bombs")
beginnerButton.grid(row=1, column=0, padx=5, pady=5)
beginnerLabel.grid(row=1, column=1, padx=5, pady=5)
intermediateButton = tkinter.ttk.Button(menu, text="Intermediate", command=(lambda: setup(1)))
intermediateLabel = tkinter.ttk.Label(menu, text="16x16 grid, 40 bombs")
intermediateButton.grid(row=2, column=0, padx=5, pady=5)
intermediateLabel.grid(row=2, column=1, padx=5, pady=5)
advancedButton = tkinter.ttk.Button(menu, text="Advanced", command=(lambda: setup(2)))
advancedLabel = tkinter.ttk.Label(menu, text="16x30 grid, 99 bombs")
advancedButton.grid(row=3, column=0, padx=5, pady=5)
advancedLabel.grid(row=3, column=1, padx=5, pady=5)
menu.mainloop()
game_over = False


def dfs_minesweeper(x, y, board):
    if adjacent_bombs[x][y] != 0 or board[x][y].marked:
        return  # Only perform search if the tile clicked was an empty one (AKA no numbers or mines).
    if x == 0:
        if y == 0:
            if board[1][0].clicked == False and adjacent_bombs[1][0] >= 0:
                board[1][0].clicked = True
                dfs_minesweeper(1, 0, board)
            if board[0][1].clicked == False and adjacent_bombs[0][1] >= 0:
                board[0][1].clicked = True
                dfs_minesweeper(0, 1, board)
            if board[1][1].clicked == False and adjacent_bombs[1][1] >= 0:
                board[1][1].clicked = True
                dfs_minesweeper(x + 1, y + 1, board)
        elif y + 1 == len(adjacent_bombs[x]):
            if board[1][y].clicked == False and adjacent_bombs[1][y] >= 0:
                board[1][y].clicked = True
                dfs_minesweeper(1, y, board)
            if board[0][y - 1].clicked == False and adjacent_bombs[0][y - 1] >= 0:
                board[0][y - 1].clicked = True
                dfs_minesweeper(0, y - 1, board)
            if board[1][y - 1].clicked == False and adjacent_bombs[1][y - 1] >= 0:
                board[1][y - 1].clicked = True
                dfs_minesweeper(x + 1, y - 1, board)
        else:
            # Cardinal
            if board[x][y - 1].clicked == False and adjacent_bombs[x][y - 1] >= 0:
                board[x][y - 1].clicked = True
                dfs_minesweeper(x, y - 1, board)
            if board[x][y + 1].clicked == False and adjacent_bombs[x][y + 1] >= 0:
                board[x][y + 1].clicked = True
                dfs_minesweeper(x, y + 1, board)
            if board[x + 1][y].clicked == False and adjacent_bombs[x + 1][y] >= 0:
                board[x + 1][y].clicked = True
                dfs_minesweeper(x + 1, y, board)
            # Diagonal
            if board[x + 1][y - 1].clicked == False and adjacent_bombs[x + 1][y - 1] >= 0:
                board[x + 1][y - 1].clicked = True
                dfs_minesweeper(x + 1, y + 1, board)
            if board[x + 1][y + 1].clicked == False and adjacent_bombs[x + 1][y + 1] >= 0:
                board[x + 1][y + 1].clicked = True
                dfs_minesweeper(x + 1, y + 1, board)
    elif x + 1 == len(adjacent_bombs):
        if y == 0:
            if board[x - 1][0].clicked == False and adjacent_bombs[x - 1][0] >= 0:
                board[x - 1][0].clicked = True
                dfs_minesweeper(x - 1, 0, board)
            if board[x][1].clicked == False and adjacent_bombs[x][1] >= 0:
                board[x][1].clicked = True
                dfs_minesweeper(x, 1, board)
            if board[x - 1][1].clicked == False and adjacent_bombs[x - 1][1] >= 0:
                board[x - 1][1].clicked = True
                dfs_minesweeper(x - 1, y + 1, board)
        elif y + 1 == len(adjacent_bombs[x]):
            if adjacent_bombs[x - 1][y] >= 0 and board[x - 1][y].clicked == False:
                board[x - 1][y].clicked = True
                dfs_minesweeper(x - 1, y, board)
            if adjacent_bombs[x][y - 1] >= 0 and board[x][y - 1].clicked == False:
                board[x][y - 1].clicked = True
                dfs_minesweeper(x, y - 1, board)
            if adjacent_bombs[x - 1][y - 1] >= 0 and board[x - 1][y - 1].clicked == False:
                board[x - 1][y - 1].clicked = True
                dfs_minesweeper(x - 1, y - 1, board)
        else:
            # Cardinal
            if adjacent_bombs[x][y - 1] >= 0 and board[x][y - 1].clicked == False:
                board[x][y - 1].clicked = True
                dfs_minesweeper(x, y - 1, board)
            if adjacent_bombs[x][y + 1] >= 0 and board[x][y + 1].clicked == False:
                board[x][y + 1].clicked = True
                dfs_minesweeper(x, y + 1, board)
            if adjacent_bombs[x - 1][y] >= 0 and board[x - 1][y].clicked == False:
                board[x - 1][y].clicked = True
                dfs_minesweeper(x - 1, y, board)
            # Diagonal
            if adjacent_bombs[x - 1][y - 1] >= 0 and board[x - 1][y - 1].clicked == False:
                board[x - 1][y - 1].clicked = True
                dfs_minesweeper(x - 1, y - 1, board)
            if adjacent_bombs[x - 1][y + 1] >= 0 and board[x - 1][y + 1].clicked == False:
                board[x - 1][y + 1].clicked = True
                dfs_minesweeper(x - 1, y + 1, board)
    else:
        if y == 0:
            # Cardinal
            if adjacent_bombs[x + 1][y] >= 0 and board[x + 1][y].clicked == False:
                board[x + 1][y].clicked = True
                dfs_minesweeper(x + 1, y, board)
            if adjacent_bombs[x][y + 1] >= 0 and board[x][y + 1].clicked == False:
                board[x][y + 1].clicked = True
                dfs_minesweeper(x, y + 1, board)
            if adjacent_bombs[x - 1][y] >= 0 and board[x - 1][y].clicked == False:
                board[x - 1][y].clicked = True
                dfs_minesweeper(x - 1, y, board)
            # Diagonal
            if adjacent_bombs[x + 1][y + 1] >= 0 and board[x + 1][y + 1].clicked == False:
                board[x + 1][y + 1].clicked = True
                dfs_minesweeper(x + 1, y + 1, board)
            if adjacent_bombs[x - 1][y + 1] >= 0 and board[x - 1][y + 1].clicked == False:
                board[x - 1][y + 1].clicked = True
                dfs_minesweeper(x - 1, y + 1, board)
        elif y + 1 == len(adjacent_bombs[x]):
            if adjacent_bombs[x + 1][y] >= 0 and board[x + 1][y].clicked == False:
                board[x + 1][y].clicked = True
                dfs_minesweeper(x + 1, y, board)
            if adjacent_bombs[x][y - 1] >= 0 and board[x][y - 1].clicked == False:
                board[x][y - 1].clicked = True
                dfs_minesweeper(x, y - 1, board)
            if adjacent_bombs[x - 1][y] >= 0 and board[x - 1][y].clicked == False:
                board[x - 1][y].clicked = True
                dfs_minesweeper(x - 1, y, board)
            # Diagonal
            if adjacent_bombs[x + 1][y - 1] >= 0 and board[x + 1][y - 1].clicked == False:
                board[x + 1][y - 1].clicked = True
                dfs_minesweeper(x + 1, y - 1, board)
            if adjacent_bombs[x - 1][y - 1] >= 0 and board[x - 1][y - 1].clicked == False:
                board[x - 1][y - 1].clicked = True
                dfs_minesweeper(x - 1, y - 1, board)
        else:
            # Cardinal
            if adjacent_bombs[x + 1][y] >= 0 and board[x + 1][y].clicked == False:
                board[x + 1][y].clicked = True
                dfs_minesweeper(x + 1, y, board)
            if adjacent_bombs[x][y - 1] >= 0 and board[x][y - 1].clicked == False:
                board[x][y - 1].clicked = True
                dfs_minesweeper(x, y - 1, board)
            if adjacent_bombs[x - 1][y] >= 0 and board[x - 1][y].clicked == False:
                board[x - 1][y].clicked = True
                dfs_minesweeper(x - 1, y, board)
            if adjacent_bombs[x][y + 1] >= 0 and board[x][y + 1].clicked == False:
                board[x][y + 1].clicked = True
                dfs_minesweeper(x, y + 1, board)
            # Diagonal
            if adjacent_bombs[x + 1][y + 1] >= 0 and board[x + 1][y + 1].clicked == False:
                board[x + 1][y + 1].clicked = True
                dfs_minesweeper(x + 1, y + 1, board)
            if adjacent_bombs[x - 1][y + 1] >= 0 and board[x - 1][y + 1].clicked == False:
                board[x - 1][y + 1].clicked = True
                dfs_minesweeper(x - 1, y + 1, board)
            if adjacent_bombs[x + 1][y - 1] >= 0 and board[x + 1][y - 1].clicked == False:
                board[x + 1][y - 1].clicked = True
                dfs_minesweeper(x + 1, y - 1, board)
            if adjacent_bombs[x - 1][y - 1] >= 0 and board[x - 1][y - 1].clicked == False:
                board[x - 1][y - 1].clicked = True
                dfs_minesweeper(x - 1, y - 1, board)
                

def min_clicks():
    minimum = 0
    for y in range(len(scoreboard)):
        for x in range(len(scoreboard[y])):
            if adjacent_bombs[y][x] == 0 and scoreboard[y][x].clicked == False:
                minimum += 1
                dfs_minesweeper(x, y, scoreboard)
    for y in range(len(scoreboard)):
        for x in range(len(scoreboard[y])):
            if adjacent_bombs[y][x] > 0 and scoreboard[y][x].clicked == False:
                minimum += 1
    return minimum


if difficulty != -1:
    board = [[Cell(minesweeper_grid[y][x]) for x in range(grid_sizes[difficulty][1])] for y in range(grid_sizes[difficulty][0])]
    scoreboard = copy.deepcopy(board)
    minimum = min_clicks()

# Below for loop reveals solution, but I'll disable it on submission
# for each in board:
#     for tile in each:
#         print(tile.mine, end=" ")
#     print()


def minesweeper():
    startTime = time.time()
    global screen
    global difficulty
    pygame.init()
    resolutions = ((400, 560), (640, 800), (1200, 800))
    fontsizes = (30, 35, 40)
    offsets = (740, 540, 0)
    screen = pygame.display.set_mode(resolutions[difficulty])
    pygame.display.set_caption('Minesweeper')
    # icon = pygame.image.load('icon/icon.png')  # Doesn't work
    # pygame.display.set_icon(icon)
    screen.fill((200, 200, 200))
    timer_font = pygame.font.SysFont("Consolas.ttf", fontsizes[difficulty])
    game_font = pygame.font.SysFont("Consolas.ttf", 40)
    timeDiff = startTime
    clicks = 0  # Get number of clicks
    finished = False
    tiles_remaining = (grid_sizes[difficulty][0] * grid_sizes[difficulty][1]) - bomb_counts[difficulty]  # Initiate tiles count
    mines = bomb_counts[difficulty]  # Initiate mines count
    while True:
        text = timer_font.render("Time: " + str(int(timeDiff)), False, (200, 200, 200))  # To "erase" old timer text.
        click_text = timer_font.render("Clicks: " + str(clicks), False, (200, 200, 200))  # To "erase" old clicks text.
        screen.blit(text, (1000 - offsets[difficulty], 20))
        screen.blit(click_text, (20, 20))
        mines_text = timer_font.render("Mines: " + str(mines), False,
                                       (200, 200, 200))  # To "erase" old mines count text
        screen.blit(mines_text, (1000 - offsets[difficulty], 60))
        tiles_text = timer_font.render("Remaining Tiles: " + str(tiles_remaining), False,
                                       (200, 200, 200))  # To "erase" old tiles remaining text
        screen.blit(tiles_text, (20, 60))
        currTime = time.time()
        timeDiff = currTime - startTime
        global game_over
        if game_over:
            messagebox.showinfo('Game Over!', 'You hit a mine.')
            pygame.quit()
            sys.exit()
        if finished:
            messagebox.showinfo('Congratulations!', 'You successfully found all safe tiles!\nScore: ' + str(round((minimum / timeDiff) * bonus[difficulty])))
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicks += 1
                    row = (event.pos[1] - 160) // 40
                    col = event.pos[0] // 40
                    if event.pos[1] >= 160 and not board[row][col].marked:
                        board[row][col].clicked = True
                        if board[row][col].mine == 1:
                            pygame.draw.rect(screen, (65, 65, 65), (col * 40 + 1, row * 40 + 161, 38, 38))
                            pygame.display.update()
                            game_over = True
                            for x in board:
                                for y in x:
                                    if y.mine == 1:
                                        y.clicked = True
                            for iy, rowOfCells in enumerate(board):
                                for ix, cell in enumerate(rowOfCells):
                                    color = (225, 225, 225) if cell.clicked and cell.mine == 0 else (
                                        65, 65, 65) if cell.clicked and cell.mine == 1 else (164, 164, 164)
                                    pygame.draw.rect(screen, color, (ix * 40 + 1, iy * 40 + 161, 38, 38))
                                    pygame.display.update()
                        else:
                            dfs_minesweeper(row, col, board)  # Find all safe adjacent blocks
                            finished = True
                            for x in board:
                                for y in x:
                                    if y.mine == 0 and y.clicked == False:
                                        finished = False
                elif event.button == 3 and mines > 0:  # Right-click, and user still has flags to place down.
                    row = (event.pos[1] - 160) // 40
                    col = event.pos[0] // 40
                    if event.pos[1] >= 160:
                        if board[row][col].marked:
                            board[row][col].marked = False
                        else:
                            board[row][col].marked = True

        text = timer_font.render("Time: " + str(int(timeDiff)), False, (0, 0, 0))
        click_text = timer_font.render("Clicks: " + str(clicks), False, (0, 0, 0))
        screen.blit(text, (1000 - offsets[difficulty], 20))
        screen.blit(click_text, (20, 20))

        # Redrawing grid
        tiles_remaining = (grid_sizes[difficulty][0] * grid_sizes[difficulty][1]) - bomb_counts[difficulty]  # Initiate tiles count
        mines = bomb_counts[difficulty]  # Initiate mines count
        for iy, rowOfCells in enumerate(board):
            for ix, cell in enumerate(rowOfCells):
                if cell.clicked and cell.mine == 0:
                    color = (225, 225, 225)
                    tiles_remaining -= 1

                elif cell.clicked and cell.mine == 1:
                    color = (65, 65, 65)
                else:
                    if cell.marked:
                        mines -= 1
                    color = (164, 164, 164)
                pygame.draw.rect(screen, color, (ix * 40 + 1, iy * 40 + 161, 38, 38))
                if adjacent_bombs[iy][ix] > 0 and cell.clicked:
                    screen.blit(
                        game_font.render(str(adjacent_bombs[iy][ix]), False, colorList[adjacent_bombs[iy][ix] - 1]),
                        (ix * 40 + 12, iy * 40 + 167))
                if cell.marked and not cell.clicked:
                    screen.blit(
                        game_font.render('!', False, (255, 0, 0)),
                        (ix * 40 + 15, iy * 40 + 167))
                elif not cell.clicked:
                    screen.blit(
                        game_font.render('!', False, (164, 164, 164)),
                        (ix * 40 + 15, iy * 40 + 167))
        mines_text = timer_font.render("Mines: " + str(mines), False, (0, 0, 0))  # Display number of mines
        screen.blit(mines_text, (1000 - offsets[difficulty], 60))
        tiles_text = timer_font.render("Remaining Tiles: " + str(tiles_remaining), False,
                                       (0, 0, 0))  # Display tiles remaining
        screen.blit(tiles_text, (20, 60))
        pygame.display.flip()
        pygame.display.update()


if difficulty != -1:
    minesweeper()
