# shuts off program, pulls from GitHub, the runs in the background and exits screen
pkill -f "python3 server.py"
git pull
screen -X detach python3 server.py
clear
echo "Flask server is now active!"