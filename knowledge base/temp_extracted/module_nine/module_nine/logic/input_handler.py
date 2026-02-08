def collect_user_details():
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    email = input("Enter your email: ")
    country = input("Enter your country: ")
    return f"User: {name}, Age: {age}, Email: {email}, Country: {country}"

def menu_system():
    print("Main Menu:")
    print("1. Say Hello")
    print("2. Say Goodbye")
    print("3. Exit")
    choice = input("Choose an option (1-3): ")

    if choice == "1":
        print("Hello, User!")
    elif choice == "2":
        print("Goodbye, User!")
    elif choice == "3":
        print("Exiting...")
    else:
        print("Invalid option selected.")