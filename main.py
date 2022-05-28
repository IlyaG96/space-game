import random
import asyncio
import curses
import time
from itertools import cycle

from curses_tools import draw_frame, read_controls, get_frame_size


async def blink(canvas,
                row,
                column,
                symbol,
                start,
                growth,
                shine,
                end):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(start):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(growth):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(shine):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(end):
            await asyncio.sleep(0)


async def animate_spaceship(canvas,
                            max_row,
                            max_column,
                            position_row,
                            position_column,
                            screen_border_distance,
                            frame1,
                            frame2,
                            spaceship_size_in_rows,
                            spaceship_size_in_cols,):
    frames = [
        frame1,
        frame2,
    ]
    for frame in cycle(frames):
        # draw frame
        draw_frame(canvas, position_row, position_column, frame, False)

        delta_row, delta_column, space = read_controls(canvas)
        preposition_row = position_row + delta_row
        preposition_column = position_column + delta_column

        if preposition_row >= max_row - 2 * spaceship_size_in_rows:
            position_row = max_row - 2 * spaceship_size_in_rows
        elif preposition_row <= 0:
            position_row = 1
        else:
            position_row = preposition_row

        if preposition_column >= max_column - spaceship_size_in_cols:
            position_column = max_column - (spaceship_size_in_cols / 2) - screen_border_distance
        elif preposition_column <= 0:
            position_column = 1
        else:
            position_column = preposition_column

        await asyncio.sleep(0)
        # erases previous frame
        draw_frame(canvas,
                   preposition_row - delta_row,
                   preposition_column - delta_column,
                   frame, True)


def draw(canvas):
    curses.curs_set(False)
    screen_height, screen_width = curses.window.getmaxyx(canvas)
    canvas.border()
    canvas.nodelay(True)
    screen_border_distance = 1  # minimal distance between object and screen border
    stars_density = 100  # less is more stars
    game_speed = 0.1  # delay (pause?) between coroutines, less is higher game speed

    with open(file='./animations/rocket/rocket_frame_one.txt') as file:
        frame1 = file.read()
    with open(file='./animations/rocket/rocket_frame_two.txt') as file:
        frame2 = file.read()
    spaceship_size_in_cols, spaceship_size_in_rows = get_frame_size(frame1)
    stars_quantity = screen_height * screen_width // stars_density
    coroutines = [
        blink(canvas,
              row=random.choice(range(1, screen_height - screen_border_distance)),
              column=random.choice(range(1, screen_width - screen_border_distance)),
              symbol=random.choice('+*.:'),
              start=random.randint(3, 6),
              growth=random.randint(8, 16),
              shine=random.randint(8, 16),
              end=random.randint(3, 6))
        for _ in range(stars_quantity)
    ]

    coroutines.append(animate_spaceship(canvas,
                                        screen_height,
                                        screen_width,
                                        int(screen_height / 2),
                                        int(screen_width / 2),
                                        screen_border_distance,
                                        frame1=frame1,
                                        frame2=frame2,
                                        spaceship_size_in_rows=spaceship_size_in_rows,
                                        spaceship_size_in_cols=spaceship_size_in_cols))

    while True:
        time.sleep(game_speed)
        canvas.refresh()
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        if not coroutines:
            break


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
