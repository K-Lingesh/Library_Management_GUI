import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from datetime import date

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="your_db_name",
    user="your_username",
    password="your_password"  # 🔑 Replace with your PostgreSQL password
)
cur = conn.cursor()

# Main window
root = tk.Tk()
root.title("Library Management System")
root.geometry("800x600")

# ---------- FUNCTIONS ----------

def add_book():
    title = entry_title.get()
    author = entry_author.get()
    genre = entry_genre.get()
    quantity = entry_quantity.get()
    if title and quantity.isdigit():
        cur.execute("INSERT INTO books (title, author, genre, quantity) VALUES (%s, %s, %s, %s)",
                    (title, author, genre, int(quantity)))
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully")
    else:
        messagebox.showerror("Error", "Invalid data")

def add_member():
    name = entry_mname.get()
    phone = entry_phone.get()
    email = entry_email.get()
    if name:
        cur.execute("INSERT INTO members (name, phone, email) VALUES (%s, %s, %s)",
                    (name, phone, email))
        conn.commit()
        messagebox.showinfo("Success", "Member added successfully")
    else:
        messagebox.showerror("Error", "Name is required")

def borrow_book():
    book_id = entry_bbook.get()
    member_id = entry_bmember.get()
    today = date.today()
    if book_id.isdigit() and member_id.isdigit():
        cur.execute("SELECT quantity FROM books WHERE book_id = %s", (int(book_id),))
        qty = cur.fetchone()
        if qty and qty[0] > 0:
            cur.execute("INSERT INTO borrow (book_id, member_id, borrow_date, status) VALUES (%s, %s, %s, %s)",
                        (int(book_id), int(member_id), today, 'Borrowed'))
            cur.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id = %s", (int(book_id),))
            conn.commit()
            messagebox.showinfo("Success", "Book borrowed")
        else:
            messagebox.showerror("Error", "Book not available")
    else:
        messagebox.showerror("Error", "Invalid IDs")

def return_book():
    borrow_id = entry_return.get()
    today = date.today()
    if borrow_id.isdigit():
        cur.execute("SELECT book_id FROM borrow WHERE borrow_id = %s AND status = 'Borrowed'", (int(borrow_id),))
        book = cur.fetchone()
        if book:
            cur.execute("UPDATE borrow SET return_date = %s, status = 'Returned' WHERE borrow_id = %s",
                        (today, int(borrow_id)))
            cur.execute("UPDATE books SET quantity = quantity + 1 WHERE book_id = %s", (book[0],))
            conn.commit()
            messagebox.showinfo("Success", "Book returned")
        else:
            messagebox.showerror("Error", "Invalid borrow ID")
    else:
        messagebox.showerror("Error", "Invalid ID")

def view_books():
    top = tk.Toplevel()
    top.title("Books")
    tree = ttk.Treeview(top, columns=("ID", "Title", "Author", "Genre", "Qty"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
    cur.execute("SELECT * FROM books ORDER BY book_id")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)
    tree.pack(fill='both', expand=True)

def view_members():
    top = tk.Toplevel()
    top.title("Members")
    tree = ttk.Treeview(top, columns=("ID", "Name", "Phone", "Email"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
    cur.execute("SELECT * FROM members ORDER BY member_id")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)
    tree.pack(fill='both', expand=True)

def view_borrowed():
    top = tk.Toplevel()
    top.title("Borrow Records")
    tree = ttk.Treeview(top, columns=("ID", "Book ID", "Member ID", "Borrow Date", "Return Date", "Status"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
    cur.execute("SELECT * FROM borrow ORDER BY borrow_id")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)
    tree.pack(fill='both', expand=True)

# ---------- ADD BOOK ----------
frame_book = tk.LabelFrame(root, text="Add Book")
frame_book.pack(fill="x", padx=10, pady=5)

tk.Label(frame_book, text="Title:").grid(row=0, column=0, sticky="e")
entry_title = tk.Entry(frame_book)
entry_title.grid(row=0, column=1, padx=5)

tk.Label(frame_book, text="Author:").grid(row=1, column=0, sticky="e")
entry_author = tk.Entry(frame_book)
entry_author.grid(row=1, column=1, padx=5)

tk.Label(frame_book, text="Genre:").grid(row=2, column=0, sticky="e")
entry_genre = tk.Entry(frame_book)
entry_genre.grid(row=2, column=1, padx=5)

tk.Label(frame_book, text="Quantity:").grid(row=3, column=0, sticky="e")
entry_quantity = tk.Entry(frame_book)
entry_quantity.grid(row=3, column=1, padx=5)

tk.Button(frame_book, text="Add Book", command=add_book).grid(row=4, column=0, columnspan=2, pady=5)

# ---------- ADD MEMBER ----------
frame_member = tk.LabelFrame(root, text="Add Member")
frame_member.pack(fill="x", padx=10, pady=5)

tk.Label(frame_member, text="Name:").grid(row=0, column=0, sticky="e")
entry_mname = tk.Entry(frame_member)
entry_mname.grid(row=0, column=1, padx=5)

tk.Label(frame_member, text="Phone:").grid(row=1, column=0, sticky="e")
entry_phone = tk.Entry(frame_member)
entry_phone.grid(row=1, column=1, padx=5)

tk.Label(frame_member, text="Email:").grid(row=2, column=0, sticky="e")
entry_email = tk.Entry(frame_member)
entry_email.grid(row=2, column=1, padx=5)

tk.Button(frame_member, text="Add Member", command=add_member).grid(row=3, column=0, columnspan=2, pady=5)

# ---------- BORROW & RETURN ----------
frame_borrow = tk.LabelFrame(root, text="Borrow / Return")
frame_borrow.pack(fill="x", padx=10, pady=5)

tk.Label(frame_borrow, text="Book ID:").grid(row=0, column=0, sticky="e")
entry_bbook = tk.Entry(frame_borrow)
entry_bbook.grid(row=0, column=1, padx=5)

tk.Label(frame_borrow, text="Member ID:").grid(row=1, column=0, sticky="e")
entry_bmember = tk.Entry(frame_borrow)
entry_bmember.grid(row=1, column=1, padx=5)

tk.Button(frame_borrow, text="Borrow Book", command=borrow_book).grid(row=2, column=0, columnspan=2, pady=5)

tk.Label(frame_borrow, text="Borrow ID:").grid(row=3, column=0, sticky="e")
entry_return = tk.Entry(frame_borrow)
entry_return.grid(row=3, column=1, padx=5)

tk.Button(frame_borrow, text="Return Book", command=return_book).grid(row=4, column=0, columnspan=2, pady=5)

# ---------- VIEW BUTTONS ----------
frame_view = tk.Frame(root)
frame_view.pack(pady=10)

tk.Button(frame_view, text="View Books", command=view_books).pack(side="left", padx=5)
tk.Button(frame_view, text="View Members", command=view_members).pack(side="left", padx=5)
tk.Button(frame_view, text="View Borrow Records", command=view_borrowed).pack(side="left", padx=5)

root.mainloop()

# Close DB connection
cur.close()
conn.close()
