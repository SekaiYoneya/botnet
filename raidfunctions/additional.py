import random
import os
import toml
from telethon.sync import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest

with open("config.toml") as file:
    config = toml.load(file)

api_id = config["authorization"]["api_id"]
api_hash = config["authorization"]["api_hash"]


class Set:
    def __init__(self, tg_accounts):
        self.tg_accounts = tg_accounts

    def bio(self, bio_text):
        for tg_acc in self.tg_accounts:
            try:
                with TelegramClient("tgaccs/" + tg_acc, api_id, api_hash) as client:
                    client(UpdateProfileRequest(about=bio_text))
                print(f'Био было обновлено на акке {tg_acc}')
            except Exception as err:
                print(f'Ошибка:\n{err}')

    def avatar(self):
        for tg_acc in self.tg_accounts:
            try:
                with TelegramClient("tgaccs/" + tg_acc, api_id, api_hash) as client:
                    photo = 'avatars/' + random.choice(os.listdir('avatars/'))
                    upload_file = client.upload_file(photo)
                    client(UploadProfilePhotoRequest(upload_file))
                    print(f'Аватар был обновлен на аккаунте {tg_acc}')
            except Exception as err:
                print(f'Ошибка:\n{err}')

    def name(self):
        for tg_acc in self.tg_accounts:
            f = open("name.txt", encoding='utf-8', errors='ignore')
            f_text = f.read()
            v = open("surname.txt", encoding='utf-8', errors='ignore')
            v_text = v.read()
            while True:
                name = random.choice(f_text.split('\n'))
                surname = random.choice(v_text.split('\n'))
                if name != "" and surname != "":
                    break
            f.close()
            v.close()
            try:
                with TelegramClient("tgaccs/" + tg_acc, api_id, api_hash) as client:
                    client(
                        UpdateProfileRequest(
                            first_name=name,
                            last_name=surname
                        )
                    )
                    print(f'Поставлено имя {name} {surname} на аккаунте {tg_acc}')
            except Exception as err:
                print(f'Ошибка:\n{err}')
