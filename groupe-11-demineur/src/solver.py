# solver.py

from settings import ROWS, COLS

class MinesweeperSolver:
    def __init__(self):
        pass

    def get_neighbors(self, r, c):
        neighbors = []
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr==0 and dc==0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    neighbors.append((nr,nc))
        return neighbors

    def solve(self, grid):
        """
        Retourne deux listes :
        - safe_moves : cases à révéler en toute sécurité
        - mine_moves : cases à drapeau en toute sécurité
        """
        safe_moves = []
        mine_moves = []

        for r in range(ROWS):
            for c in range(COLS):
                val = grid[r][c]
                if 0 <= val <= 8:
                    neighbors = self.get_neighbors(r,c)
                    hidden = []
                    flagged_count = 0
                    for nr, nc in neighbors:
                        if grid[nr][nc] == -1:      # cachée
                            hidden.append((nr,nc))
                        elif grid[nr][nc] == -2:    # drapeau
                            flagged_count += 1

                    # mines deja marque ?
                    if val == flagged_count and hidden:
                        safe_moves.extend(hidden)

                    # mines autour ?
                    if val - flagged_count == len(hidden) and hidden:
                        mine_moves.extend(hidden)

        # retirer doublons
        safe_moves = list(set(safe_moves))
        mine_moves = list(set(mine_moves))
        return safe_moves, mine_moves
