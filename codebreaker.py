from abc import ABC, abstractmethod

from colors import Color

def flatten(list):
    return [it for sublist in list for it in sublist]

class Codebreaker(ABC):
    def __init__(self, num_pegs):
        self.num_colors = len(Color)
        self.num_pegs = num_pegs
    
    @abstractmethod
    def guess(self, last_rating, num_tries):
        pass

class Player(Codebreaker):
    def guess(self, last_rating, num_tries):
        if last_rating != None:
            print(f"Black pegs: {last_rating[0]:d}, White pegs: {last_rating[1]:d}")
        pattern = self.input_pattern(num_tries)
        print("Your guess:", " ".join(list(map(lambda c: c.name, pattern))))
        return pattern

    def input_pattern(self, num_tries):
        while True:
            try:
                pattern = list(map(lambda s: Color[s.lower()], input(f"Attempt {num_tries:d}: ").split()))
            except KeyError as err:
                print(f"No such color: {err.args[0]:s}")
                continue
            if len(pattern) == self.num_pegs:
                break
            print(f"You need to guess all {self.num_pegs:d} pegs.")
        return pattern


class Knuth(Codebreaker):
    def __init__(self, num_pegs):
        super().__init__(num_pegs)
        self.guesses = []
        self.generate_all_combinations()
        self.generate_ratings()
        self.solutions = self.all[:]

    def guess(self, last_rating, _):
        if last_rating != None:
            print(f"Black pegs: {last_rating[0]:d}, White pegs: {last_rating[1]:d}")
        pattern = self.knuth_algorithm(last_rating)
        print("Knuth's guess:", " ".join(list(map(lambda c: c.name, pattern))))
        return pattern

    def generate_all_combinations(self):
        if self.num_pegs == 0:
            self.all = []
        else:
            self.all = [[color] for color in map(lambda i: Color(i), range(0, self.num_colors))]
            self.generate_helper(self.num_pegs - 1)
    
    def generate_helper(self, pegs_left):
        if pegs_left == 0:
            return
        self.all = flatten(list(map(lambda pattern: [pattern[:] + [color] for color in map(lambda i: Color(i), range(0, self.num_colors))], self.all)))
        self.generate_helper(pegs_left - 1)

    def generate_ratings(self):
        self.rating_scores = {}
        for black in range(0, self.num_pegs + 1):
            for white in range(0, self.num_pegs + 1 - black):
                if black == self.num_pegs - 1 and white == 1:
                    # This rating is impossible
                    continue
                self.rating_scores[(black, white)] = 0

    # Knuth's algorithm, see https://en.wikipedia.org/wiki/Mastermind_(board_game)#Five-guess_algorithm
    def knuth_algorithm(self, last_rating):
        if self.guesses == [] and last_rating == None:
            if self.num_pegs == 4 and self.num_colors > 1:
                # return original guess of Knuth
                best_guess = [Color(0), Color(0), Color(1), Color(1)]
            else:
                best_guess = [Color(i % self.num_colors) for i in range(0, self.num_pegs)]
        elif last_rating == (4, 0):
            return self.guesses[-1]
        else:
            self.solutions = self.prune_solutions(last_rating, self.guesses[-1])

            best_score = None
            for pattern in self.all:
                # clear scores
                for key in self.rating_scores:
                    self.rating_scores[key] = 0
                for rating in self.rating_scores:
                    self.rating_scores[rating] += len(self.prune_solutions(rating, pattern))
                pattern_score = max(self.rating_scores.values())
                if best_score == None or pattern_score < best_score:
                    best_guess = pattern
                    best_score = pattern_score
                elif pattern_score == best_score and pattern in self.solutions:
                    best_guess = pattern

        self.guesses.append(best_guess)
        self.all.remove(best_guess)
        if best_guess in self.solutions:
            self.solutions.remove(best_guess)
        return best_guess


    def prune_solutions(self, rating, guess):
        import game
        return list(filter(lambda pattern: game.rate(pattern, guess) == rating, self.solutions))