import random

modes = {
    "general": {
        "subjects": [
            "Shahrukh Khan",
            "Virat Kohli",
            "Nirmala Sitharaman",
            "A Mumbai Cat",
            "A Group Of Monkeys",
            "Prime Minister Modi",
            "An Auto Rickshaw Driver from Delhi"
        ],

        "actions": {
            "launches": {
                "type": "objects",
                "items": [
                    "a giant samosa",
                    "a chai startup",
                    "a dance reality show"
                ]
            },

            "cancels": {
                "type": "events",
                "items": [
                    "an IPL afterparty",
                    "a political rally",
                    "a concert in Mumbai"
                ]
            },

            "dances with": {
                "type": "places",
                "items": [
                    "at India Gate",
                    "at Red Fort",
                    "during IPL Match"
                ]
            },

            "eats": {
                "type": "objects",
                "items": [
                    "47 pani puris",
                    "a plate of Samosa",
                    "an entire wedding cake"
                ]
            },

            "declares war on": {
                "type": "objects",
                "items": [
                    "slow internet",
                    "mosquitoes in Delhi",
                    "fake motivational reels"
                ]
            },

            "orders": {
                "type": "objects",
                "items": [
                    "500 cups of chai",
                    "a truck full of laddoos",
                    "100 pizzas"
                ]
            },

            "celebrates": {
                "type": "places",
                "items": [
                    "inside Parliament",
                    "at Ganga Ghat",
                    "during IPL Match"
                ]
            }
        }
    },

    "sports": {
        "subjects": [
            "Virat Kohli",
            "Rohit Sharma",
            "A Furious Cricket Fan"
        ],

        "actions": {
            "celebrates": {
                "type": "places",
                "items": [
                    "inside Wankhede Stadium",
                    "during IPL Match"
                ]
            },

            "orders": {
                "type": "objects",
                "items": [
                    "200 cricket bats",
                    "50 protein shakes"
                ]
            },

            "declares war on": {
                "type": "objects",
                "items": [
                    "bad umpiring decisions",
                    "rain interruptions"
                ]
            }
        }
    },

    "political": {
        "subjects": [
            "Prime Minister Modi",
            "Nirmala Sitharaman",
            "A Confused MLA"
        ],

        "actions": {
            "launches": {
                "type": "objects",
                "items": [
                    "a new tax policy",
                    "a digital chai scheme"
                ]
            },

            "cancels": {
                "type": "events",
                "items": [
                    "a parliament meeting",
                    "a press conference"
                ]
            },

            "celebrates": {
                "type": "places",
                "items": [
                    "inside Parliament",
                    "at India Gate"
                ]
            }
        }
    },

    "chaotic": {
        "subjects": [
            "A Flying Cow",
            "A Group Of Monkeys",
            "A Time Traveling Auto Driver"
        ],

        "actions": {
            "launches": {
                "type": "objects",
                "items": [
                    "a banana-powered rocket",
                    "a UFO startup"
                ]
            },

            "eats": {
                "type": "objects",
                "items": [
                    "300 samosas in one minute",
                    "an entire truck of noodles"
                ]
            },

            "declares war on": {
                "type": "objects",
                "items": [
                    "traffic lights",
                    "WiFi routers"
                ]
            },

            "dances with": {
                "type": "places",
                "items": [
                    "on top of India Gate",
                    "during a blackout"
                ]
            }
        }
    }
}

templates = [
    "BREAKING NEWS: {subject} {action} {target}!",
    "SHOCKING: {subject} suddenly {action} {target}!",
    "EXCLUSIVE: {subject} reportedly {action} {target}!",
    "VIRAL: {subject} spotted {action} {target}!",
    "JUST IN: {subject} officially {action} {target}!"
]

last_headline = ""

print("AVAILABLE MODES: GENERAL | SPORTS | POLITICAL | CHAOTIC")

mode = input("SELECT MODE: ").strip().lower()

if mode not in modes:
    mode = "general"

custom_subject = input("ENTER CUSTOM SUBJECT (OPTIONAL): ").strip()
custom_target = input("ENTER CUSTOM TARGET (OPTIONAL): ").strip()

current_mode = modes[mode]
subjects = current_mode["subjects"][:]
if custom_subject:
    subjects.append(custom_subject)

while True:
    subject = random.choice(subjects)

    action = random.choice(list(current_mode["actions"].keys()))

    action_data = current_mode["actions"][action]

    targets = action_data["items"][:]

    if custom_target:
        targets.append(custom_target)

    target = random.choice(targets)

    headline = random.choice(templates).format(
        subject=subject,
        action=action,
        target=target
    )

    while headline == last_headline:
        headline = random.choice(templates).format(
            subject=subject,
            action=action,
            target=target
        )

    last_headline = headline

    print("\n" + headline)

    user_input = input(
        "\nDO YOU WANT ANOTHER HEADLINE? (YES/NO): "
    ).strip().lower()

    if user_input == "no":
        break

    if user_input not in ["yes", "no"]:
        print("INVALID INPUT. GENERATING ANOTHER HEADLINE...")

print("\nTHANKS FOR USING THE FAKE NEWS GENERATOR. HAVE A FUN DAY!")
