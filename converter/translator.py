mainFunctionName = "root"


def getFileContent(file):
    try:
        file = open(file, "r")
        fileContent = file.read()
        file.close()
        
        return fileContent

    except FileNotFoundError:
        print(f"Error: '{file}' not found!")
        exit(1)
        
    except Exception:
        print("Error: unknown error, something went wrong!")
        exit(2)
        
rootBuff = getFileContent("root.onpp")

for i, c in enumerate(rootBuff):
    cNext = rootBuff[i + 1]
    
    spaceBuff = ""
    setSignBuff = ""
    equalSignBuff = ""
    bracketOpenBuff = ""
    bracketCloseBuff = ""
    blockBracketOpenBuff = ""
    blockBracketCloseBuff = ""
    curlBracketOpenBuff = ""
    curlBracketCloseBuff = ""
    greaterThanBuff = ""
    smallerThenBuff = ""
    
    if (c != ' '): spaceBuff += c
    else: spaceBuff = ""
    
    # --> W.I.P <--
    
    # if (c != '=' and cNext != '='): setSignBuff += c
    # elif (c != '='):
    # else: equalSignBuff = ""
    
    # if (c != '=' and cNext != '='): equalSignBuff += c
    # else: equalSignBuff = ""
    
    