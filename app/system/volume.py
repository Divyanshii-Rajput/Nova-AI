class VolumeController:
    """
    Temporary volume controller.

    Real implementation will be added
    after Nova integration is complete.
    """

    def increase(self):

        print("🔊 Increase Volume")

        return True

    def decrease(self):

        print("🔉 Decrease Volume")

        return True

    def mute(self):

        print("🔇 Muted")

        return True

    def unmute(self):

        print("🔊 Unmuted")

        return True

    def get(self):

        return 50