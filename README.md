# StyleTransferBot
**Style transfer telegram bot использующий NST и GAN**
Что за Style Transfer Telegram Bot?
------------------------------------
Style Transfer Telegram Bot - это мой финальный проект конца перого семестра курса [Deep Learning School by MIPT](https://en.dlschool.org/).

Целью проекта было создание NST-сети, которая могла преносить стиль одного изображения на любую дургую фотографию. Так же нужно было написать простого бота в телеграмме, который бы как раз и использовал нашу сеть. К дополнительным заданиям относился так же деплой бота на сервер, чтобы было удобно им пользоваться, и ещё прикрутка готового (если есть вычислительные мощности, то и создание самому) GAN'а.

Скорее всего бот упадет, так как на время проверки он будет лежать на платном сервере от [Reg.ru](https://www.reg.ru), для того чтобы он мог выдавать картинки в высоком разрешении (об этой проблеме будет написано ниже), а после он уже будет находиться на сервере AWS, где он частнько падает.

Вот сам бот: `@StylishTransBot` (Telegram)

Нейронная сеть
-------
В меню бота есть выбор из трех нейронных сетей:
1) Это обычная NST-модель, которая была взята с [PyTorch](https://pytorch.org/tutorials/advanced/neural_style_tutorial.html). Сама модель лежит [здесь](https://github.com/Tiltovskii/StyleTransferBot/blob/master/TransferStyles.py). Принцип работы достаточно прост, но итоговое изображеие получается достаточно долго: от 2 минут до получаса (зависит от выбранного качества изображения). Но хочется сказать, что итоговые изображения при высоком качестве получаются достаточно хорошими. Приведу примеры:

<p align='center'>
  <img src='photos/538614504/me.jpg' height='256' width='256'/>
  <img src='photos/538614504/vangh.jpg' height='256' width='256'/>
  <img src='photos/538614504/me+vangh.jpg' height='256' width='256'/>
</p>

<p align='center'>
  <img src='photos/538614504/sob.jpg' height='256' width='256'/>
  <img src='photos/538614504/moz.jpg' height='256' width='256'/>
  <img src='photos/538614504/sob+moz.jpg' height='256' width='256'/>
</p>

<p align='center'>
  <img src='photos/538614504/phi.jpg' height='256' width='256'/>
  <img src='photos/538614504/picasso.jpg' height='256' width='256'/>
  <img src='photos/538614504/pho+picasso.jpg' height='256' width='256'/>
</p>

2) Это уже предобученная модель [MSG-Net](https://github.com/zhanghang1989/PyTorch-Multi-Style-Transfer) от [zhanghang1989](https://github.com/zhanghang1989). Модель находится [здесь](https://github.com/Tiltovskii/StyleTransferBot/blob/master/Pretrained.py) и использует эти [веса](https://github.com/Tiltovskii/StyleTransferBot/blob/master/21styles.model). Результат этой модели получается очень быстро, так как модель не особо большая, и уже присутствуют предобученные веса, но качество получаемых изображений меня не совсем устраивает, хотя, может, кому-то и понравится. Примеры снизу:

<p align='center'>
  <img src='photos/538614504/sob.jpg' height='256' width='256'/>
  <img src='photos/538614504/vangh.jpg' height='256' width='256'/>
  <img src='photos/538614504/sob+vangh.jpg' height='256' width='256'/>
</p>

<p align='center'>
  <img src='photos/538614504/sob.jpg' height='256' width='256'/>
  <img src='photos/538614504/moz.jpg' height='256' width='256'/>
  <img src='photos/538614504/sob+moz2.jpg' height='256' width='256'/>
</p>

3) Последняя модель - [CycleGAN](https://github.com/Lornatang/CycleGAN-PyTorch) от [Loranatang](https://github.com/Lornatang). Модель полностью находится в [CycleGan/cycle/](https://github.com/Tiltovskii/StyleTransferBot/tree/master/CycleGan/cycle). Данная модель уже меняет стиль на какой-то предобученный и у [Loranatang](https://github.com/Lornatang) есть тройка весов, первый из которых меняет яблоки на апельсины и обратно, второй меняет лошадей на зебр, а трейтий изменяет фотографии в стиле Поль Сезанна. Мне показалось, что этого мало и поэтому, используя [Colab](https://colab.research.google.com) и [SaturnCloud](https://saturncloud.io/), удалось обучить модель изменять летнюю фотографию на зимнюю и добавить стиль картин Винсента Ван Гога. Если разобраться в принципе CycleGan, то можно задаться вопрсом: почему, например, есть изменение летней фотографии в зимнюю, но нет зимней в летнюю? Я отвечу, что вычислительные мощности были не шибко огромные, поэтому вариант, когда зимняя фотография преобразовывалась в летнюю, имел слишком много артефактов. Примеры фотографий:


<p align='center'>
  <b>Летняя фотография в зимнюю</b>
</p>

<p align='center'>
  <img src='photos/538614504/forest.jpg' height='512' width='256'/>
  <img src='photos/538614504/forest_to_winter.jpg' height='512' width='256'/>
</p>

<p align='center'>
  <b>Фотография в стиле картин Поль Сезанне</b>
</p>

<p align='center'>
  <img src='photos/538614504/forest.jpg' height='512' width='256'/>
  <img src='photos/538614504/forest_to_cezanne.jpg' height='512' width='256'/>
</p>

<p align='center'>
  <b>Фотография в стиле картин Винсента Ван Гога</b>
</p>

<p align='center'>
  <img src='photos/538614504/forest.jpg' height='512' width='256'/>
  <img src='photos/538614504/forest_to_vanghgog.jpg' height='512' width='256'/>
</p>

<p align='center'>
  <img src='photos/538614504/forest2.jpg' height='256' width='256'/>
  <img src='photos/538614504/forest2_to_naghgog.jpg' height='256' width='256'/>
</p>

<p align='center'>
  <b>Апельсины в Яблоки</b>
</p>

<p align='center'>
  <img src='photos/538614504/oranges.jpg' height='256' width='256'/>
  <img src='photos/538614504/apples.jpg' height='256' width='256'/>
</p>

<p align='center'>
  <b>Яблоки в Апельсины</b>
</p>

<p align='center'>
  <img src='photos/538614504/apples2.jpg' height='350' width='256'/>
  <img src='photos/538614504/oranges2.jpg' height='350' width='256'/>
</p>

<p align='center'>
  <b>Зебры в лошадей</b>
</p>

<p align='center'>
  <img src='photos/538614504/zebras.jpg' height='256' width='256'/>
  <img src='photos/538614504/hourses.jpg' height='256' width='256'/>
</p>

<p align='center'>
  <b>Лошади в Зебр</b>
</p>

<p align='center'>
  <img src='photos/538614504/horses2.jpg' height='256' width='256'/>
  <img src='photos/538614504/zebras2.jpg' height='256' width='256'/>
</p>

Бот
---
Я выбрал [aiogram](https://docs.aiogram.dev/en/latest/index.html) за фрэймворк для написания бота.

Преимущество данного фрэймворка в том, что она поддерживает ассинхронность, благодаря чему можно получать запросы от множества пользователей. Так же в нем присутсвует поддержка
вебхука, но я использовал пулинг, так как он легче реализуется, и я не деплоил на сервисах таких как, например, [Heroku](https://www.heroku.com/), где программа засыпает после одного часа.

Код бота присутсвует в [main.py](https://github.com/t0efL/Style-Transfer-Telegram-Bot/blob/master/main.py).

Настройка
----------------
Свой уникальный токен для бота можно получить через `@BotFather`.
Благодаря ему получилось сделать удобные команды и произвести настройку бота.

![alt text](https://i2.paste.pics/FNW5X.png)

**Перед началом убедитесь, что вы получили токен бота и указали его в bot.ini.**

Деплой
------
Для деплоя я выбрал сервис AWS, так как он бесплатен и с ним достаточно легко работать. Туториал, который мне помог в этом [здесь](https://github.com/hse-aml/natural-language-processing/blob/master/AWS-tutorial.md)
Тут я сделал всё до "Connect to your instance using SSH. If you have problems connecting to the instance, try following this troubleshooting guide." и вместо  Ubuntu 16.04 выбрал Ubuntu 20.04.
Дальше с помощью WinSCP я заугрузил нужные файлы и, используя PuTTY, уже управлял VPS из консоли.
Скорее всего понадобится ввести слежующие команды, чтобы установить питон и избежать ошибок:
`$ sudo apt update`

`$ sudo apt install python3-pip`

`$ sudo apt install libgl1-mesa-glx`

После нужно установить requirments.txt один находится в главной директории, а другой в `CycleGan/cycle`, где лежат нужные библиотеки для CycleGan.

`$ pip3 install -r requirements.txt`

После всего уже можно будет запускать самого бота командой 

`$ python3 main.py`

Файл `Procfile` нигде не используется, так как он вообще был расчитан для деплоя на `Heroku`, чего я по итогу не сделал.

Итоги
------
Результаты в принципе выглядят хорошими, но если бы имелись вычислительные мощности, то можно было б сделать больше интересных весов для GAN'а. А так вы сами можете попытаться им воспользоваться, если он еще работает.

