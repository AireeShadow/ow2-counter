import os
import pickle
import logging
from logging import Logger

import PySimpleGUI as sg

from data import Tank, DPS, Support


class OW2():
    def __init__(self):
        self.version = '1.0.1'
        self.logger = self._get_logger()
        self.savefile = 'counter.dat'
        self.backup = 'backup.dat'
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
                self.logger.debug(f'Coounter tuple is {counter_tuple}')
                self.tank = counter_tuple[0]
                self.dps = counter_tuple[1]
                self.support = counter_tuple[2]
        else:
            self.tank = Tank()
            self.dps = DPS()
            self.support = Support()
            
    #TODO: logger is not working, for some reason         
    def _get_logger(self) -> Logger:
        logger = logging.getLogger('ow2_logger')
        fh = logging.FileHandler('ow2-counter.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger
    
    def _save(self, counter_tuple: tuple) -> None:
        if os.path.exists(self.savefile):
            if os.path.exists(self.backup):
                os.remove(self.backup)
            os.rename(self.savefile, self.backup)
        with open(self.savefile, 'ab') as savefile:
            pickle.dump(counter_tuple, savefile)
    
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
                                return 
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
    
    def _update_matcher(self, event: str) -> list:
        match event:
            case 'tank_wins_plus' | 'tank_wins_minus' | 'tank_wins_input':
                result_list = [
                    ('tank_wins_input', self.tank.current_wins),
                    ('tank_total_wins', self.tank.total_wins),
                    ('tank_total_games', self.tank.total)
                    
                ]
            case 'tank_losses_plus' | 'tank_losses_minus' | 'tank_losses_input':
                result_list = [
                    ('tank_losses_input', self.tank.current_losses),
                    ('tank_total_losses', self.tank.total_losses),
                    ('tank_total_games', self.tank.total)
                ]
            case 'dps_wins_plus' | 'dps_wins_minus' | 'dps_wins_input':
                result_list = [
                    ('dps_wins_input', self.dps.current_wins),
                    ('dps_total_wins', self.dps.total_wins),
                    ('dps_total_games', self.dps.total)
                    
                ]
            case 'dps_losses_plus' | 'dps_losses_minus' | 'dps_losses_input':
                result_list = [
                    ('dps_losses_input', self.dps.current_losses),
                    ('dps_total_losses', self.dps.total_losses),
                    ('dps_total_games', self.dps.total)
                ]
            case 'support_wins_plus' | 'support_wins_minus' | 'support_wins_input':
                result_list = [
                    ('support_wins_input', self.support.current_wins),
                    ('support_total_wins', self.support.total_wins),
                    ('support_total_games', self.support.total)
                    
                ]
            case 'support_losses_plus' | 'support_losses_minus' | 'support_losses_input':
                result_list = [
                    ('support_losses_input', self.support.current_losses),
                    ('support_total_losses', self.support.total_losses),
                    ('support_total_games', self.support.total)
                ]
        return result_list
    
    
    #TODO: find the issue with double event processing
    #TODO: find the issue with input text noot working as intended
    def gui(self) -> None:
        self.logger.debug('Initializing the GUI')
        sg.theme('Purple')
        layout = [
            [
                sg.Text('Tank'), 
                sg.Button('+', key='tank_wins_plus'), 
                sg.InputText(self.tank.current_wins, key='tank_wins_input', size=2), 
                sg.Button('-', key='tank_wins_minus'),
                sg.Button('+', key='tank_losses_plus'), 
                sg.InputText(self.tank.current_losses, key='tank_losses_input', size=2), 
                sg.Button('-', key='tank_losses_minus'),
                sg.Text('Total wins: '), 
                sg.Text(str(self.tank.total_wins), key='tank_total_wins'),
                sg.Text('Total loses/ties: '), 
                sg.Text(str(self.tank.total_losses), key='tank_total_losses'),
                sg.Text('Total games: '), 
                sg.Text(str(self.tank.total), key='tank_total_games')
            ],
            [
                sg.Text('DPS'), 
                sg.Button('+', key='dps_wins_plus'),
                sg.InputText(self.dps.current_wins, key='dps_wins_input', size=2), 
                sg.Button('-', key='dps_wins_minus'),
                sg.Button('+', key='dps_losses_plus'), 
                sg.InputText(self.dps.current_losses, key='dps_losses_input', size=2), 
                sg.Button('-', key='dps_losses_minus'),
                sg.Text('Total wins: '),
                sg.Text(str(self.dps.total_wins), key='dps_total_wins'),
                sg.Text('Total loses/ties: '), 
                sg.Text(str(self.dps.total_losses), key='dps_total_losses'),
                sg.Text('Total games: '), 
                sg.Text(str(self.dps.total), key='dps_total_games')
            ],
            [
                sg.Text('Support'), 
                sg.Button('+', key='support_wins_plus'), 
                sg.InputText(self.support.current_wins, key='support_wins_input', size=2), 
                sg.Button('-', key='support_wins_minus'),
                sg.Button('+', key='support_losses_plus'), 
                sg.InputText(self.support.current_losses, key='support_losses_input', size=2), 
                sg.Button('-', key='support_losses_minus'),
                sg.Text('Total wins: '), 
                sg.Text(str(self.support.total_wins), key='support_total_wins'),
                sg.Text('Total loses/ties: '), 
                sg.Text(str(self.support.total_losses), key='support_total_losses'),
                sg.Text('Total games: '), 
                sg.Text(str(self.support.total), key='support_total_games')
            ]
        ]
        window = sg.Window(f'Overwatch 2 games counter, version {self.version}', layout)
        while True:
            event, context = window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                counter_tuple = (
                    self.tank,
                    self.dps,
                    self.support
                )
                self._save(counter_tuple=counter_tuple)
                break
            if 'input' not in event:
                event_list = event.split('_')
                self._the_counter(
                    role=event_list[0],
                    result=event_list[1],
                    operator=event_list[2]
                )
                
            else:
                match event.split('_'):
                    case ['tank', 'wins', _]:
                        self.tank.current_wins = int(context['tank_wins_input'])
                    case ['tank', 'losses', _]:
                        self.tank.current_losses = int(context['tank_losses_input'])
                    case ['dps', 'wins', _]:
                        self.dps.current_wins = int(context['dps_wins_input'])
                    case ['dps', 'losses', _]:
                        self.dps.current_losses = int(context['dps_losses_input'])
                    case ['support', 'wins', _]:
                        self.support.current_wins = int(context['support_wins_input'])
                    case ['support', 'losses', _]:
                        self.support.current_losses = int(context['support_losses_input'])
            update_list = self._update_matcher(event)
            for update_tuple in update_list:
                window[update_tuple[0]].update(update_tuple[1])        
                        
                        
    
if __name__ == '__main__':
    ow2 = OW2()
    ow2.gui()