import pygame
import os
import random
import time
import math


class Square:
    def __init__(self, value=0, color_index=0):
        self.value = value
        self.at_start = False if value == 0 else True
        self.color_index = color_index

    def set_start_value(self, amount):
        self.at_start = False if amount == 0 else True
        self.value = amount


def change_selected(amount, is_solving=True):
    global backtrack
    global solve
    global solve_rn
    global selected_x
    global selected_y
    if is_solving:
        grid.grid[selected_x][selected_y].color_index = amount + 1
    else:
        grid.grid[selected_x][selected_y].color_index = 0
    selected_x += amount

    if selected_x < 0:
        if selected_y <= 0:
            print("No Solution")
            selected_x -= amount
            solve_rn = False
            solve = False
            backtrack = False
            return
        selected_x += 9
        selected_y -= 1
    elif selected_x > 8:
        if selected_y >= 8:
            print("Done")
            set_at_start_values()
            selected_x -= amount
            solve_rn = False
            solve = False
            backtrack = False
            return
        selected_x -= 9
        selected_y += 1
    grid.grid[selected_x][selected_y].color_index = 1


def set_at_start_values():
    for x in range(9):
        for y in range(9):
            if grid.grid[x][y].value != 0:
                grid.grid[x][y].at_start = True
            else:
                grid.grid[x][y].at_start = False
            grid.grid[x][y].color_index = 0


class Grid9x9:
    grid = [[Square() for i in range(9)] for i in range(9)]

    def __init__(self, width, height):
        self.min_x_pos = WIDTH / 2 - width / 2
        self.min_y_pos = HEIGHT / 2 - height / 2
        self.width = width
        self.height = height
        self.square_height = height / 9
        self.square_width = width / 9
        for temp_x in range(9):
            for temp_y in range(9):
                self.grid[temp_x][temp_y] = Square()


pygame.init()
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku solver")

run = True
solve_rn = False
solve = False
backtrack = False
grid = Grid9x9(450, 450)
selected_x = 0
selected_y = 0
grid.grid[selected_x][selected_y].color_index = 1

# Text stuff
font = pygame.font.SysFont("comicsansms", 26)
text = font.render("Press space to solve the current board", True, (0, 128, 0))
solveState = font.render("", True, (0, 128, 0))

