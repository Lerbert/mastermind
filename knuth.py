from colors import Color

def flatten(list):
    return [it for sublist in list for it in sublist]

class Knuth:
    def __init__(self, num_colors, num_pegs):
        self.num_colors = num_colors
        self.num_pegs = num_pegs
        self.guesses = []
        self.generate_all_combinations()
        self.generate_ratings()
        self.solutions = self.all[:]

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
    def guess(self, last_rating):
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


if __name__ == "__main__":
    try:
        k = Knuth(6, 4)
        # k.guesses.append([Color(0), Color(0), Color(0), Color(0)])
        print(k.guess(None))
        print(k.guess((3, 0)))
        print(k.guess((2, 0)))
        print(k.guess((2, 2)))
        # print(k.solutions)
        # print(k.rating_scores)
    except KeyboardInterrupt as _:
        print("")  # newline to tidy up console