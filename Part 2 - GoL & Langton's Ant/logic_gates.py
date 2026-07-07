import numpy as np
from conway import GameOfLife


class GliderLogicGates:

    def setup_and_gate(
            self, grid_size=35, input_a_present=False, input_b_present=False
    ):
        sim = GameOfLife(N=grid_size, finite=True, fastMode=False)
        if input_a_present:
            # Glider A (حرکت به پایین-راست)
            sim.grid[2, 6] = 1
            sim.grid[3, 7] = 1
            sim.grid[4, 5] = 1
            sim.grid[4, 6] = 1
            sim.grid[4, 7] = 1
        if input_b_present:
            # Glider B (حرکت به بالا-راست)
            sim.grid[22, 6] = 1
            sim.grid[21, 7] = 1
            sim.grid[20, 5] = 1
            sim.grid[20, 6] = 1
            sim.grid[20, 7] = 1
        return sim

    def setup_not_gate(self, grid_size=35, input_a_present=False):
        sim = GameOfLife(N=grid_size, finite=True, fastMode=False)
        # گلایدر کنترل (همیشه شلیک می‌شود، حرکت به پایین-راست)
        sim.grid[2, 6] = 1
        sim.grid[3, 7] = 1
        sim.grid[4, 5] = 1
        sim.grid[4, 6] = 1
        sim.grid[4, 7] = 1

        if input_a_present:
            # گلایدر A اصلاح‌شده (حرکت به بالا-چپ برای برخورد دقیق شاخ‌به‌شاخ)
            # مختصات در مسیر مستقیم گلایدر کنترل تنظیم شده است
            sim.grid[20, 23] = 1
            sim.grid[20, 24] = 1
            sim.grid[20, 25] = 1
            sim.grid[21, 23] = 1
            sim.grid[22, 24] = 1
        return sim

    def run_and_gate(self, input_a_present, input_b_present):
        sim = self.setup_and_gate(35, input_a_present, input_b_present)
        for _ in range(85):
            sim.evolve()

        # بررسی یک ناحیه وسیع‌تر در مرکز شبکه
        # اگر برخوردی صورت گرفته باشد، بلوک در این ناحیه گیر می‌افتد
        collision_zone = sim.grid[10:16, 13:19]
        if np.sum(collision_zone) > 0:
            return True
        return False

    def run_not_gate(self, input_a_present):
        sim = self.setup_not_gate(35, input_a_present)
        for _ in range(100):
            sim.evolve()

        # منطقه هدف در پایین-راست نقشه (جایی که گلایدر کنترل باید برسد)
        output_region = sim.grid[20:, 20:]
        if np.sum(output_region) > 0:
            return True
        return False


if __name__ == "__main__":
    gates = GliderLogicGates()

    print("--- Testing AND Gate ---")
    print("0 AND 0 =", gates.run_and_gate(False, False))
    print("1 AND 0 =", gates.run_and_gate(True, False))
    print("0 AND 1 =", gates.run_and_gate(False, True))
    print("1 AND 1 =", gates.run_and_gate(True, True))

    print("\n--- Testing NOT Gate ---")
    print("NOT 0 =", gates.run_not_gate(False))
    print("NOT 1 =", gates.run_not_gate(True))