import random
from time import time

DICE_SIDES = 6
FAILS = 1

def simulation(turns=10**6, max_strat=70):
    """
    This is a simulation for the game pig assuming that strategies are based on stop bidding when you reach a particular
    score for a round. This function will return the expected value of each turn given a particular goal score.
    :param turns: int this is how many turns the function will simulate to get the answer.
    :param max_strat: int The simulation will give expected returns for each goal score up to this number.
    :return: this will return a list of floats with max_strat entries where each entry is an expected return on a
    single turn.
    """
    hist = [0] * max_strat
    for turn in range(1,turns+1):
        turn_score = 0
        while turn_score < max_strat:
            roll = random.randint(1, DICE_SIDES)
            if roll <= FAILS:
                break
            for ndx in range(turn_score,min(turn_score + roll, max_strat)):
                hist[ndx] += (turn_score + roll)
            turn_score += roll
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



def main():
    start = time()
    results = simulation()
    solvertime = time()
    results2 = solver()
    end = time()
    for ndx in range(len(results)):
        print(ndx+1, results[ndx], results2[ndx])

    print("The simulation time: \t{0} s \nThe solver time: \t{1} s".format(solvertime - start, end - solvertime))
if __name__ == "__main__":
    main()
