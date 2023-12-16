# Import necessary modules
import pygame
import sys
from cell import Cell  # Assuming Cell class is defined in the 'cell' module

# Pygame initialization
pygame.init()

# Constants
SCREEN_MIN_SIZE = 750
AMOUNT_OF_CELLS = 16
BOMB_CHANCE = 0.25

CELL_SIZE = SCREEN_MIN_SIZE // AMOUNT_OF_CELLS
READJUSTED_SIZE = CELL_SIZE * AMOUNT_OF_CELLS
CELL_WIDTH = CELL_HEIGHT = CELL_SIZE

# Set up the game window
SCREEN_WIDTH, SCREEN_HEIGHT = READJUSTED_SIZE, READJUSTED_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the window caption
pygame.display.set_caption("MineSweeper")

# List to store the cells
cells = []


def create_cells():
    # Access the global cells variable and clear it
    global cells
    cells.clear()
    # Create a 2D list of Cell objects
    for i in range(AMOUNT_OF_CELLS):
        row = []
        for j in range(AMOUNT_OF_CELLS):
            # Create a Cell object and append it to the current row
            cell = Cell(j * CELL_SIZE, i * CELL_SIZE,
                        CELL_WIDTH, CELL_HEIGHT, BOMB_CHANCE, i, j)
            row.append(cell)
        # Append the current row to the cells list
        cells.append(row)


def reveal_cell(cell):
    # Reveal the cell and update nearby bomb counts
    if not cell.revealed:
        cell.reveal()
        if cell.is_bomb:
            print("Game Over! You hit the mine.")
            # terminate_program()  # End the game when a mine is clicked
          # run_setup() (kan aktiveras för att starta om spelet)
        elif not cell.is_bomb:
            bombs_nearby = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= cell.row + i < AMOUNT_OF_CELLS and 0 <= cell.col + j < AMOUNT_OF_CELLS:
                        neighbor = cells[cell.row + i][cell.col + j]
                        if neighbor.is_bomb:
                            bombs_nearby += 1
            cell.bombs_nearby = bombs_nearby
            if bombs_nearby == 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= cell.row + i < AMOUNT_OF_CELLS and 0 <= cell.col + j < AMOUNT_OF_CELLS:
                            neighbor = cells[cell.row + i][cell.col + j]
                            # Recursively reveal neighboring cells
                            reveal_cell(neighbor)


def draw_cells():
    # Draw cells on the screen
    for row in cells:
        for cell in row:
            cell.draw(screen)
            if cell.revealed:
                if cell.is_bomb:
                    # Display bomb emoji when a bomb is revealed
                    font = pygame.font.SysFont(None, 36)
                    text = font.render(
                        "B", True, (255, 0, 0))  # Bomb emoji
                    text_rect = text.get_rect(
                        center=(cell.x + CELL_SIZE // 2, cell.y + CELL_SIZE // 2))
                    screen.blit(text, text_rect)
                elif cell.bombs_nearby > 0:
                    # Display the count if bombs are nearby
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(cell.bombs_nearby),
                                       True, (255, 255, 255))
                    text_rect = text.get_rect(
                        center=(cell.x + CELL_SIZE // 2, cell.y + CELL_SIZE // 2))
                    screen.blit(text, text_rect)


def handle_mouse_click(pos, left_click, right_click):
    # Handle mouse clicks
    if left_click:
        for row in cells:
            for cell in row:
                if pygame.Rect(cell.x, cell.y, cell.width, cell.height).collidepoint(pos):
                    reveal_cell(cell)


def terminate_program():
    # Terminate the program
    pygame.quit()
    sys.exit()


def run_setup():
    # Run initial setup
    create_cells()


def event_handler(event):
    # Handle Pygame events
    if event.type == pygame.QUIT:
        terminate_program()
    elif event.type == pygame.MOUSEBUTTONDOWN:
        left_click, _, right_click = pygame.mouse.get_pressed()
        handle_mouse_click(event.pos, left_click, right_click)


def main():
    # Main game loop
    run_setup()
    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            event_handler(event)

        draw_cells()
        pygame.display.flip()


if __name__ == "__main__":
    main()
