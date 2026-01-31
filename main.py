import pygame
import sys
import random
import math
from game_logic import NQueensModel
from renderer import IsometricRenderer
from ui_components import Button, Label

# Configuration
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

class Balloon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(2, 5)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.wobble = random.uniform(0, 6.28)

    def update(self):
        self.y -= self.speed
        self.x += math.sin(self.y * 0.02 + self.wobble) * 1.0

    def draw(self, screen):
        pygame.draw.line(screen, (150, 150, 150), (int(self.x), int(self.y + 20)), (int(self.x), int(self.y + 50)), 1)
        pygame.draw.ellipse(screen, self.color, (int(self.x - 15), int(self.y - 20), 30, 40))
        pygame.draw.ellipse(screen, (255, 255, 255), (int(self.x - 8), int(self.y - 12), 8, 12))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("N-Queens 2.5D")
    clock = pygame.time.Clock()

    # Initialize Game Components
    model = NQueensModel(n=5) # Default size 8
    renderer = IsometricRenderer(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # UI Components
    font_large = pygame.font.SysFont("impact", 42) # Interesting visual font
    font_small = pygame.font.SysFont("Segoe UI", 20)
    
    # Brighter Purple color
    btn_color = (130, 90, 180)
    btn_hover = (160, 120, 210)
    btn_reset = Button(20, 20, 100, 40, "Reset", font_small, bg_color=btn_color, hover_color=btn_hover)
    btn_solve = Button(130, 20, 100, 40, "Solve (AI)", font_small, bg_color=btn_color, hover_color=btn_hover)
    
    # Size toggles
    btn_size_inc = Button(20, 80, 40, 30, "+", font_small, bg_color=btn_color, hover_color=btn_hover)
    btn_size_dec = Button(70, 80, 40, 30, "-", font_small, bg_color=btn_color, hover_color=btn_hover)
    label_size = Label(120, 85, f"Size: {model.n}", font_small)
    
    label_status = Label(SCREEN_WIDTH - 450, 20, "Place Queens!", font_large, color=(255, 215, 0), shadow_color=(100, 100, 100))
    label_info = Label(20, SCREEN_HEIGHT - 40, "Click to place/remove Queens", font_small, color=(200,200,200))

    # Solver state
    solver_generator = None
    solving = False
    solve_timer = 0
    SOLVE_DELAY = 100 # ms between steps
    
    # Input state
    is_dragging = False
    total_drag_move = 0
    balloons = []
    mouse_trail = []

    running = True
    while running:
        dt = clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        screen.fill((35, 35, 45)) # Little bright background

        mouse_pos = pygame.mouse.get_pos()
        
        # Mouse Trail (Interface Colour Waves)
        mouse_trail.append(mouse_pos)
        if len(mouse_trail) > 20:
            mouse_trail.pop(0)
            
        if len(mouse_trail) > 1:
            for i in range(len(mouse_trail) - 1):
                hue = (current_time * 0.5 + i * 10) % 360
                color = pygame.Color(0)
                color.hsva = (hue, 100, 100, 100)
                pygame.draw.line(screen, color, mouse_trail[i], mouse_trail[i+1], 3)
        
        # Handle Rotation
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            renderer.angle += 2
        if keys[pygame.K_RIGHT]:
            renderer.angle -= 2

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                w, h = event.w, event.h
                screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
                
                # Update Renderer dimensions
                renderer.screen = screen
                renderer.screen_width = w
                renderer.screen_height = h
                renderer.start_x = w // 2 - 100
                renderer.start_y = h // 2
                
                # Update UI positions
                label_status.x = w - 450
                label_info.y = h - 40
                
            # Handle UI Clicks
            if btn_reset.handle_event(event):
                model.reset()
                solving = False
                label_status.set_text("Board Reset")
                label_status.color = (200, 200, 0)

            if btn_solve.handle_event(event):
                model.reset()
                solving = True
                solver_generator = model.solve_step_generator()
                label_status.set_text("Solving...")
                label_status.color = (100, 200, 255)
            
            if btn_size_inc.handle_event(event):
                if model.n < 12: # Limit max size
                    model.set_size(model.n + 1)
                    label_size.set_text(f"Size: {model.n}")
            
            if btn_size_dec.handle_event(event):
                if model.n > 4: # Limit min size
                    model.set_size(model.n - 1)
                    label_size.set_text(f"Size: {model.n}")

            # Handle Mouse Interaction (Rotate & Click)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    is_dragging = True
                    total_drag_move = 0
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_dragging = False
                    # If minimal movement, treat as click (Place Queen)
                    if total_drag_move < 5 and not solving:
                        r, c = renderer.iso_to_grid(event.pos[0], event.pos[1], model.n)
                        if 0 <= r < model.n and 0 <= c < model.n:
                            old_count = model.get_placed_queens_count()
                            model.toggle_queen(r, c)
                            new_count = model.get_placed_queens_count()
                            if new_count > old_count:
                                label_status.set_text(f"Placed {new_count}/{model.n}")
                            else:
                                label_status.set_text("Removed Queen")
                            label_status.color = (200, 200, 200)

            elif event.type == pygame.MOUSEMOTION:
                if is_dragging:
                    renderer.angle += event.rel[0] * 0.5
                    total_drag_move += abs(event.rel[0]) + abs(event.rel[1])

        # Update Solver
        if solving and solver_generator:
            solve_timer += dt
            if solve_timer > SOLVE_DELAY:
                solve_timer = 0
                try:
                    # Next step
                    # The generator yields the board state (list)
                    next_board = next(solver_generator)
                    if next_board is True: # Solved! (Actually my generator yields True at the very end maybe? let's check) 
                        # Ah, my generator yields board states. 'return True' stops it.
                        pass
                    # If it's a list, update visuals.
                    if isinstance(next_board, list):
                        model.board = next_board
                except StopIteration:
                    solving = False
                    label_status.set_text("Solved!")
                    label_status.color = (50, 255, 50)

        # Check Win State (if not solving)
        if not solving:
            if model.is_solved():
                label_status.set_text("You are the winner")
                label_status.color = (0, 255, 0)
                
                # Spawn balloons
                if random.random() < 0.1: # 10% chance per frame
                    balloons.append(Balloon(random.randint(0, renderer.screen_width), renderer.screen_height + 50))
            else:
                 # Check for conflicts
                invalid = model.get_invalid_queens()
                if invalid:
                    label_status.set_text("Conflict Detected!")
                    label_status.color = (255, 50, 50)

        # Helper to get highlight info
        hover_r, hover_c = renderer.iso_to_grid(mouse_pos[0], mouse_pos[1], model.n)
        valid_hover = (0 <= hover_r < model.n and 0 <= hover_c < model.n)

        # Drawing
        renderer.draw_board(model.n, model.board, model.get_invalid_queens(), current_time)
        
        if valid_hover and not solving:
            is_safe = model.is_safe(hover_r, hover_c)
            renderer.draw_hover(hover_r, hover_c, model.n, is_safe)
            
        # Draw Balloons
        for b in balloons[:]:
            b.update()
            b.draw(screen)
            if b.y < -100:
                balloons.remove(b)
            
        # Draw UI
        btn_reset.draw(screen)
        btn_solve.draw(screen)
        btn_size_inc.draw(screen)
        btn_size_dec.draw(screen)
        label_size.draw(screen)
        label_status.draw(screen)
        label_info.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
