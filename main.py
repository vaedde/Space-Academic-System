import os
import time
import json
from dataclasses import dataclass, fields, asdict

# Define data classes

@dataclass
class Aspirant:
    code: int = 0
    name: str = ""
    cpf: str = ""

@dataclass
class Subject:
    code: int = 0
    name: str = ""
    description: str = ""

@dataclass
class Teacher:
    code: int = 0
    name: str = ""
    cpf: str = ""

@dataclass
class Class:
    code: int = 0
    teacher_code: int = 0
    subject_code: int = 0
    letter: str = ""
    team: str = ""

@dataclass
class Enrollment:
    code: int = 0
    class_code: int = 0
    aspirant_code: int = 0

# MAIN FUNCTIONS

# Starting point of the program
def start():
    try:
        while True:
            clear()
            slogan() # Display the slogan
            main_menu() # Display the main menu
            print()
            option = input("Select an option: ") # Prompt user for input

            # Navigate to different sections based on user input
            if option == "1":
                college_start()
            elif option == "2":
                config_start()
            elif option == "3":
                about_start()
            elif option == "9":
                break
            else: 
                valid_option()
    finally:
        clear()
        exit()
        print()
        print("Finishing Application...")

# COLLEGE FUNCTIONS

# Starting point of the program
def college_start():
    college_load()
    while True:
        clear()
        college_menu()
        option = input("Select an option: ")
        if option == "1":
            aspi_start()
        elif option == "2":
            subj_start()
        elif option == "3":
            teac_start()
        elif option == "4":
            clas_start()
        elif option == "5":
            cert_start()
        elif option == "9":
            break
        else: 
            valid_option()

# Function for managing aspirants
def aspi_start():
    while True:
        clear()
        aspi_menu()
        path_db="./db/aspirants.json"
        option = input("Select an option: ")
        if option == "1":
            add(Aspirant)
        elif option == "2":
            list(Aspirant)
        elif option == "3":
            edit(Aspirant)
        elif option == "4":
            delete(Aspirant)
        elif option == "9":
            break
        else: 
            valid_option()

# Function for managing subjects
def subj_start():
    while True:
        clear()
        subj_menu()
        option = input("Select an option: ")
        if option == "1":
            add(Subject)
        elif option == "2":
            list(Subject)
        elif option == "3":
            edit(Subject)
        elif option == "4":
            delete(Subject)
        elif option == "9":
            break
        else: 
            valid_option()

# Function for managing teachers
def teac_start():
    while True:
        clear()
        teac_menu()
        option = input("Select an option: ")
        if option == "1":
            add(Teacher)
        elif option == "2":
            list(Teacher)
        elif option == "3":
            edit(Teacher)
        elif option == "4":
            delete(Teacher)
        elif option == "9":
            break
        else: 
            valid_option()

# Function for managing classes
def clas_start():
    while True:
        clear()
        clas_menu()
        option = input("Select an option: ")
        if option == "1":
            add(Class)
        elif option == "2":
            list(Class)
        elif option == "3":
            edit(Class)
        elif option == "4":
            delete(Class)
        elif option == "9":
            break
        else: 
            valid_option()

# Function for managing enrollments
def cert_start():
    while True:
        clear()
        enro_menu()
        option = input("Select an option: ")
        if option == "1":
            add(Enrollment)
        elif option == "2":
            list(Enrollment)
        elif option == "3":
            edit(Enrollment)
        elif option == "4":
            delete(Enrollment)
        elif option == "9":
            break
        else: 
            valid_option()

# Add a new entity to the database
def add(clazz):
    print()
    name = str(clazz.__name__)
    print(f"Let's add a new {name}: ")

    objs = list_load(clazz)
    obj = clazz() # Create a new instance of the class

    code = len(objs)+1 # Generate a unique code for the new entity

    for field in fields(clazz):
        if field.name == "code":
            value = code
        else:
            value = input(f"{field.name.capitalize()}: ")
        setattr(obj, field.name, value)

    objs.append(obj) # Add the new entity to the list of entities

    json_objs = [asdict(obj) for obj in objs] # Convert entities to JSON format

    with open(f"./db/{str(clazz.__name__).lower()}.json", 'w') as f:
        json.dump(json_objs, f, indent=4) # Write JSON data to the file
        f.close()

    print(f"{name} added!")
    time.sleep(1.5)

