import screen_brightness_control as sbc


class BrightnessController:
    """
    Controls system brightness.
    """

    def increase(self, step: int = 10):

        try:

            current = sbc.get_brightness(display=0)[0]

            current = min(100, current + step)

            sbc.set_brightness(current)

            print(f"☀ Brightness: {current}%")

            return True

        except Exception as error:

            print(error)

            return False

    def decrease(self, step: int = 10):

        try:

            current = sbc.get_brightness(display=0)[0]

            current = max(0, current - step)

            sbc.set_brightness(current)

            print(f"🌙 Brightness: {current}%")

            return True

        except Exception as error:

            print(error)

            return False

    def set(self, value: int):

        try:

            value = max(0, min(100, value))

            sbc.set_brightness(value)

            print(f"☀ Brightness set to {value}%")

            return True

        except Exception as error:

            print(error)

            return False

    def get(self):

        try:

            return sbc.get_brightness(display=0)[0]

        except Exception:

            return None