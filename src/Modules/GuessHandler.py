import Modules.Randomizer as Randomizer
import time


# The things
GUESS_COUNT = 3
CURRENT_GUESS_COUNT = 0
HINTS_ENABLED = False


# Functions
def Lerp(a, b, t):
    return a + (b - a) * t


def ChangeGuessLimit(newLimit):
    global GUESS_COUNT

    GUESS_COUNT = newLimit


def ChangeHintsEnabled(new):
    global HINTS_ENABLED

    HINTS_ENABLED = new


def CreateHint(answer):
    AnswerLength = (len(answer) - str.count(answer, " "))
    Count = Lerp(0, (AnswerLength * 0.5), (CURRENT_GUESS_COUNT / (GUESS_COUNT - 1)))
    Count = int(Count)

    CanReveal = []
    for i in range(len(answer)):
        if (answer[i] != " "):
            CanReveal.append(i)

    Shuffled = Randomizer.RandomizeList(CanReveal, answer)
    Shuffled = Shuffled[:Count]

    hint = []
    for i, char in enumerate(answer):
        if (char == " "):
            hint.append(" ")
        elif (i in Shuffled):
            hint.append(char)
        else:
            hint.append("_")

    return "".join(hint)


def Guess(guess, answer):
    global CURRENT_GUESS_COUNT
    global GUESS_COUNT

    CURRENT_GUESS_COUNT += 1

    AnsweredRight = (guess.lower() == answer.lower())
    Left = (GUESS_COUNT - CURRENT_GUESS_COUNT)

    if AnsweredRight:
        CURRENT_GUESS_COUNT = 0
        return True, 1
    elif (Left <= 0):
        CURRENT_GUESS_COUNT = 0
        return False, 0
    elif (guess.lower() == "!pass"):
        return False, 0
    else:
        return False, Left


def StartGuessing(answer):
    CurrentAmountLeft = GUESS_COUNT
    NotCorrect = True

    while (CurrentAmountLeft > 0) and (NotCorrect == True):
        NewGuess = input("")
        Correct, GuessesLeft = Guess(NewGuess, answer)

        NotCorrect = (Correct == False)
        CurrentAmountLeft = GuessesLeft

        if (NotCorrect) and (GuessesLeft > 0):
            HintPortion = ""

            if HINTS_ENABLED:
                HintPortion = f"\nHint: {CreateHint(answer)}"

            print(f"Wrong! Guesses left: {GuessesLeft}{HintPortion}\n")

    return (NotCorrect == False)