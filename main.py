import time
import json
import os
import pyautogui
import random

# Change this to your preferred log file location

play = None  # Global variable to store the parsed JSON response
json_file_path = "play_data.json"

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




# Initial placeholder hands (to simulate responses)
hands = {
    "dealer": None,
    "player1": None,
    "player2": None,
    "player3": None
}

def process_hand_response(data):
    """ Processes a single hand and determines the best move. """
    action = None
    dealer_value = data["spin"]["dealer"]["total_value"]
    hard_value = None
    soft_value = None
    can_double = None
    can_split = None
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
    return action


def hit():
    human_like_mouse_move(850,930)
    human_like_click()

def stand():
    human_like_mouse_move(1300,930)
    human_like_click()

def double():
    human_like_mouse_move(1000,930)
    human_like_click()

def split():
    human_like_mouse_move(1150,930)
    human_like_click()

def reset():
    #START
    human_like_mouse_move(1150, 930)
    human_like_click()


    # PICK UP MONEY
    human_like_mouse_move(1700, 930)
    human_like_click()
    # DROP MONEY
    human_like_mouse_move(1375, 700)
    human_like_click()

    # DROP MONEY
    human_like_mouse_move(1075, 700)
    human_like_click()

    # DROP MONEY
    human_like_mouse_move(750, 700)
    human_like_click()

    #DEAL
    human_like_mouse_move(1100, 930)
    human_like_click()


def human_like_mouse_move(x, y):
    """Move the mouse to a target (x, y) position with random variations."""
    # Current mouse position
    start_x, start_y = pyautogui.position()

    # Random offset to simulate imprecision
    offset_x = random.randint(-10, 10)
    offset_y = random.randint(-10, 10)

    duration = random.uniform(1.0,2.0)

    # Move with a slight curve or random path
    steps = random.randint(5, 15)  # Number of steps for the movement
    for i in range(steps):
        # Interpolate the position
        new_x = start_x + (x - start_x) * (i / steps) + offset_x * (1 - i / steps)
        new_y = start_y + (y - start_y) * (i / steps) + offset_y * (1 - i / steps)

        # Move to the intermediate point
        pyautogui.moveTo(new_x, new_y, duration=random.uniform(0.05, 0.1))

    # Final precise move to the target
    pyautogui.moveTo(x, y, duration=random.uniform(0.1, 0.3))

def human_like_click():
    """Simulate a human-like mouse click."""
    # Simulate a slight delay before and after the click
    time.sleep(random.uniform(0.2, 0.5))
    pyautogui.click()
    time.sleep(random.uniform(0.1, 0.3))




# Function to read and process the JSON file
def read_and_process_json():
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
            move = process_hand_response(data)
            print(move)
            time.sleep(random.uniform(4,5.5))
            if move == "hit":
                hit()
            elif move == "stand":
                stand()
            elif move == "double":
                double()
            elif move == "split":
                split()
            else:
                reset()
            # Add your processing logic here
    except FileNotFoundError:
        print("The file play_data.json was not found.")
    except json.JSONDecodeError:
        print("Error: The file does not contain valid JSON.")


def main():
    """Wait for the JSON file to update after startup and process it once."""
    clear_json_file()  # Clear the file at startup

    # Get the modification time when the program starts
    try:
        initial_modified_time = os.path.getmtime(json_file_path)
    except FileNotFoundError:
        initial_modified_time = None

    while True:
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


if __name__ == "__main__":
    main()
