import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
CHARGE_COLOR_POSITIVE = (255, 0, 0)  # Red for positive charge
CHARGE_COLOR_NEGATIVE = (0, 0, 255)  # Blue for negative charge
CHARGE_RADIUS = 15
K = 8.99e9  # Coulomb's constant (in N m^2/C^2)
FPS = 60
ARROW_LENGTH = 100
ARROW_HEAD_SIZE = 10
FONT_SIZE = 20

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Electromagnetic Charge Simulation")
font = pygame.font.SysFont(None, FONT_SIZE)


# Charge class
class Charge:
    def __init__(self, x, y, charge):
        self.x = x
        self.y = y
        self.charge = charge
        self.color = CHARGE_COLOR_POSITIVE if charge > 0 else CHARGE_COLOR_NEGATIVE
        self.dragging = False

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), CHARGE_RADIUS)

    def calculate_force(self, other):
        """
        Calculate the force exerted on this charge by another charge.

        Parameters:
        - other: Another Charge object

        Returns:
        - (force_x, force_y): Force vector components (in newtons)
        """
        dx = other.x - self.x
        dy = other.y - self.y
        distance_squared = dx**2 + dy**2
        distance = math.sqrt(distance_squared)

        if distance == 0:
            return (0, 0)  # Avoid division by zero

        # Calculate the magnitude of the force
        force_magnitude = K * abs(self.charge * other.charge) / distance_squared

        # Calculate force components
        force_x = force_magnitude * (dx / distance)
        force_y = force_magnitude * (dy / distance)


        # If charges have opposite signs, the force should be attractive
        if self.charge * other.charge > 0:
            force_x = -force_x
            force_y = -force_y

        return (force_x, force_y)
    
    def calculate_resulting_force(self, charges):
        """
        Calculate the resulting force on this charge due to a list of other charges.

        Parameters:
        - charges: A list of Charge objects

        Returns:
        - (resultant_x, resultant_y): Resultant force vector components (in newtons)
        """
        resultant_x = 0
        resultant_y = 0

        for charge in charges:
            if charge != self:  # Avoid calculating force due to itself
                force_x, force_y = self.calculate_force(charge)
                resultant_x += force_x
                resultant_y += force_y

        return (resultant_x, resultant_y)

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

def draw_force_magnitude(screen, position, magnitude):
    text = font.render(f"{magnitude:.2e} N", True, (0, 0, 0))  # Display force magnitude
    text_rect = text.get_rect(center=position)
    screen.blit(text, text_rect)


def is_point_within_circle(x, y, cx, cy, radius):
    return (x - cx)**2 + (y - cy)**2 <= radius**2

# Create charges
charge1 = Charge(WIDTH // 3, HEIGHT // 2, 1e-6)  # Positive charge
charge2 = Charge(2 * WIDTH // 3, HEIGHT // 2, -1e-6)  # Negative charge
charge3 = Charge(3 * WIDTH // 3, HEIGHT // 2, -2e-6)  # Negative charge
charges = [
    charge1,
    charge2,
    charge3,
]

dragging_charge = None
clock = pygame.time.Clock()

running = True
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

    
    # Calculate and draw charge and forces
    for charge in charges:
        charge.draw()
        force_x, force_y = charge.calculate_resulting_force(charges)
        force_magnitude = math.sqrt(force_x**2 + force_y**2)
        scale = ARROW_LENGTH / max(force_magnitude, 1e-6)  # Avoid division by zero

        force_scaled = (charge.x + scale * force_x, charge.y + scale * force_y)
        draw_arrow(screen, (charge.x, charge.y), force_scaled, charge.color)
        draw_force_magnitude(screen, force_scaled, force_magnitude)

    

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
