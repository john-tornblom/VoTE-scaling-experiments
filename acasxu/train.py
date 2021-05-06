#!/usr/bin/env python3
'''
Train a tree ensemble classifier by sampling a neural network from 
the Reluplex ACAS Xu case study.
'''
import logging
import optparse
import sys
import json

import numpy as np

from sklearn.metrics import accuracy_score
from catboost import CatBoostClassifier

import vote
import oracle


logger = logging.getLogger('train-acasxu')

        
def catboost_to_dict(inst):
    '''
    Convert a CatBoost model into a dictionary.
    '''
    import tempfile, os, collections
    
    filename = tempfile.mktemp()
    inst.save_model(filename, format='json')
    with open(filename, 'r') as f:
        cb = json.load(f)

    os.remove(filename)

    nb_inputs = len(cb['features_info']['float_features'])
    nb_classes = (cb['model_info']['params']['data_processing_options']
                  ['classes_count'])

    if nb_classes > 1:
        post_process = 'softmax'

    elif inst._estimator_type == 'classifier':
        post_process = 'sigmoid'

    elif inst._estimator_type == 'regressor':
        post_process = 'none'

    else:
        raise NotImplementedError
    
    tree_obj_list = list()
    for tree in cb['oblivious_trees']:
        tree_obj = dict()
        
        nb_splits = len(tree['splits'])
        depth = nb_splits + 1
        nb_nodes = (2 ** depth) - 1
        nb_leaves = len(tree['leaf_values'])
        nb_outputs = nb_leaves // (2 ** nb_splits)
        
        tree_obj['nb_inputs'] = nb_inputs
        tree_obj['nb_outputs'] = nb_outputs
        tree_obj['left'] = [-1] * nb_nodes
        tree_obj['right'] = [-1] * nb_nodes
        tree_obj['feature'] = [-1] * nb_nodes
        tree_obj['threshold'] = [None] * nb_nodes
        tree_obj['value'] = [[0] * nb_outputs] * nb_nodes
        tree_obj['left'][0:nb_nodes//2] = [ind for ind in range(2, nb_nodes, 2)
                                          if ind % 2 == 0]
        tree_obj['right'][0:nb_nodes//2] = [ind for ind in range(1, nb_nodes, 2)
                                           if ind % 2 == 1]

        splits = list(reversed(tree['splits']))
        for node_id in range(2 ** nb_splits - 1):
            d = int(np.log2(node_id + 1))
            tree_obj['feature'][node_id] = splits[d]['float_feature_index']
            tree_obj['threshold'][node_id] = splits[d]['border']

        queue = collections.deque(tree['leaf_values'])
        for node_id in range(2 ** nb_splits - 1, nb_nodes):
            values = [queue.pop() for _ in range(nb_outputs)]
            tree_obj['value'][node_id] = list(reversed(values))

        tree_obj_list.append(tree_obj)

    d = dict(trees=tree_obj_list,
             post_process=post_process)

    return d


def main():
    parser = optparse.OptionParser(usage='%prog [options]')
    parser.set_description(__doc__.strip())
    
    parser.add_option('-B', dest='nb_trees', action='store',
                      help='Train a tree ensemble with INTEGER number of trees',
                      metavar='INTEGER', default=1, type=int)
    
    parser.add_option('-d', dest='max_depth', action='store',
                      help='Limit depth of trees to INTEGER',
                      metavar='INTEGER', default=None, type=int)

    parser.add_option('-n', dest='nb_samples', action='store',
                      help='Train on INTEGER number of samples',
                      metavar='INTEGER', default=100_000, type=int)
    
    parser.add_option('-a', dest='aprev', action='store',
                      help='Previous advisory (1-5)',
                      metavar='INDEX', default=None, type=int)

    parser.add_option('-t', dest='tau', action='store',
                      help='Time until loss of vertical separation index (1-9)',
                      metavar='INDEX', default=None, type=int)
    
    parser.add_option('-o', dest='output', action='store',
                      help='Save trained random forest to PATH',
                      metavar='PATH', default=None)

    parser.add_option('-v', '--verbosity', dest='verbosity', action='count',
                      default=1, help='increase debug logging level')
    
    (opts, args) = parser.parse_args()
    if not opts.output or not opts.aprev or not opts.tau:
        parser.print_help()
        sys.exit(1)
        
    levels = {
              0: logging.ERROR,
              1: logging.WARNING,
              2: logging.INFO,
              3: logging.DEBUG,
    }
    logging.basicConfig(level=levels.get(opts.verbosity, logging.DEBUG))

    m = CatBoostClassifier(max_depth=opts.max_depth,
                           num_trees=opts.nb_trees,
                           learning_rate=0.5,
                           classes_count=5,
                           loss_function='MultiClass',
                           #logging_level='Silent',
                           random_state=12345)

    logger.info('aprev:%s', opts.aprev)
    logger.info('tau:%s', opts.tau)
    logger.info('nb_samples:%s', opts.nb_samples)
    logger.info('nb_trees:%s', opts.nb_trees)
    logger.info('max_depth:%s', opts.max_depth)
    
    X_train, Y_train = oracle.mk_samples(opts.aprev, opts.tau, opts.nb_samples)
    X_test, Y_test = oracle.mk_samples(opts.aprev, opts.tau, opts.nb_samples)
    m.fit(X_train, Y_train, eval_set=(X_test, Y_test))

    Y_pred = m.predict(X_train)
    score = accuracy_score(Y_train, Y_pred)
    logger.info('train score:%s', score)
    
    del X_train
    del Y_train
    del Y_pred
    
    Y_pred = m.predict(X_test)
    score = accuracy_score(Y_test, Y_pred)
    logger.info('test score:%s', score)

    del X_test
    del Y_test
    del Y_pred
    
    logger.info('output:%s', opts.output)
    obj = catboost_to_dict(m)

    for tree_obj in obj['trees']:
        for value_vec in tree_obj['value']:
            for ind in range(len(value_vec)):
                value_vec[ind] = -value_vec[ind]
                
    with open(opts.output, 'w') as f:
        json.dump(obj, f)
        

if __name__ == '__main__':
    main()
        
