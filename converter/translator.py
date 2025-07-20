from lark import Lark, Transformer

class ToCpp(Transformer):
    grammar = r"""
    ALLVALUES: /[a-zA-Z_][a-zA-Z0-9_]*/

    start: func+

    func: func_name "=" "(" [arguments] ")" "=>" "{" stmt* "}" "<" TYPE ">"
    
    func_name: ALLMETHODNAMES

    arguments: argument ("," argument)*

    argument: ALLVALUES ALLVALUES

    ?stmt: say_stmt | return_stmt

    say_stmt: "say" "(" STRING ")" ";"
    return_stmt: "return" [NUMBER] ";"

    TYPE: ALLVALUES
    
    ALLMETHODNAMES: ALLVALUES

    STRING: ESCAPED_STRING
    NUMBER: /\d+/

    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
    """
    
    def start(self, items):
        return '\n\n'.join(items)

    def func(self, items):
        func_name = items[0]          # now first item is the function name
        return_type = items[-1]       # last item is the return type
        rest = items[1:-1]            # everything in between

        if rest and isinstance(rest[0], str):
            arguments = rest[0]
            stmts = rest[1:]
        else:
            arguments = ''
            stmts = rest

        stmts = [stmt for stmt in stmts if stmt is not None]
        args = arguments if arguments else ''
        body = '\n'.join(stmts)

        return f'{return_type} {func_name}({args}) {{\n{body}\n}}'



    def arguments(self, items): return ', '.join(items)
    def argument(self, items): return f'{items[0]} {items[1]}'
    def say_stmt(self, items): return f'std::cout << {items[0]};'
    
    def return_stmt(self, items):
        if (items[0] == None): items = None
        if (items): return f'return {items[0]};'
        return f'return;'
    
    def TYPE(self, token): return str(token)
    def ALLVALUES(self, token): return str(token)
    def func_name(self, items): return str(items[0])
    
    
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
        header = """
        #include <iostream>
        """
        
        #if (platform == "linux"):
        
        outBuff = header + "\n\n" + outBuff
        #
        
        outFile = open(cppFile, "w")
        outFile.write(outBuff)
        outFile.close()