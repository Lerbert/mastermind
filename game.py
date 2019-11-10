from colors import Color
import random

def choosePattern(n):
    pattern = []
    for _ in range(n):
        pattern.append(random.choice(list(Color)))
    return pattern

def guess(n):
    while True:
        try:
            pattern = list(map(lambda s: Color[s], input(f"Enter your guess ({n:d} colors):").split()))
        except KeyError as err:
            print(f"No such color: {err.args[0]:s}")
            continue
        print(pattern)
        if len(pattern) == n:
            break
    print("Your guess:", " ".join(list(map(lambda c: c.name, pattern))))
    return pattern

def main():
    num_pegs = 4
    master_pattern = choosePattern(num_pegs)
    print(master_pattern)
    while True:
        player_pattern = guess(num_pegs)
        if player_pattern == master_pattern:
            print("You win!")
            break
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as _:
        print("")  # newline to tidy up console