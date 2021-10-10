import os

from raidfunctions import tgraid


class Settings:
    def __init__(self, join_chat):
        self.join_chat = join_chat

    def start_spam(self):
        tg_accounts = os.listdir('tgaccs')
        q = False
        if not self.join_chat:
            q = True
            chat = 0
        else:
            link_to_chat = input('Введите ссылку на чат: ')
            spam_speed = int(input('Скорость спама:\n1.Быстро\n2.Медленно\n'))

            chat = tgraid.ConfJoin(
                accs=tg_accounts,
                chat_link=link_to_chat,
                speed=spam_speed
            ).join()
        answ = tgraid.PrepareRaid().questions(q)
        if answ[2] == 1:
            msg_type = int(
                input(
                    '1.Спам рандомными фразами из args.txt\n'
                    '2.Спам одинаковой фразой из message.txt\n\n'
                )
            )

            for account in tg_accounts:
                print(
                    "Спам был запущен с {0} аккаунта!".format(account)
                )

                ms_type = tgraid.PrepareRaid().msgs_type(msg_type)
                tgraid.RaidGroup(
                    session_name=account,
                    spam_type=answ[2],
                    files='',
                    messages=ms_type,
                    trigger=answ[0],
                    msg_tp=msg_type,
                    speed=answ[1],
                    chat=chat).start()
        if answ[2] == 2:
            print('Файлы для спама берутся из папки raidfiles')
            files = os.listdir('raidfiles')
            for account in tg_accounts:
                print(
                    "Спам запущен с {0} аккаунта!".format(account)
                )
                tgraid.RaidGroup(
                    session_name=account,
                    spam_type=answ[2],
                    files=files,
                    messages=[],
                    trigger=answ[0],
                    msg_tp=0,
                    speed=answ[1],
                    chat=chat
                ).start()
        if q:
            print(
                'Боты активированы!\n'
                f'Отправьте команду "{answ[0]}" для запуска!'
            )
