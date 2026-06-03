import pygame
import sys
import copy

# --- CONFIGURATION ---
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10  # Taille d'une cellule en pixels
FPS = 10        # Vitesse de la simulation (générations par seconde)

# Couleurs (RGB)
COLOR_BG = (10, 10, 15)        # Fond presque noir
COLOR_GRID = (20, 20, 30)      # Grille subtile
COLOR_DIE = (100, 10, 50)      # Reflet de mort (optionnel)
COLOR_ALIVE = (0, 255, 150)    # Vert néon "bactérie"

# Calcul du nombre de colonnes et de lignes
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

def init_grid():
    """Crée une grille vide (toutes les cellules sont mortes = 0)."""
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def count_neighbors(grid, x, y):
    """Compte les 8 voisins vivants d'une cellule avec effet torique (les bords se touchent)."""
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            # Le modulo % permet de faire boucler la grille sur elle-même
            col = (x + i + COLS) % COLS
            row = (y + j + ROWS) % ROWS
            count += grid[row][col]
    return count

def update_grid(grid):
    """Applique les règles du Jeu de la Vie de Conway."""
    new_grid = copy.deepcopy(grid)
    for r in range(ROWS):
        for c in range(COLS):
            neighbors = count_neighbors(grid, c, r)
            
            # Règle 1 : Une cellule vivante meurt de sous-population ( < 2) ou de surpopulation ( > 3)
            if grid[r][c] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[r][c] = 0
            # Règle 2 : Une cellule morte naît si elle a exactement 3 voisins
            else:
                if neighbors == 3:
                    new_grid[r][c] = 1
    return new_grid

def draw_grid(screen, grid):
    """Dessine la grille et les cellules actives."""
    screen.fill(COLOR_BG)
    
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[r][c] == 1:
                pygame.draw.rect(screen, COLOR_ALIVE, rect)
            else:
                # Optionnel : dessine la grille pour aider au placement des pixels
                pygame.draw.rect(screen, COLOR_GRID, rect, 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("L'Automate Cellulaire : Boîte de Petri")
    clock = pygame.time.Clock()
    
    grid = init_grid()
    simulating = False  # En pause par défaut pour pouvoir dessiner
    drawing = False     # Pour savoir si l'utilisateur maintient le clic
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Contrôles clavier
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulating = not simulating  # Pause / Lecture
                    pygame.display.set_caption("Simulation en cours..." if simulating else "Simulation en PAUSE")
                elif event.key == pygame.K_c:
                    grid = init_grid()  # Effacer la grille (Clear)
                    simulating = False
            
            # Contrôles souris pour dessiner
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                
        # Gestion du dessin à la souris
        if drawing:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            c = mouse_x // CELL_SIZE
            r = mouse_y // CELL_SIZE
            if 0 <= c < COLS and 0 <= r < ROWS:
                # Un clic gauche ajoute une cellule, un clic droit (ou autre) peut l'effacer
                if pygame.mouse.get_pressed()[0]: 
                    grid[r][c] = 1
                elif pygame.mouse.get_pressed()[2]: 
                    grid[r][c] = 0

        # Mise à jour de la simulation
        if simulating:
            grid = update_grid(grid)
            
        draw_grid(screen, grid)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()