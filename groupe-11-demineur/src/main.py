# main.py
import pygame
import sys
from settings import *
from game import Game
from solver import MinesweeperSolver

def draw_grid(screen, game):
    screen.fill(GRAY)

    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE + TOOLBAR_HEIGHT, CELL_SIZE, CELL_SIZE)

            if game.revealed[r][c]:
                # Case révélée
                pygame.draw.rect(screen, DARK_GRAY, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

                if game.grid[r][c] == -1:  # Mine
                    pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 4)
                elif game.grid[r][c] > 0:
                    font = pygame.font.SysFont(None, 40)
                    text = font.render(str(game.grid[r][c]), True, NUM_COLORS.get(game.grid[r][c], BLACK))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
            else:
                # Case cachée
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)
                if game.flags[r][c]:
                    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + TOOLBAR_HEIGHT))
    pygame.display.set_caption("Démineur IA - CSP Solver")
    clock = pygame.time.Clock()

    game = Game()
    ai = MinesweeperSolver()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Clic souris
            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                mx, my = pygame.mouse.get_pos()
                my -= TOOLBAR_HEIGHT
                if my >= 0:
                    r, c = my // CELL_SIZE, mx // CELL_SIZE
                    if event.button == 1:
                        game.reveal(r, c)
                    elif event.button == 3:
                        game.toggle_flag(r, c)

            # Touche clavier
            if event.type == pygame.KEYDOWN:
                if not game.game_over:
                    if event.key == pygame.K_SPACE:
                        # Lancer IA
                        solver_grid = game.get_state_for_solver()
                        safes, mines = ai.solve(solver_grid)

                        for rr, cc in mines:
                            if not game.flags[rr][cc]:
                                game.toggle_flag(rr, cc)
                        for rr, cc in safes:
                            game.reveal(rr, cc)

                        if not safes and not mines:
                            print("IA bloquée, aucun coup sûr trouvé !")

                if event.key == pygame.K_r:
                    game = Game()
                    print("Jeu redémarré !")

        # Vérifier victoire
        if not game.game_over:
            revealed_count = sum(sum(1 for cell in row if cell) for row in game.revealed)
            total_safe = ROWS * COLS - MINES_COUNT
            if revealed_count == total_safe:
                game.game_over = True
                game.won = True

        draw_grid(screen, game)

        # Message fin de partie
        if game.game_over:
            font = pygame.font.SysFont(None, 60)
            if getattr(game, "won", False):
                text = font.render("GAGNÉ !", True, GREEN)
            else:
                text = font.render("PERDU !", True, RED)
            screen.blit(text, (WIDTH // 2 - 80, HEIGHT // 2))

            # Indiquer comment rejouer
            font2 = pygame.font.SysFont(None, 30)
            msg = font2.render("Appuyez sur R pour rejouer", True, BLACK)
            screen.blit(msg, (WIDTH // 2 - 120, HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
