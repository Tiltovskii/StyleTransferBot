# StyleTransferBot
**Style transfer telegram bot использующий NST и GAN**
Что за Style Transfer Telegram Bot?
------------------------------------
Style Transfer Telegram Bot - это мой финальный проект конца перого семестра курса [Deep Learning School by MIPT](https://en.dlschool.org/).

Целью проекта было создание NST-сети, которая могла преносить стиль одного изображения на любую дургую фотографию. Так же нужно было написать простого бота в телеграмме, который бы как раз и использовал нашу сеть. К дополнительным заданиям относился так же деплой бота на сервер, чтобы было удобно им пользоваться, и ещё прикрутка готового (если есть вычислительные мощности, то и создание самому) GAN'а.

Скорее всего бот упадет, так как на время проверки он будет лежать на платном сервере от [Reg.ru](https://www.reg.ru), для того чтобы он мог выдавать картинки в высоком разрешении (об этой проблеме будет написано ниже), а после он уже будет наодиться на сервере AWS, где он частнько падает.

Вот сам бот: `@StylishTransBot` (Telegram)

Нейронная сеть
-------
В меню бота есть выбор из трех нейронных сетей:
1) Это обычная NST-модель, которая была взята с [PyTorch](https://pytorch.org/tutorials/advanced/neural_style_tutorial.html). Принцип работы достаточно прост, но итоговое изображеие получается достаточно долго: от 2 минут до получаса (зависит от выбранного качества изображения). Но хочется сказать, что итоговые изображения при высоком качестве получаются достаточно хорошими. Приведу примеры:
2) 
<p align='center'>
  <img src='photos/538614504/me.jpg' height='194' width='290'/>
  <img src='photos/538614504/vangh.jpg' height='194' width='290'/>
  <img src='photos/538614504/me+vangh.jpg' height='194' width='290'/>
</p>

2) 
4) I chose [MSG-Net](https://github.com/zhanghang1989/PyTorch-Multi-Style-Transfer) by [zhanghang1989](https://github.com/zhanghang1989) as the network that performs style transfer. I  took a fully pre-trained model with ready-made weights and immediately made predictions based on it, without additional training for each new image. This made the response process noticeably faster, but it had a slight impact on the quality. The network has shown quite good results. In this repository all the network code is placed in a separate module called [net.py](https://github.com/t0efL/Style-Transfer-Telegram-Bot/blob/master/net.py). I haven't changed the network architecture much, except to [fix an error when loading weights](https://github.com/zhanghang1989/PyTorch-Multi-Style-Transfer/pull/37). Weights are [here](https://github.com/t0efL/Style-Transfer-Telegram-Bot/blob/master/21styles.model). All additional functions for image processing are included in the module [functions.py](https://github.com/t0efL/Style-Transfer-Telegram-Bot/blob/master/functions.py).
