
import json
import os

FILE_NAME = "contacts.json"


# Storage: Load contacts
def load_contacts():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            contacts = json.load(file)

        if not isinstance(contacts, list):
            raise ValueError("Invalid JSON file format")

        return contacts

    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError("JSON file is corrupt. Original data preserved.") from error


# Storage: Save contacts
def save_contacts(contacts):
    temp_file = FILE_NAME + ".tmp"

    with open(temp_file, "w") as file:
        json.dump(contacts, file, indent=4)

    os.replace(temp_file, FILE_NAME)


# Business Logic: Add contact
def add_contact(contact_id, name, phone, email):
    contacts = load_contacts()

    if not all([contact_id, name, phone, email]):
        raise ValueError("All fields are required")

    if any(contact["id"] == str(contact_id) for contact in contacts):
        raise ValueError("Contact ID already exists")

    contact = {
        "id": str(contact_id),
        "name": name,
        "phone": phone,
        "email": email
    }

    contacts.append(contact)
    save_contacts(contacts)

    return "Contact added successfully"


# Business Logic: Search contact
def search_contact(name):
    contacts = load_contacts()

    return [
        contact for contact in contacts
        if name.casefold() in contact["name"].casefold()
    ]


# Business Logic: Update contact
def update_contact(contact_id, name, phone, email):
    contacts = load_contacts()

    for contact in contacts:
        if contact["id"] == str(contact_id):
            if not all([name, phone, email]):
                raise ValueError("All fields are required")

            contact["name"] = name
            contact["phone"] = phone
            contact["email"] = email

            save_contacts(contacts)
            return "Contact updated successfully"

    return "Contact not found"


# Business Logic: Delete contact
def delete_contact(contact_id):
    contacts = load_contacts()

    updated_contacts = [
        contact for contact in contacts
        if contact["id"] != str(contact_id)
    ]

    if len(updated_contacts) == len(contacts):
        return "Contact not found"

    save_contacts(updated_contacts)

    return "Contact deleted successfully"


# Business Logic: List contacts
def list_contacts():
    return load_contacts()


# Command-Line Menu
def main():
    while True:
        print("\n===== CONTACT MANAGER =====")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. List Contacts")
        print("6. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                contact_id = input("Enter ID: ")
                name = input("Enter Name: ")
                phone = input("Enter Phone: ")
                email = input("Enter Email: ")

                print(add_contact(contact_id, name, phone, email))

            elif choice == "2":
                name = input("Enter name to search: ")
                results = search_contact(name)

                if results:
                    for contact in results:
                        print(contact)
                else:
                    print("Contact not found")

            elif choice == "3":
                contact_id = input("Enter ID: ")
                name = input("Enter new name: ")
                phone = input("Enter new phone: ")
                email = input("Enter new email: ")

                print(update_contact(contact_id, name, phone, email))

            elif choice == "4":
                contact_id = input("Enter ID: ")
                print(delete_contact(contact_id))

            elif choice == "5":
                contacts = list_contacts()

                if contacts:
                    for contact in contacts:
                        print(contact)
                else:
                    print("No contacts available")

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Try again.")

        except (ValueError, OSError) as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
