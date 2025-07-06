import Modules.CommandLineHandler as CLI
import Modules.FileReader as FileReader
import Modules.GuessHandler as Guesser
import Modules.Randomizer as Random


CurrentMode = 1
CurrentlyUsing = []
PreviousIndex = 0


def OpenFile():
    FileWanted = CLI.GetInput("What file do you want to make flashcards with?")

    if (FileWanted.endswith(".txt") == False):
        FileWanted = FileWanted + ".txt"

    ParsedContents = FileReader.ParseFileContents(FileWanted)

    return ParsedContents


def GetValueInDictionary(key, dictionary):
    Found = dictionary.get(key)

    if (Found != None):
        return Found, key
    
    ConvertedToLower = {}

    for convert in dictionary.keys():
        lowered = str.lower(convert)
        ConvertedToLower[lowered] = convert

    KeyFound = ConvertedToLower.get(key)

    if (KeyFound != None):
        return dictionary.get(KeyFound), KeyFound


def GetCategory(fileContents):
    Categories = list(fileContents.keys())
    CategoryCount = len(Categories)

    CategoryListStr = ", ".join(Categories)
    CategoryChosen = CLI.GetInput(f"Found {CategoryCount} categorie(s) to chose from:\n{CategoryListStr}\nIf you have no preference, you can input \"All\" to ignore the category type.\nSeparate categories by commas (,) to use multiple of your choice.")

    if (CategoryChosen.lower() == "all"):
        Using = []
        print("Chose all categories.")

        for cat, data in fileContents.items():
            for d in data:
                d.update({"Category": cat})
                Using.append(d)

        return Using
    
    Combined = []
    Cats = []

    Split = str.split(CategoryChosen, ",")
    Len = len(Split)

    for cat in Split:
        if int(cat):
            Fixed = Categories[int(cat) - 1]
            Found = fileContents.get(Fixed)
        else:
            Found, Fixed = GetValueInDictionary(cat, fileContents)

        if (Found == None):
            print(f"No category found called {cat}.")
            continue

        for x in Found:
            if Len > 1:
                x.update({"Category": Fixed})
            
            Combined.append(x)

        Cats.append(Fixed)

    if (len(Combined) <= 0):
        print("Failed to find the categories given. Please re-run the script.")
        return

    print(f"Chose {", ".join(Cats)}.")

    return Random.RandomizeList(Combined, Random.GetKey())


def GetMode():
    ModeChosen = CLI.GetInput("Do you want to practice in:\n1. Question mode - The question is shown to you, making you have to type out an answer.\n2. Answer mode - The answer is shown to you, making you have to type out the question.")

    if (ModeChosen == "1"):
        return 1
    elif (ModeChosen == "2"):
        return 2
    
    print("Chosen mode not found. Defaulting to 1.")

    return 1


def GetGuessingLimit():
    AmountStr = CLI.GetInput("How many total guesses do you want per question? Input a number larger than 0.")

    Converted = max(abs(int(AmountStr)), 1)

    Guesser.ChangeGuessLimit(Converted)

    HintsOn = CLI.GetInput("Do you want hints? (Y/N)")

    Guesser.ChangeHintsEnabled(HintsOn.lower() == "y")


def GetRandomItemInList():
    global PreviousIndex
    global CurrentlyUsing

    if (PreviousIndex > len(CurrentlyUsing) - 1):
        CurrentlyUsing = Random.RandomizeList(CurrentlyUsing, Random.GetKey())
        PreviousIndex = 0
    
    New = CurrentlyUsing[PreviousIndex]
    PreviousIndex += 1

    return New


def Next():
    Message, BufferCount = CLI.Prettify("\nWhen you're done, input \"exit\" or \"e\" to stop the program.")
    CLI.ClearCLI(Message)

    ChosenData = GetRandomItemInList()

    QuestionKey = CurrentMode == 1 and "Question" or "Answer"
    AnswerKey = CurrentMode == 1 and "Answer" or "Question"

    ShownMessage = f"{ChosenData[QuestionKey]}"

    Category = ChosenData.get("Category")
    if (Category != None):
        ShownMessage = f"Category: {Category}\nInfo: {ShownMessage}"

    #GivenAnswer = CLI.GetInput(ShownMessage)
    ActualAnswer = ChosenData[AnswerKey]
    Source = ChosenData.get("Source") or "No source found."

    Prompt, c = CLI.Prettify(ShownMessage)
    print("\n" + Prompt + "\n")

    Correct = Guesser.StartGuessing(ActualAnswer)

    if (Correct):
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
    GetGuessingLimit()

    CLI.GetInput("When you're ready, input anything into the console in order to start using the flashcards.")

    ContinueGoing = True

    while (ContinueGoing == True):
        Given = Next()

        if (Given.lower() == "exit") or (Given.lower() == "e"):
            ContinueGoing = False

    print("Stopping the program.")


MainFunction()