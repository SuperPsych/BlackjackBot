import time
import json
import os
import pyautogui
import random
from humancursor import SystemCursor
from numpy.ma.core import absolute

# Change this to your preferred log file location
cursor = SystemCursor()
play = None  # Global variable to store the parsed JSON response
json_file_path = "play_data.json"
limit = 0.5

dealing = False

def clear_json_file():
    with open(json_file_path, "w") as json_file:
        json.dump({}, json_file)  # Empty JSON object (or use [] for an empty list)
    print("JSON file cleared.")


def optimal_blackjack_action(dealer_value, hard_value, soft_value, can_double, can_split):
    """
    Determines the optimal Blackjack action.

    Args:
    - dealer_value (int): Dealer's upcard value (2 to 11, where 11 is Ace).
    - hard_value (int): Player's hard hand value (Ace counted as 1).
    - soft_value (int): Player's soft hand value (Ace counted as 11, or 0 if no soft hand).
    - can_double (bool): Whether the player can double down.
    - can_split (bool): Whether the player can split pairs.

    Returns:
    - str: One of "hit", "stand", "double", or "split".
    """

    # --- 1. Handle Splitting ---
    if can_split:
        # Define optimal splitting strategy based on dealer upcard
        split_rules = {
            11: "split",  # Always split Aces
            8: "split",   # Always split 8s
            10: "stand",  # Never split 10s (e.g., 10 + 10)
            9: "split" if dealer_value not in [7, 10, 11] else "stand",
            7: "split" if dealer_value <= 7 else "hit",
            6: "split" if dealer_value <= 6 else "hit",
            5: "double",  # Treat pair of 5s like a hard 10
            4: "split" if dealer_value in [5, 6] else "hit",
            3: "split" if dealer_value <= 7 else "hit",
            2: "split" if dealer_value <= 7 else "hit"
        }

        pair_value = hard_value // 2  # Pair value, assuming player has a pair (e.g., 8 + 8 = 16)
        if pair_value in split_rules:
            return split_rules[pair_value]

    # --- 2. Handle Soft Hands ---
    if soft_value > 0:
        # Soft hand strategy (Ace counted as 11)
        if soft_value >= 19:
            return "stand"
        elif soft_value == 18:
            if 2 <= dealer_value <= 6:
                return "double" if can_double else "stand"
            elif dealer_value in [9, 10, 11]:
                return "hit"
            else:
                return "stand"
        else:  # Soft 13 to Soft 17
            return "double" if 3 <= dealer_value <= 6 and can_double else "hit"

    # --- 3. Handle Hard Hands ---
    if hard_value >= 17:
        return "stand"
    elif hard_value >= 13 and dealer_value <= 6:
        return "stand"
    elif hard_value == 12:
        if 4 <= dealer_value <= 6:
            return "stand"
        else:
            return "hit"
    elif hard_value == 11:
        return "double" if can_double else "hit"
    elif hard_value == 10:
        return "double" if dealer_value <= 9 and can_double else "hit"
    elif hard_value == 9:
        return "double" if 3 <= dealer_value <= 6 and can_double else "hit"
    else:
        return "hit"




def process_hand_response(data):
    """ Processes a single hand and determines the best move. """
    if "EVENMONEY" in data["spin"]["steps"].values():
        time.sleep(random.uniform(4, 5.5))
        reject_even_money()
        return
    if "INSURE" in data["spin"]["steps"].values():
        time.sleep(random.uniform(4, 5.5))
        reject_all()
        return
    global spent
    global earned
    global dealing
    action = None
    dealer_value = data["spin"]["dealer"]["total_value"]
    hands = data["spin"]["hands"]
    for i in ["0","1","2"]:
        if i in hands:
            if type(hands[i]["split"]) != int and hands[i]["split"]["active"]:
                hard_value = hands[i]["split"]["hard_value"]
                soft_value = hard_value
                if hard_value == hands[i]["split"]["soft_value"]:
                    soft_value = 0
                can_double = "DOUBLE" in data["spin"]["steps"].values()
                can_split = "SPLIT" in data["spin"]["steps"].values()
                action = optimal_blackjack_action(dealer_value, hard_value, soft_value, can_double, can_split)
                break
            elif hands[i]["active"]:
                hard_value = hands[i]["hard_value"]
                soft_value = hard_value
                if hard_value == hands[i]["soft_value"]:
                    soft_value = 0
                can_double = "DOUBLE" in data["spin"]["steps"].values()
                can_split = "SPLIT" in data["spin"]["steps"].values()
                action = optimal_blackjack_action(dealer_value, hard_value, soft_value, can_double, can_split)
                break
    if dealing:
        time.sleep(random.uniform(4, 5.5))
    else:
        time.sleep(random.uniform(1, 2))
    dealing = False
    if action == "hit":
        hit()
    elif action == "stand":
        stand()
    elif action == "double":
        double()
    elif action == "split":
        split()
    else:
        time.sleep(random.uniform(0.5, 1))
        spent += data["spin"]["total_bet"]
        earned += data["spin"]["total_win"]
        print("Spent:", spent)
        print("Earned:", earned)
        print()
        reset()


def hit():
    human_action(875,930)

def stand():
    human_action(1300,930)

def double():
    human_action(1000,930)

def split():
    human_action(1150,930)

def reject_all():
    human_action(1300, 930)

def reject_even_money():
    human_action(1150, 930)

def reset():
    global dealing

    if spent >= limit:
        return

    #RESTART
    human_action(1000, 930)

    dealing = True
    #START
    #human_action(1150, 930)

    # PICK UP MONEY
    #human_action(1700, 930)

    # DROP MONEY
    #human_action(1375, 700)

    # DROP MONEY
    #human_action(1075, 700)

    # DROP MONEY
    #human_action(775, 700)

    #DEAL
    #human_action(1100, 930)

def human_action(x,y):
    human_like_mouse_move(x, y)
    human_like_click()

def human_like_mouse_move(x, y):
    cursor.move_to([x,y])

def human_like_click():
    """Simulate a human-like mouse click."""
    # Simulate a slight delay before and after the click
    time.sleep(random.uniform(0.2, 0.5))
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.2, 0.5))
    pyautogui.mouseUp()




# Function to read and process the JSON file
def read_and_process_json():
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
            process_hand_response(data)
            # Add your processing logic here
    except FileNotFoundError:
        print("The file play_data.json was not found.")
    except json.JSONDecodeError:
        print("Error: The file does not contain valid JSON.")

spent = 0
earned = 0

def main():
    """Wait for the JSON file to update after startup and process it once."""

    clear_json_file()  # Clear the file at startup

    # Get the modification time when the program starts
    try:
        initial_modified_time = os.path.getmtime(json_file_path)
    except FileNotFoundError:
        initial_modified_time = None

    while spent<limit:
        try:
            # Get the current modification time of the file
            current_modified_time = os.path.getmtime(json_file_path)

            # If the file is updated after startup, process it once and exit
            if initial_modified_time is None or current_modified_time > initial_modified_time:
                read_and_process_json()
                initial_modified_time = current_modified_time


        except FileNotFoundError:
            print("Waiting for the JSON file to be created...")

        # Sleep to prevent high CPU usage
        time.sleep(0.5)

if __name__ == "__main__":
    main()


