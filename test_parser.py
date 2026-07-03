from app.nlp.command_parser import CommandParser

parser = CommandParser()

tests = [

    "open calculator",

    "open github",

    "open resume",

    "play believer",

    "search binary search",

    "take screenshot",

    "exit",

    "explain dbms"

]

for text in tests:

    command = parser.parse(text)

    print("=" * 50)

    print("Input :", text)

    print("Intent:", command.intent.value)

    print("Entity:", command.entity)