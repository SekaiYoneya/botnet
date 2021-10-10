import asyncio
import time
import random
import toml
from threading import Thread
from telethon.sync import TelegramClient, events
from telethon import functions

with open("config.toml") as file:
    config = toml.load(file)

api_id = config["authorization"]["api_id"]
api_hash = config["authorization"]["api_hash"]


class PrepareRaid:
    def __init__(self):
        pass

    @staticmethod
    def msgs_type(msg_type):
        ms = ""
        if msg_type == 1:
            a = open('args.txt', encoding='utf8')
            ms = a.read().split('\n')
            a.close()
        elif msg_type == 2:
            a = open('message.txt', encoding='utf8')
            ms = a.read()
            a.close()
        return ms

    @staticmethod
    def questions(qtype):
        answlist = []
        if qtype:
            answlist.append(input('Введите фразу, которой активируете ботов: '))
        else:
            answlist.append('')
        answlist.append(int(input('Спам режим:\n1.Быстро\n2.Медленно\n')))
        answlist.append(int(input('1.Спамить текстом\n2.Спамить файлами\n')))
        return answlist


class LsRaid(Thread):
    def __init__(self, user_id, session_name, msg_tp, messages, spam_type):
        Thread.__init__(self)
        self.user_id = user_id
        self.session_name = session_name
        self.msg_tp = msg_tp
        self.messages = messages
        self.spam_type = spam_type

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient("tgaccs/" + self.session_name, api_id, api_hash)
        client.start()
        count = 1
        while True:
            try:
                if self.spam_type == 1:
                    if self.msg_tp == 1:
                        client(
                            functions.messages.SendMessageRequest(peer=self.user_id, message=random.choice(self.messages)))
                    else:
                        client(functions.messages.SendMessageRequest(peer=self.user_id, message=self.messages))
                else:
                    client.send_file(self.user_id, f"raidfiles/{random.choice(self.messages)}")
                print(f"[LS RAID] Отправлено {count} раз с аккаунта {self.session_name}!")
            except Exception as er:
                print(f"[LS RAID] Ошибка в {self.session_name}:\n{er}")
                break
            count += 1
            time.sleep(0.5)
        client.run_until_disconnected()


class RaidGroup(Thread):
    def __init__(self, session_name, spam_type, files, messages, trigger, msg_tp, speed, chat):
        Thread.__init__(self)
        self.session_name = session_name
        self.spam_type = spam_type
        self.files = files
        self.messages = messages
        self.trigger = trigger
        self.msg_tp = msg_tp
        self.speed = speed
        self.chat = chat

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            if self.chat == 0:
                client = TelegramClient(
                    "tgaccs/" + self.session_name,
                    api_id, api_hash
                )
                client.connect()

                @client.on(events.NewMessage)
                async def my_event_handler(event):
                    if event.text == self.trigger:
                        count = 1
                        while True:
                            try:
                                if self.spam_type == 1:
                                    if self.msg_tp == 1:
                                        await client(
                                            functions.messages.SendMessageRequest(
                                                peer=event.chat_id, message=random.choice(self.messages)
                                            )
                                        )
                                    else:
                                        await client(
                                            functions.messages.SendMessageRequest(
                                                peer=event.chat_id, message=self.messages
                                            )
                                        )
                                else:
                                    await client.send_file(
                                        event.chat_id,
                                        f"raidfiles/{random.choice(self.files)}"
                                    )
                                if self.speed == 2:
                                    time.sleep(random.randint(1, 3))
                                else:
                                    time.sleep(0.5)
                                print(f"[GROUP RAID] Отправлено {count} раз с аккаунта {self.session_name}!")
                            except Exception as error:
                                print(f"[GROUP RAID] Ошибка в {self.session_name}:\n{error}")
                                break
                            count += 1
                client.start()
                client.run_until_disconnected()
            else:
                client = TelegramClient(
                    "tgaccs/" + self.session_name,
                    api_id, api_hash
                )
                print(self.chat)
                client.connect()
                i = 1
                while True:
                    try:
                        if self.spam_type == 1:
                            if self.msg_tp == 1:
                                client(
                                    functions.messages.SendMessageRequest(
                                        peer=self.chat, message=random.choice(self.messages)
                                    )
                                )
                            else:
                                client(
                                    functions.messages.SendMessageRequest(
                                        peer=self.chat, message=self.messages
                                    )
                                )
                        else:
                            client.send_file(
                                self.chat,
                                f"raidfiles/{random.choice(self.messages)}"
                            )
                        if self.speed == 2:
                            time.sleep(random.randint(1, 3))
                        else:
                            time.sleep(0.5)
                        print(f"[GROUP RAID] Отправлено {i} раз с аккаунта {self.session_name}!")
                    except Exception as e:
                        print(f"[GROUP RAID] Ошибка в:\n{e}")
                        break
                    i += 1
                client.start()
                client.run_until_disconnected()
        except Exception as err:
            print(f"Ошибка:\n{err}")


class ConfJoin:
    def __init__(self, accs, chat_link, speed):
        self.accs = accs
        self.chat_link = chat_link
        self.speed = speed

    def join(self):
        chat_id = 0
        for account in self.accs:
            try:
                with TelegramClient("tgaccs/"+account, api_id, api_hash) as client:
                    client.connect()
                    if self.chat_link[:1] == '@':
                        chat = client.get_entity(self.chat_link[1:])
                        client(functions.channels.JoinChannelRequest(chat.id))
                        chat_id = (1000000000000 + chat.id) * -1
                    try:
                        if self.chat_link[:13] == 'https://t.me/':
                            chat = client.get_entity(self.chat_link[13:])
                            client(functions.channels.JoinChannelRequest(chat.id))
                            chat_id = (1000000000000 + chat.id) * -1
                    except:
                        pass
                    if self.chat_link[13:22] == 'joinchat/':
                        chat = client(functions.messages.ImportChatInviteRequest(hash=self.chat_link[22:]))
                        chat_id = -1 * chat.updates[1].participants.chat_id
                print("{0} успешно зашел в чат!".format(account))
                del client
            except Exception as err:
                print(f"{account} не смог зайти в чат. Причина:\n{err}")
            if self.speed == 2:
                time.sleep(random.randint(1, 3))
        return chat_id


class RaidComments(Thread):
    def __init__(self, channel, session_name, msg_tp, messages, spam_type, post_id):
        Thread.__init__(self)
        self.channel = channel
        self.session_name = session_name
        self.msg_tp = msg_tp
        self.messages = messages
        self.spam_type = spam_type
        self.post_id = int(post_id)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient("tgaccs/" + self.session_name, api_id, api_hash)
        client.start()
        channel_id = self.channel
        count = 1
        while True:
            try:
                if self.spam_type == 1:
                    if self.msg_tp == 1:
                        client.send_message(
                            channel_id,
                            message=random.choice(self.messages),
                            comment_to=self.post_id
                        )
                    else:
                        client.send_message(
                            channel_id,
                            message=self.messages,
                            comment_to=self.post_id
                        )
                else:
                    client.send_file(
                        channel_id,
                        f"raidfiles/{random.choice(self.messages)}",
                        comment_to=self.post_id
                    )
                print(f"[LS RAID] Отправлено {count} раз с аккаунта {self.session_name}!")
            except Exception as er:
                print(f"[LS RAID] Ошибка в {self.session_name}:\n{er}")
                break
            count += 1
            time.sleep(0.5)
        client.run_until_disconnected()
