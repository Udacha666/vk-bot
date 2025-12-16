import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import string
import time



TOKEN = "vk1.a.TufZSbbPtz6CRcj5if2PfHtkf7vsbKqRK2Rq7RUrcxmqG3wkkP-Lv0jdkc2QtFB2sZEu__fbHTkO6IWqH-IiZcJSSUrjv2vSa6aI8IdSlHIQMUfRaRu28CSPrEfZHhPtulzamBHkyJWeDy7q3nElQBkbGc_tMNru_0BLJ3V1ZRHZKHDQx6d2VUofZyiopnauq5FsKU0GNaYNJHI4fqUFEQ"

# ТВОЙ VK ID, куда будут приходить уведомления
ADMIN_ID = 855467334



# Хранилище всех кодов (в памяти)
CODES = {}  # пример: { "AB12CD": "обычный" }

vk = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk)


def send(uid, text):
    vk.method("messages.send", {
        "user_id": uid,
        "message": text,
        "random_id": random.randint(1, 999999)
    })


def notify_admin(text):
    vk.method("messages.send", {
        "user_id": ADMIN_ID,
        "message": text,
        "random_id": random.randint(1, 999999)
    })


def generate_code():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


def open_chest(chest):
    if chest == "обычный":
        return random.choice([200000, 300000, 400000])[45, 35, 20])[0]   

    if chest == "снежный":
        return random.choice([600000, 700000, 800000], weights=[45, 35, 20])[0]    

    if chest == "секретный":
        return random.choices([100000, 1000000], weights=[60, 40])[0]


print("Бот запущен!")

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:

        uid = event.user_id
        msg = event.text.strip().lower()

        # ========================
        #   АДМИН СОЗДАЁТ КОД
        # ========================
        if uid == ADMIN_ID and msg.startswith("создать код"):
            parts = msg.split()

            if len(parts) < 3:
                send(uid, "Пример: создать код обычный")
                continue

            chest_type = parts[2]

            if chest_type not in ["обычный", "снежный", "секретный"]:
                send(uid, "Тип должен быть: обычный / снежный / секретный")
                continue

            code = generate_code()
            CODES[code] = chest_type   # ← САМЫЙ ВАЖНЫЙ МОМЕНТ !!!

            send(uid, f"✔ Код создан!\nКод: {code}\nСундук: {chest_type}\nУдачи!")
            continue

        # ========================
        #   ПОЛЬЗОВАТЕЛЬ ВВОДИТ КОД
        # ========================
        if msg.upper() in CODES:
            chest = CODES[msg.upper()]  # сундук

            send(uid, f"🎁 Вы получили {chest} сундук! Открываем...")

            time.sleep(1)
            send(uid, "🔄 Крутится...")
            time.sleep(1)
            send(uid, "✨ Выпадает награда...")
            time.sleep(1)

            reward = open_chest(chest)

            send(uid, f"🎉 Вам выпало: {reward:,}, поздравляю!".replace(",", " "))

            notify_admin(f"Пользователь vk.com/id{uid} открыл {chest}, выпало {reward:,}".replace(",", " "))

            del CODES[msg.upper()]  # одноразовый код
            continue

        # ========================
        #   КОД НЕ НАЙДЕН
        # ========================
        send(uid, "Введите код сундука 🔐")
