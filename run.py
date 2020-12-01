#!flask/bin/python
from app import app

print("")
print("______      _                     _                    ")
print("| ___ \    | |                   (_)                   ")
print("| |_/ /___ | |__   ___  ___ _ __  _  ___ _ __ _ __ ___ ")
print("|    // _ \| '_ \ / _ \/ __| '_ \| |/ _ \ '__| '__/ _ \\")
print("| |\ \ (_) | |_) |  __/\__ \ |_) | |  __/ |  | | |  __/")
print("\_| \_\___/|_.__/ \___||___/ .__/|_|\___|_|  |_|  \___|")
print("                           | |                         ")
print("                           |_|                         ")
print("")

#app.run(debug=False)

#When Ended
from waitress import serve
serve(app, host="127.0.0.1", port=5000)
