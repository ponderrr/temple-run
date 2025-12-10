
        
"""
Score System - Track Progress and Rewards
"""

import time
import config

class ScoreManager:
    """
    Manages game score, distance, and high score.
    """
    
    def __init__(self):
        self.score = 0.0
        self.distance = 0.0
        self.high_score = 0.0  # Could load from file in future
        self.orbs_collected = 0
        self.shield_active = False
        self.shield_timer = 0.0
        
        print("[SCORE] Initialized")
    
    def update(self, speed):
        """
        Update score based on time and distance.
        
        Args:
            speed (float): Current movement speed
        """
        # Distance score (units traveled)
        distance_delta = speed * time.dt
        self.distance += distance_delta
        self.score += distance_delta * config.SCORE_PER_UNIT / 10.0 # Scale down a bit or use config
        
        # Survival score (time based)
        self.score += config.SCORE_PER_SECOND * time.dt
        
        # Update shield timer
        if self.shield_active:
            self.shield_timer -= time.dt
            if self.shield_timer <= 0:
                self.deactivate_shield()
    
    def add_points(self, amount, is_orb=False):
        """
        Add points to score.
        """
        self.score += amount
        if is_orb:
            self.orbs_collected += 1
            print(f"[SCORE] +{amount} (Total: {int(self.score)}) | Orbs: {self.orbs_collected}")
        else:
            print(f"[SCORE] +{amount} (Total: {int(self.score)})")
    
    def activate_shield(self):
        """
        Activate invincibility shield.
        """
        self.shield_active = True
        self.shield_timer = config.SHIELD_DURATION
        print("[SCORE] Shield ACTIVATED!")
    
    def deactivate_shield(self):
        """
        Deactivate invincibility shield.
        """
        self.shield_active = False
        print("[SCORE] Shield expired")
    
    def reset(self):
        """
        Reset score for new game.
        """
        if self.score > self.high_score:
            self.high_score = int(self.score)
        
        self.score = 0.0
        self.distance = 0.0
        self.orbs_collected = 0
        
        # Shield state
        self.shield_active = False
        self.shield_timer = 0.0
        print("[SCORE] Reset")
