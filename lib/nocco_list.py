from lib.color import Color
from ui.frame import Frame
from lib.nocco_key import NoccoKey
import os
import time
import datetime


class NoccoList:
    ALPHABET = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', \
                'g', 'H', 'h', 'I', 'i', 'J', 'j', 'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o' \
        , 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V', 'v', 'W', 'w', 'X', \
                'x', 'Y', 'y', 'Z', 'z']

    def __init__(self):
        self.nocco_key = NoccoKey()
        self.color = Color()
        self.frame = Frame()

    def print_alternatives(self, question, alternatives, alternative_index):
        print('[{}] {}: {}'.format(
            self.color.return_colored('!', 'yellow'),
            question,
            self.color.return_colored(alternatives[alternative_index], 'bold')
        ))
        for i, alternative in enumerate(alternatives):
            if i == alternative_index:
                if alternative == alternatives[-1]:
                    print()
                    print('   {}'.format(self.color.return_colored('> ' + alternative, 'red')))
                else:
                    print('   {}'.format(self.color.return_colored('> ' + alternative, 'cyan')))
            else:
                if alternative == alternatives[-1]:
                    print()
                print('     {}'.format(alternative))

    def choose_one(self, question, alternatives, answer_key, get_chosen_index=False):
        alternative_index = 0
        self.print_alternatives(
            question,
            alternatives,
            alternative_index
        )
        while 1:
            key = self.nocco_key.get()
            if key == 'up':
                if alternative_index != 0:
                    alternative_index -= 1
            elif key == 'down':
                if alternative_index != len(alternatives) - 1:
                    alternative_index += 1
            elif key == 'enter' or key == 'right':
                if get_chosen_index:
                    return {answer_key: alternatives[alternative_index], 'index': alternative_index}
                else:
                    return {answer_key: alternatives[alternative_index]}
            elif key == 'left':
                pass
            elif key not in self.ALPHABET:
                if get_chosen_index:
                    return {answer_key: alternatives[alternative_index], 'index': alternative_index}
                else:
                    return {answer_key: alternatives[alternative_index]}
            self.frame.delete_last_lines(n=len(alternatives) + 2)
            self.print_alternatives(
                question,
                alternatives,
                alternative_index
            )

    def single_list(self, alternative):
        print()
        print(' {}'.format(self.color.return_colored('> ' + alternative, 'red')))
        while 1:
            key = self.nocco_key.get()
            if key not in self.ALPHABET and key != 'down' and key != 'up':
                return alternative
            self.frame.delete_last_lines(1)
            print(' {}'.format(self.color.return_colored('> ' + alternative, 'red')))
