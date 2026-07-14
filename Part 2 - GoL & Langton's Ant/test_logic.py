from logic_gates import GliderLogicGates

if __name__ == "__main__":
    gates = GliderLogicGates()

    print("=== Testing AND Gate ===")

    print("Input A=0, B=0  --> Output:", gates.run_and_gate(False, False))
    print("Input A=0, B=1  --> Output:", gates.run_and_gate(False, True))
    print("Input A=1, B=0  --> Output:", gates.run_and_gate(True, False))
    print("Input A=1, B=1  --> Output:", gates.run_and_gate(True, True))

    print("\n=== Testing NOT Gate ===")

    print("Input A=0 (False) --> Output:", gates.run_not_gate(False))
    print("Input A=1 (True)  --> Output:", gates.run_not_gate(True))