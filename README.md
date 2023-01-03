<!-- Describe your project in brief -->
# Barista-bot :robot:

Barista-bot is a Discord bot for the Code and Coffee Discord community. It guides new recruits through the onboarding process and makes it easy for them to join city-specific channels. For admins, Barista-bot automates the process of creating new city channels and sends notifications and reminders.

## Features

- Onboarding process for new recruits
- City-specific channels
- Automated creation of new city channels for admins
- Notifications and reminders

## Technologies Used

This project is written in Python using the [discord.py](https://github.com/Rapptz/discord.py) framework.

## Getting Started

### Prerequisites

- A Discord account and server
- Python 3.5.3 or higher
- [discord.py](https://github.com/Rapptz/discord.py)

### Installation

1. Clone the repository and navigate to the directory:

```bash
git clone https://github.com/CodeandCoffeeCommunity/Barista-bot.git
cd Barista-bot
```
### Install the dependencies:
```bash
pip install -r requirements.txt
```
Set up the bot by following the [Discord Developer Portal](https://discord.com/developers/docs/intro) guide.

Copy the bot's token and paste it in a file called .env in the root directory of the project.

### Run the bot:
```bash
python main.py
```

## Deployment

You can deploy this project for free on [Railway.app](https://railway.app/).

1. Create a new project and select `Deploy from GitHub repo`. Give Railway.app access to your newly created GitHub repo.
2. Go to the Variables tab and add the [above mentioned](#Installation) variable.
3. Set the `Start Command` to `python main.py`.

Barista bot will now be running all the time.

## Contributing

We welcome contributions to this project! If you have an idea for a new feature or have found a bug, please [open an issue](https://github.com/CodeandCoffeeCommunity/Barista-bot/issues). If you'd like to contribute code, please create a pull request.

## License

This project is licensed under the [MIT License](https://mit-license.org/) see the [LICENSE](LICENSE) file for details.



