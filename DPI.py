import re
import networkx as nx
import circuit as cir
from collections import defaultdict
import sympy as sy

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
        


class SFG():
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def add_edge(self, source , target , wt):
        self.graph.add_edge(source, target , weight = wt)
    
def DPI_algorithm( circuit : cir.Circuit ):
    sfg = SFG()
    impedance_list = []
    for n in circuit.multigraph.nodes:
        if n is "0":
            continue
        impedance = "1/("
        #print(n)
        for ne in circuit.multigraph.neighbors(n):
            for k in circuit.multigraph.get_edge_data(n , ne):
                if not isinstance(circuit.multigraph.edges[n,ne,k]['component'] , cir.VoltageDependentCurrentSource) and not isinstance(circuit.multigraph.edges[n,ne,k]['component'] , cir.VoltageSource) and not isinstance(circuit.multigraph.edges[n,ne,k]['component'] , cir.CurrentSource):
                    impedance += " + " + ("(s*"+circuit.multigraph.edges[n,ne,k]['component'].name +")" if isinstance(circuit.multigraph.edges[n,ne,k]['component'] , cir.Capacitor) else "1/" + circuit.multigraph.edges[n,ne,k]['component'].name)
                if ne != "0":
                    #print("not ground!")
                    #print(isinstance(circuit.multigraph.edges[n,ne,k]['component'] , cir.VoltageDependentCurrentSource))
                    #print(circuit.multigraph.edges[n,ne,k]['component'])
                    if not isinstance(circuit.multigraph.edges[n,ne,k]['component'] , cir.VoltageDependentCurrentSource) and not isinstance(circuit.multigraph.edges[n,ne,k]['component'] , cir.VoltageSource) and not isinstance(circuit.multigraph.edges[n,ne,k]['component'] , cir.CurrentSource):
                        cur_target = "Isc" + ne[1:].lower() if ne.startswith("V") else "Isc" + ne.lower()
                        cur_source = "V" + n.lower() if not n.startswith("V") else n
                        if sfg.graph.has_edge(cur_source, cur_target):
                            sfg.graph.edges[cur_source , cur_target]['weight'] += " + " + ("(s*"+circuit.multigraph.edges[n,ne,k]['component'].name +")" if isinstance(circuit.multigraph.edges[n,ne,k]['component'] , cir.Capacitor) else "1/" + circuit.multigraph.edges[n,ne,k]['component'].name)
                        else:
                            sfg.graph.add_edge(cur_source , cur_target , weight = "+" + ("(s*"+circuit.multigraph.edges[n,ne,k]['component'].name +")" if isinstance(circuit.multigraph.edges[n,ne,k]['component'] , cir.Capacitor) else "1/" + circuit.multigraph.edges[n,ne,k]['component'].name))
                    elif isinstance(circuit.multigraph.edges[n,ne,k]['component'] , cir.VoltageDependentCurrentSource):
                        print("found volage dependent current source!!")
                        cur_target = "Isc" + n[1:].lower() if n.startswith("V") else "Isc" + n.lower()
                        pos_input_node = circuit.multigraph.edges[n,ne,k]['component'].pos_input_node
                        neg_input_node = circuit.multigraph.edges[n,ne,k]['component'].neg_input_node
                        cur_source_1 = "V" + pos_input_node.lower() if not pos_input_node.startswith("V") else pos_input_node
                        if sfg.graph.has_edge(cur_source_1, cur_target):
                            sfg.graph.edges[cur_source_1, cur_target]['weight'] += (" - " if n == circuit.multigraph.edges[n,ne,k]['component'].pos_node else " + ") + "gm_" + str(circuit.multigraph.edges[n,ne,k]['component'].name[-1])
                        else:
                            sfg.graph.add_edge( cur_source_1, cur_target , weight = (" - " if n == circuit.multigraph.edges[n,ne,k]['component'].pos_node else " + ") + "gm_" + str(circuit.multigraph.edges[n,ne,k]['component'].name[-1]))
                            
                        cur_source_2 = "V" + neg_input_node.lower() if not neg_input_node.startswith("V") else neg_input_node
                        
                        if sfg.graph.has_edge(cur_source_2, cur_target):
                            sfg.graph.edges[cur_source_2, cur_target]['weight'] += (" + " if n == circuit.multigraph.edges[n,ne,k]['component'].pos_node else " - ") + "gm_" + str(circuit.multigraph.edges[n,ne,k]['component'].name[-1])
                        else:
                            sfg.graph.add_edge( cur_source_2, cur_target , weight = (" + " if n == circuit.multigraph.edges[n,ne,k]['component'].pos_node else " - ") + "gm_" + str(circuit.multigraph.edges[n,ne,k]['component'].name[-1]))
        if impedance != "1/(":
            impedance += ")"
        #print(impedance)
        impedance_list.append(impedance)
        source = "Isc" + n[1:].lower() if n.startswith("V") else "Isc" + n.lower()
        target = "V" + n.lower() if not n.startswith("V") else n
        sfg.graph.add_edge(  source , target , weight = impedance )
        
        
        
        
    print("graph information")
    for e in sfg.graph.edges:
        print(e)
        print(sfg.graph.get_edge_data(*e))
    #print("impedance_list:",impedance_list)
        sfg.graph.get_edge_data(*e)['weight'] = sy.sympify( sfg.graph.get_edge_data(*e)['weight'] )
    print("After transferring data to sympy")
    for e in sfg.graph.edges:
        print("edge:(source , target)",e)
        print("weight information:",sfg.graph.get_edge_data(*e))
        print("\n")
    return sfg

