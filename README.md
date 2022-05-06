# Space-game

## Установка
Вам понадобится установленный Python 3.6-3.10 и git.

Склонируйте репозиторий:
```bash
$ git clone git@github.com:IlyaG96/space-game.git
```

Создайте в этой папке виртуальное окружение:
```bash
$ python3 -m venv [полный путь до папки space-game] env
```

Активируйте виртуальное окружение и установите зависимости:
```bash
$ cd space-game
$ source env/bin/activate
```
## Использование

Простейший способ запустить игру:
```bash
$ python main.py
```


### curses_tools.py
Содержит логику для отображения картинки и работы с клавишами управления.