from colors import Color
import random

def choosePattern(n):
    pattern = []
    for _ in range(n):
        pattern.append(random.choice(list(Color)))
    return pattern

def guess(n, pegs):
    while True:
        try:
            pattern = list(map(lambda s: Color[s.lower()], input(f"Attempt {n:d}: ").split()))
        except KeyError as err:
            print(f"No such color: {err.args[0]:s}")
            continue
        if len(pattern) == pegs:
            break
    print("Your guess:", " ".join(list(map(lambda c: c.name, pattern))))
    return pattern

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

def main():
    num_pegs = 4
    master_pattern = choosePattern(num_pegs)
    # print(master_pattern)
    print(f"{num_pegs:d} pegs, {len(Color):d} colors")
    print("The colors are:", ", ".join([e.name for e in Color]))
    print("You may abbreviate them by typing only the first letter")
    num_guesses = 0
    while True:
        num_guesses += 1
        player_pattern = guess(num_guesses, num_pegs)
        black, white = rate(master_pattern, player_pattern)
        print(f"Black pegs: {black:d}, White pegs: {white:d}")
        if black == 4:
            print(f"You win after {num_guesses:d} attempt(s)!")
            print("The code was:", " ".join(list(map(lambda c: c.name, master_pattern))))
            break
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as _:
        print("")  # newline to tidy up console