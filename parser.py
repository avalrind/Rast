from rast import rast 
import networkx as nx
import matplotlib.pyplot as plt

class raster :
    '''
    This class is used to load a C program into a raster object.
    '''

    def __init__(self , path) : 
        '''
        This function is used to initialize the raster object.

        Args :
            1) path : The path to the C program.
        '''

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
        '''
        This function is used to remove spaces from a list.

        Args :
            1) lis : The list to remove spaces from.

        Returns :
            The list without spaces.
        '''

        for index in range(len(lis)) :
            
            if lis[index] : lis[index] = lis[index].split()[0]

        return lis

    def remove_cols(self , lis) :
        '''
        This function is used to remove colons from a list.

        Args :
            1) lis : The list to remove colons from.

        Returns :
            The list without colons.
        '''

        for index in range(len(lis)) : 

            if lis[index] : lis[index] = lis[index].split(';')[0]

        return lis

    def gen_ast_cpp(self , body) :
        '''
        This function is used to generate the AST for a C++ program.

        Args :

            1) body : The body of the C++ program.

        Returns :
            The AST for the C++ program.
        '''

        stack = [] 

        if isinstance(body , str) : stack.append(body)
        
        elif isinstance(body , list) :

            index = 0

            while index < len(body) :

                line = body[index]

                line = line.strip()

                if line.startswith('//') : continue

                elif line in self.names : 

                    stack.append(self.names[line])
                    index += 1

                elif line in self.ops : 

                    stack.append(rast.Operator(line))
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

                        function_body = function_body[1:]

                        if function in self.names : stack.append(self.names[function])
                        else : 

                            stack.append(rast.FunctionDef(function , function_body , args))
                            self.names[function] = stack[-1]                        
                        
                        index += 1

                    else : 
                        
                        if line.split()[1] in self.names : stack.append(self.names[line.split()[1]])
                        else : 

                            stack.append(rast.NamedVariable(line.split()[1] , line.split()[0] , line.split()[3].split(';')[0]))
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

                    if_body = if_body[1:]
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

                    for_body = for_body[1:]
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

                    while_body = while_body[1:]
                    stack.append(rast.WhileLoop(condition , while_body))
                    index += 1

                else :

                    if line : 

                        if (line[0] == '"' and line[-1] == '"') or (line[0] == "'" and line[-1] == "'") :

                            stack.append(rast.Variable('str' , line))
                            index += 1

                        else : 

                            line = line.split()

                            for value in line :

                                value = value.split(';')[0]

                                if '.' in value : stack.append(rast.Variable('float' , value))
                                    index += 1
                                
                                elif value.isdigit() : stack.append(rast.Variable('int' , value))
                                    index += 1

                                elif value in self.names : stack.append(self.names[value.split()[0]])
                                    index += 1

                                elif value in self.ops : stack.append(rast.Operator(value))
                                    index += 1

                                else : 

                                    stack.append(value)
                                    index += 1

                    else : index += 1

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
            elif isinstance(value , rast.Return) : stack[index].value = self.gen_ast_cpp(stack[index].value.split())

        return stack

    def load_files(self) : 
        '''
        This function is used to load the files into the raster object.

        Args :
            None
        
        Returns :
            The AST for the C program.
        '''

        if self.load_type == 'cpp' : 
            
            self.ast.body = self.gen_ast_cpp(self.ast.body)
            
            return self.ast
