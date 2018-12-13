from lib.color import Color
from ui.frame import Frame
from lib.nocco_key import NoccoKey
import os
import time
import datetime
import string

class NoccoList:

    def __init__(self):
        self.nocco_key = NoccoKey()
        self.color = Color()
        self.frame = Frame()

    def print_alternatives(self, question, alternatives, alternative_index):
        print("[{}] {}: {}".format(
            self.color.return_colored("!", "yellow"),
            question,
            self.color.return_colored(alternatives[alternative_index], "bold")
        ))
        for i, alternative in enumerate(alternatives):
            if i == alternative_index:
                if alternative == alternatives[-1]:
                    print()
                    print("   {}".format(self.color.return_colored("> " + alternative, "red")))
                else:
                    print("   {}".format(self.color.return_colored("> " + alternative, "cyan")))
            else:
                if alternative == alternatives[-1]:
                    print()
                print("     {}".format(alternative))

    def choose_one(self, question, alternatives, answer_key, get_chosen_index=False):
        """ from a list of alternatives, let user choose one of them """
        
        alternative_index = 0
        answer_from_user = ""
        #print the alternatives
        self.print_alternatives(
            question,
            alternatives,
            alternative_index
        )
        while not answer_from_user: # run until the user chooses an alternative
            key = self.nocco_key.getKey()
            if key == "up":
                if alternative_index != 0:
                    alternative_index -= 1
            elif key == "down":
                if alternative_index != len(alternatives) - 1:
                    alternative_index += 1
            elif key == "right":
                if get_chosen_index:
                    answer_from_user = {
                        answer_key: alternatives[alternative_index], 
                        "index": alternative_index
                    }
                else:
                    answer_from_user = { answer_key: alternatives[alternative_index] }
            elif key == "left":
                pass
            else:
                if os.name == "nt": # for Windows
                    key = key.decode("utf-8")
                if key not in string.digits and key not in string.ascii_letters and key not in string.punctuation: 
                    if get_chosen_index:
                        answer_from_user = {
                            answer_key: alternatives[alternative_index], 
                            "index": alternative_index
                        }
                    else:
                        answer_from_user = { answer_key: alternatives[alternative_index] }
            self.frame.delete_last_lines(len(alternatives) + 2)
            self.print_alternatives(
                question,
                alternatives,
                alternative_index
            )

        # return answer
        return answer_from_user

    def single_list(self, alternative):
        """ 
            Only one alternative. Useful when for instance only giving 
            "Go back" alternative to the user 
        """
        print()
        print(" {}".format(self.color.return_colored("> " + alternative, "red"))) 

        pressed = False

        while not pressed:
            key = self.nocco_key.getKey() # get key_press from user
            enter_key = string.digits + string.ascii_letters + string.punctuation
            if key not in enter_key and key != "down" and key != "up":
                pressed = True
            self.frame.delete_last_lines(1)
            print(" {}".format(self.color.return_colored("> " + alternative, "red")))
