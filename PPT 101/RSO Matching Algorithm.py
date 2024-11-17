import difflib

# Function to get the list of RSOs from line-separated input
def get_rso_list():
    print("Please enter the list of RSOs (one per line), followed by an empty line when finished:")
    rso_list = []
    while True:
        line = input()
        if line.strip() == "":
            break
        rso_list.append(line.strip())
    return rso_list

# Function to get Senator names from line-separated input
def get_senator_names():
    print("Please enter the names of the Senators (one per line), followed by an empty line when finished:")
    senator_names = []
    while True:
        line = input()
        if line.strip() == "":
            break
        senator_names.append(line.strip())
    return senator_names

# Function to suggest the closest RSO name if there's a typo
def suggest_rso_name(input_rso, valid_rsos):
    suggestion = difflib.get_close_matches(input_rso, valid_rsos, n=1)
    return suggestion[0] if suggestion else None

# Function to get preferences for each Senator, as a comma-separated list
def get_senator_preferences(senator_names, rsos):
    preferences = {}
    for senator in senator_names:
        while True:
            rso_preferences = input(f"Please enter the 8 RSO preferences for {senator} (comma-separated, no spaces): ")
            rso_preferences_list = rso_preferences.split(",")
            
            if len(rso_preferences_list) != 8:
                print("Error: You must enter exactly 8 RSOs.")
                continue  # Ask again if there are not exactly 8 entries

            invalid_rso = None
            for rso in rso_preferences_list:
                if rso not in rsos:
                    invalid_rso = rso
                    break  # Stop checking once we find an invalid RSO
            
            if invalid_rso:
                suggestion = suggest_rso_name(invalid_rso, rsos)
                if suggestion:
                    print(f"Error: '{invalid_rso}' is not a valid RSO. Did you mean '{suggestion}'?")
                else:
                    print(f"Error: '{invalid_rso}' is not a valid RSO.")
                continue  # Ask again if there's an invalid RSO
            else:
                preferences[senator] = rso_preferences_list
                break  # Exit the loop once all preferences are valid
    return preferences

# Function to assign RSOs based on preferences
def assign_rso_to_senators(rsos, preferences):
    assigned_rsos = {}  # To track which RSO has been assigned and to whom
    senator_rso_responsibility = {senator: [] for senator in preferences}  # To track what RSOs each senator is responsible for
    
    # Loop over preferences, prioritize top picks
    for i in range(8):  # Each Senator has 8 choices
        for senator, rso_list in preferences.items():
            if i < len(rso_list):
                preferred_rso = rso_list[i]
                if preferred_rso not in assigned_rsos:  # If RSO hasn't been assigned yet
                    assigned_rsos[preferred_rso] = senator  # Assign this RSO to the senator
                    senator_rso_responsibility[senator].append(preferred_rso)
    
    return senator_rso_responsibility

# Function to print the assigned RSOs and their corresponding Senators
def print_senator_responsibilities(assignments):
    print("Senator Responsibilities for RSOs:")
    for senator, rso_list in assignments.items():
        print(f"{senator} is responsible for:")
        for rso in rso_list:
            print(f"  - {rso}")
        print()

# Main function
def main():
    # Get RSO list
    rsos = get_rso_list()
    
    # Get Senator names
    senator_names = get_senator_names()
    
    # Get preferences for each Senator
    senator_preferences = get_senator_preferences(senator_names, rsos)
    
    # Assign RSOs to Senators
    assignments = assign_rso_to_senators(rsos, senator_preferences)
    
    # Print the final assignments
    print_senator_responsibilities(assignments)

# Execute the main function
main()
