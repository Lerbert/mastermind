import getpass

from colors import Color

def random_code(num_pegs):
    import random
    return [random.choice(list(Color)) for _ in range(num_pegs)]

def choose_code(num_pegs):
    while True:
        try:
            pattern = list(map(lambda s: Color[s.lower()], getpass.getpass(f"Choose a secret code: ").split()))
        except KeyError as err:
            print(f"No such color: {err.args[0]:s}")
            continue
        if len(pattern) == num_pegs:
            break
        print(f"You need to set all {num_pegs:d} pegs.")
    return pattern