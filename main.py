#/usr/bin/env python
#coding=utf-8
import argparse
from read_conllx import read_instance
from kcrossing import ( build_adjacencylist , 
                        find_crossing_arc )
def main(ifo) :
    for instance in read_instance(ifo) :
        adj_list = build_adjacencylist(instance)
        arc_list , status = find_crossing_arc(adj_list)
        print arc_list
        print status

if __name__ == "__main__" :
    argp = argparse.ArgumentParser(description="K-Crossing Procedure")
    argp.add_argument("--input" , "-i" , help="path to training dataset" , type=argparse.FileType('r') , required=True)
    args = argp.parse_args()
    
    main(args.input)

    args.input.close()
