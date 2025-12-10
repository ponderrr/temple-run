"""
HUD System - Heads-Up Display
"""

from ursina import *
import config

class HUD:
    """
    Manages all UI elements.
    """
    
    def __init__(self):
        # Score (Top Left)
        self.score_text = Text(
            text='Score: 0',
            position=config.UI_SCORE_POSITION,
            scale=config.UI_FONT_SIZE,
            color=config.UI_COLOR
        )
        
        # Distance (Top Right)
        self.distance_text = Text(
            text='Distance: 0m',
            position=config.UI_DISTANCE_POSITION,
            scale=config.UI_FONT_SIZE,
            color=config.UI_COLOR
        )
        
        # High Score (Top Right, below distance)
        self.high_score_text = Text(
            text='Best: 0',
            position=(0.65, 0.40),
            scale=config.UI_FONT_SIZE * 0.8,  # Slightly smaller
            color=config.COLOR_MENU_TITLE,  # Gold color
            enabled=False
        )
        
        # Shield Status (Center Top)
        self.shield_text = Text(
            text='SHIELD ACTIVE',
            position=config.UI_SHIELD_POSITION,
            scale=config.UI_FONT_SIZE,
            color=config.COLOR_SHIELD,
            origin=(0, 0),
            enabled=False
        )
        
        # Game Over (Center)
        self.game_over_text = Text(
            text='GAME OVER\nPress R to Restart',
            position=config.UI_GAME_OVER_POSITION,
            scale=config.UI_FONT_SIZE * 2,
            color=color.red,
            origin=(0, 0),
            enabled=False
        )
        

        
        # Menu Elements
        self.menu_title = Text(
            text='TEMPLE RUN 3D',
            position=config.UI_MENU_TITLE_POS,
            scale=config.UI_FONT_SIZE * 3,
            color=config.COLOR_MENU_TITLE,
            origin=(0, 0),
            enabled=False
        )
        
        self.menu_subtitle = Text(
            text='ARCADE EDITION',
            position=config.UI_MENU_SUBTITLE_POS,
            scale=config.UI_FONT_SIZE * 1.5,
            color=config.COLOR_MENU_TEXT,
            origin=(0, 0),
            enabled=False
        )
        
        self.menu_instructions = Text(
            text='Press ENTER to Start\nPress ESC to Quit',
            position=config.UI_MENU_INSTRUCT_POS,
            scale=config.UI_FONT_SIZE,
            color=config.COLOR_MENU_TEXT,
            origin=(0, 0),
            enabled=False
        )
        
        # Pause Element
        self.pause_text = Text(
            text='PAUSED\nPress P to Resume',
            position=(0, 0),
            scale=config.UI_FONT_SIZE * 2,
            color=color.white,
            origin=(0, 0),
            enabled=False
        )
        
        print("[HUD] Initialized")
    
    def update(self, score, distance, shield_active, shield_timer, game_state, orbs_collected=0, high_score=0):
        """
        Update UI elements.
        """
        # Hide everything by default
        self.score_text.enabled = False
        self.score_text.enabled = False
        self.distance_text.enabled = False
        self.high_score_text.enabled = False
        self.shield_text.enabled = False
        self.game_over_text.enabled = False
        self.menu_title.enabled = False
        self.menu_subtitle.enabled = False
        self.menu_instructions.enabled = False
        self.pause_text.enabled = False
        
        if game_state == 'menu':
            self.menu_title.enabled = True
            self.menu_subtitle.enabled = True
            self.menu_instructions.enabled = True
            
        elif game_state == 'playing':
            self.score_text.enabled = True
            self.distance_text.enabled = True
            
            self.score_text.text = f'Score: {int(score)}'
            self.distance_text.text = f'Distance: {int(distance)}m'
            
            # Show high score if it exists
            if high_score > 0:
                self.high_score_text.enabled = True
                self.high_score_text.text = f'Best: {int(high_score)}'
            
            if shield_active:
                self.shield_text.enabled = True
                self.shield_text.text = f'SHIELD ACTIVE ({shield_timer:.1f}s)'
            
        elif game_state == 'paused':
            self.score_text.enabled = True
            self.distance_text.enabled = True
            self.pause_text.enabled = True
            
        elif game_state == 'game_over':
            self.score_text.enabled = False
            self.distance_text.enabled = False
            self.game_over_text.enabled = True
            self.game_over_text.text = f'GAME OVER\n\nFinal Score: {int(score)}\nDistance: {int(distance)}m\nOrbs Collected: {orbs_collected}\n\nPress R to Restart\nPress ESC to Main Menu'
