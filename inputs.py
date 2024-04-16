import subprocess
import time

# List of commands to input
commands = [
    "A",
    "w",
    "n",
    "Y",
    "w",
    "ne",
    "A",
    "n",
    "w",
    "Y",
    "e",
    "nw",
    "A",
    "w",
    "w",
    "Y",
    "w",
    "n",
    "A",
    "w",
    "se",
    "yesn't",
    "A",
    "w",
    "n",
    "Y",
    "w",
    "ne",
    "A",
    "n",
    "w",
    "Y",
    "e",
    "nw",
    "A",
    "w",
    "w",
    "Y",
    "w",
    "n",
    "A",
    "w",
    "se",
]

# Start cli.py as a subprocess
process = subprocess.Popen(['python', 'cli.py'], stdin=subprocess.PIPE, text=True)

# Function to send a command to the CLI
def send_command(cmd):
    process.stdin.write(cmd + '\n')
    process.stdin.flush()  # Ensure the command is sent

# Send each command to the CLI, with a delay

for command in commands:
    send_command(command)
    time.sleep(0.05)  # Delay between commands to simulate typing

# Close the subprocess's stdin to indicate that no more input will be sent
process.stdin.close()

# Wait for the subprocess to finish
process.wait()
