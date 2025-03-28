import random

def generate_human_message():
    # Build a fake human-sounding message using simple slang pieces
    openings = ["yo", "hey", "what's good", "sup", "quick msg", "lol"]
    bodies = [
        "streakkk",
        "keeping it alive",
        "forgot to reply lol",
        "don’t ghost me",
        "yo just checking in",
        "u up?",
        "i’m so bad at replying haha"
    ]
    closers = ["", "", "fr tho", "be safe"]

    msg = f"{random.choice(openings)} {random.choice(bodies)} {random.choice(closers)}".strip()

    # Remove emojis and weird characters that crash ChromeDriver
    return ''.join(c for c in msg if ord(c) <= 0xFFFF)
