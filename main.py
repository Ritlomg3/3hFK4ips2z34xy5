import requests
import time

# Replace with your Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1347399326737104906/TfUc3CukEgfAg7UCtrlsivcwtfmes30VOmCuD0TXzxLie4z1vzQmtF5VCHRp6MJCGhrd"

# File containing usernames (one per line)
USERNAMES_FILE = "usernames.txt"

def send_discord_notification(username, api_message):
    """Send a notification to Discord using a webhook."""
    data = {
        "content": f"@everyone **{username}** has been cached as an unblock\n\n{api_message}"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print(f"Notification sent for username: {username}")
    else:
        print(f"Failed to send notification for username: {username}")

def check_username(username):
    """Check if a username is valid using the Roblox API."""
    url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Check if the username is valid (code 0 means valid)
        if data.get("code") == 0:
            return True, data
    return False, None

def load_usernames():
    """Load usernames from the file."""
    try:
        with open(USERNAMES_FILE, "r") as file:
            usernames = [line.strip() for line in file.readlines() if line.strip()]
        return usernames
    except FileNotFoundError:
        print(f"Error: The file '{USERNAMES_FILE}' was not found.")
        return []

def main():
    while True:
        # Load usernames from the file in each loop
        usernames = load_usernames()
        if not usernames:
            print("No usernames to check. Exiting.")
            return

        for username in usernames:
            is_valid, api_message = check_username(username)
            status = "valid" if is_valid else "taken"
            print(f"{username} - {status}")

            if is_valid:
                print(f"Valid username found: {username}")
                send_discord_notification(username, api_message)

            # Delay for 1 second between each username check
            time.sleep(1)

        # Wait 3 seconds after finishing a loop
        print("Finished checking all usernames. Waiting 3 seconds before the next loop...")
        time.sleep(3)

if __name__ == "__main__":
    main()
