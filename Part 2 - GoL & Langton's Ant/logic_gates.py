# -*- coding: utf-8 -*-
"""
Glider-based Logic Gates Student Template Module.
"""
import numpy as np
from conway import GameOfLife


class GliderLogicGates:
    """
    Implementation of logic gates (AND, NOT) using glider collisions
    to demonstrate the Turing completeness of Conway's Game of Life.
    """

    def __init__(self):
        # ذخیره نتایج محاسبات پویا برای جلوگیری از تکرار محاسبات
        self._and_setup = None
        self._not_setup = None

    def _step_game(self, gol):
        """متد کمکی برای اجرای یک گام شبیه‌سازی با سازگاری بالا"""
        if hasattr(gol, 'step'):
            gol.step()
        elif hasattr(gol, 'update'):
            gol.update()
        elif hasattr(gol, 'evolve'):
            gol.evolve()
        elif hasattr(gol, 'next_generation'):
            gol.next_generation()

    def _get_grid(self, gol):
        """متد کمکی برای دسترسی ایمن به آرایه دو بعدی گرید"""
        if hasattr(gol, 'grid'):
            return gol.grid
        elif hasattr(gol, 'get_grid'):
            return gol.get_grid()
        elif hasattr(gol, 'board'):
            return gol.board
        return None

    def _find_and_gate_setup(self):
        """
        یافتن خودکار مختصات برخورد برای تشکیل بلوک 2x2 در نقطه دقیق
        """
        glider_se = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        glider_sw = [(0, 1), (1, 0), (2, 0), (2, 1), (2, 2)]

        # استفاده از گرید بزرگتر برای جلوگیری از تداخل با مرزها حین جستجو
        for r_b in range(0, 30):
            for c_b in range(4, 35):
                grid = np.zeros((60, 60), dtype=int)
                for dr, dc in glider_se:
                    grid[5 + dr, 5 + dc] = 1
                for dr, dc in glider_sw:
                    grid[r_b + dr, c_b + dc] = 1

                temp_grid = grid.copy()
                boundary_hit = False

                for step in range(1, 80):
                    N = np.zeros_like(temp_grid, dtype=int)
                    N[1:-1, 1:-1] = (
                            temp_grid[:-2, :-2] + temp_grid[:-2, 1:-1] + temp_grid[:-2, 2:] +
                            temp_grid[1:-1, :-2] + temp_grid[1:-1, 2:] +
                            temp_grid[2:, :-2] + temp_grid[2:, 1:-1] + temp_grid[2:, 2:]
                    )
                    next_grid = ((temp_grid == 1) & ((N == 2) | (N == 3))) | ((temp_grid == 0) & (N == 3))
                    temp_grid = next_grid.astype(int)

                    # اگر به مرزها برخورد کرد، شبیه‌سازی این نقطه نامعتبر است
                    if np.any(temp_grid[0:3, :]) or np.any(temp_grid[-3:, :]) or np.any(temp_grid[:, 0:3]) or np.any(
                            temp_grid[:, -3:]):
                        boundary_hit = True
                        break

                    # بررسی اینکه آیا دقیقاً یک بلوک 2x2 باقی مانده است
                    if np.sum(temp_grid) == 4:
                        r_coords, c_coords = np.where(temp_grid == 1)
                        if (max(r_coords) - min(r_coords) == 1) and (max(c_coords) - min(c_coords) == 1):
                            block_r, block_c = min(r_coords), min(c_coords)

                            # شیفت دادن مختصات برای قرارگیری بلوک دقیقاً در (12, 15)
                            shift_r = 12 - block_r
                            shift_c = 15 - block_c

                            sa_r, sa_c = 5 + shift_r, 5 + shift_c
                            sb_r, sb_c = r_b + shift_r, c_b + shift_c

                            # اطمینان از قرارگیری نقاط شروع در گرید استاندارد 35x35
                            if 0 <= sa_r <= 32 and 0 <= sa_c <= 32 and 0 <= sb_r <= 32 and 0 <= sb_c <= 32:
                                return (sa_r, sa_c), (sb_r, sb_c), step

        return (2, 5), (2, 19), 24

    def _find_not_gate_setup(self):
        """
        یافتن خودکار مختصات نابودی کامل (Annihilation) برای گیت NOT
        """
        glider_se = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        glider_sw = [(0, 1), (1, 0), (2, 0), (2, 1), (2, 2)]

        for r_a in range(0, 30):
            for c_a in range(4, 35):
                grid = np.zeros((60, 60), dtype=int)
                # گلایدر کنترل
                for dr, dc in glider_se:
                    grid[5 + dr, 5 + dc] = 1
                # گلایدر ورودی A
                for dr, dc in glider_sw:
                    grid[r_a + dr, c_a + dc] = 1

                temp_grid = grid.copy()
                annihilated = False
                boundary_hit = False

                for step in range(1, 80):
                    N = np.zeros_like(temp_grid, dtype=int)
                    N[1:-1, 1:-1] = (
                            temp_grid[:-2, :-2] + temp_grid[:-2, 1:-1] + temp_grid[:-2, 2:] +
                            temp_grid[1:-1, :-2] + temp_grid[1:-1, 2:] +
                            temp_grid[2:, :-2] + temp_grid[2:, 1:-1] + temp_grid[2:, 2:]
                    )
                    next_grid = ((temp_grid == 1) & ((N == 2) | (N == 3))) | ((temp_grid == 0) & (N == 3))
                    temp_grid = next_grid.astype(int)

                    # اگر قبل از تصادم به مرز گرید داخلی برخورد کند، نابودی کاذب است
                    if np.any(temp_grid[0:3, :]) or np.any(temp_grid[-3:, :]) or np.any(temp_grid[:, 0:3]) or np.any(
                            temp_grid[:, -3:]):
                        boundary_hit = True
                        break

                    # نابودی مطلق یعنی صفر شدن تمام سلول‌ها در فضای آزاد
                    if np.sum(temp_grid) == 0:
                        annihilated = True
                        annihilation_step = step
                        break

                if annihilated and not boundary_hit:
                    if 0 <= r_a <= 32 and 0 <= c_a <= 32:
                        return (5, 5), (r_a, c_a), annihilation_step

        return (2, 2), (2, 10), 20

    def setup_and_gate(self, grid_size=35, input_a_present=False, input_b_present=False):
        if self._and_setup is None:
            self._and_setup = self._find_and_gate_setup()

        pos_a, pos_b, _ = self._and_setup
        gol = GameOfLife(grid_size)
        grid = self._get_grid(gol)

        if grid is not None:
            grid.fill(0)
            glider_se = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
            glider_sw = [(0, 1), (1, 0), (2, 0), (2, 1), (2, 2)]

            if input_a_present:
                for dr, dc in glider_se:
                    grid[pos_a[0] + dr, pos_a[1] + dc] = 1
            if input_b_present:
                for dr, dc in glider_sw:
                    grid[pos_b[0] + dr, pos_b[1] + dc] = 1

        return gol

    def setup_not_gate(self, grid_size=35, input_a_present=False):
        if self._not_setup is None:
            self._not_setup = self._find_not_gate_setup()

        pos_control, pos_a, _ = self._not_setup
        gol = GameOfLife(grid_size)
        grid = self._get_grid(gol)

        if grid is not None:
            grid.fill(0)
            glider_se = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
            glider_sw = [(0, 1), (1, 0), (2, 0), (2, 1), (2, 2)]

            # گلایدر کنترل (کمکی) همیشه شلیک می‌شود
            for dr, dc in glider_se:
                grid[pos_control[0] + dr, pos_control[1] + dc] = 1

            # شلیک گلایدر ورودی تنها در صورتی که سیگنال فعال باشد
            if input_a_present:
                for dr, dc in glider_sw:
                    grid[pos_a[0] + dr, pos_a[1] + dc] = 1

        return gol

    def run_and_gate(self, input_a_present, input_b_present):
        if self._and_setup is None:
            self._and_setup = self._find_and_gate_setup()
        _, _, steps = self._and_setup

        gol = self.setup_and_gate(grid_size=35, input_a_present=input_a_present, input_b_present=input_b_present)

        for _ in range(steps + 5):
            self._step_game(gol)

        grid = self._get_grid(gol)
        if grid is not None:
            # بررسی قطعی وجود بلوک 2x2 پایدار در مختصات (12, 15)
            block_exists = np.all(grid[12:14, 15:17] == 1)
            return bool(block_exists)
        return False

    def run_not_gate(self, input_a_present):
        if self._not_setup is None:
            self._not_setup = self._find_not_gate_setup()
        _, _, steps = self._not_setup

        gol = self.setup_not_gate(grid_size=35, input_a_present=input_a_present)

        for _ in range(steps + 5):
            self._step_game(gol)

        grid = self._get_grid(gol)
        if grid is not None:
            # اگر نابودی اتفاق افتاده باشد مجموع 0 خواهد بود (False). در غیر این صورت گلایدر کنترل زنده است (True).
            live_cells = np.sum(grid)
            return bool(live_cells > 0)
        return False