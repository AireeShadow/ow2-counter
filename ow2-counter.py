import os
import pickle
import logging
import base64
from logging import Logger

import PySimpleGUI as sg

from data import Tank, DPS, Support, Open

class OW2():
    def __init__(self):
        self.version = '1.2.0'
        self.logger = OW2._get_logger()
        self.savefile = 'counter.dat'
        self.backup = 'backup.dat'
        self._load()
        self.total_games = self.tank.total + self.dps.total + self.support.total + self.open.total
            
    #FIXME: logger is not working, for some reason      
    @staticmethod   
    def _get_logger() -> Logger:
        logger = logging.getLogger('ow2_logger')
        fh = logging.FileHandler('ow2-counter.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger
    
    @staticmethod
    def _percent(total: int, part: int) -> float:
        '''
        Returns which percent is part from total
        '''
        result = 100 * float(part) / float(total)
        return round(result, 2)
    
    def _win_percent(self) -> None:
        self.tank.win_percentage = OW2._percent(total=self.tank.total, part=self.tank.total_wins)
        self.dps.win_percentage = OW2._percent(total=self.dps.total, part=self.dps.total_wins)   
        self.support.win_percentage = OW2._percent(total=self.support.total, part=self.support.total_wins)  
        self.open.win_percentage = OW2._percent(total=self.open.total, part=self.open.total_wins)  
    
    def _save(self, counter_tuple: tuple) -> None:
        with open(self.savefile, 'wb') as savefile:
            pickle.dump(counter_tuple, savefile)

    def _load(self) -> None:
        if os.path.exists(self.savefile):
            self.logger.info('Loading the save file.')
            load_file = self.savefile
        elif os.path.exists(self.backup):
           self.logger.warning(f'Saved file not found, using the backup file instead')
           load_file = self.backup
        else:
            self.logger.warning('Neither save file, nor backup file found, creating new save.')
            load_file = False
        if load_file:
            with open(load_file, 'rb') as counter:
                counter_tuple = pickle.load(counter)
                self.logger.debug(f'Counter tuple is {counter_tuple}')
                self.tank = counter_tuple[0]
                self.dps = counter_tuple[1]
                self.support = counter_tuple[2]
                #Backward compatibility for 1.0.2 version
                try:
                    self.open = counter_tuple[3]
                except (AttributeError, IndexError):
                    self.open = Open()
        else:
            self.tank = Tank()
            self.dps = DPS()
            self.support = Support()
            self.open = Open()
    
    def _save_backup(self) -> None:
        if os.path.exists(self.savefile):
            if os.path.exists(self.backup):
                os.remove(self.backup)
            os.rename(self.savefile, self.backup)
            
    def _load_backup(self) -> bool:
        if os.path.exists(self.backup):
           self.logger.warning(f'Loading from backup')
           load_file = self.backup
           if load_file:
                with open(load_file, 'rb') as counter:
                    counter_tuple = pickle.load(counter)
                    self.logger.debug(f'Counter tuple is {counter_tuple}')
                    self.tank = counter_tuple[0]
                    self.dps = counter_tuple[1]
                    self.support = counter_tuple[2]
                    #Backward compatibility for 1.0.2 version
                    try:
                        self.open = counter_tuple[3]
                    except (AttributeError, IndexError):
                        self.open = Open()
                os.remove(self.savefile)
                os.rename(self.backup, self.savefile)
                return True
        else:
            return False 
           
    
    def _the_counter(self, role: str, result: str, operator: str) -> None:
        match role:
            case 'tank':
                match result:
                    case 'wins':
                        match operator:
                            case 'plus':
                                self.tank.current_wins += 1
                                self.tank.total_wins += 1
                                self.tank.total += 1
                                if self.tank.current_wins > 6:
                                    self.tank.current_wins = 0
                                    self.tank.current_losses = 0
                            case 'minus':
                                self.tank.current_wins -= 1
                                self.tank.total_wins -= 1
                                self.tank.total -= 1
                                if self.tank.current_wins < 0:
                                    self.tank.current_wins = 0
                                if self.tank.total_wins < 0:
                                    self.tank.total_wins = 0
                                if self.tank.total < 0:
                                    self.tank.total = 0
                    case 'losses':
                        match operator:
                            case 'plus':
                                self.tank.current_losses += 1
                                self.tank.total_losses += 1
                                self.tank.total += 1
                                if self.tank.current_losses > 19:
                                    self.tank.current_wins = 0
                                    self.tank.current_losses = 0
                            case 'minus':
                                self.tank.current_losses -= 1
                                self.tank.total_losses -= 1
                                self.tank.total -= 1
                                if self.tank.current_losses < 0:
                                    self.tank.current_losses = 0
                                if self.tank.total_losses < 0:
                                    self.tank.total_losses = 0
                                if self.tank.total < 0:
                                    self.tank.total = 0
            case 'dps':
                match result:
                    case 'wins':
                        match operator:
                            case 'plus':
                                self.dps.current_wins += 1
                                self.dps.total_wins += 1
                                self.dps.total += 1
                                if self.dps.current_wins > 6:
                                    self.dps.current_wins = 0
                                    self.dps.current_losses = 0
                            case 'minus':
                                self.dps.current_wins -= 1
                                self.dps.total_wins -= 1
                                self.dps.total -= 1
                                if self.dps.current_wins < 0:
                                    self.dps.current_wins = 0
                                if self.dps.total_wins < 0:
                                    self.dps.total_wins = 0
                                if self.dps.total < 0:
                                    self.dps.total = 0
                    case 'losses':
                        match operator:
                            case 'plus':
                                self.dps.current_losses += 1
                                self.dps.total_losses += 1
                                self.dps.total += 1
                                if self.dps.current_losses > 19:
                                    self.dps.current_wins = 0
                                    self.dps.current_losses = 0
                            case 'minus':
                                self.dps.current_losses -= 1
                                self.dps.total_losses -= 1
                                self.dps.total -= 1
                                if self.dps.current_losses < 0:
                                    self.dps.current_losses = 0
                                if self.dps.total_losses < 0:
                                    self.dps.total_losses = 0
                                if self.dps.total < 0:
                                    self.dps.total = 0                            
            case 'support':
                match result:
                    case 'wins':
                        match operator:
                            case 'plus':
                                self.support.current_wins += 1
                                self.support.total_wins += 1
                                self.support.total += 1
                                if self.support.current_wins > 6:
                                    self.support.current_wins = 0
                                    self.support.current_losses = 0
                            case 'minus':
                                self.support.current_wins -= 1
                                self.support.total_wins -= 1
                                self.support.total -= 1
                                if self.support.current_wins < 0:
                                    self.support.current_wins = 0
                                if self.support.total_wins < 0:
                                    self.support.total_wins = 0
                                if self.support.total < 0:
                                    self.support.total = 0                           
                    case 'losses':
                        match operator:
                            case 'plus':
                                self.support.current_losses += 1
                                self.support.total_losses += 1
                                self.support.total += 1
                                if self.support.current_losses > 19:
                                    self.support.current_wins = 0
                                    self.support.current_losses = 0
                            case 'minus':
                                self.support.current_losses -= 1
                                self.support.total_losses -= 1
                                self.support.total -= 1
                                if self.support.current_losses < 0:
                                    self.support.current_losses = 0
                                if self.support.total_losses < 0:
                                    self.support.total_losses = 0
                                if self.support.total < 0:
                                    self.support.total = 0   
            case 'open':
                match result:
                    case 'wins':
                        match operator:
                            case 'plus':
                                self.open.current_wins += 1
                                self.open.total_wins += 1
                                self.open.total += 1
                                if self.open.current_wins > 6:
                                    self.open.current_wins = 0
                                    self.open.current_losses = 0
                            case 'minus':
                                self.open.current_wins -= 1
                                self.open.total_wins -= 1
                                self.open.total -= 1
                                if self.open.current_wins < 0:
                                    self.open.current_wins = 0
                                if self.open.total_wins < 0:
                                    self.open.total_wins = 0
                                if self.open.total < 0:
                                    self.open.total = 0                           
                    case 'losses':
                        match operator:
                            case 'plus':
                                self.open.current_losses += 1
                                self.open.total_losses += 1
                                self.open.total += 1
                                if self.open.current_losses > 19:
                                    self.open.current_wins = 0
                                    self.open.current_losses = 0
                            case 'minus':
                                self.open.current_losses -= 1
                                self.open.total_losses -= 1
                                self.open.total -= 1
                                if self.open.current_losses < 0:
                                    self.open.current_losses = 0
                                if self.open.total_losses < 0:
                                    self.open.total_losses = 0
                                if self.open.total < 0:
                                    self.open.total = 0   
        self._win_percent()
                
    
    def _update_matcher(self, event: str) -> list:
        match event:
            case 'tank_wins_plus' | 'tank_wins_minus' | 'tank_wins' | 'tank_losses_plus' | 'tank_losses_minus' | 'tank_losses':
                result_list = [
                    ('tank_wins', self.tank.current_wins),
                    ('tank_total_wins', self.tank.total_wins),
                    ('tank_total_games', self.tank.total),
                    ('tank_losses', self.tank.current_losses),
                    ('tank_total_losses', self.tank.total_losses),
                    ('tank_total_games', self.tank.total),
                    ('tank_percent', f'{self.tank.win_percentage}%'),
                    ('total_games', self.total_games)
                ]    
            case 'dps_wins_plus' | 'dps_wins_minus' | 'dps_wins' | 'dps_losses_plus' | 'dps_losses_minus' | 'dps_losses':
                result_list = [
                    ('dps_wins', self.dps.current_wins),
                    ('dps_total_wins', self.dps.total_wins),
                    ('dps_total_games', self.dps.total),
                    ('dps_losses', self.dps.current_losses),
                    ('dps_total_losses', self.dps.total_losses),
                    ('dps_total_games', self.dps.total),
                    ('dps_percent', f'{self.dps.win_percentage}%'),
                    ('total_games', self.total_games)
                    
                ]
            case 'support_wins_plus' | 'support_wins_minus' | 'support_wins' | 'support_losses_plus' | 'support_losses_minus' | 'support_losses':
                result_list = [
                    ('support_wins', self.support.current_wins),
                    ('support_total_wins', self.support.total_wins),
                    ('support_total_games', self.support.total),
                    ('support_losses', self.support.current_losses),
                    ('support_total_losses', self.support.total_losses),
                    ('support_total_games', self.support.total),
                    ('support_percent', f'{self.support.win_percentage}%'),
                    ('total_games', self.total_games)
                    
                ]
            case 'open_wins_plus' | 'open_wins_minus' | 'open_wins' | 'open_losses_plus' | 'open_losses_minus' | 'open_losses':
                result_list = [
                    ('open_wins', self.open.current_wins),
                    ('open_total_wins', self.open.total_wins),
                    ('open_total_games', self.open.total),
                    ('open_losses', self.open.current_losses),
                    ('open_total_losses', self.open.total_losses),
                    ('open_total_games', self.open.total),
                    ('open_percent', f'{self.open.win_percentage}%'),
                    ('total_games', self.total_games)
                    
                ]
            case 'total_games':
                result_list = [
                    ('total_games', self.total_games)
                ]
            case 'set' | 'backup':
                self._win_percent()
                result_list = [
                    ('tank_wins', self.tank.current_wins),
                    ('tank_total_wins', self.tank.total_wins),
                    ('tank_total_games', self.tank.total),
                    ('tank_losses', self.tank.current_losses),
                    ('tank_total_losses', self.tank.total_losses),
                    ('tank_total_games', self.tank.total),
                    ('dps_wins', self.dps.current_wins),
                    ('dps_total_wins', self.dps.total_wins),
                    ('dps_total_games', self.dps.total),
                    ('dps_losses', self.dps.current_losses),
                    ('dps_total_losses', self.dps.total_losses),
                    ('dps_total_games', self.dps.total),
                    ('support_wins', self.support.current_wins),
                    ('support_total_wins', self.support.total_wins),
                    ('support_total_games', self.support.total),
                    ('support_losses', self.support.current_losses),
                    ('support_total_losses', self.support.total_losses),
                    ('support_total_games', self.support.total),
                    ('open_wins', self.open.current_wins),
                    ('open_total_wins', self.open.total_wins),
                    ('open_total_games', self.open.total),
                    ('open_losses', self.open.current_losses),
                    ('open_total_losses', self.open.total_losses),
                    ('open_total_games', self.open.total),
                    ('open_percent', f'{self.open.win_percentage}%'),
                    ('support_percent', f'{self.support.win_percentage}%'),
                    ('dps_percent', f'{self.dps.win_percentage}%'),
                    ('tank_percent', f'{self.tank.win_percentage}%'),
                    ('total_games', self.total_games)
                ]
            case _:
                result_list = list()
        return result_list
    
    @staticmethod
    def _league() -> list:
        league_list = list()
        for league in ['Bronze', 'Silver', 'Gold', 'Diamond', 'Master', 'Grandmaster']:
            for i in range(5, 0, -1):
               league_list.append(f'{league} {i}')
        league_list.append('Top 500')        
        return league_list
        
    def _layout(self) -> list:
        tank_frame = [
            [
                sg.Text('Victories:', size=15),
                sg.Button('+', key='tank_wins_plus'), 
                sg.Text(self.tank.current_wins, key='tank_wins', size=2), 
                sg.Button('-', key='tank_wins_minus')
            ],
            [
                sg.Text('Defeats:', size=15),
                sg.Button('+', key='tank_losses_plus'), 
                sg.Text(self.tank.current_losses, key='tank_losses', size=2), 
                sg.Button('-', key='tank_losses_minus')
            ],
            [   sg.Text('Total victories:', size=15), 
                sg.InputText(self.tank.total_wins, key='tank_total_wins', size=3)
            ],
            [
                sg.Text('Total defeats/ties:', size=15), 
                sg.InputText(self.tank.total_losses, key='tank_total_losses', size=3)
            ],
            [
                sg.Text('Total games:', size=15), 
                sg.Text(self.tank.total, key='tank_total_games')
            ],
            [
                sg.Text('Victory percentage:', size=15),
                sg.Text(f'{self.tank.win_percentage}%', key='tank_percent')
            ],
            [
                sg.Text('League:', size=8),
                sg.Combo(values=OW2._league(), default_value=self.tank.league, key='tank_league', enable_events=True)
            ]
        ]
        dps_frame = [
            [
                sg.Text('Victories:', size=15),
                sg.Button('+', key='dps_wins_plus'),
                sg.Text(self.dps.current_wins, key='dps_wins', size=2), 
                sg.Button('-', key='dps_wins_minus')
            ],
            [
                sg.Text('Defeats:', size=15),
                sg.Button('+', key='dps_losses_plus'), 
                sg.Text(self.dps.current_losses, key='dps_losses', size=2), 
                sg.Button('-', key='dps_losses_minus')
            ],
            [
                sg.Text('Total victories:', size=15),
                sg.InputText(self.dps.total_wins, key='dps_total_wins', size=3)
            ],
            [
                sg.Text('Total defeats/ties:', size=15), 
                sg.InputText(self.dps.total_losses, key='dps_total_losses', size=3)
            ],
            [
                sg.Text('Total games:', size=15), 
                sg.Text(self.dps.total, key='dps_total_games')
            ],
            [
                sg.Text('Victory percentage:', size=15),
                sg.Text(f'{self.dps.win_percentage}%', key='dps_percent')
            ],
            [
                sg.Text('League:', size=8),
                sg.Combo(values=OW2._league(), default_value=self.dps.league, key='dps_league', enable_events=True)
            ]
        ]
        support_frame = [
            [
                sg.Text('Victories:', size=15),
                sg.Button('+', key='support_wins_plus'),
                sg.Text(self.support.current_wins, key='support_wins', size=2), 
                sg.Button('-', key='support_wins_minus')
            ],
            [
                sg.Text('Defeats:', size=15),
                sg.Button('+', key='support_losses_plus'), 
                sg.Text(self.support.current_losses, key='support_losses', size=2), 
                sg.Button('-', key='support_losses_minus')
            ],
            [
                sg.Text('Total victories:', size=15), 
                sg.InputText(self.support.total_wins, key='support_total_wins', size=3)
            ],
            [
                sg.Text('Total defeats/ties:', size=15), 
                sg.InputText(self.support.total_losses, key='support_total_losses', size=3)
            ],
            [
                sg.Text('Total games:', size=15), 
                sg.Text(self.support.total, key='support_total_games')
            ],
            [
                sg.Text('Victory percentage:', size=15),
                sg.Text(f'{self.support.win_percentage}%', key='support_percent')
            ],
            [
                sg.Text('League:', size=8),
                sg.Combo(values=OW2._league(), default_value=self.support.league, key='support_league', enable_events=True)
            ]
        ]
        open_frame = [
            [
                sg.Text('Victories:', size=15),
                sg.Button('+', key='open_wins_plus'), 
                sg.Text(self.open.current_wins, key='open_wins', size=2), 
                sg.Button('-', key='open_wins_minus')
            ],
            [
                sg.Text('Defeats:', size=15),
                sg.Button('+', key='open_losses_plus'), 
                sg.Text(self.open.current_losses, key='open_losses', size=2), 
                sg.Button('-', key='open_losses_minus'),
            ],
            [
                sg.Text('Total victories:', size=15), 
                sg.InputText(self.open.total_wins, key='open_total_wins', size=3)
            ],
            [
                sg.Text('Total defeats/ties:', size=15), 
                sg.InputText(self.open.total_losses, key='open_total_losses', size=3)
            ],
            [
                sg.Text('Total games:', size=15), 
                sg.Text(self.open.total, key='open_total_games')
            ],
            [
                sg.Text('Victory percentage:', size=15),
                sg.Text(f'{self.open.win_percentage}%', key='open_percent')
            ],
            [
                sg.Text('League:', size=8),
                sg.Combo(values=OW2._league(), default_value=self.open.league, key='open_league', enable_events=True)
            ]
        ]
        layout = [
            [
                sg.Frame('Tank', tank_frame),
                sg.Frame('DPS', dps_frame),
                sg.Frame('Support', support_frame),
                sg.Frame('Open queue', open_frame)
            ],
            [
                sg.Button('Set values', key='set'),
                sg.Button('Restore from backup', key='backup'),
                sg.Text('Total ranked games:'),
                sg.Text(self.total_games, key='total_games')
            ]
        ]
        return layout
    
    def gui(self) -> None:
        self.logger.debug('Initializing the GUI')
        sg.theme('Purple')
        layout = self._layout()
        window = sg.Window(f'Overwatch 2 games counter, version {self.version}', layout, icon='overwatch.ico')
        # sg.set_options(icon=base64.b64encode(open('icon.png', 'rb').read()))
        while True:
            event, context = window.read()
            match event:
                case sg.WIN_CLOSED | 'Exit':
                    self._save_backup()
                    counter_tuple = (
                        self.tank,
                        self.dps,
                        self.support,
                        self.open
                    )
                    self._save(counter_tuple=counter_tuple)  
                    break
                case 'set':
                    self.tank.total_wins = int(context['tank_total_wins'])
                    self.tank.total_losses = int(context['tank_total_losses'])
                    self.tank.total = self.tank.total_wins + self.tank.total_losses
                    self.dps.total_wins = int(context['dps_total_wins'])
                    self.dps.total_losses = int(context['dps_total_losses'])
                    self.dps.total = self.dps.total_wins + self.dps.total_losses
                    self.support.total_wins = int(context['support_total_wins'])
                    self.support.total_losses = int(context['support_total_losses'])
                    self.support.total = self.support.total_wins + self.support.total_losses
                    self.open.total_wins = int(context['open_total_wins'])
                    self.open.total_losses = int(context['open_total_losses'])
                    self.open.total = self.open.total_wins + self.open.total_losses
                case 'open_league':
                    self.open.league = context['open_league']
                case 'support_league':
                    self.support.league = context['support_league']
                case 'dps_league':
                    self.dps.league = context['dps_league']
                case 'tank_league':
                    self.tank.league = context['tank_league']
                case 'backup':
                    popup = sg.popup_yes_no('Are you sure you want restore from backup?', title='Restore backup?', icon='overwatch.ico')
                    if popup =='Yes':
                        load_result = self._load_backup()
                        if not load_result:
                            sg.popup('Backup not loaded, as it not found.', title='File not found', icon='overwatch.ico')
                case _ if 'input' not in event:
                    event_list = event.split('_')
                    self._the_counter(
                        role=event_list[0],
                        result=event_list[1],
                        operator=event_list[2]
                    )
            self.total_games = self.tank.total + self.dps.total + self.support.total + self.open.total    
            update_list = self._update_matcher(event)
            for update_tuple in update_list:
                window[update_tuple[0]].update(update_tuple[1])    
            counter_tuple = (
                self.tank,
                self.dps,
                self.support,
                self.open
            )
            self._save(counter_tuple=counter_tuple)    
                        
                        
    
if __name__ == '__main__':
    ow2 = OW2()
    ow2.gui()