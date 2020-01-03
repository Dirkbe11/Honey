# **Honey**
![honey](resources/images/HoneyLogo.png)

*Voice Activated Discord Bot*
___


**Installing Dependencies:**
---/home/dirk/workspace/JamesDirkBell/resources/images/HoneyLogo.png

To use Honey, please ensure you have done the following:

1. *Installed Python*
	* Python version 3.5.3+ required

2. *Activate the virtual environment*


	* 1.) Honey has a python virtual-environment that allows for easy dependency handling. To use, simple navigate to Honey's root directory and run:

			`source bot-env/bin/activate`
	

3. *Installed the following:*
	* libffi
	* libnacl
	* python3-dev
	* libopus

	On Ubuntu, these can be obtained by running the following:

		`apt install libffi-dev libnacl-dev python3-dev libopus0`

4. *Installed a Language Model:*
	
	* From the root directory, navigate to /honey/voice/
	* Run the following 2 commands:

		`curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.6.0/deepspeech-0.6.0-models.tar.gz`
		
		`tar xvf deepspeech-0.6.0-models.tar.gz`

