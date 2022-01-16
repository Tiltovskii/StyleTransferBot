import configparser
from dataclasses import dataclass

content_types = ["photo", 'text', 'audio', 'document', 'sticker', 'video', 'voice']
direction_of_the_files = 'photos'
quality = ['Низкое', 'Среднее', 'Высокое']
quality_to_sizes = {'низкое': 128,
                    'среднее': 256,
                    'высокое': 512}

styles = ['Апельсины 🔄 Яблоки',
          'Лошади 🔄 Зебры',
          'Лето ➡ Зима',
          'Фото ➡ Поль Сезанн',
          'Фото ➡ Винсент Ван Гог']

to_second_keyboard = ['Апельсины 🔄 Яблоки',
                      'Лошади 🔄 Зебры']

Apples2oranges = ['Передлать апельсины в яблоки',
                  'Переделать яблоки в апельсины']

horses2zebras = ['Переделать лошадей в зебр',
                 'Переделать зебр в лошадей']


style2model = {'Передлать апельсины в яблоки': 'CycleGan/cycle/weights/apple2orange/netG_B2A.pth',
               'Переделать яблоки в апельсины': 'CycleGan/cycle/weights/apple2orange/netG_A2B.pth',
               'Переделать лошадей в зебр': 'CycleGan/cycle/weights/horse2zebra/netG_A2B.pth',
               'Переделать зебр в лошадей': 'CycleGan/cycle/weights/horse2zebra/netG_B2A.pth',
               'Фото ➡ Поль Сезанн': 'CycleGan/cycle/weights/cezanne2photo/netG_B2A.pth',
               'Фото ➡ Винсент Ван Гог': 'CycleGan/cycle/weights/vangh2photo/netG_B2A.pth',
               'Лето ➡ Зима': 'CycleGan/cycle/weights/summer2winter_yosemite/netG_A2B.pth',
               }


@dataclass
class TgBot:
    token: str
    admin_id: int


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"],
            admin_id=int(tg_bot["admin_id"])
        )
    )
