PROJECT DESCRIPTION
My project is a computerized version of the ancient board game Go. In the game, players alternate placing down black and white stones, and aim to
capture as much territory as possible. 

-------------------------------------------------------------------------------------------------------------------------------------------------------
INSTALLATION AND RUN INSTRUCTIONS
First, install python 3 on your computer. Follow the instructions at: https://www.python.org/downloads/

Then, you must have pygame installed. To do so, you just need to go to your command prompt (Windows) or command line (Mac) and type 
"pip install pygame", and hit enter. If you have python, the system should install pygame for you at this point.

Next, you need to download this directory "tp2" and all of the files inside of it. Save it somewhere in which it ca be easily accessed.

Then, open your command prompt/line again. If you are looking to play locally, type "python goLocal.py" and hit enter. At this point, the game will run and
you can play locally.

Alternatively, if you are looking to play with two computers, make sure that the other computer has pygame and this directory downloaded also. Then, open
the goServer.py and goClient.py in a python text editor. Look up your IP address by Googling "My IP", and copy it. Paste your IP address into goServer.py's
line 8 (for example, HOST = "123.456.789.12") and into goClient.py's line 290 (for example, HOST = "123.456.789.12"). The other person should do the same
in his goClient.py line 290 but not in his goServer.py file. 

Next, open your command prompt/line. Change the path variable to the directory in which you stored the project (the other person should do this also).
Type "python goServer.py" and hit enter. Make sure that the person operating the other computer DOES NOT do this. Then, both you and the other person 
should open up another command prompt/line and type "python goClient.py" and hit enter. When both players click "PLAY" on the start screen, the game is ready
to start.