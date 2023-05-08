# POCSAG rpitx - Pager - Telegram bot

Telegram-бот, который может отправлять сообщения через rpitx / Motorola Advisor Русская кодировка / декодирование

Бот работает только на raspberry pi, используя программное обеспечение rpitx для отправки сигналов

0. Установите python 3 и запустите `pip3 install pyTelegramBotAPI` или `pip install pyTelegramBotAPI`
1. Создайте телеграмм-бота через `@BotFather` и получите его токен, вставьте этот токен вместо `YOUR_TELEGRAM_BOT_TOKEN_HERE_From_BotFather` в строке 7.
2. Поместите rpitx в /home/pi/rpitx/ и убедитесь, что у этого приложения есть `chmod +x /home/pi/rpitx/pocsag` и вы можете запустить `/home/pi/rpitx/pocsag`
(также вы можете изменить путь к месту установки rpitx в самом скрипте Python, это довольно просто)
3. Найдите строку `markup.add('110', '122', '121', '111', '3123', '1123A')` эти числа (часть капкодов так как в моем случае капкод в начале состоит из нулей), которые вы будете использовать для отправки сообщений
используя cmd(или control) + F, найдите число, например `122`, и замените его своим Капкодом! если ваш капкод длиннее, найдите строку, которая вызывает функцию отправки, она понадобится вам на следующем шаге, и установите полный капкод здесь ` send_msg_to_pgr("КАПКОД", "ЧАСТОТА", sendmsg)`
4. Найдите строки `send_msg_to_pgr("0000111", "160037000", sendmsg)` и замените `0000111` на ваш Капкод, а `160037000` на частоту, которую использует ваш пейджер.
5. Найдите «-r 1200» — это тип/скорость POCSAG, POCSAG 1200, измените его на другое значение, если вам нужно
6. Найдите `111111111` и `222222222` в `user_dict` и замените эти числа на свой телеграм айди, который вы можете получить, отправив сообщение в своего бота и посмотрев в консоль когда он запущен или через @userinfobot (используйте чьи-то боты на свой страх и риск!!!)
7. Измените `U1` и `U2` на имена отправителей, эти имена будут отображаться на экране пейджера, вы также можете удалить их, если хотите, для этого нужно сделать имена пустыми ""
8. Если вы внесли все необходимые изменения, вы можете запустить свой скрипт с помощью `python3 pgr.py` или `python pgr.py`


---------

Telegram bot that can send messages via rpitx / Motorola Advisor Russian encoding/decoding option

Bot works only on raspberry pi using rpitx software to send signals

0. install python 3 and run `pip3 install pyTelegramBotAPI` or `pip install pyTelegramBotAPI`
1. Create telegram bot via `@BotFather` and get its token, paste that token instead of `YOUR_TELEGRAM_BOT_TOKEN_HERE_From_BotFather` on line 7
2. Put rpitx into /home/pi/rpitx/ and make sure that this app has `chmod +x /home/pi/rpitx/pocsag` and you can run `/home/pi/rpitx/pocsag`
(also you can change path to your rpitx set-up place in python script itself, its pretty simple)
3. find line `markup.add('110', '122', '121', '111', '3123', '1123A')` this is numbers (end part of CAPCodes) that you gonna use
using cmd(control) + F, search for number for example `122` and replace it with your CAPCODE, if your CAPCODE is longer look for line that calls sending function, you will need it in next step, and set full CAPCODE here `send_msg_to_pgr("CAPCODE", "FREQUENCY", sendmsg)`
4. Find lines `send_msg_to_pgr("0000111", "160037000", sendmsg)` and replace `0000111` with your CAPCODE and `160037000` with frequency your pager uses
5. Search for `-r 1200` - This is POCSAG type/speed, POCSAG 1200, change it to different value if you need
6. Search for `111111111` and `222222222` in `user_dict` and replace that numbers with your telegram ID, that you can get by sending message in your bot or via @userinfobot (use someone's bots on your risk!!!)
7. Change `U1` and `U2` with sender names, this names will be shown on pager screen, you can also remove them if you want and set names to empty ""
8. If you made all needed changes, you can run your script with `python3 pgr.py` or `python pgr.py`
