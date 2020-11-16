import re

class test:
    def __init__(self):
        pass

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
           
                
        elif isinstance(self, VoltageSource):
            self.voltage = kwargs["voltage"]
            self.polar = kwargs["polarization"]
        
        elif isinstance(self, CurrentSource):
            self.current = kwargs["current"]
            self.direction = kwargs["direction"]
            pass
        #
        #... ... for more types
        

class VoltageSource(Component):
    def __init__(self, name , voltage, polar):
        super().__init__( name = name, voltage = voltage , polarization = polar)
    
        
class CurrentSource(Component):
    def __init__(self, name , current, direc):
        super().__init__( name = name , current = current, direction = direc)
        #control voltage is a tuple with positive node and negative node. Voltage difference is Vposnode - Vneganode
    def __repr__(self):
        return "current source:" + self.name + "current:" + str(self.direction) + self.current
        
class Resistor(Component):
    def __init__(self, name , value):
        #print(super().__init__)
        super().__init__( name = name, resistance = value)
        
    def __repr__(self):
        return "Resistor:" + self.name + " resistance:" + str(self.resistance)


class SFGraph(object):
    nodes_list = []
    def __init__(self , nodes_list):
        self.nodes_list = nodes_list
        
        pass
    def arrange_attr(self):
        # this part depends on the parser output
        pass
            
    def process_nodeList(self):
        for each_node in self.nodes_list:
            each_node.DPI_analysis()
        pass
    def __repr__(self):
        result = []
        for each_node in self.nodes_list:
            result.append(each_node.__repr__())
        return '\n'.join(result)


class Node:
    def __init__(self, **kwargs):
        # name of this node
        self.voltage = 0 if kwargs["is_ground"] is True else ("V" + kwargs["node_name"].lower())
        if self.voltage == 0:
            return 
        self.short_circuit_I = "0"
        self.DPImpedence = "0"

        self.node_name = kwargs["node_name"]
        
        # components is a dictionary stores the information between this node and each of its neighbors. We can access the components between node 1 and node 2 using components["node2"] and returns a list of component objects in between
        self.components = kwargs["components"]
        
        # a list of the adjacent neighbors
        self.neighbors = kwargs["neighbors"]
        
    def __repr__(self):
        if self.voltage == 0:
            return "ground"
        return "voltage: " + self.voltage + "\n short circuit current: "+ self.short_circuit_I + "\n  driving point impedence:" + self.DPImpedence
    
    def in_parallel(self, r1 , r2):
        return 1 / ( 1/r1 + 1/r2 )


    #this is a sketch of structure of what the algorithm will look like
    def DPI_analysis(self):
        #compute impedence of this node
        if self.voltage == 0:
            return
        impedence = ""
        for component, node in self.components.items():
            if not isinstance(component , VoltageSource) and not isinstance(component , CurrentSource):
                impedence +=   (component.name + "//")
        impedence = impedence[:-2]
        # dpi * short_circuit crruent
        # compute the current flow in or out on each branch connected to this node
            # need further polish
        current_Isc = ""
        for component , node in self.components.items():
            
                # if they are connected by a current source it is complicated.
            if isinstance( component , CurrentSource):
                current_Isc += ( component.direction )
                current_Isc += ( component.current )
                # if they are connected by resistors simply add 1/R to the current list
            elif node.voltage != 0:
                current_Isc += ( " + " + node.voltage + '/' + component.name + " " )
        #current_Isc = current_Isc[:-1]
        if current_Isc == "":
            current_Isc = "0"
        if impedence == "":
            impedence = "0"
        #print("here")
        self.short_circuit_I = current_Isc
        self.DPImpedence = impedence
    
