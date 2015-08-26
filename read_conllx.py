#coding=utf-8

CONLL_X_FORMAT = ["id" , "form" , "lemma" ,"cpostag" , "postag" , "feat" , "head" , "deprel" , "phead" , "pdeprel"]

def read_instance(f) :
    instance = []
    for line in f :
        line = line.strip()
        if len(line) == 0 :
            if len(instance) > 0 :
                yield instance
            instance = []
        else :
            parts = line.split()
            node = {CONLL_X_FORMAT[i] : parts[i] for i in range(len(CONLL_X_FORMAT)) }
            instance.append(node)
