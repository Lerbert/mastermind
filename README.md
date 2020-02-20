# mastermind
A command line version of the mastermind game. You can try to break the code yourself or watch [Donald Knuth's algorithm](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Five-guess_algorithm) do the work.
```
usage: game.py [-h] [-p | -k] [PEGS]

MASTERMIND Break the code using the hints you get. N black pegs --> correct
color and position for N pegs of your guess, N white pegs --> correct color
but wrong position for N pegs of your guess

positional arguments:
  PEGS          number of pegs used in the game

optional arguments:
  -h, --help    show this help message and exit
  -p, --player  break the code yourself
  -k, --knuth   use Knuth's algorithm to break the code
  ```