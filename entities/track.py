"""
Track Entity - Infinite Scrolling Floor

The track is a static plane with a scrolling texture effect.
The player stays at Z=0, and the texture offset updates to create movement illusion.
"""

from ursina import *
import config

class Track(Entity):
    """
    Infinite scrolling track with grid lines.
    
    The track doesn't actually move - instead, the texture offset scrolls
    to create the illusion of forward movement.
    """
    
    def __init__(self):
        super().__init__(
            model='plane',
            texture=config.TEXTURE_TRACK,
            texture_scale=(2, 20), # Tile the texture
            color=config.COLOR_TRACK,
            scale=(config.TRACK_WIDTH, 1, config.TRACK_LENGTH),
            position=(0, 0, config.TRACK_LENGTH / 2),  # Centered ahead of player
            rotation_x=0,  # Flat on ground
            collider=None  # We don't need collision on the track itself
        )
        
        # Z tiling: Based on track length and grid spacing
        grid_lines = int(config.TRACK_LENGTH / config.GRID_SPACING)
        self.texture_scale = (1, grid_lines)
        
        # Scrolling offset
        self.scroll_offset = 0.0
        
        # Grid lines (visual enhancement)
        self.create_grid_lines()
        
        print(f"[TRACK] Created with {grid_lines} grid divisions")
    
    def create_grid_lines(self):
        """
        Create visible grid lines for visual effect.
        These are thin planes that also scroll with the texture.
        """
        # We'll create a few grid line entities
        self.grid_lines = []
        
        line_count = int(config.TRACK_LENGTH / config.GRID_SPACING)
        
        for i in range(line_count):
            z_pos = i * config.GRID_SPACING
            
            line = Entity(
                model='plane',
                scale=(config.TRACK_WIDTH, 1, 0.1),
                color=config.COLOR_GRID_LINES,
                position=(0, 0.01, z_pos),  # Slightly above track to avoid z-fighting
                rotation_x=0
            )
            self.grid_lines.append(line)
    
    def update(self, speed=None):
        """
        Update track position to create scrolling effect.
        
        Args:
            speed (float, optional): Current scroll speed. If None, uses config default.
        """
        # Use provided speed or default
        current_speed = speed if speed is not None else config.TRACK_SCROLL_SPEED
        
        # Update scroll offset
        scroll_speed = current_speed * config.GRID_ANIMATION_SPEED
        self.scroll_offset += time.dt * scroll_speed
        
        # Apply texture offset (creates scrolling effect)
        self.texture_offset = (0, self.scroll_offset)
        
        # Move grid lines (for enhanced visual effect)
        for line in self.grid_lines:
            # Move line towards player (negative Z)
            line.z -= current_speed * time.dt
            
            # Reset if it goes behind camera
            if line.z < -config.GRID_SPACING:
                line.z += config.TRACK_LENGTH
