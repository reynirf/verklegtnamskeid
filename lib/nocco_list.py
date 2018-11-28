from lib.color import Color
from ui.frame import Frame
from lib.nocco_key import NoccoKey
import os
import time
import datetime


class NoccoList:
    def print_alternatives_and_get_index(question, alternatives, alternative_index):
        Color.print_colored('Use the RIGHT ARROW KEY (>) to choose an action', 'red')
        print('[{}] {}: {}'.format(Color.return_colored('?', 'yellow'), question, alternatives[alternative_index]))
        for i,alternative in enumerate(alternatives):
            if i == alternative_index:
                print('   {}'.format(Color.return_colored('> ' + alternative,'cyan')))
            else:
                print('     {}'.format(alternative))

    def choose_one(question, alternatives, answer_key):
        alternative_index = 0
        NoccoList.print_alternatives_and_get_index(question, alternatives, alternative_index)
        
        while 1:
            key = NoccoKey.get()
            if key == 'up':
                if alternative_index != 0:
                    alternative_index -= 1
            elif key == 'down':
                if alternative_index != len(alternatives)-1:
                    alternative_index += 1
            else:
                return {answer_key:alternatives[alternative_index]}
            Frame.delete_last_lines(n=len(alternatives)+2)
            NoccoList.print_alternatives_and_get_index(question, alternatives, alternative_index)

        # os.system('cls' if os.name == 'nt' else 'clear')

    def write_many():
        pass
    def checkbox():
        pass
