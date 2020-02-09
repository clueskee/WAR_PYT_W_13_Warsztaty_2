#!/usr/bin/env python3.6
from models import User

print('Users:')
for user in User.load_all():
    print('-',user,'ID:',user.id)
