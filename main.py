from models.car import Car
from models.frame import Frame
from lib.color import Color
import inquirer




frame = Frame()
print(frame)



questions = [
inquirer.List('answer',
                message="What do you want to do?",
                choices=['test1', 'test2', 'test3', 'test4', 'test5', 'test6'],
            ),
]
answers = inquirer.prompt(questions)

print(answers)


# for i in Color.COLORS:
#     Color.print_colored('tetetssteta', i)
# # Color.print_colored('HALHAHLALOHLAHLA', 'blue')
