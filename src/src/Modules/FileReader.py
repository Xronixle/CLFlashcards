def GetFileData(fileName):
    Path = f"{fileName}"

    Contents = ""

    with open(Path, "r") as file:
        Contents = file.read()
        file.close()

    return Contents


def ParseFileContents(file):
    FileContents = GetFileData(file)
    Split = str.split(FileContents, "\n")

    Full = {}
    
    CategoryKey = "NOTFOUND"
    CurrentCategoryData = []

    for lineData in Split:
        if (lineData == ""):
            continue

        if (lineData.startswith("#") == True):
            continue

        if (lineData.startswith("//") == True):
            if (CategoryKey != "NOTFOUND"):
                Full[CategoryKey] = CurrentCategoryData

            CurrentCategoryData = []
            CategoryKey = lineData.removeprefix("// ")
            
            continue

        lineData = str.replace(lineData, "||", "\n")
        LineSplit = str.split(lineData, " - ")

        Source = None

        try:
            Source = LineSplit[2]
        except IndexError:
            Source = None
        
        LineDict = {
            "Question": LineSplit[0],
            "Answer": LineSplit[1],
            "Source": Source
        }

        CurrentCategoryData.append(LineDict)

    Full[CategoryKey] = CurrentCategoryData
    CurrentCategoryData = []

    return Full