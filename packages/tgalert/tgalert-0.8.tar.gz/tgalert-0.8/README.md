# tgalert
Repository containing a simple Python3 module to allow messages for code updates using the Telegram messaging service. Original intention is to notify a programmer when a long process is finished, such as training a model or building a dataset.

How to setup with pip:
```
pip3 install tgalert
nano ~/.tg-config  # type auth token for your Telegram bot (use @BotFather to create new bot, can be shared), new line, followed by your client id (use @get_id bot)
```

To test the installation (should send two Telegram messages, one alert and one error):

```
python3 -c "from tgalert import tg_alert; tg_alert.test()"
```

Then in your code:

```
from tgalert import TelegramAlert
alert = TelegramAlert()
alert.write('Training complete')
```

Extra features:

- If .tg-config does not exist, write() performs no action and throws no error; it can be used in code without worry
- Can specify different config location if necessary
- If program crashes on exception it will notify on Telegram (all but KeyboardInterupt and SyntaxError)
