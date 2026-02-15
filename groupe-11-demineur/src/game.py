# game.py

import random
from settings import *

class Game:
    def __init__(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.flags = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.mines = set()
        self.game_over = False
        self.won = False
        self._generate_mines()
        self._calculate_numbers()

    def _generate_mines(self):
        """Place les mines aléatoirement."""
        count = 0
        while count < MINES_COUNT:
            r = random.randint(0, ROWS - 1)
            c = random.randint(0, COLS - 1)
            if (r, c) not in self.mines:
                self.mines.add((r, c))
                self.grid[r][c] = -1 
                count += 1

    def _calculate_numbers(self):
        """Calcule les chiffres pour chaque case adjacente aux mines."""
        for r in range(ROWS):
            for c in range(COLS):
                if (r, c) in self.mines:
                    continue
                count = 0
                for dr in [-1,0,1]:
                    for dc in [-1,0,1]:
                        if dr==0 and dc==0: continue
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < ROWS and 0 <= nc < COLS:
                            if (nr,nc) in self.mines:
                                count += 1
                self.grid[r][c] = count

    def reveal(self, r, c):
        """Révèle une case et ses voisins si 0 (itératif pour éviter recursion error)."""
        if not (0 <= r < ROWS and 0 <= c < COLS) or self.revealed[r][c] or self.flags[r][c]:
            return

        stack = [(r,c)]
        while stack:
            rr, cc = stack.pop()
            if self.revealed[rr][cc] or self.flags[rr][cc]:
                continue
            self.revealed[rr][cc] = True
            if (rr, cc) in self.mines:
                self.game_over = True
                return
            if self.grid[rr][cc] == 0:
                for dr in [-1,0,1]:
                    for dc in [-1,0,1]:
                        nr, nc = rr+dr, cc+dc
                        if 0 <= nr < ROWS and 0 <= nc < COLS and not self.revealed[nr][nc]:
                            stack.append((nr,nc))

    def toggle_flag(self, r, c):
        if not self.revealed[r][c]:
            self.flags[r][c] = not self.flags[r][c]

    def get_state_for_solver(self):
        """
        -1 : Inconnu
        -2 : Drapeau
        0-8 : Chiffre révélé
        """
        solver_grid = []
        for r in range(ROWS):
            row_data = []
            for c in range(COLS):
                if self.revealed[r][c]:
                    row_data.append(self.grid[r][c])
                elif self.flags[r][c]:
                    row_data.append(-2)
                else:
                    row_data.append(-1)
            solver_grid.append(row_data)
        return solver_grid
