import subprocess


class AppLauncher:
    """
    Opens desktop applications.
    """

    APPS = {
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
    }

    def open_application(self, text: str):

        text = text.lower()

        for app in self.APPS:

            if app in text:

                try:
                    subprocess.Popen(self.APPS[app])

                    print(f"✅ Opening {app.title()}")

                    return True

                except Exception as e:

                    print(e)

                    return False

        print("❌ Application not found")

        return False