# List entities from the database
def list(clazz):
    print()
    while True:
        print("______________________")
        print("|| 1. List All      ||")
        print("|| 2. Search        ||")
        print("|| 3. Edit          ||")
        print("||                  ||")
        print("|| 9. Return        ||")
        print("----------------------")
        print()
        option = input("Select an option: ")

        if option == "1":
            list_all(clazz)
        elif option == "2":
            list_search(clazz)
        elif option == "3":
            edit(clazz)
        elif option == "9":
            break
        else: 
            valid_option()

# Print a menu with fields of a class inside 
def fields_menu(clazz, hide_exit_option, hide_code_option):
    print("______________________")
    j = 0
    for i, field in enumerate(fields(clazz), start=1):
        if not hide_code_option and field.name == "code":
            j = -1
            continue
        print(f"|| {str(i+j)}. {field.name.capitalize().ljust(13)} ||")
    if not hide_exit_option:
        print("||                  ||")
        print("|| 9. Return        ||")
    print("----------------------")
    print()

# Print all objects inside a list 
def print_objs(objs):
    print()
    print("----------------------")
    for obj in objs:
        for field in fields(obj):
            print(f"{field.name.capitalize()}: {str(getattr(obj, field.name))}")
        print("----------------------")

# Load entities from the database
def list_load(clazz):
    objs = []
    with open(f"./db/{str(clazz.__name__).lower()}.json", 'r') as f:
        json_data = f.read()
        if json_data:
            json_objs = json.loads(json_data) # Deserialize JSON data
            objs = [clazz(**json_obj) for json_obj in json_objs] # Create instances of the class
        f.close()

    return objs

# List all entities from the database
def list_all(clazz):
    objs = list_load(clazz)
    if len(objs) <= 0:
        print()
        print(f"No {clazz.__name__} found!")
    else:
        print_objs(objs)

# Search for an entity in the database
def list_search(clazz):
    objs = list_load(clazz)
    while True:        
        fields_menu(clazz, True, True)

        option = input("Select an option: ")
        
        field_list = fields(clazz)

        if option != "0" and option <= str(len(field_list)):
            field = field_list[int(option)-1]
            value = input(f"Search a {field.name.capitalize()}: ")
            
            if field.type == str:
                objs_filter = [obj for obj in objs if value.lower() in str(getattr(obj, field.name)).lower()] # Filter entities
            else:
                objs_filter = [obj for obj in objs if value in getattr(obj, field.name)] # Filter entities
            
            if len(objs_filter) <= 0:
                print()
                print(f"No {clazz.__name__} found!")
            else:
                print_objs(objs_filter)
            break
        else: 
            valid_option()

# Edit an entity in the database
def edit(clazz):
    objs = list_load(clazz)
    print()

    code = int(input(f"{clazz.__name__} code: "))
    
    if len(objs) <= 0: # Check if there are no entities
        print()
        print(f"No {clazz.__name__} found!")
        time.sleep(1.5)
    else:
        for obj in objs:
            if getattr(obj, "code") == code:
                while True:
                    fields_menu(clazz, False, False)
                    
                    option = input("Select an option: ")
                    
                    if option == "9":
                        break                
                    elif option != "0" and option <= str(len(fields(clazz))-1):
                        field_name = fields(clazz)[int(option)].name # Get the name of the field
                        new_value = input(f"Enter new value for {field_name.capitalize()}: ")
                        
                        setattr(obj, field_name, new_value) # Set the value of the field
                        
                        json_objs = [asdict(obj) for obj in objs]

                        with open(f"./db/{str(clazz.__name__).lower()}.json", 'w') as f:
                            f.write("")
                            json.dump(json_objs, f, indent=4)
                            f.close()
                        
                        print(f"{clazz.__name__} updated successfully!")
                        time.sleep(1.5)
                    else:
                        valid_option()

