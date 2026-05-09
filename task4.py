def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Give me name please"
        except KeyError:
            return "Contact not found"

    return inner

@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    save_contacts(contacts)
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, new_phone = args

    if name not in contacts:
        return "Contact not found."

    if contacts[name] == new_phone:
        return "This phone number is already saved for this contact."
    
    contacts[name] = new_phone
    save_contacts(contacts)

    return "Contact updated."


@input_error
def show_phone(args, contacts):
    name = args[0]
    return contacts[name]    
    
@input_error
def show_all(args, contacts):
    if not contacts:
        return "No contacts found."

    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def save_contacts(contacts):
    with open("contacts.txt", "w") as file:
        for name, phone in contacts.items():
            file.write(f"{name},{phone}\n")


def get_contacts():
    contacts = {}

    try:
        with open("contacts.txt", "r") as file:
            for line in file:
                name, phone = line.strip().split(",")
                contacts[name] = phone
    except FileNotFoundError:
        pass

    return contacts


def parse_input(user_input):
    parts = user_input.split()

    if not parts:
        return "", []
    
    cmd = parts[0].lower()
    args = parts[1:]
    
    return cmd, args


def main():
    print("Welcome to the assistant bot!")

    contacts = get_contacts()

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "phone":
            print(show_phone(args, contacts))

        elif command == "all":
            print(show_all(args, contacts))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()