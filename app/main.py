from app.config.settings import settings


def main():
    print("=" * 40)
    print(settings.APP_NAME)
    print(settings.VERSION)
    print(settings.DEFAULT_LANGUAGE)
    print("=" * 40)


if __name__ == "__main__":
    main()