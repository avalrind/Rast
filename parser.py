from rast import rast 
import os

class parser :

    def __init__(self , path) : 

        self.path = path 
        self.names = {}

        if self.path.endswith('.cpp') : 
        
            self.load_type = 'cpp'
            self.ast = rast.Filename(self.path , open(self.path , 'r').read().split('\n'))

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

                if line in self.names : 

                    stack.append(self.names[line])
                    index += 1

                elif line == '==' : 

                    stack.append(rast.Operator('=='))
                    index += 1
                


                elif line.startswith('#include') : 

                    stack.append(rast.Include(line.split(' ')[1] , line))
                    index += 1
                
                elif line.startswith('int') or line.startswith('void') :
    
                    if line.endswith(';') : 
                        
                        if line.split()[1] in self.names : stack.append(self.names[line.split()[1]])
                        else : 
                            stack.append(rast.NamedVariable(line.split()[1] , line.split()[0] , line.split()[2].split(';')))
                            self.names[line.split()[1]] = stack[-1]
                        index += 1              
                    
                    elif line.endswith(')') : 

                        function = line.split()[1]
                        function_body = []

                        args = line.split('(')[1].split(')')[0].split(',')
                        args = self.remove_spaces(args)

                        index += 1
                        line = body[index]

                        while not line.endswith('}') : 
                            
                            function_body.append(line)
                            index += 1
                            line = body[index]

                        function_body.append(line)
                        if function in self.names : stack.append(self.names[function])
                        else : 
                            stack.append(rast.FunctionDef(function , function_body , args))
                            self.names[function] = stack[-1]                        
                        index += 1

                    else : index += 1

                elif line.startswith('if') : 

                    condition = line.split('(')[1].split(')')[0]

                    if_body = []
                    index += 1
                    line = body[index]

                    while not line.endswith('}') :


                        if_body.append(line)
                        index += 1
                        line = body[index]

                    if_body.append(line)
                    stack.append(rast.IfDef(condition , if_body))
                    index += 1

                elif line.startswith('std') :
                    
                    stack.append(rast.SRO(line.split(' ')[1] , self.remove_cols(line.split('<<')[1:])))
                    index += 1

                elif line.startswith('return') : 

                    stack.append(rast.Return(line.split(' ')[1]))
                    index += 1

                else :

                    if line : 

                        if (line[0] == '"' and line[-1] == '"') or (line[0] == "'" and line[-1] == "'") :

                            stack.append(rast.BuiltInFunction('str' , line))
                            index += 1

                        elif line in self.names :

                            stack.append(self.names[line])
                            index += 1

                        elif '.' in line : 

                            stack.append(rast.BuiltInFunction('float' , line))
                            index += 1
                        
                        elif line.isdigit() :

                            stack.append(rast.BuiltInFunction('int' , line))
                            index += 1

                        else : 

                            stack.append(line)
                            index += 1

                    else : index += 1

        for index in range(len(stack)) : 

            value = stack[index]

            if isinstance(value , rast.FunctionDef) : 

                stack[index].body = self.gen_ast_cpp(stack[index].body)
                stack[index].args = self.gen_ast_cpp(stack[index].args)

            elif isinstance(value , rast.IfDef) :
                
                stack[index].body = self.gen_ast_cpp(stack[index].body)
                stack[index].condition = self.gen_ast_cpp(stack[index].condition.split())
            
            elif isinstance(value , rast.SRO) : stack[index].body = self.gen_ast_cpp(stack[index].body)

        return stack

    def load_files(self) : 

        if self.load_type == 'cpp' : 
            
            self.ast.body = self.gen_ast_cpp(self.ast.body)
            
            return self.ast