while run:

    # Solving the board
    # Inputs don't register if this is true
    # While loop runs more than once only once if solve_rn is False
    while True:
        if solve:
            # Skip over numbers that are already solved
            if grid.grid[selected_x][selected_y].at_start:
                if backtrack:
                    change_selected(-1)
                else:
                    change_selected(1)
                continue

            #print("starts at pos " + str(selected_x) + " " + str(selected_y))

            # Check what number can be put
            num = grid.grid[selected_x][selected_y].value + 1
            while True:
                #print("while loop. num = " + str(num))
                if num > 9:
                    backtrack = True
                    grid.grid[selected_x][selected_y].value = 0
                    change_selected(-1)
                    #print("num was above 9, break")
                    break

                next_while = False
                # Check the column
                for square in grid.grid[selected_x]:
                    if square.value == num:
                        #print("num is " + str(num) +". failed in COLUMN. Pos idk " + str(selected_y) + ", value in the pos is " + str(grid.grid[x2][selected_y].value))
                        num += 1
                        next_while = True
                        break
                if next_while:
                    continue

                # Check the row
                for x2 in range(9):
                    if grid.grid[x2][selected_y].value == num:
                        #print("num is " + str(num) +". failed in ROW. Pos " + str(x2) + " " + str(selected_y) + ", value in the pos is " + str(grid.grid[x2][selected_y].value))
                        num += 1
                        next_while = True
                        break
                if next_while:
                    continue

                # Check the box
                boxX = selected_x // 3
                boxY = selected_y // 3
                for x3 in range(boxX * 3, boxX * 3 + 3):
                    for y3 in range(boxY * 3, boxY * 3 + 3):
                        if grid.grid[x3][y3].value == num:
                            #print("num is " + str(num) +". failed in BOX. Pos " + str(x3) + " " + str(y3) + ", value in the pos is " + str(grid.grid[x2][selected_y].value))
                            num += 1
                            next_while = True
                            break
                if next_while:
                    continue

                # The current num can be put
                grid.grid[selected_x][selected_y].value = num
                backtrack = False
                change_selected(1)
                break
        else:
            break
        if not solve_rn:
            break
    for event in pygame.event.get():
        # Quit the game
        if event.type == pygame.QUIT:
            run = False
        elif solve:
            if event.type == pygame.KEYDOWN:
                solve_rn = True
            break
        # Clicking on the squares
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Calculate the clicked square position
            mousePos = pygame.mouse.get_pos()
            mousePos_x = mousePos[0]
            mousePos_x -= grid.min_x_pos
            mousePos_x /= grid.square_width
            mousePos_x = math.floor(mousePos_x)

            mousePos_y = mousePos[1]
            mousePos_y -= grid.min_y_pos
            mousePos_y /= grid.square_height
            mousePos_y = math.floor(mousePos_y)
            if not -1 < mousePos_y < 9 or not -1 < mousePos_x < 9:
                continue
            grid.grid[selected_x][selected_y].color_index = 0
            selected_x = mousePos_x
            selected_y = mousePos_y
            grid.grid[selected_x][selected_y].color_index = 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0 or event.key == pygame.K_ESCAPE or event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                grid.grid[selected_x][selected_y].set_start_value(0)
            elif event.key == pygame.K_1:
                grid.grid[selected_x][selected_y].set_start_value(1)
            elif event.key == pygame.K_2:
                grid.grid[selected_x][selected_y].set_start_value(2)
            elif event.key == pygame.K_3:
                grid.grid[selected_x][selected_y].set_start_value(3)
            elif event.key == pygame.K_4:
                grid.grid[selected_x][selected_y].set_start_value(4)
            elif event.key == pygame.K_5:
                grid.grid[selected_x][selected_y].set_start_value(5)
            elif event.key == pygame.K_6:
                grid.grid[selected_x][selected_y].set_start_value(6)
            elif event.key == pygame.K_7:
                grid.grid[selected_x][selected_y].set_start_value(7)
            elif event.key == pygame.K_8:
                grid.grid[selected_x][selected_y].set_start_value(8)
            elif event.key == pygame.K_9:
                grid.grid[selected_x][selected_y].set_start_value(9)

            if event.key == pygame.K_SPACE:
                space_down = True
                solve = True
                grid.grid[selected_x][selected_y].color_index = 0
                selected_y = 0
                selected_x = 0
            elif event.key == pygame.K_LEFT:
                change_selected(-1, False)
            else:
                change_selected(1, False)

    WIN.fill((200, 200, 200))
    # Draw the board
    y_pos = grid.min_y_pos
    for y in range(9):
        x_pos = grid.min_x_pos
        y_pos += grid.square_height + 2
        for x in range(9):
            color = (0, 0, 0)
            if grid.grid[x][y].color_index == 1:
                color = (150, 0, 0)
            elif grid.grid[x][y].color_index == 2:
                color = (0, 100, 0)
            pygame.draw.rect(WIN, color, (x_pos, y_pos, grid.square_width, -grid.square_height), 2)
            # If number is not 0 draw it
            if grid.grid[x][y].value:
                number = font.render(str(grid.grid[x][y].value), True, (30, 30, 30))
                pos = ((x_pos + grid.square_width / 2) - 6, (y_pos - grid.square_height) + 7)
                WIN.blit(number, pos)

            x_pos += grid.square_width + 1
    # Draw the sudoku lines. line order: left, right, up, down
    pygame.draw.line(WIN, (111, 150, 212), (grid.min_x_pos + grid.width / 3 + 2, grid.min_y_pos), (grid.min_x_pos + grid.width / 3 + 2, grid.min_y_pos + grid.height + 18), 4)
    pygame.draw.line(WIN, (111, 150, 212), (grid.min_x_pos + (grid.width / 3) * 2 + 5, grid.min_y_pos), (grid.min_x_pos + (grid.width / 3) * 2 + 5, grid.min_y_pos + grid.height + 18), 4)
    pygame.draw.line(WIN, (111, 150, 212), (grid.min_x_pos, grid.min_y_pos + grid.height / 3 + 6), (grid.min_x_pos + grid.width + 9, grid.min_y_pos + grid.height / 3 + 6), 4)
    pygame.draw.line(WIN, (111, 150, 212), (grid.min_x_pos, grid.min_y_pos + (grid.height / 3) * 2 + 12), (grid.min_x_pos + grid.width + 9, grid.min_y_pos + (grid.height / 3) * 2 + 12), 4)

    # Space text
    if solve:
        if solve_rn:
            words = "Solving, please don't close the program"
        else:
            words = "Press any key to solve instantly"
    else:
        words = "Press space to solve the current board"
    text = font.render(words, True, (0, 128, 0))
    WIN.blit(text, (WIDTH / 2 - text.get_width() // 2, 50 - text.get_height() // 2))

    pygame.time.delay(3)
    pygame.display.update()
pygame.quit()
