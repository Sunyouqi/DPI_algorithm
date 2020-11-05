import re

class MetaComponent(type):
    def __new__(cls, name, bases, attrs):
        
        
        return type(name, bases, attrs)
        pass
    def __init__(cls, name , bases, attrs):
    
        pass


class Component(metaclass = MetaComponent):
    def __init__(self, name, **kwargs):
        
        self.name = name
        self.type = self.__class__
        
        if isinstance(self, Resistor):
            self.resistance = kwargs["resistance"]
            
        elif isinstance(self, Transistor):
            self.transistor_attr_list = dict()
            for name , value in kwargs.items():
                self.transistor_attr_list[f"{name}"] = value
                
        elif isinstance(self, VoltageSource):
            self.voltage = kwargs["voltage"]
            self.polar = kwargs["polar"]
        #
        #... ... for more types
        

class VoltageSource(Component):
    def __init__(self, name , voltage):
        super().__init__( name = name, voltage = value , polarization = polar)
        
class CurrentSource(Component):
    def __init__(self, name , voltage):
        super().__init__( name = name, current = value , direction = dir , coefficient = coe , voltageControl = v)
        #control voltage is a tuple with positive node and negative node. Voltage difference is Vposnode - Vneganode
        
class Resistor(Component):
    def __init__(self, name , value):
        print(super().__init__)
        super().__init__( name = name, resistance = value)
        pass

class Transistor(Component):
    def __init__(self, name , **attrs):
        print(attrs)
        super().__init__( name, **attrs)
        pass

class SFGraph(object):
    nodes_list = []
    def __init__(self, name , nodes_list):
        self.nodes_list = nodes_list
        
        pass
    def arrange_attr(self):
        # this part depends on the parser output
        pass
            
    def process_nodeList(self):
        for each_node in nodes_list:
            each_node = Node(self.arrange_attr())
        pass


class Node:
    def __init__(self, **kwargs):
        # name of this node
        self.node_name = kwargs["node_name"]
        
        # components is a dictionary stores the information between this node and each of its neighbors. We can access the components between node 1 and node 2 using components["node2"] and returns a list of component objects in between
        self.components = kwargs["components"]
        
        # a list of the adjacent neighbors
        self.neighbors = kwargs["neighbors"]
        
        self.voltage = 0 if kwargs["is_ground"] is True else "TBD"
    
    def in_parallel(self, r1 , r2):
        return 1 / ( 1/r1 + 1/r2 )


    #this is a sketch of structure of what the algorithm will look like
    def DPI_analysis(self):
        #compute impedence of this node
        impedence = 0
        for each_component in self.components:
            if not isinstance(each_component , VoltageSource) and not isinstance(each_component , CurrentSource):
                impedence += self.in_parallel( impedence , each_component.resistance )

        # dpi * short_circuit crruent
        # compute the current flow in or out on each branch connected to this node
            # need further polish
        current_Isc = dict()
        for each_neighbor in self.neighbors:
            for each_component in components[each_neighbor.node_name]:
                # if they are connected by a current source it is complicated.
                if isinstance( each_component , CurrentSource):
                    current_Isc [each_neighbor] .append([ each_component.direction , each_component.coefficient , each_component.voltageControl])
                # if they are connected by resistors simply add 1/R to the current list
                else:
                    current_Isc [each_neighbor]. append( 1 / each_component.resistance )
        self.short_circuit_I = current_Isc
        self.DPImpedence = impedence
    
