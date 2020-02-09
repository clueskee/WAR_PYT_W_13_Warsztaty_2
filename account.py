#!/usr/bin/env python3.6
from models import User
import argparse, sys

# Mantra :)
## 1+2. Odbieranie danych + Obróbka danych
## Tutaj będzie to wczytywanie z konsoli paarametrów podanych do programu
parser = argparse.ArgumentParser(description='Account manager.')

# Argumenty obowiązkowe - `required=True`
parser.add_argument('-u','--user', help='user name', required=True)
parser.add_argument('-p','--passwd', help='user password', required=True)
# Argumentu opcjonalne
parser.add_argument('-e','--email', help='user email')
parser.add_argument('-n','--new-passwd', help='new user password')
parser.add_argument('-c','--create', help='create user insted of manage existing', action='store_true')

args = parser.parse_args()

## 3+4. Przetwarzanie i zwracanie treści
if not args.create:
    ## Tu odczytanie User
    user = User.load_by_username(args.user)
    if not user:
        # Jeśli się nie uda to wyświetlam komunikat i kończę program
        print('Nie znaleziono', args.user)
        sys.exit(1) # Zakończenie programu z kodem błędu 1 - wartość wybrana przezemnie :)

    print('Sprawdzanie hasła dla', user)
    if user.check_password(args.passwd):
        print('Poprawne')
        if args.new_passwd: # Jeśli nie podano `-n` to args.new_passwd = None
            print('Zmieniam hasło') # Jeśli jednak podano to zastosuj nowe hasło
            user.set_password(args.new_passwd)
            user.save()
        if args.email: # Podobnie z emailem
            print('Zmieniam email na',args.email)
            user.email = args.email
            user.save()
    else:
        print('Błędne')
else:
    # Tworzenie nowego usera
    new_user = User()
    new_user.set_password(args.passwd)
    new_user.username = args.user
    new_user.email = args.email
    # To jest zapis do bazy
    new_user.save()
    print('Zapisano',new_user)
