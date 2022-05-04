import random
import asyncio
import curses
from curses_tools import draw_frame, read_controls


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


async def animate_spaceship(canvas, start_row, start_column, text1, text2):
    while True:
        draw_frame(canvas, start_row, start_column, text1, negative=False)
        for _ in range(1000):
            await asyncio.sleep(0)

        draw_frame(canvas, start_row, start_column, text1, negative=True)
        await asyncio.sleep(0)

        draw_frame(canvas, start_row, start_column, text2, negative=False)
        for _ in range(1000):
            await asyncio.sleep(0)

        draw_frame(canvas, start_row, start_column, text2, negative=True)
        await asyncio.sleep(0)

        delta_row, delta_column, space = read_controls(canvas)
        start_row = start_row + delta_row
        start_column = start_column + delta_column
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
    max_row, max_col = curses.window.getmaxyx(canvas)
    canvas.border()
    canvas.nodelay(True)

    with open(file='./animations/rocket/rocket_frame_one.txt') as file:
        frame1 = file.read()
    with open(file='./animations/rocket/rocket_frame_two.txt') as file:
        frame2 = file.read()

    coroutines = [
        blink(canvas,
              row=random.choice(range(1, max_row - 1)),
              column=random.choice(range(1, max_col - 1)),
              symbol=random.choice('+*.:'),
              start=random.randint(20000, 40000),
              growth=random.randint(5000, 10000),
              shine=random.randint(5000, 10000),
              end=random.randint(3000, 6000))
        for _ in range(200)
    ]
    coroutines.append(fire(canvas,
                           int(max_row / 2),
                           int(max_col / 2),
                           ))

    coroutines.append(animate_spaceship(canvas,
                                        int(max_row / 2),
                                        int(max_col / 2),
                                        text1=frame1,
                                        text2=frame2))

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
