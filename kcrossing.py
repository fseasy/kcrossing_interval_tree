#coding=utf-8
import bisect 
import sys
import Queue

class _node(object) :
    def __init__(self , nodeid) :
        self.id = nodeid
        self.in_nodes = [] # in fact , in node should just only one ! but for convenience , keep it be same to out
        self.out_nodes = []
        self.intersections = []
    def add_innodes(self , node) :
        bisect.insort_left(self.in_nodes , node)
    def add_outnodes(self , node) :
        bisect.insort_left(self.out_nodes , node)
    def add_intersection(self , node) :
        if node not in self.intersections :
            bisect.insort_left(self.intersections , node)
    def get_head_id(self) :
        if(len(self.in_nodes) == 1) :
            return self.in_nodes[0]
        elif(len(self.in_nodes) == 0) :
            return -1 
        else :
            raise Exception("multiple heads is found !")
    def __str__(self) :
        return "node(id:%d , in nodes : %s , out nodes : %s , intersections : %s)" %(self.id , self.in_nodes , self.out_nodes , self.intersections)

class AdjacencyList(object) :
    def __init__(self , n) :
        self.datas = [_node(i) for i in range(n)]
        self.size = n
    def __getitem__(self , idx) : ##! overload [] operator
        return self.datas[idx]
    def __len__(self) :
        return self.size
    def __str__(self) :
        rep_str = []
        for i in range(self.size) :
             rep_str.append(str(self.datas[i]))
        return "\n".join(rep_str)

def build_adjacencylist(instance) :
    '''
    from instance to build adjacency list 
    attention : at instance , root node is not included , while adjacency should contain it !
    Args :
        instance : a dict containing instance info

    Returns :
        adj_list : AdjacencyList contains the structure info
    '''
    node_num = len(instance) + 1
    adj_list = AdjacencyList(node_num)
    for idx in range(1 , node_num) :
        node = instance[idx -1]
        head_nodeid = int(node["head"]) 
        adj_list[idx].add_innodes(head_nodeid)
        adj_list[head_nodeid].add_outnodes(idx)
    return adj_list
def _add_crossing_arc(adj_list , arc_node_1 , arc_node_2 , crossing_arc_set) :
    adj_list[arc_node_1].add_intersection(arc_node_2)
    adj_list[arc_node_2].add_intersection(arc_node_1)
    crossing_arc_set.add(arc_node_1)
    crossing_arc_set.add(arc_node_2)

def find_crossing_arc(adj_list) :
    '''
    find crossing arc according to adjacency list . 
    here we define : 
        "a arc is connected by its tail( means 'to' endpoint ) ."
    because every node have and only have one in arc (except for the root node) , so it is valid to define like this .
    so arc is represented by its tail node (id) ;
    Args :
        adj_list : AdjacencyList 

    Returns :
        arc_list : a list consisting of crossing arcs . (a list of node id )
        state    : porcessing status . True or false .
    Others :
        we'll also add the crossing arc info to the adj_list's node
    '''
    arc_list = set()
    for idx in range(1 , len(adj_list)) :
        cur_node = adj_list[idx]
        cur_node_id = cur_node.id
        try :
            cur_node_head_id = cur_node.get_head_id()
        except :
            print >> sys.stderr , "abandon current instance."
            return [] , False
        if cur_node_id == cur_node_head_id or not ( 0 <= cur_node_head_id < len(adj_list))  :
            print >> sys.stderr , "invalid head %d(node id is %d , id boundary is  [0 , %d ))" %(cur_node_head_id , cur_node_id , len(adj_list))
            return [] , False
        low_id = cur_node_id 
        high_id = cur_node_head_id
        if low_id > high_id :
            low_id , high_id = high_id , low_id
        for i in range(low_id+1 , high_id) :
            head_id = adj_list[i].get_head_id()
            if head_id < low_id or head_id > high_id :
                #crossing
                _add_crossing_arc(adj_list , cur_node_id , i , arc_list)
            for child_id in adj_list[i].out_nodes :
                if child_id < low_id or child_id > high_id :
                    _add_crossing_arc(adj_list , cur_node_id , child_id , arc_list)

    return sorted(list(arc_list)) , True

def disjoint_crossing_arcs(arc_list , adj_list) :
    '''
    partition the arc list to disjoint arc-crossing sets
    Args :
        arc_list : list , crossing arcs 
        adj_list : AdjacencyList
    Return :
        arc_sets : list , each element is a list represent a crossing arc set 
    
    Here we using the AdjacencyList's intersection info , instead of calculating whether this two arc is crossed 
    '''
    size =  len(arc_list)
    total_arc_size = len(adj_list)
    is_added = [False] * total_arc_size
    is_searched = [False] * total_arc_size
    arc_sets = []
    for crossing_node_id in arc_list :
        if not is_added[crossing_node_id] :
            queue = Queue.Queue()
            new_arc_set = set()
            queue.put(crossing_node_id)
            while not queue.empty() :
                node_id = queue.get()
                if not is_added[node_id] :
                    new_arc_set.add(node_id)
                    is_added[node_id] = True
                if not is_searched[node_id] :
                    crossing_nodes_id = adj_list[node_id].intersections
                    for crossing_id in crossing_nodes_id :
                        queue.put(crossing_id)
                    is_searched[node_id] = True
            arc_sets.append(sorted(list(new_arc_set)))
    return arc_sets
    
def get_arc_endpoints(arc , adj_list) :
    return (adj_list[arc].get_head_id() , arc)

def get_interval_and_endpoints(arc_set , adj_list) :
    arc_endpoints = []
    for arc in arc_set :
        arc_endpoints.extend(get_arc_endpoints(arc , adj_list))
    return (min(arc_endpoints) , max(arc_endpoints)) , list(set(arc_endpoints))

def get_kcrossing_vertices_of_one_crossing_interval(arc_set , adj_list) :
    interval , endpoints = get_interval_and_endpoints(arc_set , adj_list)
    k_list = []
    for endpoint in endpoints :
        head = adj_list[endpoint].get_head_id()
        if head < endpoint :
            if head < interval[0] : 
                continue # out out interval , not k
            # has a good head , to find if has a good child
            out_nodes = adj_list[endpoint].out_nodes
            is_k = False
            for out_node in out_nodes :
                if interval[0] <= out_node < endpoint :
                    is_k = True 
                    break
            if is_k :
                k_list.append(endpoint)
        else :
            if head > interval[1] :
                continue
            out_nodes = adj_list[endpoint].out_nodes
            is_k = False 
            for out_node in out_nodes :
                if endpoint < out_node <= interval[1] :
                    is_k = True
            if is_k :
                k_list.append(endpoint)
    return sorted(k_list)

def get_kcrossing_vertices_set(arc_set_list , adj_list) :
    kvertices_set = []
    for arc_set in arc_set_list :
        kvertices = get_kcrossing_vertices_of_one_crossing_interval(arc_set , adj_list)
        kvertices_set.append(kvertices)
    return kvertices_set

def _is_n_crossing_interval_tree(kvertices_set_list , n) :
    max_k = 0 
    for kvertices_set in kvertices_set_list :
        max_k = max( max_k , len(kvertices_set))
    return max_k <= n

def _is_2_crossing_interval_tree(kvertices_set_list) :
    return _is_n_crossing_interval_tree(kvertices_set_list , 2)

