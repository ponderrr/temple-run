"""
Temple Run 3D - Arcade Logic Edition
Main Entry Point
"""

from ursina import *
import os
import config
from entities.player import Player
from entities.track import Track
from systems.camera import CameraController
from systems.spawner import ObstacleSpawner
from systems.collision import CollisionDetector
from systems.score import ScoreManager
from systems.ui import HUD
from systems.difficulty import DifficultyManager
from systems.vfx import VFXManager


# ==========================================
# GLOBAL STATE
# ==========================================
game_state = 'menu'  # menu, playing, paused, game_over
player = None
track = None
camera_controller = None
spawner = None
collision_detector = None
score_manager = None
hud = None
difficulty_manager = None
vfx_manager = None
starfield = None
debug_text = None

# ==========================================
# INITIALIZATION
# ==========================================
def init_game():
    """Initialize Ursina and configure window."""
    app = Ursina()
    
    # Window setup
    window.title = config.WINDOW_TITLE
    window.size = config.WINDOW_SIZE
    window.color = config.COLOR_BACKGROUND
    window.borderless = config.WINDOW_BORDERLESS
    window.fullscreen = config.WINDOW_FULLSCREEN
    window.exit_button.visible = False
    window.fps_counter.enabled = config.DEBUG_MODE
    
    if not config.WINDOW_FULLSCREEN:
        window.center_on_screen()
    
    print(f"[INIT] {config.WINDOW_TITLE}")
    print(f"[INIT] Window: {config.WINDOW_SIZE}")
    
    return app

def init_entities():
    """Create game entities."""
    global player, track, camera_controller, debug_text, starfield
    
    # Create track first (so it's behind player visually)
    track = Track()
    
    # Create player
    player = Player()
    
    # Create camera controller
    camera_controller = CameraController(player)
    
    # Create difficulty manager
    global difficulty_manager
    difficulty_manager = DifficultyManager()

    # Create spawner
    global spawner
    spawner = ObstacleSpawner(difficulty_manager)
    
    # Create collision detector
    global collision_detector
    collision_detector = CollisionDetector()
    
    # Create score manager
    global score_manager
    score_manager = ScoreManager()
    
    # Create HUD
    global hud
    hud = HUD()
    
    # Create VFX manager
    global vfx_manager
    vfx_manager = VFXManager()
    
    # Debug text (if enabled)
    if config.DEBUG_MODE:
        debug_text = Text(
            text=f"Lane: {player.lane}",
            position=(-0.85, 0.45),
            scale=2,
            color=config.COLOR_UI_TEXT
        )
    
    print("[INIT] Entities created")

# ==========================================
# GAME LOOP
# ==========================================
def update():
    """
    Called every frame by Ursina.
    """
    global game_state
    
    if game_state == 'paused':
        # Still update HUD to show pause text
        if hud and score_manager:
            hud.update(
                score_manager.score,
                score_manager.distance,
                score_manager.shield_active,
                score_manager.shield_timer,
                game_state,
                score_manager.orbs_collected,
                score_manager.high_score
            )
        return
        
    if game_state == 'menu':
        # Still update HUD to show menu
        if hud and score_manager:
            hud.update(
                score_manager.score,
                score_manager.distance,
                score_manager.shield_active,
                score_manager.shield_timer,
                game_state,
                score_manager.orbs_collected,
                score_manager.high_score
            )
        return
    
    if game_state != 'playing':
        # Handle game over HUD update
        if hud and score_manager:
            hud.update(
                score_manager.score,
                score_manager.distance,
                score_manager.shield_active,
                score_manager.shield_timer,
                game_state,
                score_manager.orbs_collected,
                score_manager.high_score
            )
        return
    
    # Update difficulty
    current_speed = config.INITIAL_SPEED
    if difficulty_manager and score_manager:
        current_speed, _ = difficulty_manager.update(score_manager.distance)
        
    # Update VFX
    if vfx_manager:
        vfx_manager.update()
        # Apply shake to camera
        if camera_controller:
            camera_controller.shake_offset = vfx_manager.shake_offset
        
    # Get current speed (already got it, but fallback if difficulty manager missing)
    if not difficulty_manager:
        current_speed = config.TRACK_SCROLL_SPEED
    
    # Update camera
    camera_controller.update()
    
    # Update track
    track.update(current_speed)
    
    # Update spawner
    if spawner:
        spawner.update(current_speed)
        spawner.cleanup_obstacles()
    
    # Update score
    if score_manager:
        score_manager.update(current_speed)
    
    # Check collisions
    if collision_detector and player and spawner:
        # 1. Check Collectibles
        collected_item = collision_detector.check_collectibles(player, spawner.obstacles)
        if collected_item:
            if collected_item.item_type == 'orb':
                score_manager.add_points(config.SCORE_ORB, is_orb=True)
                if vfx_manager:
                    vfx_manager.create_particles(collected_item.position, config.COLOR_ORB)
            elif collected_item.item_type == 'shield':
                score_manager.activate_shield()
                if vfx_manager:
                    vfx_manager.create_particles(collected_item.position, config.COLOR_SHIELD)
            
            # Remove item
            if collected_item in spawner.obstacles:
                spawner.obstacles.remove(collected_item)
            destroy(collected_item)
            
        # 2. Check Obstacles
        collided, obstacle = collision_detector.check_collision(player, spawner.obstacles)
        if collided:
            # Check for shield
            if score_manager.shield_active:
                print(f"[GAME] Shield protected against {obstacle.obs_type}!")
                if vfx_manager:
                    vfx_manager.shake_camera(config.SHAKE_INTENSITY_SHIELD, config.SHAKE_DURATION_SHIELD)
                    vfx_manager.create_particles(obstacle.position, config.COLOR_SHIELD)
                
                # Optional: Destroy obstacle on shield hit
                if obstacle in spawner.obstacles:
                    spawner.obstacles.remove(obstacle)
                destroy(obstacle)
            else:
                print(f"[GAME] Collision with {obstacle.obs_type} obstacle!")
                if vfx_manager:
                    vfx_manager.shake_camera(config.SHAKE_INTENSITY_COLLISION, config.SHAKE_DURATION_COLLISION)
                
                game_state = 'game_over'
                print(f"[GAME] GAME OVER - Final Score: {int(score_manager.score)}")
    
    # Update HUD
    if hud and score_manager:
        hud.update(
            score_manager.score,
            score_manager.distance,
            score_manager.shield_active,
            score_manager.shield_timer,
            game_state,
            score_manager.orbs_collected,
            score_manager.high_score
        )
    
    # Update debug text
    if config.DEBUG_MODE and debug_text:
        state_display = player.vertical_state.upper()
        if player.vertical_state == 'jumping':
            progress_percent = int(player.jump_progress * 100)
            state_display = f"JUMPING ({progress_percent}%)"
        elif player.vertical_state == 'sliding':
            remaining = player.slide_timer
            state_display = f"SLIDING ({remaining:.1f}s)"
        
        score_display = f"Score: {int(score_manager.score)}"
        if score_manager.shield_active:
            score_display += f" | SHIELD ({score_manager.shield_timer:.1f}s)"
            
        debug_text.text = f"Lane: {player.lane} | State: {state_display}\n{score_display}"

