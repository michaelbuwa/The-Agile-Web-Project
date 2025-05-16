# Colour Mania
A colour differentiation application that tests you on your eyes' ability and mental subconscious to see and memorise specific colours and return you analytics of your results! You can also share these results with other users on our platform.

## Design and Usage
### Sign-In / Application's Context Page
A home page for new and returning users holding both Colour Mania's description and a login-in form. A link for new users sends them to a simpler styled page for registration.

### Colour Match Test / Upload Page
Users can choose to start a round of colour matching. They're first prompted with instructions of the game's functionality as follows:
1. Once you interact with the start button you will be presented with a colour. Remember this colour for 10s, then a black screen will come down and stay for 5 seconds.
2. After that grace period you are presented with 3 colour options. Select the colour that you saw. If you selected the right colour the container's border will go green. If not, it will be red and it will reveal what the correct colour was.
3. Choose to either play again or go to view your results.

### Colour Matching Results / Visualise Page
On the left side of the page, it will tell you how many colours you've correctly matched as well as a graph holding all the correctly matched colour's values represented in a 3D space. This introduces a gamified approach to inspire users to see how many colours they can unlock. Then on the right hand side for any incorrect matches the user made they can see as swatches. If they select a swatch they can see a gradient illustrating the difference between the correct colour and the one they incorrectly selected as well as the calculated Euclidean distance between the two.

### Share With Friends Page
Users can selectively choose to share their results with other users and view friend's results if shared to.

---
|UWA ID|Name|Github Username|
|-------------|----|---------------|
|23971718     |Michael Baker| michaelbuwa |
|23996869     |Alisa Rose|Shinetopia|
|23401613     |Suha Shahid |anonss78|
|23792503     |Max Macey|MaxMacey|

## How to Launch Our Application
The following is expected to run in a Linux system and has been tested with Ubuntu-20.04 (WSL).
```
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
```
Make sure you're in the project's root directory and make a new virtual environment
```
$ python3 -m venv venv
```
Activate the new environment and install any requirements:
```
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```
Set the environment variable
```
(venv) $ export FLASK_APP=colour_mania.py
```
Finally, run our application!
```
(venv) $ flask run
```
## How to Run Tests
```
python -m unittest app.tests.unit-tests
```

## Acknowledgements
AI tools ChatGPT and GitHub Copilot were used for assistance in suggesting model designs, routing and JS logic for DOM Manipulation (OpenAI, 2025).
