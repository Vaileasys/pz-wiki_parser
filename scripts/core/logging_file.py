import os

is_first_log = True


# Initialise log file erasing existing contents
def init_log_file(file_name="log.txt"):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    with open(file_name, 'w') as file:
        file.write("")


# Used to log important info to a log file
def log_to_file(message, print_bool="False", file_name="log.txt"):
    global is_first_log
    file_name = "output/logging/" + file_name

    # If this is the first log, initialise the log file
    if is_first_log:
        init_log_file(file_name)
        is_first_log = False

    if print_bool is True:
        print(message)

    with open(file_name, 'a') as file:
        file.write(f"{message}\n")