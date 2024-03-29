# In windows command line use this to run file: streamlit run .\main.py
import os
import pandas as pd
import pickle
import streamlit as st
class Book:
    def __init__(self, ID, title, author, publication_year, isbn=None):
        self.ID = ID
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.isbn = isbn


class TreeNode:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, root, book):
        if not root:
            return TreeNode(book)
        elif book.ID < root.book.ID:
            root.left = self.insert(root.left, book)
        else:
            root.right = self.insert(root.right, book)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance = self.get_balance(root)

        if balance > 1 and book.ID < root.left.book.ID:
            return self.right_rotate(root)

        if balance < -1 and book.ID > root.right.book.ID:
            return self.left_rotate(root)

        if balance > 1 and book.ID > root.left.book.ID:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and book.ID < root.right.book.ID:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        if y is None:
            return z

        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        if y is None:
            return z

        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def search_books_by_author(self, root, author, found_books):
        if not root:
            return

        self.search_books_by_author(root.left, author, found_books)
        if root.book.author == author:
            found_books.append(root.book)
        self.search_books_by_author(root.right, author, found_books)

    def in_order_traversal(self, root):
        # f = open('text.txt','w')
            if root:
                # Traverse the ghleft subtree
                self.in_order_traversal(root.left)
                # Print the current node (book)
                st.write(f"Book ID: {root.book.ID}, Title: {root.book.title}, Author: {root.book.author}, Publish Year: {root.book.publication_year}")
                self.in_order_traversal(root.right)

    # Define a method to serialize the AVL tree
    def serialize(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.root, file)

    # Define a class method to deserialize the AVL tree
    @classmethod
    def deserialize(cls, filename):
        avl_tree = cls()
        with open(filename, "rb") as file:
            avl_tree.root = pickle.load(file)
        return avl_tree

    def delete(self, root, book_id):
        if not root:
            return root

        # If the book ID to be deleted is smaller than the root's book ID,
        # then it lies in the left subtree
        if book_id < root.book.ID:
            root.left = self.delete(root.left, book_id)

        # If the book ID to be deleted is greater than the root's book ID,
        # then it lies in the right subtree
        elif book_id > root.book.ID:
            root.right = self.delete(root.right, book_id)

        # If the book ID is the same as the root's book ID, then this is the node to be deleted
        else:
            # Node with only one child or no child
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp

            # Node with two children: Get the inorder successor (smallest in the right subtree)
            temp = self.min_value_node(root.right)

            # Copy the inorder successor's content to this node
            root.book = temp.book

            # Delete the inorder successor
            root.right = self.delete(root.right, temp.book.ID)

        if root is None:
            return root

        # Update the height of the current node
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Get the balance factor of this node
        balance = self.get_balance(root)

        # If the node becomes unbalanced, then there are four cases

        # Left Left Case
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        # Left Right Case
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        # Right Left Case
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def min_value_node(self, node):
        current = node
        # Loop down to find the leftmost leaf
        while current.left is not None:
            current = current.left
        return current

    def delete_book_by_id(self, book_id):
        self.root = self.delete(self.root, book_id)
        
    def search_book_by_id(self, root, book_id):
        if not root or root.book.ID == book_id:
            return root

        if root.book.ID > book_id:
            return self.search_book_by_id(root.left, book_id)

        return self.search_book_by_id(root.right, book_id)   

avl_tree = AVLTree()
if not os.path.exists('avl_tree.pkl'):       
    df = pd.read_csv("books.csv")
    for index, row in df.iterrows():
        bookID = row["bookID"]
        title = row["title"]
        authors = row["authors"]
        publishDate = row["publication_date"]
        isbn = row["isbn"]

        book = Book(bookID, title, authors, publishDate[-4:], isbn)
        avl_tree.root = avl_tree.insert(avl_tree.root, book)
    avl_tree.serialize("avl_tree.pkl")
    
def insert_book():
    st.subheader("Insert Book")
    book_idstr = st.text_input("Book ID:")
    title = st.text_input("Title:")
    author = st.text_input("Author:")
    publication_year = st.text_input("Publication Year:")
    isbn = st.text_input("ISBN:")
    try:
        book_id = int(book_idstr)
        if st.button("Insert"):
            book = Book(book_id, title, author, publication_year, isbn)
            avl_tree.root = avl_tree.insert(avl_tree.root, book)
        avl_tree.serialize("avl_tree.pkl")
        st.write('Insert successfully')
    except ValueError:
        st.write("Error: Book ID must be an integer")

def delete_book():
    st.subheader("Delete Book")
    try:
        book_id_to_delete = st.text_input("Enter Book ID to delete:")
        book_id = int(book_id_to_delete)
        if st.button("Delete"):
            avl_tree.delete_book_by_id(book_id)
            
        avl_tree.serialize("avl_tree.pkl")
        st.write('Delete successfully')
    except ValueError:
        st.write('Error: Book ID must be an integer')
    
def find_book():
    try:
        st.subheader("Find Book by ID")
        book_id_to_find = st.text_input("Enter Book ID:")
        book_id = int(book_id_to_find)
        if st.button("Find"):
            node = avl_tree.search_book_by_id(avl_tree.root, book_id)
            if node:
                st.write(f"Book found: {node.book.title}, {node.book.author}")
            else:
                st.write("Book not found")
    except ValueError:
        st.write('Error: Book ID musdt be an integer')

# avl_tree.serialize("avl_tree.pkl")
avl_tree = AVLTree.deserialize("avl_tree.pkl")
st.title("Book Management")
insert_book()
delete_book()
find_book()
author_to_search = st.text_input("Enter Author Name:", "")
if st.button("Search"):
    # Search for books dby the specified author
    found_books = []
    avl_tree.search_books_by_author(avl_tree.root, author_to_search, found_books)

    # Display the found books
    if found_books:
        st.header(f"Books by {author_to_search}:")
        for book in found_books:
            st.write(
                f"ID: {book.ID} Title: {book.title}, Author: {book.author}, Publication Year: {book.publication_year}"
            )
    else:
        st.write(f"No books found by author {author_to_search}.")
st.subheader('Print all books order by ID of books')
if st.button("Show all books"):
    avl_tree.in_order_traversal(avl_tree.root)
