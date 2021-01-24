import re
import networkx as nx
import circuit as cir

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
            
        
        elif isinstance(self, CurrentSource):
            self.current = kwargs["current"]
            self.direction = kwargs["direction"]
            
        elif isinstance(self, Capacitor):
            self.capacitance = kwargs["capacitance"]
        
        #
        #... ... for more types
        

class VoltageSource(Component):
    def __init__(self, name , voltage):
        super().__init__( name = name, voltage = voltage )
    
        
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

class Capacitor(Component):
    def __init__(self, name , capacitance):
        super().__init__( name = name , capacitance = capacitance)
    
    def __repr__(self):
        return "Capacitance:" + self.name + " capacitance:" + str(self.capacitance)
        


class SFGraph(object):
    
    def __init__(self , nodes_list):
        self.nodes_list = nodes_list
        
        pass
    def arrange_attr(self):
        # this part depends on the parser output
        pass
    def generate(self):
        self.short_circuit_nodes = {}
        self.edge_list = []
        for k , v in self.nodes_list.items():
            if v.voltage != 0:
                name = "Isc" + k[1:]
                self.short_circuit_nodes[name] = Node(node_name = name , is_ground = False )
                self.edge_list.append(Edge(source = name , target = k , weight = v.DPImpedence))
                current_list = v.short_circuit_I.split(" + ")
                if len(current_list) != 0 and current_list[0] == "":
                    current_list = current_list[1:]
                for i in range(len(current_list)):
                    if not current_list[i].startswith("V"):
                        control_current = current_list[i].split("*")
                        gain = control_current[0]
                        control_current[1] = control_current[1].split("-")
                        node1 , node2 = control_current[1][0] , control_current[1][1]
                        while not node2[-1].isalpha():
                            node2 = node2[:-1]
                        while not node1[0].isalpha():
                            node1 = node1[1:]
                        while gain.startswith(" "):
                            gain = gain[1:]
                        nega_gain = ( gain[1:] if gain.startswith("-") else "-" + gain)
                        
                        
                        self.edge_list.append(Edge(source = node1 , target = name , weight = gain))
                        self.edge_list.append(Edge(source = node2 , target = name , weight = nega_gain))
                    else:
                        from_node, index = "", 0
                        while current_list[i][index] != "/":
                            from_node += current_list[i][index]
                            index += 1
                        gain = "1" + current_list[i][index:]
                        self.edge_list.append(Edge(source = from_node , target = name , weight = gain))
                        
        print(self.short_circuit_nodes)
        for ele in self.edge_list:
            print(ele)
        pass
            
    def process_nodeList(self):
        for key , each_node in self.nodes_list.items():
            each_node.DPI_analysis()
        pass
    def __repr__(self):
        result = []
        for each_node in self.nodes_list:
            result.append(each_node.__repr__())
        return '\n'.join(result)
    def __getattr__( self, name ):
        return getattr(self.nodes_list , name)
        
class Edge:
    def __init__(self, source , target , weight):
        self.source = source
        self.target = target
        self.weight = weight
    def __repr__(self):
        return f"{self.source}->{self.target} : {self.weight}"


class Node:
    def __init__(self, **kwargs):
        # name of this node
        self.components = {}
        self.neighbor_edge = {}
        self.voltage = 0 if kwargs["is_ground"] is True else "V" + kwargs["node_name"].lower() if not kwargs["node_name"].startswith("V") else kwargs["node_name"]
        self.short_circuit_I = "0"
        self.DPImpedence = "0"
        self.node_name =  kwargs["node_name"].lower()
        if self.voltage == 0:
            return
        
        
        
        # components is a dictionary stores the information between this node and each of its neighbors. We can access the components between node 1 and node 2 using components["node2"] and returns a list of component objects in between
        if "components" in kwargs:
            self.components = kwargs["components"]
        
        
    def add_components(self, input_list):
        self.components.update(input_list)
    
    def __repr__(self):
        if self.voltage == 0:
            return "ground"
        return " NodeInfor:"+ self.node_name #+" voltage: " + self.voltage + "\n short circuit current: "+ self.short_circuit_I + "\n  driving point impedence:" + self.DPImpedence
    
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
                impedence +=  ( ( ("(1/s" + component.name + ")") if isinstance( component , Capacitor) else component.name) + "//")
                
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

def construct_graph( circuit : cir.Circuit ):
    circuit_components = {}
    circuit_nodes = {}
    graph = SFGraph(dict())
    for node , neighbors in circuit.multigraph.adjacency():
        if node not in circuit_nodes:
            ground = True if node == "0" else False
            node_name =  node
            circuit_nodes[ node ] = Node( node_name = node, is_ground = ground )
            graph.update( {node_name: circuit_nodes[ node ]} )
            
    print(circuit_nodes)
    for edge in circuit.multigraph.edges(keys=True, data='component'):
        src_node, dst_node, component_name, component_object = edge
        if isinstance(component_object, cir.Resistor):
            cur_resistor = Resistor( name = component_name, value = component_object.value )
            circuit_components[component_name] = cur_resistor
        elif isinstance(component_object, cir.VoltageSource):
            cur_v = VoltageSource( name = component_name, voltage = component_object.voltage )
            circuit_components[component_name] = cur_v
        elif isinstance(component_object, cir.VoltageDependentCurrentSource):
            c = "" + component_object.gain + "*(" + component_object.pos_input_node + "-" + component_object.neg_input_node+") "
            cur_i = CurrentSource( name = component_name, current = c , direc = "+ " )
            cur_o = CurrentSource( name = component_name, current = c , direc = "- " )
            positive_node = src_node if component_object.neg_input_node == src_node else dst_node
            negative_node = src_node if component_object.pos_input_node == src_node else dst_node
            circuit_nodes[positive_node].add_components({cur_i : circuit_nodes[negative_node]})
            circuit_nodes[negative_node].add_components({cur_o : circuit_nodes[positive_node]})
            continue
        elif isinstance(component_object, cir.Capacitor):
            circuit_components[component_name] = Capacitor( name = component_name , capacitance = component_object.capacitance )
        
        circuit_nodes[src_node].add_components({circuit_components[component_name] : circuit_nodes[dst_node]})
        circuit_nodes[dst_node].add_components({circuit_components[component_name] : circuit_nodes[src_node]})
        
    return graph
                

    
    
    
