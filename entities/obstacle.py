"""
Obstacle Entity - Arcade Logic Hazards

Obstacles are simple cubes that:
1. Stay in their assigned lane
2. Move toward the player (decreasing Z)
3. Get destroyed when behind player
"""

from ursina import *
import config

class Obstacle(Entity):
    """
    Obstacle entity with type-based behavior.
    
    Types:
    - 'low': Jump over (yellow)
    - 'high': Slide under (red)
    - 'moving': Avoid (orange, switches lanes)
    """
    
    def __init__(self, lane, z_position, obs_type):
        """
        Create an obstacle.
        
        Args:
            lane (int): Lane index (0, 1, or 2)
            z_position (float): Starting Z coordinate
            obs_type (str): 'low', 'high', or 'moving'
        """
        # Set properties based on type
        if obs_type == 'low':
            model = 'cube'
            scale = config.OBS_LOW_SIZE
            y_pos = config.OBS_LOW_HEIGHT
            obs_color = config.COLOR_OBS_LOW
            texture = config.TEXTURE_WOOD
            texture_scale = (1, 1)
            
        elif obs_type == 'high':
            model = 'cube'
            scale = config.OBS_HIGH_SIZE
            y_pos = config.OBS_HIGH_HEIGHT
            obs_color = config.COLOR_OBS_HIGH
            texture = config.TEXTURE_WALL
            texture_scale = (1, 2)
            
        elif obs_type == 'moving':
            model = 'cube'
            scale = config.OBS_MOVING_SIZE
            y_pos = config.OBS_MOVING_HEIGHT
            obs_color = config.COLOR_OBS_MOVING
            texture = config.TEXTURE_METAL
            texture_scale = (1, 1)
            self.move_speed = config.OBS_MOVING_SPEED
            self.direction = 1 if random.random() > 0.5 else -1
        else:
            raise ValueError(f"Invalid obstacle type: {obs_type}")
        
        # Calculate X position from lane
        x_pos = config.LANE_POSITIONS[lane]
        
        # Initialize entity
        super().__init__(
            model=model,
            color=obs_color,
            scale=scale,
            texture=texture,
            texture_scale=texture_scale,
            position=(x_pos, y_pos, z_position),
            collider='box'
        )

        # Glow Effect (Child Entity)
        # A slightly larger, transparent sphere/cube to simulate emission
        self.glow = Entity(
            parent=self,
            model=model,
            color=color.rgba(obs_color.r, obs_color.g, obs_color.b, 100), # Transparent version of base color
            scale=1.2, # Slightly larger
            texture=None,
            unlit=True, # Glow appearance
            add_to_scene_entities=False # Optimization? No, needs to be in scene to render.
        )
        # Pulse animation handled in update if needed, or just static glow

        
        # Store state
        self.lane = lane
        self.z_position = z_position
        self.obs_type = obs_type
        
        # Moving obstacle specific
        self.move_direction = 1 if lane == 0 else -1  # Start moving away from edge
        
        print(f"[OBSTACLE] Created {obs_type} at lane {lane}, z={z_position}")
    
    def update(self):
        """
        Update obstacle position.
        Scrolls toward player and handles special behaviors.
        """
        # Scroll toward player
        self.z_position -= config.TRACK_SCROLL_SPEED * time.dt
        self.z = self.z_position
        
        # Moving obstacle behavior
        if self.obs_type == 'moving':
            self.update_moving_obstacle()
        
        # Auto-cleanup if behind player
        if self.z_position < config.OBSTACLE_DESPAWN_DISTANCE:
            self.cleanup()
    
    def update_moving_obstacle(self):
        """
        Special behavior for moving obstacles.
        Shifts between lanes over time.
        """
        # Move laterally
        self.x += self.move_direction * config.OBS_MOVING_SPEED * time.dt
        
        # Check lane boundaries and reverse
        if self.x <= config.LANE_POSITIONS[0]:
            self.x = config.LANE_POSITIONS[0]
            self.move_direction = 1
            self.lane = 0
        elif self.x >= config.LANE_POSITIONS[2]:
            self.x = config.LANE_POSITIONS[2]
            self.move_direction = -1
            self.lane = 2
        else:
            # Determine current lane
            distances = [abs(self.x - pos) for pos in config.LANE_POSITIONS]
            self.lane = distances.index(min(distances))
    
    def cleanup(self):
        """
        Remove this obstacle from the game.
        """
        print(f"[OBSTACLE] Destroyed {self.obs_type} at z={self.z_position:.1f}")
        destroy(self)
