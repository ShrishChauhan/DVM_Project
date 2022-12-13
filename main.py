
import openpyxl
from openpyxl import load_workbook
from .script import populate
import logging

class Book:
    def __init__(self, name: str, author: str, isbn: str):
        self.name = name
        self.author = author
        self.isbn = isbn
        self.borrowed = False
        self.reserved = False

    def issue_book(self):
        if not self.borrowed:
            self.borrowed = True
            logging.info(f"Book {self.name} with ISBN {self.isbn} issued to user")
            print(f"Book '{self.name}' has been borrowed")
        else:
            logging.warning(f"Book {self.name} with ISBN {self.isbn} has already been borrowed")
            print(f"Book '{self.name}' has already been borrowed by someone")


    def return_book(self):
        if self.borrowed:
            self.borrowed = False
            logging.info(f"Book {self.name} with ISBN {self.isbn} returned by user")
            print(f"Book '{self.name}' has been returned")
            return True
        else:
            logging.warning(f"Book {self.name} with ISBN {self.isbn} was not borrowed")
            print(f"Book '{self.name}' was not borrowed")
            return False


    def reserve_book(self):
        if (not self.borrowed) and (not self.reserved):
            logging.info(f"Book {self.name} with ISBN {self.isbn} reserved by user")
            print(f"Book '{self.name}' has been borrowed")
        elif (self.borrowed) and (not self.reserved):
            logging.warning(f"Book {self.name} with ISBN {self.isbn} has already been borrowed")
            print(f"Book '{self.name}' has already been borrowed")
        elif (not self.borrowed) and (self.reserved):
            logging.warning(f"Book {self.name} with ISBN {self.isbn} has already been reservedd")
            print(f"Book '{self.name}' has already been reserved")

class Shelf:
    def __init__(self, genre: str):
        self.genre = genre
        self.books = []

    def add_books(self, book: Book):
        logging.info(f"Book {book.name} with ISBN {book.isbn} added to shelf {self.genre} by user")
        self.books.append(book)

    def remove_books(self, book: Book):
        logging.info(f"Book {book.name} with ISBN {book.isbn} removed from shelf {self.genre} by user")
        self.books.remove(book)

    def show_books(self):
        print(f"Books on shelf '{self.genre}':")
        for book in self.books:
            print(f'{book.name} by {book.author} (ISBN: {book.isbn})')

    def count_books(self):
        return len(self.books)

    def populate_books(self, excel_file):

        wb = openpyxl.load_workbook(excel_file)

        sheet = wb.get_sheet_by_name('Sheet1')

        for row in sheet.rows:
            name = row[0].value
            isbn = row[1].value
            author = row[2].value

            book = Book(name=name, isbn=isbn, author=author)

            self.books.append(book)


class User:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def borrow(self, book, shelf):
        if self.role == "basic":
            if book in shelf.books:
                shelf.books.remove(book)
                book.issue_book()

            else:
                print(f"Book '{book.name}' not found on shelf '{shelf.genre}' ")

        else:
            print("Only basic users can borrow books from the library.")

    def submit(self, book, shelf):
        if self.role == "basic":
            shelf.books.append(book)
            book.return_book()
        else:
            print("Onlu basic users can return books to the library")

    def reserve(self, book, shelf):
        if self.role == "basic":
            shelf.books.append(book)
            book.reserve_book()
        else:
            print("Only basic users can reserve books of the library")

    def add_books(self, book, shelf):
        if self.role == "librarian":
            shelf.books.append(book)
            print(f"Book '{book.name}' added to shelf '{shelf.genre}' ")
        else:
            print("Only librarian users can add books to the shelves")

    def remove_books(self, book, shelf):
        if self.role == "librarian":
            shelf.books.remove(book)
            print(f"Book '{book.name}' removed from shelf '{shelf.genre}' ")
        else:
            print("Only librarian users can remove books from the shelves")



