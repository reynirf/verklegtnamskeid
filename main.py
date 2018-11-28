from models.vehicle import Vehicle
from ui.frame import Frame
from lib.color import Color
from models.user import User
from lib.nocco_list import NoccoList



def get_users():
    with open('data/ids.txt') as users:
        raw_users = users.read()

    users = {}
    for user in raw_users.split('\n'):
        users[user[0:3]] = user[4:]
    return users

def authenticate(users):
    try:
        user_id = input('Enter ID: ')
        users[user_id]
        return (users[user_id],user_id)
    except ValueError:
        return 0
    except KeyError:
        return 0

def initialize_user(user):
    name = user[0]
    user_id = user[1]
    user = User(name,user_id)
    return user

def introduce_user(user):
    print(user)

frame = Frame()
print(frame)

users = get_users()
user = authenticate(users)

print()

if not user:
    print('Invalid ID')
else:
    user = initialize_user(user)
    introduce_user(user)

print()

prompt = NoccoList.choose_one('What do you want?', ['I want money', 'Cookies','MEAT AND CHEESE','All above'],'answer')

print() 
print('THE ANSWER YOU PICKED IS: ' + prompt['answer'])

print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()



# for i in Color.COLORS:
#     Color.print_colored('tetetssteta', i)
# # Color.print_colored('HALHAHLALOHLAHLA', 'blue')
