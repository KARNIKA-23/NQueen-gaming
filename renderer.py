import pygame
import math

class IsometricRenderer:
    def __init__(self, screen, width, height, tile_size=40):
        self.screen = screen
        self.screen_width = width
        self.screen_height = height
        self.tile_size = tile_size
        self.angle = 0  # Rotation angle in degrees
        
        # Colors
        self.COLOR_BOARD_LIGHT = (240, 217, 181)
        self.COLOR_BOARD_DARK = (181, 136, 99)
        self.COLOR_HOVER = (100, 200, 100, 128) # Transparent green
        self.COLOR_INVALID = (200, 50, 50, 128) # Transparent red
        self.COLOR_QUEEN = (20, 20, 20)
        self.COLOR_QUEEN_HIGHLIGHT = (80, 80, 80)
        self.COLOR_SHADOW = (0, 0, 0, 100)
        
        # Offset to center the board
        self.start_x = width // 2 - 100
        self.start_y = height // 2
        
    def cart_to_iso(self, row, col, n):
        """Converts grid (row, col) to isometric screen coordinates (x, y)."""
        # Center of the board
        cx = n / 2.0
        cy = n / 2.0

        # Coordinates relative to center
        rx = (col - cx) * self.tile_size
        ry = (row - cy) * self.tile_size

        # Rotate
        rad = math.radians(self.angle)
        rot_x = rx * math.cos(rad) - ry * math.sin(rad)
        rot_y = rx * math.sin(rad) + ry * math.cos(rad)

        iso_x = (rot_x - rot_y)
        iso_y = (rot_x + rot_y) / 2
        return (iso_x + self.start_x, iso_y + self.start_y)

    def iso_to_grid(self, screen_x, screen_y, n):
        """
        Converts screen (x, y) back to grid (row, col).
        This is an approximation for hit detection.
        """
        # Reverse the transformation:
        # iso_x - start_x = cart_x - cart_y
        # (iso_y - start_y) * 2 = cart_x + cart_y
        
        iso_x = screen_x - self.start_x
        iso_y = screen_y - self.start_y
        
        # Reverse projection
        # rot_x - rot_y = iso_x
        # rot_x + rot_y = 2 * iso_y
        rot_x = (iso_x + 2 * iso_y) / 2
        rot_y = iso_y - iso_x / 2
        
        # Reverse Rotation
        rad = math.radians(self.angle)
        # Inverse rotation is rotation by -angle
        rx = rot_x * math.cos(rad) + rot_y * math.sin(rad)
        ry = -rot_x * math.sin(rad) + rot_y * math.cos(rad)

        cx = n / 2.0
        cy = n / 2.0

        col = int(math.floor(rx / self.tile_size + cx))
        row = int(math.floor(ry / self.tile_size + cy))
        
        return row, col

    def draw_board(self, n, board_state, invalid_queens, current_time=0):
        """Draws the entire board and pieces."""
        
        # Collect all tiles and sort by depth (projected Y)
        tiles = [(r, c) for r in range(n) for c in range(n)]
        tiles.sort(key=lambda p: self.cart_to_iso(p[0], p[1], n)[1])

        # Calculate attacked tiles for visualization
        attacked_tiles = set()
        for r in range(n):
            c = board_state[r]
            if c != -1:
                # Row & Column
                for i in range(n):
                    if i != c: attacked_tiles.add((r, i))
                    if i != r: attacked_tiles.add((i, c))
                # Diagonals
                for d in range(1, n):
                    for dr, dc in [(1,1), (1,-1), (-1,1), (-1,-1)]:
                        tr, tc = r + d*dr, c + d*dc
                        if 0 <= tr < n and 0 <= tc < n:
                            attacked_tiles.add((tr, tc))

        for r, c in tiles:
            self._draw_tile(r, c, n, is_attacked=((r, c) in attacked_tiles))

        # Draw Queens (order matters: back to front)
        # We need to sort by depth (which correlates roughly with Y position or sum of row+col)
        # In iso, smaller (row+col) is further back.
        pieces_to_draw = []
        
        # Collect placed queens
        for row in range(n):
            col = board_state[row]
            if col != -1:
                is_invalid = (row, col) in invalid_queens
                pieces_to_draw.append({'row': row, 'col': col, 'invalid': is_invalid})
                
        # Sort by depth (row + col)
        pieces_to_draw.sort(key=lambda p: self.cart_to_iso(p['row'], p['col'], n)[1])
        
        for piece in pieces_to_draw:
            self._draw_queen(piece['row'], piece['col'], piece['invalid'], current_time, n)

    def draw_hover(self, row, col, n, is_safe=True):
        """Highlights the tile under cursor."""
        x, y = self.cart_to_iso(row, col, n)
        points = [
            (x, y),
            (x + self.tile_size, y + self.tile_size/2),
            (x, y + self.tile_size),
            (x - self.tile_size, y + self.tile_size/2)
        ]
        
        # Create a temporary surface for transparency
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        pygame.draw.polygon(s, (255, 255, 255, 50), points)
        self.screen.blit(s, (0,0))
        
        # Draw outline
        pygame.draw.polygon(self.screen, (255, 255, 255), points, 2)
        
        if not is_safe:
            # Draw a red point to indicate invalid placement
            center_x = x
            center_y = y + self.tile_size/2
            pygame.draw.circle(self.screen, (255, 50, 50), (int(center_x), int(center_y)), 8)

    # Ensure _draw_tile is indented correctly as a method of IsometricRenderer
    def _draw_tile(self, row, col, n, is_attacked=False):
        x, y = self.cart_to_iso(row, col, n)
        
        # Determine color (chessboard pattern)
        if (row + col) % 2 == 0:
            color = self.COLOR_BOARD_LIGHT
            side_color = (200, 180, 150)
        else:
            color = self.COLOR_BOARD_DARK
            side_color = (140, 100, 70)
            
        # Points for top face (rhombus)
        points_top = [
            (x, y),
            (x + self.tile_size, y + self.tile_size/2),
            (x, y + self.tile_size),
            (x - self.tile_size, y + self.tile_size/2)
        ]
        
        # Thickness (3D effect base)
        thickness = 10
        points_side_left = [
            (x - self.tile_size, y + self.tile_size/2),
            (x, y + self.tile_size),
            (x, y + self.tile_size + thickness),
            (x - self.tile_size, y + self.tile_size/2 + thickness)
        ]
        
        points_side_right = [
            (x, y + self.tile_size),
            (x + self.tile_size, y + self.tile_size/2),
            (x + self.tile_size, y + self.tile_size/2 + thickness),
            (x, y + self.tile_size + thickness)
        ]
        
        # Draw sides (darker for shading)
        pygame.draw.polygon(self.screen, side_color, points_side_left)
        pygame.draw.polygon(self.screen, side_color, points_side_right)
        
        # Draw top
        pygame.draw.polygon(self.screen, color, points_top)
        
        if is_attacked:
            center_x = x
            center_y = y + self.tile_size/2
            pygame.draw.circle(self.screen, (255, 80, 80), (int(center_x), int(center_y)), 4)
        
        # Draw edge
        # pygame.draw.polygon(self.screen, (0,0,0), points_top, 1)


    def _draw_queen(self, row, col, is_invalid=False, current_time=0, n=8):
        x, y = self.cart_to_iso(row, col, n)
        
        # Center of the tile top face matches (x, y + tile_size/2) roughly?
        # Actually cart_to_iso returns the TOP corner of the tile.
        # Center of tile is:
        center_x = x
        center_y = y + self.tile_size/2
        
        # Offset for height (floating effect or just standing on board)
        # Animate height using sine wave based on time and position
        height_offset = 20 + math.sin(current_time * 0.005 + (row + col)) * 5
        
        # Shadow
        shadow_rect = pygame.Rect(0, 0, self.tile_size * 0.6, self.tile_size * 0.3)
        shadow_rect.center = (center_x, center_y + 5) # Slightly below center for perspective
        
        s = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        pygame.draw.ellipse(s, self.COLOR_SHADOW, shadow_rect)
        self.screen.blit(s, (0,0))
        
        # Queen Body (Simple representation: Cylinder/Prism)
        # Using a few circles stacked
        
        piece_y = center_y - height_offset / 2 # move up slightly
        
        color = self.COLOR_QUEEN
        if is_invalid:
            color = (200, 50, 50) # Red if invalid
            
        # Draw Base
        pygame.draw.ellipse(self.screen, color, 
                            (center_x - 15, piece_y - 10, 30, 15))
                            
        # Draw Body (Rectangle + shading)
        rect = pygame.Rect(center_x - 10, piece_y - 40, 20, 35)
        pygame.draw.rect(self.screen, color, rect)
        
        # Draw Head/Crown
        pygame.draw.ellipse(self.screen, self.COLOR_QUEEN_HIGHLIGHT, 
                           (center_x - 12, piece_y - 45, 24, 12))
                           
        # Add a simple highlight/shine
        pygame.draw.line(self.screen, (100, 100, 100), (center_x - 5, piece_y - 35), (center_x - 5, piece_y - 15), 2)
