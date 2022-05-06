import random
import asyncio
import curses
import sys

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
                            frame1,
                            frame2,
                            spaceship_size_in_rows,
                            spaceship_size_in_cols):
    while True:
        draw_frame(canvas, position_row, position_column, frame1, negative=False)
        for _ in range(1000):
            await asyncio.sleep(0)

        draw_frame(canvas, position_row, position_column, frame1, negative=True)
        await asyncio.sleep(0)

        draw_frame(canvas, position_row, position_column, frame2, negative=False)
        for _ in range(1000):
            await asyncio.sleep(0)

        draw_frame(canvas, position_row, position_column, frame2, negative=True)
        await asyncio.sleep(0)

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
            position_column = max_column - (spaceship_size_in_cols / 2) - 1
        elif preposition_column <= 0:
            position_column = 1
        else:
            position_column = preposition_column

        await asyncio.sleep(0)


async def fire(canvas, start_row, start_column, rows_speed=-0.0001, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


def draw(canvas):
    curses.curs_set(False)
    max_row, max_column = curses.window.getmaxyx(canvas)
    canvas.border()
    canvas.nodelay(True)

    with open(file='./animations/rocket/rocket_frame_one.txt') as file:
        frame1 = file.read()
    with open(file='./animations/rocket/rocket_frame_two.txt') as file:
        frame2 = file.read()
    spaceship_size_in_cols, spaceship_size_in_rows = get_frame_size(frame1)
    stars_quantity = max_row * max_column // 100
    coroutines = [
        blink(canvas,
              row=random.choice(range(1, max_row - 1)),
              column=random.choice(range(1, max_column - 1)),
              symbol=random.choice('+*.:'),
              start=random.randint(20000, 40000),
              growth=random.randint(5000, 10000),
              shine=random.randint(5000, 10000),
              end=random.randint(3000, 6000))
        for _ in range(stars_quantity)
    ]
    coroutines.append(fire(canvas,
                           int(max_row / 2),
                           int(max_column / 2),
                           ))

    coroutines.append(animate_spaceship(canvas,
                                        max_row,
                                        max_column,
                                        int(max_row / 2),
                                        int(max_column / 2),
                                        frame1=frame1,
                                        frame2=frame2,
                                        spaceship_size_in_rows=spaceship_size_in_rows,
                                        spaceship_size_in_cols=spaceship_size_in_cols))

    while True:
        canvas.refresh()
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        if len(coroutines) == 0:
            break


if __name__ == '__main__':
    curses.TIC_TIMEOUT = 0.1
    curses.update_lines_cols()
    curses.wrapper(draw)
