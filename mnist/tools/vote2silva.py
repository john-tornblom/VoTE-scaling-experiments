#!/usr/bin/env python2

import json
import sys


def export_tree(tree, f, logarithmic=False):
    stack = [0]
    while len(stack) > 0:
        node_id = stack.pop()

        if tree['left'][node_id] == tree['right'][node_id]:
            if logarithmic:
                value = ['{:f}'.format(v) for v in tree['value'][node_id]]
                f.write('LEAF_LOGARITHMIC {:s}\n'.format(' '.join(value)))
            else:
                value = [str(int(v)) for v in tree['value'][node_id]]
                f.write('LEAF {:s}\n'.format(' '.join(value)))

        else:
            f.write('SPLIT {:d} {:g}\n'.format(tree['feature'][node_id],
                                               tree['threshold'][node_id]))
            stack.append(tree['right'][node_id])
            stack.append(tree['left'][node_id])


def export_ensemble(obj, f):
    f.write('classifier-forest {:d}\n'.format(len(obj['trees'])))
    for t in obj['trees']:
        f.write('classifier-decision-tree {:d} {:d}\n'.format(t['nb_inputs'],
                                                              t['nb_outputs']))
        f.write('{:s}\n'.format(' '.join([str(i)
                                          for i in range(t['nb_outputs'])])))
        export_tree(t, f, obj['post_process'] == 'softmax')


if __name__ == '__main__':
    import sys
    d = json.load(sys.stdin)
    export_ensemble(d, sys.stdout)
    
