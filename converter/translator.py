from lark import Lark, Transformer

class ToCpp(Transformer):
    grammar = r"""
    %import common.CNAME
    %import common.INT
    %import common.FLOAT
    %import common.SIGNED_INT
    %import common.SIGNED_FLOAT
    %import common.SIGNED_NUMBER
    %import common.NUMBER
    %import common.ESCAPED_STRING
    %import common.WS
    %import common.NEWLINE
    %import common.LETTER
    %import common.DIGIT
    %import common.WS
    %ignore WS
    
    //Defining definitions
    STRING: ESCAPED_STRING
    TYPE: CNAME
    argList: arg ("," arg)*
    arg: TYPE CNAME
    ?content: (balancedParen | /[^()]+/)*
    balancedParen: "(" content ")"
    //

    start: func+

    //Functions
    func: CNAME "=" "(" [argList] ")" "=>" "{" content "}" "<" TYPE ">"
    funcCall: CNAME "(" [argList] ")" ";"
    //

    //Logic checkers
    ifStatement: "if" "(" arg ")" "{" content "}"
    //
    
    
    //Returners
    returnCall: "return" [CNAME]
    //
    """
    
    def start(self, items):
        return '\n\n'.join(items)
    
    def func(self, items):
        name = str(items[0])
        args = items[1] if isinstance(items[1], list) else []
        content = items[2] if isinstance(items[2], str) else "".join(map(str, items[2]))
        returnType = str(items[3])
        
        print(name)
        
        return ''

    
    
class Translator():
    def onppToCpp(onppFile, cppFile, platform):
        try: 
            file = open(onppFile, "r")
            mainFileCode = file.read()
            file.close()
            
        except Exception:
            print(f"Error: could not open file '{onppFile}'")
            exit(1)
            
            
        parser = Lark(ToCpp.grammar, parser='lalr', transformer=ToCpp())
        outBuff = parser.parse(mainFileCode)
        
        #Manipulating outBuff
        outBuff = outBuff.replace("string", "std::string")
        header = ""
        
        if (platform == "linux" or platform == "windows" or platform == "mac"):
            header += "#include <iostream>\n"
            header += "#define root main\n"
            header += "void say(std::string txt) { std::cout << txt; }\n"
        
        else:
            print(f"Error: platform '{platform}' not supported!")
            exit(2)
        
        if (platform == "linux"):None
        if (platform == "windows"): None
        if (platform == "mac"): None
        
        outBuff = header + "\n\n" + outBuff
        #
        
        outFile = open(cppFile, "w")
        outFile.write(outBuff)
        outFile.close()