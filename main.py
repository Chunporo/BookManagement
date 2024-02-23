import pandas as pd


class Book:
    def __init__(self, ID, title, author, publication_year):
        self.ID = ID
        self.title = title
        self.author = author
        self.publication_year = publication_year


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
        elif book.author < root.book.author:
            root.left = self.insert(root.left, book)
        else:
            root.right = self.insert(root.right, book)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance = self.get_balance(root)

        if balance > 1 and book.author < root.left.book.author:
            return self.right_rotate(root)

        if balance < -1 and book.author > root.right.book.author:
            return self.left_rotate(root)

        if balance > 1 and book.author > root.left.book.author:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and book.author < root.right.book.author:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
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

    def display_books(self, books):
        for book in books:
            print(
                f"Title: {book.title}, Author: {book.author}, Publication Year: {book.publication_year}"
            )

    def in_order_traversal(self, root):
        if root:
            # Traverse the left subtree
            self.in_order_traversal(root.left)
            # Print the current node (book)
            print(
                f"Book ID: {root.book.ID}, Title: {root.book.title}, Author: {root.book.author}, Publish Year: {root.book.publish_year}"
            )
            # Traverse the right subtree
            self.in_order_traversal(root.right)


# Example usage:
if __name__ == "__main__":
    avl_tree = AVLTree()
    df = pd.read_csv("books.csv")
    # df["publication_date"] = pd.to_datetime(df["publication_date"], format="%m/%d/%Y")
    for index, row in df.iterrows():
        bookID = row["bookID"]
        title = row["title"]
        authors = row["authors"]
        publishDate = row["publication_date"][-4:0]

        book = Book(bookID, title, authors, publishDate)
        print(bookID,' ',title,' ',authors,publishDate)
        avl_tree.root = avl_tree.insert(avl_tree.root, book)
        
    # Search for books by a specific author
    author_to_search = ""
    found_books = []
    avl_tree.search_books_by_author(avl_tree.root, author_to_search, found_books)

    # Display the found books
    print(f"Books by {author_to_search}:")
    avl_tree.display_books(found_books)
    
    avl_tree.in_order_traversal()
