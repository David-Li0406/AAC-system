import sys
sys.path.append('../')
from app import db
from app.models import UserModel

def Add_administrator(username, user_type):
    assert user_type == 'user' or user_type == 'administrator','user_type should be administrator or user'
    u = UserModel.find_by_username(username)
    if u == None:
        print('username not found')
        exit(-1)
    u.user_type = user_type
    db.session.commit()

if __name__ == '__main__':
    Add_administrator(sys.argv[1], sys.argv[2])