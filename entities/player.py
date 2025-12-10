"""
Player Entity - Arcade Lane System

The player is a cube that exists in one of three discrete lanes.
Visual position smoothly lerps between lanes, but game logic uses discrete lane index.
"""

from ursina import *
import config

class Player(Entity):
    """
    Player entity with arcade-style lane switching.
    
    The player has:
    - Discrete lane position (0, 1, or 2)
    - Smooth visual position (lerped X coordinate)
    - Vertical state (for future jump/slide mechanics)
    """
    
    def __init__(self):
        super().__init__(
            model='cube',
            color=config.COLOR_PLAYER,
            scale=config.PLAYER_SIZE,
            position=(
                config.LANE_POSITIONS[config.PLAYER_START_LANE],
                config.PLAYER_START_Y,
                config.PLAYER_START_Z
            ),
            collider='box'  # For future collision detection
        )
        
        # Lane State (DISCRETE)
        self.lane = config.PLAYER_START_LANE  # 0, 1, or 2
        
        # Visual State (SMOOTH)
        self.target_x = config.LANE_POSITIONS[self.lane]
        
        # Vertical State Machine
        self.vertical_state = 'grounded'  # grounded, jumping, sliding
        
        # Jump state
        self.jump_progress = 0.0
        
        # Slide state
        self.slide_timer = 0.0
        
        # Store original scale for restore
        self.normal_scale_y = config.PLAYER_SIZE[1]
        self.slide_scale_y = config.PLAYER_SIZE[1] * config.SLIDE_HEIGHT_SCALE
        
        # Z position (for collision detection)
        self.z_position = config.PLAYER_START_Z
        
        print(f"[PLAYER] Initialized at lane {self.lane}")
    
    def switch_lane(self, direction):
        """
        Attempt to switch lanes.
        
        Args:
            direction (int): -1 for left, +1 for right
        """
        new_lane = self.lane + direction
        
        # Check boundaries
        if new_lane < 0 or new_lane >= config.LANE_COUNT:
            print(f"[PLAYER] Cannot move to lane {new_lane} (out of bounds)")
            return
        
        # Valid move
        self.lane = new_lane
        self.target_x = config.LANE_POSITIONS[self.lane]
        
        print(f"[PLAYER] Switched to lane {self.lane}")

    def jump(self):
        """
        Initiate jump animation.
        Only works if player is grounded.
        """
        if self.vertical_state != 'grounded':
            return  # Cannot jump while already jumping/sliding
        
        self.vertical_state = 'jumping'
        self.jump_progress = 0.0
        
        print("[PLAYER] Jump started")
    
    def slide(self):
        """
        Initiate slide (crouch).
        Only works if player is grounded.
        """
        if self.vertical_state != 'grounded':
            return  # Cannot slide while jumping
        
        self.vertical_state = 'sliding'
        self.slide_timer = config.SLIDE_DURATION
        
        # Shrink height
        self.scale_y = self.slide_scale_y
        
        # Lower Y position to match new height
        # Player's Y is at their center, so we need to adjust
        self.y = self.slide_scale_y / 2.0
        
        print("[PLAYER] Slide started")
    
    def stand_up(self):
        """
        Return to normal standing state from slide.
        """
        self.vertical_state = 'grounded'
        self.scale_y = self.normal_scale_y
        self.y = config.PLAYER_START_Y
        
        print("[PLAYER] Stood up")
    
    def update(self):
        """
        Called every frame by Ursina.
        Updates all movement.
        """
        # 1. Lane Movement (Horizontal)
        self.x = lerp(self.x, self.target_x, time.dt * config.LANE_SWITCH_SPEED)
        
        # 2. Vertical Movement (State-based)
        if self.vertical_state == 'jumping':
            self.update_jump()
        elif self.vertical_state == 'sliding':
            self.update_slide()
    
    def update_jump(self):
        """
        Update jump animation using parabolic curve.
        
        The curve formula: height = 4 * t * (1 - t)
        This creates a smooth parabolic arc from 0 -> peak -> 0
        """
        # Increment progress
        self.jump_progress += time.dt / config.JUMP_DURATION
        
        # Check if jump complete
        if self.jump_progress >= 1.0:
            # Land
            self.vertical_state = 'grounded'
            self.jump_progress = 0.0
            self.y = config.PLAYER_START_Y
            
            print("[PLAYER] Landed")
            return
        
        # Calculate height using parabolic curve
        # Formula: 4*t*(1-t) where t goes from 0 to 1
        # Result: 0 -> 1 -> 0 (smooth parabola)
        t = self.jump_progress
        curve_value = 4 * t * (1 - t)
        height = curve_value * config.JUMP_HEIGHT
        
        # Apply height
        self.y = config.PLAYER_START_Y + height
    
    def update_slide(self):
        """
        Update slide state.
        Countdown timer, then stand back up.
        """
        self.slide_timer -= time.dt
        
        if self.slide_timer <= 0.0:
            # Slide complete, stand up
            self.stand_up()

    def reset(self):
        """
        Reset player to initial state.
        """
        self.lane = config.PLAYER_START_LANE
        self.target_x = config.LANE_POSITIONS[self.lane]
        self.x = self.target_x
        self.y = config.PLAYER_START_Y
        self.z = config.PLAYER_START_Z
        self.vertical_state = 'grounded'
        self.jump_progress = 0.0
        self.slide_timer = 0.0
        self.scale_y = self.normal_scale_y
        self.z_position = config.PLAYER_START_Z
        print("[PLAYER] Reset")