class SFGraph(object):
    
    def __init__(self , nodes_list):
        self.nodes_list = nodes_list
        self.short_circuit_nodes = {}
        self.edge_list = []
        self.adjacency = defaultdict(list)
        self.nodes_name_map = {}
        self.vertex = []
        
        
        
        pass
    
    def add_edge(self , source , target , weight):
        #print("in add edge")
        #print(type(source))
        source_node = Node( node_name = str(source) , is_ground = False )
        target_node = Node( node_name = str(target) , is_ground = False )
        self.edge_list.append( Edge( source_node.node_name , target_node.node_name , weight ) )
        if target_node.node_name not in self.nodes_name_map:
            #if str(target) not in self.nodes_name_map:
                #flag = True
            
            self.nodes_name_map.update( { target_node.node_name : target_node } )
            self.nodes_name_map[target_node.node_name].node_number = target
            #if flag:
            self.vertex.append(self.nodes_name_map[target_node.node_name])
        
        
        if source_node.node_name not in self.nodes_name_map:
            
            self.nodes_name_map.update( { source_node.node_name : source_node } )
            self.nodes_name_map[ source_node.node_name ].node_number = source
            self.vertex.append(self.nodes_name_map[ source_node.node_name ])
            
        self.nodes_name_map[source_node.node_name].adj_nodes.append(self.nodes_name_map[ target_node.node_name ])
            
                
        
        self.vertex.sort(reverse = False , key = lambda x : x.node_number)
    
    def generate_adjacent(self):
        
       
        self.nodes_name_map.update(self.nodes_list)
        self.nodes_name_map.update(self.short_circuit_nodes)
        index = 0
        self.nodes_name_map.pop("V0")
        for k in self.nodes_name_map.keys():
            self.nodes_name_map[k].node_number = index
            self.vertex.append(self.nodes_name_map[k])
            index += 1
            
        #print(self.vertex)
        
        #self.graph_nodes.pop("0")
        for edge in self.edge_list:
            if self.nodes_name_map[edge.target].node_number not in self.adjacency[self.nodes_name_map[edge.source].node_number]:
                self.adjacency[self.nodes_name_map[edge.source].node_number].append(self.nodes_name_map[edge.target].node_number)
        for i in range(len(self.vertex)):
            for v_number in self.adjacency[self.vertex[i].node_number]:
                self.vertex[i].adj_nodes.append( self.vertex[ v_number ] )
            #print("vertex: " + str(self.vertex[i].node_number))
            #print(self.vertex[i].adj_nodes)
        
        
    def arrange_attr(self):
        # this part depends on the parser output
        pass
    def generate(self):
        
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
        #result = []
        #for each_node in self.nodes_list:
            #result.append(each_node.__repr__())
        #return '\n'.join(result)
        result = []
        for e in self.edge_list:
            result.append(e.__repr__())
        return "graph edges: \n" + '\n'.join(result)
    #def __getattr__( self, name ):
     #   return getattr(self.nodes_list , name)
    
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
        self.adj_nodes = []
        self.node_number = 0
        self.voltage = 0 if kwargs["is_ground"] is True else "V" + kwargs["node_name"].lower() if not kwargs["node_name"].startswith("V") else kwargs["node_name"]
        self.short_circuit_I = "0"
        self.DPImpedence = "0"
        self.node_name =  "V" + kwargs["node_name"].lower() if not kwargs["node_name"].startswith("V") and not kwargs["node_name"].startswith("I") else kwargs["node_name"]
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
        return " NodeInfor: node_id " + str(self.node_number) + " node_name " + self.node_name #+" voltage: " + self.voltage + "\n short circuit current: "+ self.short_circuit_I + "\n  driving point impedence:" + self.DPImpedence
    
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
                print("node.voltage:")
                print(node.voltage)
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
            node_name =  "V" + node.lower() if not node.startswith("V") else node
            circuit_nodes[ node ] = Node( node_name = node, is_ground = ground )
            graph.nodes_list.update( {node_name: circuit_nodes[ node ]} )
            
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
    graph.process_nodeList()
    graph.generate()
    graph.generate_adjacent()
    return graph
                

    
    
    
