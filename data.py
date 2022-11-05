from dataclasses import dataclass, fields


@dataclass
class Tank:
    total_wins: int = 0
    total_losses: int = 0
    total: int = 0
    current_wins: int = 0
    current_losses: int = 0
    win_percentage: float = 0.0
    league: str = 'Bronze 5'
    
@dataclass
class DPS:
    total_wins: int = 0
    total_losses: int = 0
    total: int = 0
    current_wins: int = 0
    current_losses: int = 0
    win_percentage: float = 0.0
    league: str = 'Bronze 5'
    
@dataclass
class Support:
    total_wins: int = 0
    total_losses: int = 0
    total: int = 0
    current_wins: int = 0
    current_losses: int = 0
    win_percentage: float = 0.0
    league: str = 'Bronze 5'
    
@dataclass
class Open:
    total_wins: int = 0
    total_losses: int = 0
    total: int = 0
    current_wins: int = 0
    current_losses: int = 0
    win_percentage: float = 0.0
    league: str = 'Bronze 5'