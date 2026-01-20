# Project 3: Simple Library Manager (OOP)

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def save(self):
        with open("library.txt", "a") as file:
            file.write(f"{self.title} by {self.author}\n")

def search_book(query):
    found = False
    try:
        with open("library.txt", "r") as file:
            for line in file:
                if query.lower() in line.lower():
                    print("Found:", line.strip())
                    found = True
    except FileNotFoundError:
        print("Library is empty.")
    if not found:
        print("Book not found.")

while True:
    print("\n1. Add Book\n2. Search Book\n3. Exit")
    choice = input("Choose: ")
    if choice == '1':
        title = input("Book Title: ")
        author = input("Author: ")
        b = Book(title, author)
        b.save()
        print("Book added.")
    elif choice == '2':
        query = input("Search book by title/author: ")
        search_book(query)
    elif choice == '3':
        break
    else:
        print("Invalid option.")

