import datetime
import toml
from telethon.sync import TelegramClient
from telethon import functions

with open("config.toml") as file:
    config = toml.load(file)

api_id = config["authorization"]["api_id"]
api_hash = config["authorization"]["api_hash"]


class Register:
    @staticmethod
    def regaccountreg(name):
        try:
            with TelegramClient("tgaccs/" + name, api_id, api_hash) as client:
                client.connect()
            print('Аккаунт успешно зарегистрирован!')
        except Exception as err:
            print(f'Ошибка:\n{err}')

    @staticmethod
    def checkcode(name, show_code):
        with TelegramClient("tgaccs/" + name, api_id, api_hash) as client:
            result = client(functions.messages.GetHistoryRequest(
                peer=777000,
                offset_id=99999999,
                offset_date=datetime.datetime(2018, 6, 27),
                add_offset=0,
                limit=100,
                max_id=0,
                min_id=0,
                hash=0
            ))
            if show_code:
                print(result.messages[0].message)

    @staticmethod
    def checkvalidation(acc):
        print("\nПроверка " + acc)
        try:
            Register.checkcode(acc, False)
            print('Валидный')
            return True
        except Exception as err:
            print(f'Аккаунт умер.\n{err}')
            return False
