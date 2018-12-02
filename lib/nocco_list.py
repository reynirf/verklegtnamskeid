
#NOCCOLIST
#VERSION 1.0.2


from lib.color import Color
from ui.frame import Frame
from lib.nocco_key import NoccoKey
import os
import time
import datetime


class NoccoList:
    def print_alternatives_and_get_index(question, alternatives, alternative_index):
        # print('[{}] {}: {}'.format(Color.return_colored('?', 'yellow'), question, alternatives[alternative_index]))
        print('[{}] {}: {}'.format(Color.return_colored('!', 'yellow'), question, Color.return_colored(alternatives[alternative_index], 'bold')))
        for i,alternative in enumerate(alternatives):
            if i == alternative_index:
                if alternative == alternatives[-1]:
                    print()
                    print('   {}'.format(Color.return_colored('> ' + alternative,'red')))
                else:
                    print('   {}'.format(Color.return_colored('> ' + alternative,'cyan')))
            else:
                if alternative == alternatives[-1]:
                    print()
                print('     {}'.format(alternative))

            
    def choose_one(question, alternatives, answer_key):
        alternative_index = 0
        NoccoList.print_alternatives_and_get_index(question, alternatives, alternative_index)
        alphabet = ['A','a','B','b','C','c','D','d','E','e','F','f','G','g','H','h','I','i','J','j','K','k','L','l','M','m','N','n','O','o','P','p','Q','q','R','r','S','s','T','t','U','u','V','v','W','w','X','x','Y','y','Z','z']
        while 1:
            key = NoccoKey.get()
            if key == 'up':
                if alternative_index != 0:
                    alternative_index -= 1
            elif key == 'down':
                if alternative_index != len(alternatives)-1:
                    alternative_index += 1
            elif key not in alphabet:
                return {answer_key:alternatives[alternative_index]}
            Frame.delete_last_lines(n=len(alternatives)+2)
            NoccoList.print_alternatives_and_get_index(question, alternatives, alternative_index)

    def write_many():
        pass
    def checkbox():
        pass
