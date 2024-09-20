from datetime import datetime
import os

# File path
file = "userData/toDoList.txt"

# Function to create a new to-do list with the current date
def createList():
    with open(file, "w") as f:
        present = datetime.now()
        dt_format = present.strftime("Date: %d/%m/%Y Time: %H:%M:%S\n")
        f.write(dt_format)

# Function to add items to the to-do list
def toDoList(text):
    if not os.path.isfile(file):
        createList()

    with open(file, "r") as f:
        x = f.read(8)  # Reading the first 8 characters which contain the date in format "Date: XX"
        
    if len(x) < 8 or not x.startswith("Date: "):  # Checking if file has valid date information
        createList()  # If not, recreate the file with the current date
        return toDoList(text)  # Recursively call to add the item after creating the list

    y = x[6:]  # Extracting the day part of the date
    try:
        yesterday = int(y)
    except ValueError:
        createList()  # If the day extraction fails, recreate the list
        yesterday = datetime.now().day  # Fallback to current day

    present = datetime.now()
    today = present.day

    if (today - yesterday) >= 1:
        createList()

    with open(file, "a") as f:
        dt_format = present.strftime("%H:%M")
        f.write(f"[{dt_format}] : {text}\n")

# Function to show the current to-do list
def showtoDoList():
    if not os.path.isfile(file):
        return ["It looks like that list is empty"]

    with open(file, 'r') as f:
        items = f.readlines()

    if len(items) <= 1:
        return ["It looks like that list is empty"]

    speakList = [f"You have {len(items) - 1} items in your list:\n"]
    for item in items[1:]:
        speakList.append(item.strip().capitalize())

    return speakList
