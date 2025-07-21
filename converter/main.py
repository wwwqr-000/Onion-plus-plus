import sys, os

platform = ""
mainFile = ""

try:
    mainFile = sys.argv[1]
    platform = sys.argv[2]
    
except Exception:
    print("Use this command with arguments: 'FILENAME PLATFORM'")
    exit(1)
    
from translator import Translator

Translator.onppToCpp(mainFile, "out/main.cpp", platform)

if (platform == "linux"):
    os.system("cd out && g++ main.cpp")
    
print("Done!")