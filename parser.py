from rast import rast 
import os

class parser :

    def __init__(self , path) : 

        self.path = path 
        self.names = {}

        if self.path.endswith('.cpp') : 
        
            self.load_type = 'cpp'
            self.ast = rast.Filename(self.path , open(self.path , 'r').read().split('\n'))
            self.ops = ['==' , '=' , '<' , '>' , '<=' , '>=' , '!=' , '++']

        elif self.path.endswith('.c') : self.load_type = 'c'
        elif self.path.endswith('.py') : self.load_type = 'py'
        elif self.path.endswith('.java') : self.load_type = 'java'

    def remove_spaces(self , lis) : 

        for index in range(len(lis)) :
            
            if lis[index] : lis[index] = lis[index].split()[0]

        return lis

    def remove_cols(self , lis) :

        for index in range(len(lis)) : 

            if lis[index] : lis[index] = lis[index].split(';')[0]

        return lis

    def gen_ast_cpp(self , body) :

        stack = [] 

        if isinstance(body , str) : stack.append(body)
        
        elif isinstance(body , list) :

            index = 0

            while index < len(body) :

                line = body[index]

                line = line.strip()

                # print(line)
                if line.startswith('//') : continue

                elif line in self.names : 

                    stack.append(self.names[line])
                    index += 1

                elif line in self.ops : 

                    stack.append(rast.Operator('=='))
                    index += 1
                
                elif line.startswith('#include') : 

                    stack.append(rast.Include(line.split(' ')[1] , line))
                    index += 1
                
                elif line.startswith('int') or line.startswith('void') :
    
                    if line.endswith(')') : 

                        function = line.split()[1]
                        function_body = []

                        args = line.split('(')[1].split(')')[0].split(',')
                        args = self.remove_spaces(args)

                        index += 1
                        line = body[index]
                        line = line.strip()

                        braces = []

                        while True:

                            if line.startswith('{') : braces.append('{')
                            elif line.endswith('}') : braces.pop()

                            if len(braces) == 0 : break
                            
                            function_body.append(line)
                            index += 1
                            line = body[index]
                            line = line.strip()

                        function_body.append(line)

                        if function in self.names : stack.append(self.names[function])
                        else : 

                            stack.append(rast.FunctionDef(function , function_body , args))
                            self.names[function] = stack[-1]                        
                        
                        index += 1

                    else : 
                        
                        if line.split()[1] in self.names : stack.append(self.names[line.split()[1]])
                        else : 

                            stack.append(rast.NamedVariable(line.split()[1] , line.split()[0] , line.split()[2].split(';')))
                            self.names[line.split()[1]] = stack[-1]
                        
                        index += 1              
                    
                elif line.startswith('if') : 

                    condition = line.split('(')[1].split(')')[0]

                    if_body = []
                    index += 1
                    line = body[index]
                    line = line.strip()

                    braces = []

                    while True :

                        if line.startswith('{') : braces.append('{')
                        elif line.endswith('}') : braces.pop()

                        if len(braces) == 0 : break

                        if_body.append(line)
                        index += 1
                        line = body[index]
                        line = line.strip()

                    if_body.append(line)
                    stack.append(rast.If(condition , if_body))
                    index += 1

                elif line.startswith('std') :
                    
                    stack.append(rast.SRO(line.split(' ')[1] , self.remove_cols(line.split('<<')[1:])))
                    index += 1

                elif line.startswith('return') : 

                    stack.append(rast.Return(line.split(' ')[1]))
                    index += 1

                elif line.startswith('for') :

                    initalization = line.split(maxsplit = 1)[1].split(';')[0][1:]
                    condition = line.split(maxsplit = 1)[1].split(';')[1]
                    iteration = line.split(maxsplit = 1)[1].split(';')[2][:-1]

                    for_body = []
                    index += 1
                    line = body[index]

                    while not line.endswith('}') :

                        for_body.append(line)
                        index += 1
                        line = body[index]

                    for_body.append(line)
                    stack.append(rast.ForLoop(initalization , condition , iteration , for_body))
                    index += 1

                elif line.startswith('while') : 

                    condition = line.split('(')[1].split(')')[0]

                    while_body = []
                    index += 1
                    line = body[index]

                    while not line.endswith('}') :

                        while_body.append(line)
                        index += 1
                        line = body[index]

                    while_body.append(line)
                    stack.append(rast.WhileLoop(condition , while_body))
                    index += 1

                else :

                    if line : 

                        line = line.split()

                        for value in line : 

                            value = value.split(';')[0]

                            if (value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == "'") :

                                stack.append(rast.BuiltInFunction('str' , value))
                                index += 1

                            elif '.' in value : 

                                stack.append(rast.BuiltInFunction('float' , value))
                                index += 1
                            
                            elif value.isdigit() :

                                stack.append(rast.BuiltInFunction('int' , value))
                                index += 1

                            elif value.split()[0] in self.names : 

                                stack.append(self.names[value.split()[0]])
                                index += 1

                            elif value in self.ops :

                                stack.append(rast.Operator(value))
                                index += 1

                            else : 

                                stack.append(value)
                                index += 1

                    else : index += 1
        # print(stack)
        for index in range(len(stack)) : 

            value = stack[index]

            if isinstance(value , rast.FunctionDef) : 

                stack[index].body = self.gen_ast_cpp(stack[index].body)
                stack[index].args = self.gen_ast_cpp(stack[index].args)

            elif isinstance(value , rast.If) :
                
                stack[index].body = self.gen_ast_cpp(stack[index].body)
                stack[index].condition = self.gen_ast_cpp(stack[index].condition.split())

            elif isinstance(value , rast.ForLoop) :

                stack[index].body = self.gen_ast_cpp(stack[index].body)
                stack[index].initalization = self.gen_ast_cpp([(stack[index].initalization)])
                stack[index].condition = self.gen_ast_cpp(stack[index].condition.split())
                stack[index].iteration = self.gen_ast_cpp(stack[index].iteration.split())

            elif isinstance(value , rast.WhileLoop) :

                stack[index].body = self.gen_ast_cpp(stack[index].body)
                stack[index].condition = self.gen_ast_cpp(stack[index].condition.split())
            
            elif isinstance(value , rast.SRO) : stack[index].body = self.gen_ast_cpp(stack[index].body)

        return stack

    def load_files(self) : 

        if self.load_type == 'cpp' : 
            
            self.ast.body = self.gen_ast_cpp(self.ast.body)
            
            return self.ast
