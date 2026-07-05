# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

#create the Turing machine
transitions = {
        # TODO: Part II b) - Write your transition rules here as entries to a Python dictionary
        # For example, the key will be a pair (state, character)
        # The value will be the triple (next state, character to write, move head L or R)
        # such as ('q0', '1'): ('q1', '0', 'R'), which says if current state is q0 and 1 encountered
        # then transition to state q1, write a 0 and move head right.

        ('q0', '1'): ('q1', '', 'R'),
        ('q0', '0'): ('q_clean', '', 'R'),

        ('q1', '1'): ('q1', '1', 'R'),
        ('q1', '0'): ('q2', '0', 'R'),

        ('q2', '1'): ('q3', 'Y', 'R'),
        ('q2', 'Z'): ('q_reset_Y', 'Z', 'L'),
        ('q2', ''): ('q_reset_Y', '', 'L'),

        ('q3', '1'): ('q3', '1', 'R'),
        ('q3', 'Z'): ('q3', 'Z', 'R'),
        ('q3', ''): ('q4', 'Z', 'L'),

        ('q4', 'Z'): ('q4', 'Z', 'L'),
        ('q4', '1'): ('q4', '1', 'L'),
        ('q4', 'Y'): ('q2', 'Y', 'R'),

        ('q_reset_Y', 'Y'): ('q_reset_Y', '1', 'L'),
        ('q_reset_Y', '0'): ('q_rewind', '0', 'L'),

        ('q_rewind', '1'): ('q_rewind', '1', 'L'),
        ('q_rewind', ''): ('q0', '', 'R'),

        ('q_clean', '1'): ('q_clean', '', 'R'),
        ('q_clean', 'Z'): ('q_finish', '1', 'R'),
        ('q_clean', ''): ('qa', '', 'R'),

        ('q_finish', 'Z'): ('q_finish', '1', 'R'),
        ('q_finish', ''): ('qa', '', 'R')
}
if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)

    def run(input_):
        w = input_
        print("Input:",w)
        print("Accepted" if machine.accepts(w, step_limit=1000) else "Rejected")
        machine.debug(w, step_limit=1000)

        print()

    # SHOULD ACCEPT
    run("110111")
    # outputs 111111

    # SHOULD ACCEPT
    run("11101111")
    # outputs 111111111111

    run("01111")