# Delete an entity from the database
def delete(clazz):
    objs = list_load(clazz)
    print()

    code = int(input(f"{clazz.__name__} code: "))
    
    if len(objs) <= 0:
        print()
        print(f"No {clazz.__name__} found!")
        time.sleep(1.5)
    else:
        option = input("Do you really want to reset the database? (S/N): ")
        
        if option.upper() == "S": 
            for obj in objs:
                if getattr(obj, "code") == code:                        
                    objs.remove(obj) # Remove the entity from the list

            json_objs = [asdict(obj) for obj in objs]

            with open(f"./db/{str(clazz.__name__).lower()}.json", 'w') as f:
                f.write("")
                json.dump(json_objs, f, indent=4)
                f.close()
            
            print(f"{clazz.__name__} deleted successfully!")
            time.sleep(1.5)

# CONFIGURATION FUNCTIONS

# Start configuration management
def config_start():
    config_load()
    while True:
        clear()
        config_menu()
        option = input("Select an option: ")
        if option == "1":
            reset_db()
        elif option == "9":
            break
        else: 
            valid_option()

# Reset the database
def reset_db():
    while True:
        clear()
        option = input("Do you really want to reset the database? (S/N): ")
        if option.upper() == "S":
            path_db = "./db"

            json_files = [file for file in os.listdir(path_db) if file.endswith('.json')]

            for file in json_files:
                path_file = os.path.join(path_db, file)
                with open(path_file, 'w') as f:
                    f.write("")
                    f.close()

            print("Database reseted!")
            time.sleep(1.5)
            break
        elif option.upper() == "N":
            break
        else:
            valid_option()

# ABOUT FUNCTIONS

# Start about the program management
def about_start():
    about_load()
    while True:
        clear()
        about_menu()
        option = input("Select an option: ")
        if option == "9":
            break
        else: 
            valid_option()

# STYLE FUNCTIONS

# Print the contents of a file with styles
def print_style(path):
    with open(path, "r") as f:
        txt = f.read()
        f.close()

    print(txt)
    print()

# Display the slogan
def slogan():
    print_style("./style/slogan.txt")

# Display the main menu
def main_menu():
    print_style("./style/menu/main_menu.txt")

def college_menu():
    print_style("./style/menu/college_menu.txt")

def config_menu():
    print_style("./style/menu/config_menu.txt")

def about_menu():
    print_style("./style/menu/about_menu.txt")

def aspi_menu():
    print_style("./style/menu/aspi_menu.txt")

def subj_menu():
    print_style("./style/menu/subj_menu.txt")

def teac_menu():
    print_style("./style/menu/teac_menu.txt")

def clas_menu():
    print_style("./style/menu/clas_menu.txt")

def enro_menu():
    print_style("./style/menu/enro_menu.txt")

def college_load():
    clear()
    print_style("./style/load/college_load.txt")
    time.sleep(1.5)

def config_load():
    clear()
    print_style("./style/load/config_load.txt")
    time.sleep(1.5)

def about_load():
    clear()
    print_style("./style/load/about_load.txt")
    time.sleep(1.5)

def exit():
    print_style("./style/exit.txt")

# OTHER FUNCTIONS

# Clear the screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Creates the db structure if it does not exist
def structure():
    directory = "./db/"

    tables = {
        "Aspirant": "aspirant.json",
        "Subject": "subject.json",
        "Teacher": "teacher.json",
        "Class": "classe.json",
        "Enrollment": "enrollment.json"
    }

    if not os.path.exists(directory):
        os.makedirs(directory)

    for table, filename in tables.items():
        file_path = os.path.join(f"{directory}{filename}")
        if not os.path.exists(file_path):
            with open(file_path, 'w'):
                pass

def valid_option():
    print()
    print("Select a valid option!")
    time.sleep(1.5)

def soon():
    print()
    print("Available soon.")
    time.sleep(1.5)

# ____________________________________________________________________________________________________________________________________________________________________________________________________________________

slogan()
time.sleep(1.5)
structure()
start()