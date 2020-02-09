#!/usr/bin/env python3.6
'''
    Aby program działała należy najpierw zaimplementować brakujące
    funkcjonalności - klasę Message, oraz ewentualne metody w klasie User
'''
from models import User
import argparse, sys

parser = argparse.ArgumentParser(description='Message manager.')

# Argumenty obowiązkowe - `required=True`
parser.add_argument('-u','--user', help='user name', required=True)
parser.add_argument('-p','--passwd', help='user password', required=True)
# Argumentu opcjonalne
parser.add_argument('-t','--to-user', help='send message to')
parser.add_argument('-m','--message', help='message')
parser.add_argument('-l','--list', help='show my message', action='store_true')
parser.add_argument('-d','--delete', help='delete message by given ID')

args = parser.parse_args()

# Sprawdzenie usera
user = User.load_by_username(args.user)
if not user:
    print('Nie znaleziono', args.user)
    sys.exit(1) # Zakończenie programu z kodem błędu 1 - wartość wybrana przezemnie :)
if not user.check_password(args.passwd):
    print('Błędne hasło')
    sys.exit(2) # Zakończenie programu z kodem błędu 2 - wartość wybrana przezemnie :)

################################################################################
if args.list: # Listowanie wiadomości
    print('Work in progress... :)')
    sys.exit(0)
    # Powinno być coś w stylu
    for message in user.get_all_message():
        print(message)
elif args.delete: # Usuwanie wiadomości
    print('Work in progress... :)')
    sys.exit(0)
    # Powinno być coś w stylu
    mesg = Message.load_by_id(args.delete)
    if mesg:
        if mesg.user_id == user.id:
            mesg.delete()
        else:
            print('Nie możesz usunąć tej wiadomości!')
    else:
        print('Nie znaleziono wiadomości o podanym ID')
else: # Wysyłka wiadomości - zachowanie domyślne
    print('Work in progress... :)')
    sys.exit(0)
    # Powinno być coś w stylu
    target_user = User.load_by_username(args.to_user) # Trzeba jeszcze sprawdzić czy jest
    mesg = Message()
    mesg.sender = user # Trzeba w środku napisać setter gdzie wyciągnie się ID usera
    mesg.user_id = target_user # Trzeba w środku napisać setter gdzie wyciągnie się ID usera
    mesg.text = args.message
    mesg.save()
