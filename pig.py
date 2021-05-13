import random
from time import time

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

def main():
    strat = 100
    start = time()
    print("Start simulation.")
    #results = simulation(max_strat=strat)

    results2 = solver(max_strat=strat)
    solvertime = time()
    print("Start solver.")
    results3 = solver2(max_strat=strat)
    end = time()
    for ndx in range(len(results2)):
        print(sum([results3[ndx][x] for x in results3[ndx]]))
        print(sum([results3[ndx][x]*x for x in results3[ndx]]))
        print("{}  \t{:.6f}  \t{}\n\n\n".format(ndx+1, results2[ndx], results3[ndx]))

    print("The simulation time: \t{0} s \nThe solver time: \t{1} s".format(solvertime - start, end - solvertime))

 
if __name__ == "__main__":
    main()