def input(key):
    """
    Handle keyboard input.
    """
    global game_state
    
    if key == 'escape':
        if game_state == 'menu':
            print("[INPUT] ESC pressed - Exiting game")
            quit()
        elif game_state == 'playing':
            game_state = 'paused'
            print("[GAME] Paused")
        elif game_state == 'paused':
            game_state = 'playing'
            print("[GAME] Resumed")
            
    # Menu controls
    if game_state == 'menu':
        if key == 'enter':
            game_state = 'playing'
            print("[GAME] Started")
            
    # Pause controls
    if key == 'p':
        if game_state == 'playing':
            game_state = 'paused'
            print("[GAME] Paused")
        elif game_state == 'paused':
            game_state = 'playing'
            print("[GAME] Resumed")
    
    # Lane switching
    if game_state == 'playing':
        if key == 'a' or key == 'left arrow':
            player.switch_lane(-1)
            # if vfx_manager:
            #     vfx_manager.create_particles(player.position + Vec3(-0.5, 0, 0), color.cyan, count=3)
        elif key == 'd' or key == 'right arrow':
            player.switch_lane(1)
            # if vfx_manager:
            #     vfx_manager.create_particles(player.position + Vec3(0.5, 0, 0), color.cyan, count=3)
        
        # Jump
        elif key == 'space':
            player.jump()
        
        # Slide
        elif key == 's' or key == 'down arrow':
            player.slide()
            
    # Restart
    if game_state == 'game_over':
        if key == 'r':
            reset_game()
        elif key == 'escape':
            game_state = 'menu'
            reset_game()
            game_state = 'menu' # Ensure it stays menu after reset

def reset_game():
    """
    Reset all game state to start over.
    """
    global game_state
    
    print("[GAME] Restarting...")
    
    # Reset entities
    player.reset()
    spawner.reset()
    score_manager.reset()
    difficulty_manager.reset()
    
    # Reset camera
    camera_controller.update()
    
    # Reset state
    game_state = 'playing'
    print("[GAME] Restart complete")

# ==========================================
# ENTRY POINT
# ==========================================
if __name__ == '__main__':
    # Generate textures if they don't exist
    required_textures = [
        'assets/track_texture.png',
        'assets/wall_texture.png',
        'assets/wood_texture.png',
        'assets/metal_texture.png',
        'assets/orb_texture.png'
    ]
    
    missing_textures = [tex for tex in required_textures if not os.path.exists(tex)]
    
    if missing_textures:
        print("[SETUP] Generating missing textures...")
        from utils.texture_gen import (
            ensure_assets_dir,
            generate_track_texture,
            generate_wall_texture,
            generate_wood_texture,
            generate_metal_texture,
            generate_orb_texture
        )
        
        ensure_assets_dir()
        
        if not os.path.exists('assets/track_texture.png'):
            generate_track_texture()
        if not os.path.exists('assets/wall_texture.png'):
            generate_wall_texture()
        if not os.path.exists('assets/wood_texture.png'):
            generate_wood_texture()
        if not os.path.exists('assets/metal_texture.png'):
            generate_metal_texture()
        if not os.path.exists('assets/orb_texture.png'):
            generate_orb_texture()
        
        print("[SETUP] Texture generation complete!")

    app = init_game()
    init_entities()
    
    print("[READY] Game ready - Use A/D or Arrow Keys to switch lanes")
    print("[READY] Track is scrolling - Player movement creates camera follow")
    print("[READY] Press ESC to exit")
    
    app.run()
