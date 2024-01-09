class rast : 

    class Include : 

        def __init__(self, name , value) : 
            self.name = name
            self.value = value

    class BuiltInFunction : 

        def __init__(self, name, func) : 
            
            self.name = name
            self.func = func

    class NamedVariable : 

        def __init__(self, name , typer , value) : 
            
            self.name = name
            self.typer = typer
            self.value = value

    class Filename : 

        def __init__(self, name , body) : 

            self.name = name
            self.body = body

    class FunctionDef : 

        def __init__(self , name , body , args) : 

            self.name = name
            self.body = body
            self.args = args

    class Return : 

        def __init__(self , value) : 

            self.value = value

    class SRO : # Scope Resolution Operator
            
        def __init__(self , name , body) : 

            self.name = name
            self.body = body

    class IfDef : 
        
        def __init__(self , condition , body) : 

            self.condition = condition
            self.body = body

    class Operator: 

        def __init__(self , value) : 

            self.value = value
