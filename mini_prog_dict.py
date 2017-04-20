import csv
import string
import sys


def show_definition(appellation):
    mini_dict = {}
    with open('dictionary.csv', 'r') as db:
        reader = csv.reader(db, delimiter=',', quotechar='"')
        for key, definition, source in reader:
            mini_dict[key.lower()] = (definition, source)
    result = ("\n" +
              appellation +
              ":\n" +
              mini_dict[appellation.lower()][0] +
              "\nsource: " +
              mini_dict[appellation.lower()][1])
    return result  # returns a tuple (def, source)


def show_all():
    mini_dict = {}
    with open('dictionary.csv', 'r') as db:
        reader = csv.reader(db, delimiter=',', quotechar='"')
        for key, definition, source in reader:
            mini_dict[key] = (definition, source)
    result = sorted(mini_dict)
    # i don't understand why 'sorted' returns only keys in alphabetical order
    # but thats what i really need here ;) of course return is a list not dict.
    return result


def show_by_letter(letter):
    mini_dict = {}
    with open('dictionary.csv', 'r') as db:
        reader = csv.reader(db, delimiter=',', quotechar='"')
        for key, definition, source in reader:
            if key[0].lower() == letter:
                mini_dict[key] = (definition, source)
    result = sorted(mini_dict)
    return result  # look at the comment in 'show_all()'


def is_already_in_dict(key):  # checking if def is already in dict
    try:
        with open('dictionary.csv', 'r') as db:
            reader = csv.reader(db, delimiter=',', quotechar='"')
            for org_key, org_definition, org_source in reader:
                if org_key.lower() == key.lower():
                    result = True
                    break
                else:
                    result = False
    except FileNotFoundError:
        # quite obvious that when there is no file, our def is not in it :)
        result = False
    return result


def adding_new(key, definition, source):
    row = [key, definition, source]
    with open('dictionary.csv', 'a') as db:
        writer = csv.writer(db)
        writer.writerow(row)


menu = '''
Dictionary for a little programmer:\n
1) search explanation by appellation
2) add new definition
3) show all appellations alphabetically
4) show available definitions by first letter of appellation

9) show menu
0) exit'''

print(menu)  # before loop. only once, utntil not called again

while True:  # program main loop.

    try:
        action = input("\nChoose action (9 to show menu): ")

        if action == "1":  # searching by appellation
            try:
                appellation = input("\nEnter appellation: ")
                print(show_definition(appellation))
            except (KeyError):
                print("\nNo such appelation in dictionary yet.")
                print("Use menu to add it.")

        elif action == "2":  # adding new definition
            key = input("Enter new appellation: ")
            if is_already_in_dict(key):  # to avoid duplicated appelations
                print("\nDefinition already in dictionary!")
            else:
                definition = input("Enter definition: ")
                source = input("Enter source: ")
                adding_new(key, definition, source)
                print("\nSuccessfully added!")
            print(show_definition(key))  # printing added def

        # show all avaible appelations in alphabetical order
        elif action == "3":
            for item in show_all():
                print(item)

        elif action == "4":  # searching appelation by first letter
            letter = input("Enter letter: ").lower()
            if show_by_letter(letter) == []:
                print(
                    "No appelations starting with " +
                    letter.upper() +
                    ".\nUse menu to add some.")
            else:
                for item in show_by_letter(letter):
                    print(item)

        elif action == "9":  # printing menu
            print(menu)

        elif action == "0":  # goodbye
            sys.exit("\nYou have exited a dictionary")

        else:  # for entering command out of menu
            print("\nWrong choose!\nTry again")

    # KI and EOFE causes program quiting, FNFE allows to create a new file
    except (KeyboardInterrupt, EOFError):
        sys.exit("\nYou have exited a dictionary")
    except FileNotFoundError:
        print("\nMissing database file. Add new definition to make new one,")
        print("or check the program folder")
    # VE is raised when DB has empty lines. Need to be changed in future
    except ValueError:
        sys.exit("\nProblem occured while loading database: Invalid Database")
