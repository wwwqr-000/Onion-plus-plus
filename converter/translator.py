from lark import Lark, Transformer

class ToCpp(Transformer):
    grammar = r"""
    ALLVALUES: /[a-zA-Z_][a-zA-Z0-9_]*/

    start: func+

    func: func_name "=" "(" [arguments] ")" "=>" "{" stmt* "}" "<" TYPE ">"
    
    if_statement_inline: "if" "(" if_statement_inline_args ")" ":" if_statement_inline_content ";"
    
    if_statement: "if" "(" if_statement_inline_args ")" "{" stmt* "}"
    
    func_name: ALLMETHODNAMES
    
    func_call: func_name "(" [call_args] ")" ";"
    
    call_args: call_arg ("," call_arg)*
    call_arg: STRING | NUMBER | ALLVALUES
    
    if_statement_inline_args: /[^)]+/
    if_statement_inline_content: /[^;]+/

    arguments: argument ("," argument)*

    argument: ALLVALUES ALLVALUES

    ?stmt: func_call
        | return_stmt
        | if_statement_inline
        | if_statement

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
        func_name = items[0]
        return_type = items[-1]
        rest = items[1:-1]

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
    
    def func_call(self, items):
        funcName = items[0]
        arguments = items[1]
        if (arguments != None): arguments = arguments.children[0].children[0].value
        else: arguments = ""
        
        return f"{funcName}({arguments});"
    
    def return_stmt(self, items):
        if (items[0] == None): items = None
        if (items): return f'return {items[0]};'
        return f'return;'
    
    def TYPE(self, token): return str(token)
    def ALLVALUES(self, token): return str(token)
    def func_name(self, items): return str(items[0])
    
    def if_statement(self, items):
        condition = items[0].children[0]
        stmts = items[1:]
        body = ''.join(stmts)
        return f'if ({condition}) {{ {body} }}'
    
    def if_statement_inline(self, items):
        conditionTree = items[0]
        contentTree = items[1]
        
        condition = conditionTree.children[0].value
        content = contentTree.children[0].value
        
        if (items[0] == None): items = None
        return f'if ({condition}) {{ {content}; }}'
    
    
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