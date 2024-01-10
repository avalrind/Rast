from rast import rast
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

class graph : 
    '''
    This class is used to generate a graph from a raster object.
    '''

    def __init__(self , node , 
        Filename = ['body'] , 
        Include = ['value'] , 
        NamedVariable = ['typer' , 'value'] , 
        FunctionDef = ['args' , 'body'] , 
        SRO = ['body'] , 
        If = ['condition' , 'body'] , 
        ForLoop = ['initialization' , 'condition' , 'iteration' , 'body'] , 
        WhileLoop = ['condition' , 'body'] , 
        Operator = ['value'] , 
        Return = ['value']) : 

        '''
        This function is used to initialize the graph object.

        Args : 
            1) node : The node to generate the graph from.
            2) Filename : The attributes to include from the Filename node.
            3) Include : The attributes to include from the Include node.
            4) NamedVariable : The attributes to include from the NamedVariable node.
            5) FunctionDef : The attributes to include from the FunctionDef node.
            6) SRO : The attributes to include from the SRO node.
            7) If : The attributes to include from the If node.
            8) ForLoop : The attributes to include from the ForLoop node.
            9) WhileLoop : The attributes to include from the WhileLoop node.
            10) Operator : The attributes to include from the Operator node.
            11) Return : The attributes to include from the Return node.

        Returns :
            None
        '''

    
        self.node = node
        self.Filename = Filename
        self.Include = Include
        self.NamedVariable = NamedVariable
        self.FunctionDef = FunctionDef
        self.SRO = SRO
        self.If = If
        self.ForLoop = ForLoop
        self.WhileLoop = WhileLoop
        self.Operator = Operator
        self.Return = Return

        self.gen_graph()

    def add_nodes(self , node) :
        '''
        This function is used to add nodes to the graph.

        Args :
            1) node : The node to add to the graph.

        Returns :
            None
        ''' 

        if node : 

            if isinstance(node , rast.Filename) : 

                if 'body' in self.Filename : 

                    for value in node.body : 

                        self.g.add_edge(node.graph_name , value.graph_name)
                        self.add_nodes(value)

            elif isinstance(node , rast.NamedVariable) : 

                if 'value' in self.NamedVariable : self.g.add_edge(node.graph_name , node.value)

            elif isinstance(node , rast.FunctionDef) :

                if 'args' in self.FunctionDef : 

                    for value in node.args : 

                        self.g.add_edge(node.graph_name , value.graph_name)
                        self.add_nodes(value)

                if 'body' in self.FunctionDef : 

                    for value in node.body : 

                        self.g.add_edge(node.graph_name , value.graph_name)
                        self.add_nodes(value)

            elif isinstance(node , rast.SRO) : 

                if 'body' in self.SRO : 

                    for value in node.body : 

                        self.g.add_edge(node.graph_name , value.graph_name)
                        self.add_nodes(value)

            elif isinstance(node , rast.If) :

                if 'condition' in self.If : 
                    
                    for value in node.condition : 

                        self.g.add_edge(node.graph_name , value.graph_name)
                        self.add_nodes(value)
                    
                if 'body' in self.If : 

                    for value in node.body : 

                        self.g.add_edge(node.graph_name , value.graph_name)
                        self.add_nodes(value)

            elif isinstance(node , rast.ForLoop) : 

                if 'initialization' in self.ForLoop : 

                    for value in node.initialization : 

                        self.g.add_edge(node.graph_name , value.graph_name)
                        self.add_nodes(value)

                if 'condition' in self.ForLoop : 

                    for value in node.condition : 

                        self.g.add_edge(node.graph_name , value.graph_name)
                        self.add_nodes(value)

                if 'iteration' in self.ForLoop : 

                    for value in node.iteration : 

                        self.g.add_edge(node.graph_name , value.graph_name)
                        self.add_nodes(value)

                if 'body' in self.ForLoop : 

                    for value in node.body : 

                        self.g.add_edge(node.graph_name , value.graph_name)
                        self.add_nodes(value)

            elif isinstance(node , rast.WhileLoop) : 

                if 'condition' in self.WhileLoop : 

                    for value in node.condition : 

                        self.g.add_edge(node.graph_name , value.graph_name)
                        self.add_nodes(value)

                if 'body' in self.WhileLoop : 

                    for value in node.body : 

                        self.g.add_edge(node.graph_name , value.graph_name)
                        self.add_nodes(value)

            elif isinstance(node , rast.Operator) : 

                if 'value' in self.Operator : self.g.add_edge(node.graph_name , node.value)

            elif isinstance(node , rast.Return) :  

                for value in node.value : 

                    self.g.add_edge(node.graph_name , value.graph_name)
                    self.add_nodes(value)

    def gen_graph(self , node) :
        '''
        This function is used to generate the graph.

        Args : 
            1) node : The node to generate the graph from.

        Returns :
            None
        '''

        self.g = nx.Graph()
        self.node = node
        self.add_nodes(self.node)

        plt.figure(figsize=(10,10))

        nx.draw(self.g , graphviz_layout(self.g  , prog = 'dot') , with_labels=True , font_weight='bold')
        plt.show()
