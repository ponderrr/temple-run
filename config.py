from ursina import color

# ----------------------------------------------------------------------------
# SCREEN SETTINGS
# ----------------------------------------------------------------------------
WINDOW_TITLE = "Temple Run 3D - Arcade Logic"
WINDOW_SIZE = (1280, 720)
WINDOW_BORDERLESS = False
WINDOW_FULLSCREEN = False

# ----------------------------------------------------------------------------
# COLOR PALETTE
# ----------------------------------------------------------------------------
# Primary Colors
COLOR_BACKGROUND = color.black
COLOR_TRACK = color.white      # Changed to white to show texture
COLOR_GRID_LINES = color.rgba(0, 0, 0, 0.2) # Semi-transparent black

# Player
COLOR_PLAYER = color.cyan

# Obstacles
COLOR_OBS_LOW = color.white    # Changed to white to show texture
COLOR_OBS_HIGH = color.red                    # Slide under these
COLOR_OBS_MOVING = color.orange               # Move around these

# Collectibles
COLOR_ORB = color.gold                        # Points
COLOR_SHIELD = color.azure                    # Invincibility

# Textures
TEXTURE_TRACK = 'assets/track_texture.png'
TEXTURE_WALL = 'assets/wall_texture.png'
TEXTURE_WOOD = 'assets/wood_texture.png'
TEXTURE_METAL = 'assets/metal_texture.png'
TEXTURE_ORB = 'assets/orb_texture.png'

# ----------------------------------------------------------------------------
# GAME SETTINGS
# ----------------------------------------------------------------------------
# Track Settings
TRACK_WIDTH = 10.0
TRACK_LENGTH = 100.0
TRACK_SCROLL_SPEED = 20.0          # Base scroll speed
GRID_SPACING = 5.0
GRID_ANIMATION_SPEED = 0.5         # Multiplier for visual scroll effect
# Lane System
LANE_POSITIONS = [-2.0, 0.0, 2.0]  # x-coordinates for Left, Center, Right
LANE_COUNT = 3
LANE_SWITCH_SPEED = 12.0           # Visual lerp speed
LANE_SPEED = 10.0                  # (Deprecated/Unused? Keeping for safety based on previous file)

# Player Settings
PLAYER_SIZE = (0.8, 0.8, 0.8)
PLAYER_START_LANE = 1              # Center lane
PLAYER_START_Y = 0.5               # Half of height (0.8/2) + buffer? No, usually center is 0,0,0. 
                                   # Ursina cube origin is center. So y=0.5 puts bottom at 0 if size is 1.
                                   # If size is 0.8, y=0.4 puts bottom at 0.
                                   # Let's stick to the plan/instructions which might imply specific values.
                                   # Instructions say: position=(LANE_POSITIONS[...], PLAYER_START_Y, PLAYER_START_Z)
PLAYER_START_Y = 0.5
PLAYER_START_Z = 0.0
JUMP_HEIGHT = 2.5                  # Peak height of jump
JUMP_DURATION = 0.5                # Seconds to complete jump
SLIDE_DURATION = 0.8               # Seconds to remain sliding
SLIDE_HEIGHT_SCALE = 0.4           # Scale factor for height when sliding

# Collectible Settings
COLLECTIBLE_SIZE = 0.5             # Scale for orbs/shields
COLLECTIBLE_HEIGHT = 0.8           # Height above ground
SHIELD_DURATION = 5.0              # Seconds of invincibility
SCORE_PER_UNIT = 10                # Points per unit traveled
SCORE_PER_SECOND = 10              # Points per second survived
SCORE_ORB = 100                    # Points per orb collected

# Obstacle Settings
OBS_LOW_SIZE = (1.0, 0.6, 1.0)     # Width, Height, Depth
OBS_LOW_HEIGHT = 0.3               # Center Y (0.6 / 2)
OBS_HIGH_SIZE = (1.0, 2.5, 1.0)
OBS_HIGH_HEIGHT = 1.25             # Center Y (2.5 / 2)
OBS_MOVING_SIZE = (1.0, 1.2, 1.0)
OBS_MOVING_HEIGHT = 0.6            # Center Y (1.2 / 2)
OBS_MOVING_SPEED = 5.0             # Lateral speed
OBSTACLE_DESPAWN_DISTANCE = -10.0  # Z position to remove obstacle
OBSTACLE_SPAWN_DISTANCE = 60.0     # Z position to spawn obstacle
SPAWN_INTERVAL_MIN = 0.8           # Minimum seconds between spawns
SPAWN_INTERVAL_MAX = 1.5           # Maximum seconds between spawns
OBSTACLE_COLLISION_THRESHOLD = 1.5 # Distance to trigger collision

# Camera Settings
CAMERA_POSITION = (0, 6, -14)      # Lower and further back
CAMERA_ROTATION_X = 15             # Look more horizontally (moves player down)
CAMERA_FOLLOW_SPEED = 0.1          # Smooth follow factor
CAMERA_FOLLOW_SPEED = 0.1          # Smooth follow factor
COLOR_UI_TEXT = color.white

# HUD Settings
UI_SCORE_POSITION = (-0.85, 0.45)  # Top-left
UI_DISTANCE_POSITION = (0.65, 0.45)# Top-right
UI_SHIELD_POSITION = (0, 0.35)     # Top-center
UI_GAME_OVER_POSITION = (0, 0)     # Center
UI_FONT_SIZE = 1.5
UI_COLOR = color.white

# World Scrolling
INITIAL_SPEED = 20.0               # Units per second
MAX_SPEED = 50.0
SPEED_INCREMENT = 0.5              # Speed increase per second (deprecated in favor of distance scaling?)
DIFFICULTY_SCALE_DISTANCE = 500.0  # Distance to increase difficulty tier

# VFX Settings
SHAKE_INTENSITY_COLLISION = 0.5    # Reduced from 1.0
SHAKE_DURATION_COLLISION = 0.4
SHAKE_INTENSITY_SHIELD = 0.3       # Reduced from 0.5
SHAKE_DURATION_SHIELD = 0.2
CAMERA_TILT_ANGLE = 2.0            # Reduced from 5.0 (subtle tilt)
CAMERA_TILT_SPEED = 3.0            # Slower tilt

# Menu Settings
UI_MENU_TITLE_POS = (0, 0.2)
UI_MENU_SUBTITLE_POS = (0, 0.1)
UI_MENU_INSTRUCT_POS = (0, -0.2)
COLOR_MENU_TITLE = color.gold
COLOR_MENU_TEXT = color.white

# Debug
DEBUG_MODE = False

# ====================================
# PHASE 5 FIXES: MAGIC NUMBERS
# ====================================
PLAYER_COLLISION_RADIUS = 1.0
COLLECTIBLE_SPAWN_CHANCE = 0.3

