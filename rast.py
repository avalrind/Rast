class rast : 
    '''
    This module contains the classes that represent the AST of a C program.
    '''

    class Include : 
        '''
        This class represents an include statement in a C program.
        '''

        def __init__(self, name , value) :
            '''
            This function is used to initialize the Include class.

            Args :
                1) name : The name of the include statement.
                2) value : The value of the include statement.

            Returns :
                None
            ''' 

            self.name = name
            self.value = value
            self.graph_name = f'Include {name}'

    class NamedVariable : 
        '''
        This class represents a named variable in a C program.
        '''

        def __init__(self, name , typer , value) : 
            '''
            This function is used to initialize the NamedVariable class.

            Args :
                1) name : The name of the variable.
                2) typer : The type of the variable.
                3) value : The value of the variable.

            Returns :
                None
            '''
            
            self.name = name
            self.typer = typer
            self.value = value
            self.graph_name = f'Variable {name}'

    class Variable :
        '''
        This class represents a variable in a C program.
        '''

        def __init__(self , typer , value) : 
            '''
            This function is used to initialize the Variable class.

            Args :
                1) typer : The type of the variable.
                2) value : The value of the variable.

            Returns :
                None
            '''

            self.typer = typer
            self.value = value
            self.graph_name = f'Variable {value}'

    class Filename : 
        '''
        This class represents a filename in a C program.
        '''

        def __init__(self, name , body) : 
            '''
            This function is used to initialize the Filename class.

            Args :
                1) name : The name of the filename.
                2) body : The body of the filename.

            Returns :
                None
            '''

            self.name = name
            self.body = body
            self.graph_name = f'Filename {name}'

    class FunctionDef :
        '''
        This class represents a function definition in a C program.
        ''' 

        def __init__(self , name , body , args) : 
            '''
            This function is used to initialize the FunctionDef class.

            Args :
                1) name : The name of the function.
                2) body : The body of the function.
                3) args : The arguments of the function.

            Returns :
                None
            '''

            self.name = name
            self.body = body
            self.args = args
            self.graph_name = f'Function {name}'

    class Return : 
        '''
        This class represents a return statement in a C program.
        '''

        def __init__(self , value) : 
            '''
            This function is used to initialize the Return class.

            Args :
                1) value : The value of the return statement.

            Returns :
                None
            '''

            self.value = value
            self.graph_name = f'Return'

    class SRO :
        '''
        This class represents a scope resolution operator in a C program.
        '''
            
        def __init__(self , name , body) :
            '''
            This function is used to initialize the SRO class.

            Args :
                1) name : The name of the scope resolution operator.
                2) body : The body of the scope resolution operator.

            Returns :
                None
            ''' 

            self.name = name
            self.body = body
            self.graph_name = f'SRO {name}'

    class If : 
        '''
        This class represents an if statement in a C program.
        '''
        
        def __init__(self , condition , body) : 
            '''
            This function is used to initialize the If class.

            Args :
                1) condition : The condition of the if statement.
                2) body : The body of the if statement.

            Returns :
                None
            '''

            self.condition = condition
            self.body = body
            self.graph_name = f'If'

    class ForLoop : 
        '''
        This class represents a for loop in a C program.
        '''

        def __init__(self , initalization , condition , iteration , body) :
            '''
            This function is used to initialize the ForLoop class.

            Args :
                1) initalization : The initalization of the for loop.
                2) condition : The condition of the for loop.
                3) iteration : The iteration of the for loop.
                4) body : The body of the for loop.

            Returns :
                None
            ''' 

            self.initalization = initalization
            self.condition = condition
            self.iteration = iteration
            self.body = body
            self.graph_name = f'ForLoop'

    class Operator: 
        '''
        This class represents an operator in a C program.
        '''

        def __init__(self , value) : 
            '''
            This function is used to initialize the Operator class.

            Args :
                1) value : The value of the operator.

            Returns :
                None
            '''

            self.value = value
            self.graph_name = f'Operator {value}'

    class WhileLoop : 
        '''
        This class represents a while loop in a C program.
        '''

        def __init__(self , condition , body) : 
            '''
            This function is used to initialize the WhileLoop class.

            Args :
                1) condition : The condition of the while loop.
                2) body : The body of the while loop.

            Returns :
                None
            '''

            self.condition = condition
            self.body = body
            self.graph_name = f'WhileLoop'
