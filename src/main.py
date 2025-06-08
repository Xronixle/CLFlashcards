import Modules.CommandLineHandler as CLI
import Modules.FileReader as FileReader

import random
import time


random.seed(time.time())


CurrentMode = 1
CurrentlyUsing = []


def OpenFile():
    FileWanted = CLI.GetInput("What file do you want to make flashcards with?")

    if (FileWanted.endswith(".txt") == False):
        FileWanted = FileWanted + ".txt"

    ParsedContents = FileReader.ParseFileContents(FileWanted)

    return ParsedContents


def GetCategory(fileContents: dict):
    Categories = fileContents.keys()
    CategoryCount = len(Categories)

    CategoryListStr = ", ".join(Categories)
    CategoryChosen = CLI.GetInput(f"Found {CategoryCount} categorie(s) to chose from:\n{CategoryListStr}\nIf you have no preference, you can input \"All\" to ignore the category type.")

    Using = []
    if (CategoryChosen.lower() == "all"):
        print("Chose all categories.")

        for cat, data in fileContents.items():
            for d in data:
                d.update({"Category": cat})
                Using.append(d)

        return Using
    
    if (fileContents[CategoryChosen] != None):
        Using = fileContents[CategoryChosen]
    else:
        print("The chosen category wasn't found. Please re-run the script to try again.")
        return

    print(f"Chose {CategoryChosen}.")

    return Using


def GetMode():
    ModeChosen = CLI.GetInput("Do you want to practice in:\n1. Question mode - The question is shown to you, making you have to type out an answer.\n2. Answer mode - The answer is shown to you, making you have to type out the question.")

    if (ModeChosen == "1"):
        return 1
    elif (ModeChosen == "2"):
        return 2
    
    print("Chosen mode not found. Defaulting to 1.")

    return 1


def GetRandomItemInList(list):
    Length = len(list)
    Index = random.randint(0, Length-1)

    return list[Index]


def Next():
    Message, BufferCount = CLI.Prettify("\nAfter attempting to answer, input \"next\" or \"n\" to get the next random card or anything at all to stop the program.")
    CLI.ClearCLI(Message)

    ChosenData = GetRandomItemInList(CurrentlyUsing)

    QuestionKey = CurrentMode == 1 and "Question" or "Answer"
    AnswerKey = CurrentMode == 1 and "Answer" or "Question"

    ShownMessage = f"{ChosenData[QuestionKey]}"

    Category = ChosenData.get("Category")
    if (Category != None):
        ShownMessage = f"Category: {Category}\nInfo: {ShownMessage}"

    GivenAnswer = CLI.GetInput(ShownMessage)
    ActualAnswer = ChosenData[AnswerKey]
    Source = ChosenData.get("Source") or "No source found."

    if (GivenAnswer.lower() == ActualAnswer.lower()):
        print("\nCorrect!")
    else:
        print(f"\nThe correct answer is:\n{ActualAnswer}")

    print(f"Source: {Source}")

    Separator = "-" * BufferCount
    return input(Separator + "\n" + "Action: ")


def MainFunction():
    global CurrentMode
    global CurrentlyUsing

    StartMessage, _ = CLI.Prettify("Flashcard testing thing I made because I wanted something that could be ran offline technically.")
    CLI.ClearCLI(StartMessage)

    Contents = OpenFile()
    CurrentlyUsing = GetCategory(Contents)

    if (CurrentlyUsing == None):
        return
    
    CurrentMode = GetMode()

    CLI.GetInput("When you're ready, input anything into the console in order to start using the flashcards.")

    ContinueGoing = True

    while (ContinueGoing == True):
        Given = Next()

        if (Given.lower() != "next" and Given.lower() != "n"):
            ContinueGoing = False

    print("Stopping the program.")


MainFunction()