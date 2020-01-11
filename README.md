# **Honey**
![honey](resources/images/HoneyLogo.png)

*Voice Activated Discord Bot*
___


**Installing Dependencies:**
---/home/dirk/workspace/JamesDirkBell/resources/images/HoneyLogo.png

To use Honey, please ensure you have done the following:

1. *Verify correct Python version:*
	* Python version 3.5.3+ required

2. *create & activate a virtual-environment:*

			`python3 -m venv honey-bot`
			`source honey-bot/bin/activate`

3. *Install requirements via the requirements file:*
	
			`pip3 install -r requirements.txt`

4. *Installed the following:*
	* libffi
	* libnacl
	* python3-dev
	* libopus

	On Ubuntu, these can be obtained by running the following:

		`apt install libffi-dev libnacl-dev python3-dev libopus0`

5. *Installed a Language Model:*
	
	* From the root directory, navigate to /honey/voice/
	* Run the following 2 commands:

		`curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.6.0/deepspeech-0.6.0-models.tar.gz`
		
		`tar xvf deepspeech-0.6.0-models.tar.gz`

5. *Setup Bot-token and Google STT key:*

	* Verify that your Google speech-to-text certification is valid...

			`export GOOGLE_APPLICATION_CREDENTIALS="path to json cert"`
	
	* Create a .env file for your bot-token...
			
			`emacs .env`
			
			Paste the following:

			# .env
			DISCORD_TOKEN="your bots token"