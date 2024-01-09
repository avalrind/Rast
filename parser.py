from rast import rast 
import os

class parser :

    def __init__(self , path) : 

        self.path = path 

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

                if line.startswith('#include') : 

                    stack.append(rast.Include(line.split(' ')[1] , line))
                    index += 1
                
                elif line.startswith('int') or line.startswith('void') :
    
                    if line.endswith(';') : 

                        stack.append(rast.NamedVariable(line.split()[1] , line.split()[0] , line.split()[2].split(';')))
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
                        stack.append(rast.FunctionDef(function , function_body , args))
                        index += 1

                    else : index += 1

                elif line.startswith('    ') : 

                    line = line.split('    ')[1]

                    if line.startswith('std') :
                        
                        stack.append(rast.SRO(line.split(' ')[1] , self.remove_cols(line.split('<<')[1:])))
                        index += 1

                    elif line.startswith('return') : 

                        stack.append(rast.Return(line.split(' ')[1]))
                        index += 1

                    else : index += 1
                
                else :

                    stack.append(line)
                    index += 1

        for index in range(len(stack)) : 

            value = stack[index]

            if isinstance(value , rast.FunctionDef) : 
                
                stack[index].body = self.gen_ast_cpp(stack[index].body)
                stack[index].args = self.gen_ast_cpp(stack[index].args)
                
            elif isinstance(value , rast.SRO) : stack[index].body = self.gen_ast_cpp(stack[index].body)

        return stack

    def load_files(self) : 

        if self.load_type == 'cpp' : 
            
            self.ast.body = self.gen_ast_cpp(self.ast.body)
            
            return self.ast
