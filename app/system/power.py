import os


class PowerController:
    """
    Windows power operations.
    """

    def shutdown(self):

        os.system("shutdown /s /t 1")

    def restart(self):

        os.system("shutdown /r /t 1")

    def sleep(self):

        os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")

    def lock(self):

        os.system("rundll32.exe user32.dll,LockWorkStation")

    def logout(self):

        os.system("shutdown /l")