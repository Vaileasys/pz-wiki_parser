import os

is_first_log = True


# Initialise log file erasing existing contents
def init_log_file(filename="log.txt"):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Open the file for writing (this will erase existing contents)
    with open(filename, 'w') as file:
        file.write("")


# Used to log important info to a log file
def log_to_file(message, filename="log.txt"):
    global is_first_log
    filename = "logging/" + filename  # Prepend the logging directory path

    # If this is the first log, initialize the log file
    if is_first_log:
        init_log_file(filename)
        is_first_log = False

    # Append the message to the log file
    with open(filename, 'a') as file:
        file.write(f"{message}\n")
