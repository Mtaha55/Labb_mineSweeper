# Import necessary modules
import pygame
import random

# List to store the cells
grid = []  # The main grid of cells
bomb = []  # Positions of the bombs


class Cell:
    def __init__(self, x, y, width, height, bomb_chance, row, col):
        # Initialize the cell attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (0, 64, 0)  # RGB color
        self.cell_thickness = 2
        self.selected = False
        self.revealed = False  # Attribute to indicate if the cell is revealed

        self.cell_center = (
            self.x + self.width // 2,
            self.y + self.width // 2,
        )  # Useful for drawing
        self.bomb = (
            random.random() < bomb_chance
        )  # Each cell has a chance to be a bomb
        # Attribute to hold the number of neighbors that are bombs
        self.neighbouring_bombs = 0

        self.is_bomb = random.random() < bomb_chance
        self.bombs_nearby = 0
        self.row = row  # Row index of the cell
        self.col = col  # Column index of the cell

    def draw(self, screen):
        """Draw the cell on the screen"""
        # Draw the cell's rectangle
        if self.selected:
            pygame.draw.rect(screen, (128, 128, 128),
                             (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.color,
                             (self.x, self.y, self.width, self.height))

        # Draw the cell's border
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y,
                         self.width, self.height), self.cell_thickness)

        # Draw bombs inside the cells
        if self.bomb and self.selected:
            pygame.draw.circle(screen, (255, 0, 0),
                               self.cell_center, self.width // 4)

        # Show the cell's content if it is revealed
        if self.revealed:
            # if self.bomb:
            #     self.color = (255, 0, 0)  # Change color to red for bombs
            # else:
            self.color = (192, 192, 192)  # Gray color for revealed cells
            font = pygame.font.Font(None, 24)
            text = font.render(
                str(self.neighbouring_bombs), True, (0, 0, 0))
            text_rect = text.get_rect(center=self.cell_center)
            screen.blit(text, text_rect.topleft)

        # Update the cell's visual representation on the screen
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y,
                         self.width, self.height), self.cell_thickness)

        if self.revealed and not self.is_bomb:
            font = pygame.font.Font(None, 36)
            text = font.render(str(self.bombs_nearby), True, (255, 255, 255))
            text_rect = text.get_rect(
                center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(text, text_rect)

    def reveal(self):
        self.revealed = True
        # Update the cell's internal state when revealed

    def count_bombs(self, grid):
        # Count the number of neighboring bombs
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= self.y + i < len(grid) and 0 <= self.x + j < len(grid[0]):
                    if grid[self.y + i][self.x + j].is_bomb and not (i == 0 and j == 0):
                        self.bombs_nearby += 1
