# discord-bot

<!-- Add banner here -->

<!-- Describe your project in brief -->
I'm Barista - a discord bot who assigns roles based on emoji reactions in discord.  
  
  I am written in python using the [Discord.py](https://github.com/Rapptz/discord.py) framework.

# Table of contents

<!-- After you have introduced your project, it is a good idea to add a **Table of contents** or **TOC** as **cool** people say it. This would make it easier for people to navigate through your README and find exactly what they are looking for.

Here is a sample TOC that is actually the TOC for this README. -->

- [Project Title](#project-title)
- [Table of contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [License](#license)

# Installation
[(Back to top)](#table-of-contents)

First clone the repo on your device using the command below:

```  
git clone git@github.com:nyccodecoffee/discord-bot.git
```

Before running the bot you will need to install all the requirements with this command:

```
pip install -r requirements.txt
```
Create a bot on and copy the `DISCORD_TOKEN` and export it as a variable.
If discord bots are new to you I recommend this [video](https://youtu.be/nW8c7vT6Hl4) to set it up. If you are familiar with discord bots or you own one you can skip this part.
```
export BARISTA_TOKEN=<INSERT THE BOTS DISCORD TOKEN>
```

# Usage
[(Back to top)](#table-of-contents)

To start the bot you simply need to launch, either your terminal (Linux, Mac & Windows), or your Command Prompt (
Windows).


```
python main.py
```

# Deployment
[(Back to top)](#table-of-contents)

You can deploy this project for free on [Railway.app](https://railway.app/)

1. Create a new project and select `deploy from GitHub repo`
    give railway.app access to your newly created GitHub repo.
2. Go to the variables tab and add the [above mentioned](#Installation) variable.
3. Set the `start command` to be `python main.py`.

Barista bot will now be running all the time.


# License
[(Back to top)](#table-of-contents)

[MIT License](https://mit-license.org/)
