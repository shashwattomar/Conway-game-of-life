# import button
import pygame
import time

# Global variables
CELL_SIZE = 10
GRID_WIDTH = 60
GRID_HEIGHT = 40
DELAY = 0.1  # Delay in seconds

# Colors
red = (255, 0, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)

# Initialize the grid
grid = [[0] * GRID_HEIGHT for _ in range(GRID_WIDTH)]
next_grid = [[0] * GRID_HEIGHT for _ in range(GRID_WIDTH)]

# Initialize Pygame
pygame.init()
window_size = (GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

# UI elements
#start_button_rect = button.Button(10, 10, "Start-Button-Vector-PNG.png")
speed_button_rect = pygame.Rect(120, 10, 100, 30)
font = pygame.font.Font(None, 20)
start_button_text = font.render("Start", True, (0, 0, 0))
speed_button_text = font.render("Speed", True, (0, 0, 0))
speed = 1.0  # Initial speed multiplier

running = False  # Simulation state

def draw_grid():
    """Draw the grid on the window."""
    window.fill(red)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y] == 1:
                pygame.draw.rect(window, yellow, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def get_neighbour_count(x, y):
    """Get the count of live neighbors around a cell."""
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                count += grid[nx][ny]
    return count


def update_grid():
    """Update the grid based on the custom rules of the Game of Life."""
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            count = get_neighbour_count(x, y)
            if grid[x][y] == 1:
                if count < 2 or count > 3:
                    next_grid[x][y] = 0  # Cell dies due to underpopulation or overpopulation
                else:
                    next_grid[x][y] = 1  # Cell survives
            elif grid[x][y] == 0:
                if count == 3:
                    next_grid[x][y] = 1  # Cell becomes alive due to reproduction
                else:
                    next_grid[x][y] = 0  # Cell remains dead
    grid[:] = next_grid[:]


def handle_click(event):
    """Handle mouse click events."""
    x = event.pos[0] // CELL_SIZE
    y = event.pos[1] // CELL_SIZE
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        grid[x][y] = 1 - grid[x][y]  # Toggle cell state
        draw_grid()


def handle_start():
    """Start or stop the simulation."""
    global running
    running = not running


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                handle_click(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                handle_start()

    if running:
        update_grid()
        draw_grid()
        pygame.display.update()
        time.sleep(DELAY / speed)
        clock.tick()
