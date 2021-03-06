from functools import reduce, wraps, partial

from pprint import pprint
from copy   import deepcopy

from .operator import Operator
from .partial  import Partial
from .index    import Index, RevIndex
from .rule     import Rule

from .arithmetic import operators

def enumerate_relations(inputs, outputs, answer, operators, considering=None):
    if considering is None:
        considering = {Rule([])}
    rules = set()
    for i, x in enumerate(inputs):
        for j, y in enumerate(outputs):
            for name, op in operators.items():
                for previous in considering:
                    if i == 0:
                        rules.add(previous.join(
                                  Rule([Partial(op, [RevIndex(outputs, j, 'outputs'), Index(0, 'arguments')], [op.f(inputs[i], outputs[j])])])))
                    if j == 0:
                        rules.add(previous.join(
                                  Rule([Partial(op, [RevIndex(inputs, i, 'inputs'), Index(0, 'arguments')], [op.f(inputs[i], outputs[j])])])))
                    rules.add(previous.join(
                              Rule([Partial(op, [RevIndex(inputs, i, 'inputs'), RevIndex(outputs, j, 'outputs')], [])])))
                    for j2, y2 in enumerate(outputs):
                        rules.add(previous.join(
                                  Rule([Partial(op, [RevIndex(outputs, j, 'outputs'), RevIndex(outputs, j2, 'outputs')], [])])))
                    for i2, x2 in enumerate(outputs):
                        rules.add(previous.join(
                                  Rule([Partial(op, [RevIndex(inputs, i, 'inputs'), RevIndex(inputs, i2, 'inputs')], [])])))
        for i2, x2 in enumerate(inputs):
            for name, op in operators.items():
                rules.add(previous.join(
                          Rule([Partial(op, [RevIndex(inputs, i, 'inputs'), RevIndex(inputs, i2, 'inputs')], [])])))
    for j, y in enumerate(outputs):
        for j2, y2 in enumerate(outputs):
            for name, op in operators.items():
                rules.add(previous.join(
                          Rule([Partial(op, [RevIndex(outputs, j, 'outputs'), RevIndex(outputs, j2, 'outputs')], [])])))
    return rules

def tree(inputs, outputs, depth=1):
    considering = None
    for d in range(depth):
        print('Recurring to depth {}'.format(d))
        try:
            for i in range(1, len(inputs)):
                print('{}/{}\r'.format(i, len(inputs)), end='', flush=True)
                local_inputs  = inputs[:i + 1]
                local_outputs = outputs[:i]
                local_answer  = outputs[i]
                proposed = enumerate_relations(local_inputs, local_outputs,
                                               answer=local_answer, operators=operators)
                #pprint(proposed)
                final = {rule for rule in proposed if rule.guess(local_inputs, local_outputs) == local_answer}
                if final:
                    guesses = {f.guess(inputs, outputs) for f in final}
                    correct = outputs[-1]
                    for f in final:
                        guess = f.guess(inputs, outputs[:-1])
                        if guess == correct:
                            #print(f, ' gives:')
                            #print(guess)
                            #print('correct:', outputs[-1])
                            return f
                else:
                    considering = proposed
        except KeyboardInterrupt:
            return None
