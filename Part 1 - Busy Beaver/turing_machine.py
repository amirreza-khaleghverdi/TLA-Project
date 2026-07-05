# -*- coding: utf-8 -*-
"""A Turing machine simulator skeleton.

    Accepting '#'
    =============

    >>> from turing_machine import TuringMachine

    Instantiate the machine with particular transitions.

    >>> one_hash = TuringMachine(
    ...     {
    ...         ('q0', '#'): ('saw_#', '#', 'R'),
    ...         ('saw_#', ''): ('qa', '', 'R'),
    ...     }
    ... )

    Check whether it accepts a string:

    >>> one_hash.accepts('#')
    True

    >>> one_hash.accepts('##')
    False

    Check whether it rejects a string:

    >>> one_hash.rejects('#')
    False

    >>> one_hash.rejects('##')
    True

"""

import logging
from itertools import islice


class TuringMachine:
    """Turing machine simulator class.

    A machine is instantiated with transitions, start, accept and reject states
    and a blank symbol. We assume that the input and the tape alphabet can be
    deducted from the transitions.

    :param dict transitions: a mapping from (state, symbol) tuples to (state,
    symbol, direction) tuple. Directions are either 'L' (for left) or 'R' (for right).

    :param start_state: the initial state of the machine.

    :param accept_state: the accept state.

    :param reject_state: the reject state.

    :blank_symbol: the special symbol that marks the tape cell to be empty.

    """

    def __init__(self, transitions, start_state='q0', accept_state='qa', reject_state='qr', blank_symbol=''):
        # TODO: Implement the constructor. Initialize transitions, start_state, accept_state,
        # reject_state, blank_symbol, and any other helpful structures.
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol

    def run(self, input_, for_check=False, part_3=False):
        """Execute the Turing machine for a particular input.

        :param input_: the input that is written on the tape. It can be a list
        of strings, or just a string, in which case each letter is treated as a symbol.

        This method MUST be a Python generator. It should yield a (action, configuration) tuple
        at each step of the computation.
        
        The action is either 'Accept', 'Reject' or None. 
        
        Configuration is a dictionary with the following keys:
        - 'state': the current state,
        - 'left_hand_side': list of symbols on the left hand side of the current position (closest first),
        - 'symbol': the current symbol under the head,
        - 'right_hand_side': list of symbols on the right hand side of the current position.

        """
        # TODO: Implement the simulator loop as a Python generator.
        # 1. Initialize the tape using two lists (left_hand_side and right_hand_side) and the current symbol.
        # 2. Yield the current step (action, configuration).
        # 3. Read transitions and update state, write symbols, and move the head ('L' or 'R').
        # 4. Handle tape expansion dynamically for both left and right directions (double-sided infinite tape).
        # 5. Log a warning using logging.warning() if the singly-infinite tape boundary is crossed before Part III.
        # 1. Initialize the tape
        tape = list(input_) if input_ else []
        if not tape:
            tape = [self.blank_symbol]
            
        left_hand_side = []
        symbol = tape[0]
        right_hand_side = tape[1:]
        
        state = self.start_state

        # 2. Simulator loop
        while True:
            # Check acceptance / rejection criteria
            if state == self.accept_state:
                action = 'Accept'
            elif state == self.reject_state:
                action = 'Reject'
            else:
                action = None

            # Create current configuration
            config = {
                'state': state,
                'left_hand_side': list(left_hand_side),
                'symbol': symbol,
                'right_hand_side': list(right_hand_side)
            }
            if action is not None and part_3:
                pass#print("".join(left_hand_side) + symbol + "".join(right_hand_side))

            # Yield the current step
            yield (action, config)

            # If an end state is reached, break the generator loop
            
            if action is not None:
                final_tape = "".join(left_hand_side) + symbol + "".join(right_hand_side)
                print(f"{"Final tape:": <15} {final_tape}")
                if (part_3):
                    print(f"Number of 1 in final tape: {final_tape.count("1")}")
                break

            # 3. Read transitions
            transition = self.transitions.get((state, symbol))
            if transition is None:
                # Implicit reject if no transition rule is defined
                state = self.reject_state
                continue
                
            next_state, write_symbol, direction = transition
            
            # Update state and write the new symbol to the current cell
            state = next_state
            symbol = write_symbol

            # 4. Handle tape expansion & Move the head ('L' or 'R')
            if direction == 'R':
                left_hand_side.append(symbol)
                if right_hand_side:
                    symbol = right_hand_side.pop(0)
                else:
                    symbol = self.blank_symbol
            elif direction == 'L':
                right_hand_side.insert(0, symbol)
                if left_hand_side:
                    symbol = left_hand_side.pop()
                else:
                    # 5. Handle infinite tape to the left and log a warning
                    if not(for_check or part_3):
                        logging.warning("Crossed the left boundary of the singly-infinite tape!")
                    # state = self.reject_state
                    symbol = self.blank_symbol
            

    def accepts(self, input_, step_limit=100):
        """Check whether the Turing machine accepts a string.

        :param input_: the input string or list.
        :param step_limit: the maximum number of steps to simulate before stopping.
        :return: True if the machine halts in accept_state, False if it rejects,
                 or None if the step limit is reached without halting.
        """
        # TODO: Run the generator up to step_limit and check the action of the final yielded state.
        # Remember to log a warning if the step_limit is reached without halting.
        for step_idx, (action, config) in enumerate(self.run(input_, for_check=True)):
            if action == 'Accept':
                return True
            elif action == 'Reject':
                return False
                
            if step_idx >= step_limit:
                logging.warning(f"Step limit {step_limit} reached without halting.")
                return None
        
                
        return False

    def rejects(self, input_, **kwargs):
        """Check whether the Turing machine rejects a string.

        :param input_: the input string or list.
        :return: True if the machine rejects the string, False if it accepts.
        """
        # TODO: Determine rejection by checking if accepts() returns False.
        result = self.accepts(input_, **kwargs)
        if result is None:
            return None
        return not result

    def debug(self, input_, step_limit=100, colored=False, part_3=False):
        """Print the execution configuration of the machine per transition for debugging.

        :param input_: the input string or list.
        :param step_limit: the maximum number of steps to output.
        :param colored: True to output colored boundaries in terminal.
        """
        # TODO: Loop over the steps yielded by run() up to step_limit and print the tape configuration.
        # E.g., print the state and the tape with the head highlighted in brackets like: left[symbol]right

        last_time = False
        for step_idx, (action, config) in enumerate(self.run(input_, part_3=part_3)):
            if (last_time):
                break

            state = config['state']
            left_str = "".join(config['left_hand_side'])
            sym = config['symbol']
            right_str = "".join(config['right_hand_side'])
            
            if colored:
                # Add terminal color formatting for the head
                sym_str = f"\033[91m[{sym}]\033[0m"
            else:
                sym_str = f"[{sym}]"
                
            # Print configuration format: state_name left[symbol]right
            print(f"{state: <15} {left_str}{sym_str}{right_str}")
            
            if action is not None:
                last_time = True
                
            if step_idx >= step_limit:
                last_time = True
                break