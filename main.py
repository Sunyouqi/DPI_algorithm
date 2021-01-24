from DPI import *
import circuit
import json

def convert_to_JSON(graph):
    preprocess = {}
    for key , value in graph.nodes_list.items():
        print(value.node_name)
        preprocess.update({key:{"id":value.node_name ,"name":value.node_name , "value":""}})
    edge_process = {}
    index = 0
    for i in range(len(graph.edge_list)):
        edge_process.update({i:{"src":graph.edge_list[i].source,"dst":graph.edge_list[i].target,"weight":graph.edge_list[i].weight}})
    
    with open("result_circuit.json", "w") as outfile:
        json.dump(preprocess, outfile)
    with open("result_edge_list.json", "w") as outfile:
        json.dump(edge_process, outfile)

def run_test1():
    print("test case 1:")
    r0 = Resistor("r0", 10)
    print(r0)
    #ground node
    ground = Node(node_name = "0",is_ground = True)
    print(ground)
    ground.DPI_analysis()
    #control source
    Cgs_in = CurrentSource("c0" , "gmVgs" , "+")
    Cgs_out = CurrentSource("c0" , "gmVgs" , "-")
    print(Cgs_in)
    print(Cgs_out)
    #rd
    Rd = Resistor("Rd" , 20)
    print(Rd)
    #rs
    Rs = Resistor("Rs" , 20)
    print(Rs)
    #input voltage source
    Vi = VoltageSource("Vi", 10 )

    Nd = Node(node_name = "Nd", components = { Rd : ground , r0 : None , Cgs_out : None }, neighbors = [ground], is_ground = False)
    Ns = Node(node_name = "Ns", components = { Rs : ground , r0 : Nd , Cgs_in : Nd }, neighbors = [ground , Nd], is_ground = False)
    Nd.components[r0] , Nd.components[Cgs_out] = Ns , Ns
    #Nd.neighbors.append(Ns)
    Ng = Node(node_name = "Ng", components = { Vi : ground } , neighbors = [ground], is_ground = False)
   

    graph = SFGraph({"Nd":Nd , "Ns":Ns , "Ng":Ng})
    graph.process_nodeList()
    print(graph)

def run_test2():
    print("test case 2:")
    Rd1 = Resistor("Rd1", 10)
    Cgs1_in = CurrentSource("c0" , "gm1Vgs1", "+")
    Cgs1_out = CurrentSource("c0" , "gm1Vgs1" , "-")
    Vi = VoltageSource("Vi", 10 )
    R1 = Resistor("R1", 10)
    R2 = Resistor("R2", 10)
    Rd2 = Resistor("Rd2", 10)
    Cgs2_out = CurrentSource("c1" , "gm2Vd1" , "-")
    ground = Node(node_name = "0",is_ground = True)
    Ng = Node(node_name = "Ng", components = { Vi : ground } , neighbors = [ground], is_ground = False)
    Nd1 = Node(node_name = "Nd1", components = { Cgs1_out : None , Rd1 : ground } ,  is_ground = False)
    Ns1 = Node(node_name = "Ns1", components = { Cgs1_in : Nd1 , R1 : ground , R2 : None } , is_ground = False)
    Nd2 = Node(node_name = "Nd2", components = { Cgs2_out : ground , Rd2 : ground , R2 : Ns1 } ,  is_ground = False)
    Nd1.components[Cgs1_out] = Ns1
    #Nd1.neighbors.append(Ns1)
    Ns1.components[R2] = Nd2
    #Ns1.neighbors.append(Nd2)
    
    graph = SFGraph({"Ng":Ng , "Nd1":Nd1 , "Ns1":Ns1 , "Nd2":Nd2})
    graph.process_nodeList()
    print(graph)

def test3():
    from os import path
    print("here")
    test_data_dir = path.join(path.dirname(__file__), 'test_data')

    netlist_file = path.join(test_data_dir, 'npn_ce.cir')
    log_file = path.join(test_data_dir, 'npn_ce.log')
    c_in = circuit.Circuit.from_ltspice(netlist_file, log_file)
    graph = construct_graph(c_in)
    print(graph.nodes_list)
    print("nodes:")
    for k , v in graph.nodes_list.items():
        print(k)
        print(v.components)
        print(v.voltage)
        print("=================")
    graph.process_nodeList()
    print("after dpi:")
    for k , v in graph.nodes_list.items():
        print(k+":")
        print("short circuit current: " + v.short_circuit_I)
        print("DPImpedence: " + v.DPImpedence)
    graph.generate()
    print("edge list:")
    print(graph.edge_list)
    print("voltage node list:")
    print(graph.nodes_list)
    print("short circuit node list:")
    print(graph.short_circuit_nodes)
    node = Node(node_name="shit",is_ground=False)
    print(node)
    convert_to_JSON(graph)
    
if __name__ == "__main__":
    test3()
    #run_test1()
    #run_test2()
    
    
