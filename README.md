# Reddit bot

This repository contains code for two different reddit bots.

The bot under the `simplebot` directory is the bot that was created for the [JakeEh YouTube video](https://www.youtube.com/watch?v=rnPDtVwBB3c) and is the exact code that Jake used in the video.

The bot under the `advancedbot` directory is the bot that Jake showed off slightly in the video mentioned above.

To use either of these, you should do the following:

1. Clone the repository
2. Ensure that PRAW is installed using `pip install praw`.
3. Create a `praw.ini` file under whichever bot you would like to use
	* See [here](https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html#format-of-praw-ini) for more information on configuring the `praw.ini` file
4. Configure your bot
	* `simplebot` - this is just done in the only file: `funbot.py`
	* `advancedbot` - this is done within the `run.py` file when you initialize the `Bot` class
5.  Run the bot
	* `simplebot` - `py funbot.py`
	* `advancedbot` - `py run.py`
 
If you have any questions, feel free to reach out on YouTube!

Made with love!
