import re
from collections import Counter, defaultdict
import random
from pprint import pprint


def generator(molecule, transitions, min_index):
    trans_set = set()
    for from_ in transitions.keys():
        for m in re.finditer(from_, molecule):
            # >>> email = "tony@tiremove_thisger.net"
            # >>> m = re.search("remove_this", email)
            # >>> email[:m.start()] + email[m.end():]
            #'tony@tiger.net'

            # if para so procurar os mais à frente
            if m.start() >= min_index:
                for to_ in transitions[from_]:
                    new_molecule = molecule[: m.start()] + to_ + molecule[m.end() :]
                    trans_set.add(new_molecule)
    return trans_set


def solution2(medicine, transitions):
    REPLACEMENTS = defaultdict()
    for simple_molecule, complex_molecules in transitions.items():
        for complex_molecule in complex_molecules:
            REPLACEMENTS[complex_molecule] = simple_molecule  # só existe uma transição
    REPLACEMENTS = dict(REPLACEMENTS)
    pprint(REPLACEMENTS)
    # REPLACEMENTS = {v: k for k, v in transitions.items()}

    MOLECULE = medicine

    count = 0
    while MOLECULE != "e":
        randomMolecule = random.choice(list(REPLACEMENTS.keys()))
        count += len(re.findall(randomMolecule, MOLECULE))
        MOLECULE = MOLECULE.replace(randomMolecule, REPLACEMENTS[randomMolecule])
        print(f"subs {randomMolecule} gives {MOLECULE} -> ${count}")


def run(input):

    transitions = defaultdict(list)
    for line in input.readlines():
        from_, _, to_, = line.split()
        transitions[from_].append(to_)
    transitions = dict(transitions)
    pprint(transitions)

    molecule = "CRnCaSiRnBSiRnFArTiBPTiTiBFArPBCaSiThSiRnTiBPBPMgArCaSiRnTiMgArCaSiThCaSiRnFArRnSiRnFArTiTiBFArCaCaSiRnSiThCaCaSiRnMgArFYSiRnFYCaFArSiThCaSiThPBPTiMgArCaPRnSiAlArPBCaCaSiRnFYSiThCaRnFArArCaCaSiRnPBSiRnFArMgYCaCaCaCaSiThCaCaSiAlArCaCaSiRnPBSiAlArBCaCaCaCaSiThCaPBSiThPBPBCaSiRnFYFArSiThCaSiRnFArBCaCaSiRnFYFArSiThCaPBSiThCaSiRnPMgArRnFArPTiBCaPRnFArCaCaCaCaSiRnCaCaSiRnFYFArFArBCaSiThFArThSiThSiRnTiRnPMgArFArCaSiThCaPBCaSiRnBFArCaCaPRnCaCaPMgArSiRnFYFArCaSiThRnPBPMgAr"

    # part 1 answer
    childs = generator(molecule, transitions, 0)
    print("New combinations from medicine =", len(childs))

    # part 2 answer
    solution2(molecule, transitions)


"""

    previous_gen = {"e"}  # set
    medicine = "CRnCaSiRnBSiRnFArTiBPTiTiBFArPBCaSiThSiRnTiBPBPMgArCaSiRnTiMgArCaSiThCaSiRnFArRnSiRnFArTiTiBFArCaCaSiRnSiThCaCaSiRnMgArFYSiRnFYCaFArSiThCaSiThPBPTiMgArCaPRnSiAlArPBCaCaSiRnFYSiThCaRnFArArCaCaSiRnPBSiRnFArMgYCaCaCaCaSiThCaCaSiAlArCaCaSiRnPBSiAlArBCaCaCaCaSiThCaPBSiThPBPBCaSiRnFYFArSiThCaSiRnFArBCaCaSiRnFYFArSiThCaPBSiThCaSiRnPMgArRnFArPTiBCaPRnFArCaCaCaCaSiRnCaCaSiRnFYFArFArBCaSiThFArThSiThSiRnTiRnPMgArFArCaSiThCaPBCaSiRnBFArCaCaPRnCaCaPMgArSiRnFYFArCaSiThRnPBPMgAr"
    steps = 0
    found = False
    from_i = 0
    while not found:
        steps += 1
        new_subjects = set()
        for test_subject in previous_gen:
            new_subjects.update(generator(test_subject, transitions, from_i))
            print(f"new subjects {len(new_subjects)}")
            if medicine in new_subjects:
                found = True
                break
        # trying to speed up
        best_subjects = set()
        for subject in new_subjects:
            l = len(subject) - LOOKAHEAD_SIZE
            if l > 0:
                if steps == 8:
                    print(subject)
                    print(subject[:l])
                    print(medicine[:l])
                if subject[:l] == medicine[:l]:
                    print("found", subject)
                    best_subjects.add(subject)
                    from_i = l if l > from_i else from_i

        # fase de rejeição
        # for subject in new_subjects:
        #    if len(subject) < from_i:
        #        previous_gen.remove(subject)

        if len(best_subjects) == 0:
            previous_gen = new_subjects
        else:
            previous_gen = set(
                s for s in best_subjects if len(s) >= from_i + LOOKAHEAD_SIZE
            )

        print(f"Step {steps}, subjects {len(previous_gen)}, min_len {from_i}")
        # print(previous_gen)
        # if steps == 2:
        #    break
"""
