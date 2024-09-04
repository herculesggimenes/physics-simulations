import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
CHARGE_COLOR_POSITIVE = (255, 0, 0)  # Red for positive charge
CHARGE_COLOR_NEGATIVE = (0, 0, 255)  # Blue for negative charge
CHARGE_RADIUS = 15
K = 8.99e9  # Coulomb's constant (in N m^2/C^2)
GRID_STEP = 20  # Step size for grid points
ARROW_LENGTH = 20
ARROW_HEAD_SIZE = 10
FONT_SIZE = 20

# Initialize screen and font
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Electric Field Simulation")
font = pygame.font.SysFont(None, FONT_SIZE)

class Charge:
    def __init__(self, x, y, charge):
        self.x = x
        self.y = y
        self.charge = charge
        self.color = CHARGE_COLOR_POSITIVE if charge > 0 else CHARGE_COLOR_NEGATIVE
        self.dragging = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), CHARGE_RADIUS)

    def calculate_field(self, x, y):
        """
        Calculate the electric field at a point (x, y) due to this charge.
        """
        dx = x - self.x
        dy = y - self.y
        distance_squared = dx**2 + dy**2
        distance = math.sqrt(distance_squared)

        if distance == 0:
            return (0, 0)  # Avoid division by zero

        # Calculate the magnitude of the electric field
        field_magnitude = K * self.charge / distance_squared
        # Calculate field components
        field_x = field_magnitude * (dx / distance)
        field_y = field_magnitude * (dy / distance)

        return (field_x, field_y)

def draw_arrow(screen, start, end, color):
    pygame.draw.line(screen, color, start, end, 2)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    pygame.draw.polygon(screen, color, [
        (end[0] - ARROW_HEAD_SIZE * math.cos(angle - math.pi / 6),
         end[1] - ARROW_HEAD_SIZE * math.sin(angle - math.pi / 6)),
        (end[0] - ARROW_HEAD_SIZE * math.cos(angle + math.pi / 6),
         end[1] - ARROW_HEAD_SIZE * math.sin(angle + math.pi / 6)),
        end
    ])

# Create charges
charge1 = Charge(WIDTH // 3, HEIGHT // 2, 1e-3)  # Positive charge
charge2 = Charge(2 * WIDTH // 3, HEIGHT // 2, 1e-3)  # Negative charge

charges = [charge1, charge2]

dragging_charge = None
clock = pygame.time.Clock()

running = True

def is_point_within_circle(x, y, cx, cy, radius):
    return (x - cx)**2 + (y - cy)**2 <= radius**2

while running:
    screen.fill(BACKGROUND_COLOR)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for charge in charges:
                if is_point_within_circle(event.pos[0], event.pos[1], charge.x, charge.y, CHARGE_RADIUS):
                    charge.dragging = True
                    dragging_charge = charge
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_charge:
                dragging_charge.dragging = False
                dragging_charge = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging_charge:
                dragging_charge.x, dragging_charge.y = event.pos

    # Draw charges
    for charge in charges:
        charge.draw(screen)

    # Calculate and draw electric field vectors
    for x in range(0, WIDTH, GRID_STEP):
        for y in range(0, HEIGHT, GRID_STEP):
            total_field_x = 0
            total_field_y = 0

            for charge in charges:
                field_x, field_y = charge.calculate_field(x, y)
                total_field_x += field_x
                total_field_y += field_y

            field_magnitude = math.sqrt(total_field_x**2 + total_field_y**2)
            if field_magnitude > 0:
                # Scale the field vector for visualization
                scale = ARROW_LENGTH / field_magnitude
                end_x = x + scale * total_field_x
                end_y = y + scale * total_field_y
                draw_arrow(screen, (x, y), (end_x, end_y), (0, 0, 0))

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
