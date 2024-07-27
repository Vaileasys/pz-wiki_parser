is_first_log = True


# Initialise log file erasing existing contents
def init_log_file(filename="log.txt"):
    with open(filename, 'w') as file:
        file.write("")


# Used to log important info to a log file
def log_to_file(message, filename="log.txt"):
    filename = "logging/" + filename
    global is_first_log
    if is_first_log:
        init_log_file(filename)
        is_first_log = False
    with open(filename, 'a') as file:
        file.write(f"{message}\n")