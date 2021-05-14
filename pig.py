import random
from time import time
from matplotlib import pyplot as plt

DICE_SIDES = 6
FAILS = 1

def simulation(turns=2 * 10**6, max_strat=70):
    """
    This is a simulation for the game pig assuming that strategies are based on stop bidding when you reach a particular
    score for a round. This function will return the expected value of each turn given a particular goal score.
    :param turns: int this is how many turns the function will simulate to get the answer.
    :param max_strat: int The simulation will give expected returns for each goal score up to this number.
    :return: this will return a list of floats with max_strat entries where each entry is an expected return on a
    single turn.
    """
    hist = [0] * max_strat
    for turn in range(1, turns+1):
        if not turn %10**4:
            print("{} turns finished {:.2f}% done".format(turn, (turn/turns)*100), end="\r")
        turn_score = 0
        while turn_score < max_strat:
            roll = random.randint(1, DICE_SIDES)
            if roll <= FAILS:
                break
            for ndx in range(turn_score,min(turn_score + roll, max_strat)):
                hist[ndx] += (turn_score + roll)
            turn_score += roll
    print("")
    hist = [x/turn for x in hist]
    return hist


def solver(max_strat=70):
    """
    This is a solver for the game pig assuming that strategies are based on stop bidding when you reach a particular
    score for a round. This function will return the expected value of each turn given a particular goal score.
    :param max_strat: this is an int. The solver will give expected returns for each goal score up to this number.
    :return: this will return a list of floats with max_strat entries where each entry is an expected return on a
    single turn.
    """
    if max_strat < DICE_SIDES:
        raise ValueError("need to increase max strategy for this one, fam.")
    hist = [0] * (max_strat + 1)
    hist[0] = 1
    solved = [0] * (max_strat + 1)
    for ndx in range(1, len(hist)):
        for roll in range(FAILS+1, DICE_SIDES+1):
            hist[ndx] += hist[ndx - roll] / DICE_SIDES
    for ndx in range(1, len(hist)):
        for offset in range(1, DICE_SIDES+1):
            if ndx-offset >= 0:
                for roll in range(FAILS + 1, DICE_SIDES + 1):
                    if offset <= roll:
                        solved[ndx] += hist[ndx - offset] * (ndx - offset + roll) / DICE_SIDES
    return solved[1:]

def solver2(max_strat=70):
    """
    This is a solver for the game pig assuming that strategies are based on stop bidding when you reach a particular
    score for a round. This function will return the chace for each point total of each turn given a particular goal
    score.
    :param max_strat: this is an int. The solver will give expected returns for each goal score up to this number.
    :return: this will return a list of dicts that are corresponding to the with max_strat entries where each entry is an expected return on a
    single turn.
    """
    if max_strat < DICE_SIDES:
        raise ValueError("need to increase max strategy for this one, fam.")
    hist = [0] * (max_strat + 1)
    hist[0] = 1
    solved = [{}] * (max_strat + 1)
    for ndx in range(1, len(hist)):
        for roll in range(FAILS+1, DICE_SIDES+1):
            hist[ndx] += hist[ndx - roll] / DICE_SIDES

    for ndx in range(1, len(hist)):
        solved[ndx] = {0: 0}
        for offset in range(1, DICE_SIDES+1):
            if ndx-offset >= 0:
                for roll in range(FAILS + 1, DICE_SIDES + 1):
                    if offset <= roll:
                        if (ndx - offset + roll) not in solved[ndx]:
                            solved[ndx][(ndx - offset + roll)] = 0
                        solved[ndx][(ndx - offset + roll)] += hist[ndx - offset] / DICE_SIDES
            left = 1.
            for i in solved[ndx]:
                left -= solved[ndx][i]
        solved[ndx][0] = left
    return solved[1:]

def game_strat_approximater(chances, goal=200, scans=30):
    """
    this will give an output of the chances and appropriate strategy to follow at the start of a round in the pig game
    :param chances: this is a result of solver2 for the game that you want to play
    :param goal: this is an int that describes the number of points that you need to win
    :param scans: this is how many times the approximater will update each of the game states before resolving
    :return: 2 2-d lists the first says what your optimal strategy is, the second says what your chances of wining
    with that strategy are.
    """
    expected = [[.25 for _ in range(goal)] for __ in range(goal)]
    strats = [[0. for _ in range(goal)] for __ in range(goal)]
    for yyy in range(scans):
        print("{} scans complete {:.2f}% done".format(yyy, yyy / scans * 100), end="\r")
        for x_score in range(goal-1, -1, -1):
            for n_score in range(goal - 1, -1, -1):
                best_strat = None
                best_score = 0.          #this should never be below 0 so I chosse this instead of float("-inf")
                for ndx in range(len(chances)):
                    strat = chances[ndx]
                    score = 0.
                    for points in strat:
                        if (points + x_score) >= goal:
                            score += strat[points]
                        else:
                            score += strat[points] * (1. - expected[n_score][x_score + points])

                    if score > best_score:
                        best_score = score
                        best_strat = ndx + 1
                expected[x_score][n_score] = best_score
                strats[x_score][n_score] = best_strat
    print("{} scans complete {:.2f}% done".format(yyy+1, (yyy+1) / scans * 100))
    return expected, strats

def game_strat_approximater2(chances, goal=200, threshold=10**-3):
    """
    this will give an output of the chances and appropriate strategy to follow at the start of a round in the pig game
    :param chances: this is a result of solver2 for the game that you want to play
    :param goal: this is an int that describes the number of points that you need to win
    :param threshold: this is a maximum level of change from any point value's chance of winning in a perticular
    iteration compared to it's chance of wining in the last iteration before the approximater will resolve.
    :return: 2 2-d lists the first says what your optimal strategy is, the second says what your chances of wining
    with that strategy are.
    """
    expected = [[.25 for _ in range(goal)] for __ in range(goal)]
    strats = [[0 for _ in range(goal)] for __ in range(goal)]
    delta = 1
    yyy = 0
    while delta >= threshold:
        print("{} scans complete delta = {:.6f}".format(yyy, delta), end="\r")
        delta = 0
        yyy += 1
        for x_score in range(goal-1, -1, -1):
            for n_score in range(goal - 1, -1, -1):
                best_strat = None
                best_score = 0.          #this should never be below 0 so I chosse this instead of float("-inf")
                for ndx in range(len(chances)):
                    strat = chances[ndx]
                    score = 0.
                    for points in strat:
                        if (points + x_score) >= goal:
                            score += strat[points]
                        else:
                            score += strat[points] * (1. - expected[n_score][x_score + points])

                    if score >= best_score:
                        best_score = score
                        best_strat = ndx + 1
                delta = max(delta, abs(expected[x_score][n_score] - best_score))
                expected[x_score][n_score] = best_score
                strats[x_score][n_score] = best_strat

    print("{} scans complete delta = {:.6f}".format(yyy, delta))
    return expected, strats

def main():
    goal = 100
    chances = solver2(max_strat=goal)

    time1 = time()
    expected1, strat1 = game_strat_approximater(chances, goal=goal, scans=30)
    time2 = time()
    expected2, strat2 = game_strat_approximater2(chances, goal=goal, threshold=10 ** -3)
    time3 = time()
    print("approx. 1:\t{:.3f}s\napprox. 2:\t{:.3f}s".format(time2 - time1, time3 - time2))

    plt.imshow(strat2)
    plt.show()


if __name__ == "__main__":
    main()




