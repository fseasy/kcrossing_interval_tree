#/usr/bin/env python
#coding=utf-8
import argparse
import logging

from read_conllx import read_instance
from kcrossing import ( build_adjacencylist , 
                        find_crossing_arc , 
                        disjoint_crossing_arcs , 
                        get_kcrossing_vertices_of_one_crossing_interval ,
                        get_kcrossing_vertices_set ,
                        _is_2_crossing_interval_tree ,
                        _is_n_crossing_interval_tree
                        )
logging.basicConfig(level=logging.DEBUG ,
                    format="%(levelname)s : %(message)s")

def test_is_ok(ifo) :
    for instance in read_instance(ifo) :
        adj_list = build_adjacencylist(instance)
        arc_list , status = find_crossing_arc(adj_list)
        if status :
            print adj_list
            print arc_list
            arc_sets = disjoint_crossing_arcs(arc_list , adj_list)
            kvertices_set = get_kcrossing_vertices_set(arc_sets , adj_list)
            print arc_sets 
            print kvertices_set
def get_2crossing_interval_tree_coverage(ifo) :
    nr_instance = 0
    nr_2crossing_tree = 0
    nr_projective_tree = 0
    nr_bad_tree = 0
    logging_interval = 1000
    for instance in read_instance(ifo) :
        nr_instance += 1
        adj_list = build_adjacencylist(instance)
        crossing_arc_list , status = find_crossing_arc(adj_list)
        if status :
            crossing_arc_set_list = disjoint_crossing_arcs(crossing_arc_list , adj_list )
            kvertices_set_list = get_kcrossing_vertices_set(crossing_arc_set_list , adj_list)
            if _is_2_crossing_interval_tree(kvertices_set_list) :
                nr_2crossing_tree += 1
                if _is_n_crossing_interval_tree(kvertices_set_list , 0):
                    nr_projective_tree += 1
        else :
            nr_bad_tree += 1
        if nr_instance % logging_interval == 0 :
            logging.info("%d instance processed." %(nr_instance))

    print """
    instance num : %d(including bad tree num : %d) 
    2 crossing interval tree num : %d , including  projective tree : %d 
    2 crossing interval tree coverage %.2f%% , projective tree coverage %.2f%%
    """ %(nr_instance , nr_bad_tree , nr_2crossing_tree , nr_projective_tree , 
          float(nr_2crossing_tree) / (nr_instance - nr_bad_tree) * 100 , 
          float(nr_projective_tree) / (nr_instance - nr_bad_tree) * 100)

def main(ifo) :
    get_2crossing_interval_tree_coverage(ifo)

if __name__ == "__main__" :
    argp = argparse.ArgumentParser(description="K-Crossing Procedure")
    argp.add_argument("--input" , "-i" , help="path to training dataset" , type=argparse.FileType('r') , required=True)
    args = argp.parse_args()
    
    main(args.input)

    args.input.close()
