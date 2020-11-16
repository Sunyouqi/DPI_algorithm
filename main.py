from circuit import *

def run_test1():
    print("test case 1:")
    r0 = Resistor("r0", 10)
    print(r0)
    #ground node
    ground = Node(is_ground = True)
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
    Vi = VoltageSource("Vi", 10 , True)

    Nd = Node(node_name = "Nd", components = { Rd : ground , r0 : None , Cgs_out : None }, neighbors = [ground], is_ground = False)
    Ns = Node(node_name = "Ns", components = { Rs : ground , r0 : Nd , Cgs_in : Nd }, neighbors = [ground , Nd], is_ground = False)
    Nd.components[r0] , Nd.components[Cgs_out] = Ns , Ns
    Nd.neighbors.append(Ns)
    Ng = Node(node_name = "Ng", components = { Vi : ground } , neighbors = [ground], is_ground = False)
   

    graph = SFGraph([Nd , Ns , Ng])
    graph.process_nodeList()
    print(graph)

def run_test2():
    print("test case 2:")
    Rd1 = Resistor("Rd1", 10)
    Cgs1_in = CurrentSource("c0" , "gm1Vgs1", "+")
    Cgs1_out = CurrentSource("c0" , "gm1Vgs1" , "-")
    Vi = VoltageSource("Vi", 10 , True)
    R1 = Resistor("R1", 10)
    R2 = Resistor("R2", 10)
    Rd2 = Resistor("Rd2", 10)
    Cgs2_out = CurrentSource("c1" , "gm2Vd1" , "-")
    ground = Node(is_ground = True)
    Ng = Node(node_name = "Ng", components = { Vi : ground } , neighbors = [ground], is_ground = False)
    Nd1 = Node(node_name = "Nd1", components = { Cgs1_out : None , Rd1 : ground } , neighbors = [ground], is_ground = False)
    Ns1 = Node(node_name = "Ns1", components = { Cgs1_in : Nd1 , R1 : ground , R2 : None } , neighbors = [ground , Nd1], is_ground = False)
    Nd2 = Node(node_name = "Nd2", components = { Cgs2_out : ground , Rd2 : ground , R2 : Ns1 } , neighbors = [ground , Ns1], is_ground = False)
    Nd1.components[Cgs1_out] = Ns1
    Nd1.neighbors.append(Ns1)
    Ns1.components[R2] = Nd2
    Ns1.neighbors.append(Nd2)
    
    graph = SFGraph([Ng , Nd1 , Ns1 , Nd2])
    graph.process_nodeList()
    print(graph)

if __name__ == "main":
   
    #run_test1()
    run_test2()

    
