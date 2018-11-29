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
    except KeyError:
        Frame.delete_last_lines(2)
        Color.print_colored('Invalid ID: '+user_id, 'red')
        return authenticate(users)

def initialize_user(user):
    name = user[0]
    user_id = user[1]
    user = User(name,user_id)
    return user

def introduce_user(user):
    print(user)

# def logout(user):
#     Frame.delete_last_lines(12)

frame = Frame()
print(frame) #ekki remove'a

users = get_users()
print() #ekki remove'a
user = authenticate(users)

print() 

user = initialize_user(user)
introduce_user(user)

print()

prompt = NoccoList.choose_one('Choose an action', ['Order','Customer','Reports','Logout'],'answer')

print() 
print('The action you picked: ' + prompt['answer'])

print()
print()



# for i in Color.COLORS:
#     Color.print_colored('tetetssteta', i)
# # Color.print_colored('HALHAHLALOHLAHLA', 'blue')
