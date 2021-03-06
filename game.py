import argparse

from colors import Color
import codebreaker as cb
import codemaker as cm

def format_pattern(pattern):
    return " ".join(list(map(lambda c: c.name, pattern)))

def rate(master, guess):
    assert(len(master) == len(guess))
    black, white = 0, 0
    master_not_rated = master[:]
    guess = guess[:] # copy guess

    for i in range(len(guess)):
        if guess[i] == master[i]:
            black += 1
            master_not_rated[i] = None
            guess[i] = None

    for i in range(len(guess)):
        if guess[i] != None and guess[i] in master_not_rated:
            white += 1
            master_not_rated[master_not_rated.index(guess[i])] = None

    return black, white

def game_loop(num_pegs, master_pattern, breaker):
    num_guesses = 0
    last_rating = None
    while True:
        num_guesses += 1
        pattern = breaker.guess(last_rating, num_guesses)
        last_rating = rate(master_pattern, pattern)
        if last_rating[0] == num_pegs:
            print(f"You win after {num_guesses:d} attempt(s)!")
            print("The code was:", format_pattern(master_pattern))
            break
    

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="MASTERMIND Break the code using the hints you get. N black pegs --> correct color and position for N pegs of your guess, N white pegs --> correct color but wrong position for N pegs of your guess")
        breakerargs = parser.add_mutually_exclusive_group()
        breakerargs.add_argument("-p", "--player", action="store_const", const=lambda p: cb.Player(p), dest="breaker", help="break the code yourself")
        breakerargs.add_argument("-k", "--knuth", action="store_const", const=lambda p: cb.Knuth(p), dest="breaker", help="use Knuth's algorithm to break the code")
        makerargs = parser.add_mutually_exclusive_group()
        makerargs.add_argument("-s", "--select", action="store_const", const=cm.choose_code, dest="maker", help="choose the code yourself")
        makerargs.add_argument("-r", "--random", action="store_const", const=cm.random_code, dest="maker", help="start with a random code")
        parser.add_argument("-c", "--cheat", action="store_true", default=False, help="display the code at game start")
        parser.add_argument("pegs", type=int, metavar="PEGS", default=4, help="number of pegs used in the game", nargs="?")
        parser.set_defaults(breaker=lambda p: cb.Player(p))
        args = parser.parse_args()

        print(f"{args.pegs:d} pegs, {len(Color):d} colors")
        print("The colors are:", ", ".join([e.name for e in Color]))
        print("You may abbreviate them by typing only the first letter")

        master_pattern = args.maker(args.pegs)
        print("Code accepted")
        if (args.cheat):
            print("The code is:", format_pattern(master_pattern))
        
        game_loop(args.pegs, master_pattern, args.breaker(args.pegs))
    except KeyboardInterrupt as _:
        print("")  # newline to tidy up console
        print("You conceded! The code was:", format_pattern(master_pattern))