# Import biblioteki do obsługi postgresa
from psycopg2 import connect
# Import funkcji obsługi hashowania haseł i ich sprawdzania
from .clcrypto import check_password, password_hash

class BaseModel:
    __db_con = None # W tej właściwości będę przechowywać pojedyncze połączenie do bazy
    @staticmethod
    def connect(username = "postgres",passwd = "coderslab",hostname = "127.0.0.1",db_name = "workshop_2_db"):
        # Sprawdzanie czy połączenie już jest ustanowione
        if BaseModel.__db_con == None:
            # Jeśli nie to wywołaj je i ustaw opcje
            BaseModel.__db_con = connect(user=username, password=passwd, host=hostname, database=db_name)
            BaseModel.__db_con.autocommit = True
        # Zwróć połącznie
        return BaseModel.__db_con
    @staticmethod
    def disconnect():
        # Sprawdzanie czy połączenie już ustanowione
        if BaseModel.__db_con != None:
            # Jeśli tak rozłącz
            BaseModel.__db_con.close()
            BaseModel.__db_con = None
    @staticmethod
    def cursor():
        # Sprawdzanie czy połączenie już jest ustanowione
        if BaseModel.__db_con == None:
            BaseModel.connect()
        # Zwróć nowy kursor do połączenia
        return BaseModel.__db_con.cursor()
    @staticmethod
    def execute_one(sql,values=()):
        # Metoda wywołuje zapytanie i zwraca pojedynczy wynik
        cur = BaseModel.cursor()
        cur.execute(sql,values)
        output = cur.fetchone()
        cur.close()
        return output

class User(BaseModel):
    __id = None # ID objektu w bazie
    __hashed_password = None # Zasolone i skrócone hasło
    username = None # Nazwa użytkownika
    email = None # email

    def __init__(self):
        # Wartość informuje, że objekt nie jest zapisany w bazie
        self.__id = -1
        # Wstawiam puste wartość
        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    def __str__(self):
        return '{} <{}>'.format(self.username,self.email)

    # Getter dla ID
    @property
    def id(self):
        return self.__id

    # Metody obsługi hasła
    def set_password(self,password):
        # Może da się to zamienić na getter i setter :)
        self.__hashed_password = password_hash(password)

    def check_password(self,password):
        # Sprawdza czy podane hasło pasuje do hasha
        return check_password(password,self.__hashed_password)

    # Metody bazodanowe dla instancji - skorzystamy z nich na konkretnym objekcie tej klasy
    def delete(self):
        # Może dało by się tę metodę przenieść do klasy BaseModel
        cur = User.cursor()
        cur.execute("DELETE FROM Users WHERE id=%s", (self.__id, ))
        cur.close()
        self.__id = -1
        return True

    def save(self):
        # Metoda zapisuje lub aktualizauje dane
        cur = User.cursor()
        if self.__id == -1: # Zapis nowego usera
            cur.execute(
                'INSERT INTO Users(username, email, hashed_password) VALUES(%s, %s, %s) RETURNING id;',
                (self.username, self.email, self.__hashed_password)
            )
            self.__id = cur.fetchone()[0]
        else: # Aktualizacja jeśli posiadamy ID
            cur.execute(
                'UPDATE Users SET hashed_password = %s, email = %s WHERE id = %s;',
                (self.__hashed_password, self.email, self.__id)
            )
        cur.close()
        return True

    # Metody bazodanowe dla obiektów tej klasy - pracują na całym zbiorze
    @staticmethod
    def __from_row(row):
        # Metoda tworzy i zwraca usera na podstawie danych z wiersza
        usr = User()
        usr.__id = row[0]
        usr.username = row[1]
        usr.email = row[2]
        usr.__hashed_password = row[3]
        return usr
    @staticmethod
    def load_by_id(user_id): # Wczytanie po ID
        # Metoda `User.execute_one` zaimplementowana w klasie rodzica
        row = User.execute_one( # Wczytaj jeden wiersz
            'SELECT id, username, email, hashed_password FROM users WHERE id=%s',
            (user_id, )
        )
        if row: # Jeśli udało się wczytać
            return User.__from_row(row) # Tworzenie usera na podstawie wiersza
        else:
            return None

    @staticmethod
    def load_by_username(username): # Wczytanie po ID
        # Metoda `User.execute_one` zaimplementowana w klasie rodzica
        row = User.execute_one( # Wczytaj jeden wiersz
            'SELECT id, username, email, hashed_password FROM users WHERE username=%s',
            (username, )
        )
        if row: # Jeśli udało się wczytać
            return User.__from_row(row) # Tworzenie usera na podstawie wiersza
        else:
            return None

    @staticmethod
    def load_all(): # Wczytuje wszystkich userów - przykład generatora :)
        cur  = User.cursor()
        cur.execute('SELECT id, username, email, hashed_password FROM users;')
        for row in cur:
            yield User.__from_row(row) # Tworzenie usera na podstawie wiersza
        cur.close()

    @staticmethod
    def create_storage(): # Tworzenie tabeli na userów
        cur = User.cursor()
        cur.execute('''
            CREATE TABLE Users(
                id SERIAL,
                username VARCHAR(64),
                hashed_password VARCHAR(128),
                email VARCHAR(128),
                PRIMARY KEY(id)
            );
        ''')
        cur.close()
        return True

class Message(BaseModel):
    pass
