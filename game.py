from colors import Color
import codebreaker as cb
import random

def choosePattern(n):
    pattern = []
    for _ in range(n):
        pattern.append(random.choice(list(Color)))
    return pattern

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
    print(f"{num_pegs:d} pegs, {len(Color):d} colors")
    print("The colors are:", ", ".join([e.name for e in Color]))
    print("You may abbreviate them by typing only the first letter")
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
        pegs = 4
        knuth = cb.Knuth(pegs)
        player = cb.Player(pegs)
        master_pattern = choosePattern(pegs)
        game_loop(pegs, master_pattern, player)
    except KeyboardInterrupt as _:
        print("")  # newline to tidy up console
        print("You conceded! The code was:", format_pattern(master_pattern))