import os
from raidfunctions import register, tgraid
from raidfunctions import additional, start_spam

menu = \
    '\n\nВыход из любого меню, нажмите [paste] или [Enter]'\
    '\n\nДоступные функции:\n'\
    '0. Управление сессиями\n'\
    '1. Рейд чата\n'\
    '2. Зайти в чат\n'\
    '3. Рейд в лс\n'\
    '4. Рейд в комментарии канала\n'\
    '5. Управление профилями\n\n>> '

for filename in os.listdir("tgaccs"):
    if filename.endswith(".session-journal"):
        os.remove(
            os.path.join("tgaccs", filename)
        )

while True:
    try:
        a = int(input(menu))
        if a == 0:
            while True:
                print(
                    '\n1) Добавить аккаунт\n'\
                    '2) Получить код\n'\
                    '3) Валидность\n'\
                    '4) Назад\n'
                )
                b = int(input(">> "))
                if b == 1:
                    name = input("Введите название сессии ниже\n>> ")
                    register.Register().regaccountreg(name)
                elif b == 2:
                    print("Введите номер телефона ниже\n>> ")
                    name = input()
                    register.Register().checkcode(name, True)
                elif b == 3:
                    accounts = os.listdir('tgaccs')
                    for account in accounts:
                        try:
                            res = register.Register().checkvalidation(account)
                            if not res:
                                print(f"Аккаунт под сессией {account} умер. Помянем...")
                        except:
                            pass
                elif b == 4:
                    break
        elif a == 1:
            spam = start_spam.Settings(False)
            spam.start_spam()
        elif a == 2:
            spam = start_spam.Settings(True)
            spam.start_spam()
        elif a == 3:
            idtg = input("Введи ссылку на акк, куда спамить\n")
            spam_type = int(input("1.Спамить текстом\n2.Спам файлами\n"))
            if spam_type == 1:
                msg_tp = int(input("1.Спамить рандомными фразами из args.txt\n2.Спамить повторной фразой из message.txt\n\n"))
                msg = tgraid.PrepareRaid().msgs_type(msg_tp)
            else:
                msg_tp = 1
                msg = os.listdir('raidfiles')
            accs = os.listdir('tgaccs')
            for acc in accs:
                print("Спам был запущен с {0} аккаунта!".format(acc))
                tgraid.LsRaid(
                    user_id=idtg,
                    session_name=acc,
                    msg_tp=msg_tp,
                    messages=msg,
                    spam_type=spam_type
                ).start()
        elif a == 4:
            idtg = input("Введи ссылку на пост, куда спамить\n").split("/")
            channel = idtg[3]
            post_id = idtg[4]
            spam_type = int(input("1.Спамить текстом\n2.Спам файлами\n"))
            if spam_type == 1:
                msg_tp = int(input(
                    "1.Спамить рандомными фразами из args.txt\n2.Спамить повторной фразой из message.txt\n\n"))
                msg = tgraid.PrepareRaid().msgs_type(msg_tp)
            else:
                msg_tp = 1
                msg = os.listdir('raidfiles')
            accs = os.listdir('tgaccs')
            for acc in accs:
                print("Спам был запущен с {0} аккаунта!".format(acc))
                tgraid.RaidComments(
                    channel=channel,
                    session_name=acc,
                    msg_tp=msg_tp,
                    messages=msg,
                    spam_type=spam_type,
                    post_id=post_id
                ).start()
        elif a == 5:
            tg_accs = os.listdir('tgaccs')
            set_tg = additional.Set(tg_accs)
            while True:
                print('1. Сменить "О себе"\n'
                      '2. Сменить фотографию\n'
                      '3. Сменить имя и фамилию\n>> ')
                try:
                    a = int(input())
                    if a == 1:
                        bio_text = input("Введите текст ниже\n>> ")
                        set_tg.bio(bio_text)
                    if a == 2:
                        set_tg.avatar()
                    if a == 3:
                        set_tg.name()
                except:
                    break
    except KeyboardInterrupt:
        break
    except ValueError:
        break
    except:
        pass
