import logging
import os


#If the logs folder does not exist,create it first.
os.makedirs("logs", exist_ok=True)

#Create logger instance - can be identified by name
logger = logging.getLogger("travel_deal_app")
logger.setLevel(logging.DEBUG) #  captures all log levels(DEBUG,INFO,WARNING,ERROR)

# ------------ Format ----------------
# Format of logs time,level,message

formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ----------- Console Handler -------------
# Display logs in the terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)


# ----------- File Handler ----------------
# Logs will be saved in the logs/app.log file

file_handler = logging.FileHandler("logs/app.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# ----------- Attach handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)