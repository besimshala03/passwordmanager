import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from cryptography.fernet import Fernet
import sqlite3
import hashlib
import random

currentuser = None
userid = None
key = None

def handle_logout():
    global currentuser
    currentuser = None
    show_login_page()

def hash_password(password):
    hash_algorithm = hashlib.sha256()

    hash_algorithm.update(password.encode('utf-8'))

    hashed_password = hash_algorithm.hexdigest()

    return hashed_password


def encrypt_password(password, key):
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    cipher = Fernet(key)
    decrypted_password = cipher.decrypt(encrypted_password)
    return decrypted_password.decode()

def handle_logIn():
    global currentuser
    username = login_username_entry.get()
    password = login_passwords_entry.get()
    currentuser = username
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()

    c.execute('SELECT * FROM users')
    users_data = c.fetchall()

    # Check if any field is empty
    if not username or not password:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    # Check if the username and password match any entry in the users_data
    for user_data in users_data:
        if username == user_data[0] and hash_password(password) == user_data[1]:
            show_start_page()
            break
    else:
        messagebox.showerror("Error", "Invalid username or password")

    conn.close()


def handle_register():
    global key
    username = usernameregister_entry.get()
    password = passwordregister_entry.get()

    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS keys (
        userid INTEGER,
        key TEXT
    )
''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            password TEXT,
            userid INTEGER
        )
    ''')
    c.execute('SELECT * FROM users')
    users_data = c.fetchall()

    if not username or not password:
        messagebox.showerror("Error", "Please fill in all fields")
        return
    
    for user_data in users_data:
        if username == user_data[0]:
            messagebox.showerror("Error", "Username already exists")
            return
    
    userid = random.randint(1, 10000)
    key = Fernet.generate_key()
    c.execute('''
        INSERT INTO keys (userid, key) VALUES (?, ?)
    ''', (userid, key.decode()))
    c.execute('''
            INSERT INTO users (username, password, userid) VALUES (?, ?,?)
            ''', (username, hash_password(password), userid))
    conn.commit()
    conn.close()
    register_page.pack_forget()
    show_login_page()
         

def handle_click():
    global currentuser, key
    username = username_entry.get()
    password = password_entry.get()
    url = url_entry.get()

    # Check if any field is empty
    if not username or not password or not url:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()

    
    c.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            username TEXT,
            password TEXT,
            url TEXT,
            userid INTEGER
        )
    ''')

    c.execute('SELECT userid FROM users WHERE username = ?', (currentuser,))    
    userid = c.fetchone()[0]
    c.execute('SELECT key FROM keys WHERE userid = ?', (userid,))
    key_data = c.fetchone()
    key = key_data[0].encode()
    c.execute('''
        INSERT INTO passwords (username, password, url, userid) VALUES (?, ?, ?,?)
    ''', (username,encrypt_password(password, key), url, userid))

    conn.commit()
    conn.close()

    show_start_page()

def show_password_page():
    start_page.pack_forget()
    password_page.pack()

def show_start_page():
    register_page.pack_forget()
    login_page.pack_forget()
    password_page.pack_forget()
    view_page.pack_forget()
    details_page.pack_forget()  # Add this line
    start_page.pack()

def show_login_page():
    start_page.pack_forget()
    password_page.pack_forget()
    view_page.pack_forget()
    details_page.pack_forget()
    login_page.pack()

def show_view_page():
    start_page.pack_forget()
    details_page.pack_forget()  # Add this line
    view_passwords()

def view_passwords():
    for widget in view_page.winfo_children():
        widget.destroy()

    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()

    # Fetch the userid of the current logged-in user
    c.execute('SELECT userid FROM users WHERE username = ?', (currentuser,))
    userid = c.fetchone()[0]

    # Fetch passwords associated with the current userid
    c.execute('SELECT * FROM passwords WHERE userid = ?', (userid,))
    rows = c.fetchall()

    for row in rows:
        label = tk.Label(view_page, text=f"Username: {row[0]}")
        label.bind("<Button-1>", lambda event, row=row: show_details(row))
        label.pack()

    back_button_view = tk.Button(view_page, text="Back", command=show_start_page)
    back_button_view.pack()

    view_page.pack()

def show_details(row):
    view_page.pack_forget()
    details_page.pack()

    for widget in details_page.winfo_children():
        widget.destroy()

    # Open a new database connection
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()

    # Fetch the userid of the current logged-in user
    c.execute('SELECT userid FROM users WHERE username = ?', (currentuser,))
    userid = c.fetchone()[0]

    # Fetch the key for the current user
    c.execute('SELECT key FROM keys WHERE userid = ?', (userid,))
    key_data = c.fetchone()
    if key_data is None:
        messagebox.showerror("Error", "Key not found")
        return
    key = key_data[0].encode()

    cipher_suite = Fernet(key)

    password = cipher_suite.decrypt(row[1]).decode()

    details_label = tk.Label(details_page, text=f"Username: {row[0]}, Password: {password}, URL: {row[2]}")
    details_label.pack()

    back_button_details = tk.Button(details_page, text="Back", command=show_view_page)
    back_button_details.pack()

   

def show_register_page():
    login_page.pack_forget()
    register_page.pack()

window = tk.Tk()
window.title("Password Manager")

start_page = tk.Frame(window, bg="lightblue")
password_page = tk.Frame(window, bg="lightblue")
view_page = tk.Frame(window, bg="lightblue")
details_page = tk.Frame(window, bg="lightblue")
login_page = tk.Frame(window, bg="lightblue")
register_page = tk.Frame(window, bg="lightblue")

style = ttk.Style()
style.configure('TButton', font=('Helvetica', 14), background='lightgreen')

# Login Page

login_username_label = tk.Label(login_page, text="Type in your Username", font=("Helvetica", 14), bg='lightblue')
login_username_label.pack(pady=10)

login_username_entry = tk.Entry(login_page, fg="black", bg="white", width=50, font=("Helvetica", 12))
login_username_entry.pack(pady=10)

login_passwords_label = tk.Label(login_page, text="Type in your Password", font=("Helvetica", 14), bg='lightblue')
login_passwords_label.pack(pady=10)

login_passwords_entry = tk.Entry(login_page, fg="black", bg="white", width=50, show="*", font=("Helvetica", 12))
login_passwords_entry.pack(pady=10)

subbmit_button = tk.Button(login_page, text="Login", command=handle_logIn, font=("Helvetica", 14), bg='lightblue')
subbmit_button.pack(pady=10)

labelregister = tk.Label(login_page, text="Not registered yet?", font=("Helvetica", 14), bg='lightblue')
labelregister.pack(pady=10)

register_button = tk.Button(login_page, text="Register", command=show_register_page, font=("Helvetica", 14), bg='lightgreen')
register_button.pack(pady=10)


# Password Page

username_label = tk.Label(password_page, text="Type in a Username", font=("Helvetica", 14), bg='lightblue')
username_label.pack(pady=10)

username_entry = tk.Entry(password_page, fg="black", bg="white", width=50, font=("Helvetica", 12))
username_entry.pack(pady=10)

password_label = tk.Label(password_page, text="Type in a Password", font=("Helvetica", 14), bg='lightblue')
password_label.pack(pady=10)

password_entry = tk.Entry(password_page, fg="black", bg="white", width=50, show="*", font=("Helvetica", 12))
password_entry.pack(pady=10)

url_label = tk.Label(password_page, text="Type in a URL", font=("Helvetica", 14), bg='lightblue')
url_label.pack(pady=10)

url_entry = tk.Entry(password_page, fg="black", bg="white", width=50, font=("Helvetica", 12))
url_entry.pack(pady=10)

submit_button = tk.Button(password_page, text="Submit", command=handle_click, font=("Helvetica", 14), bg='lightgreen')
submit_button.pack(pady=10)

# Start Page

# Create a logout button with text
logout_button = tk.Button(start_page, text="Logout", command=handle_logout, font=("Helvetica", 14), bg='lightblue', bd=0)  # bd=0 removes the button border
logout_button.pack(pady=10)

create_button = tk.Button(start_page, text="Create New Password", command=show_password_page, font=("Helvetica", 14), bg='lightgreen')
create_button.pack(pady=10)

view_button = tk.Button(start_page, text="View Passwords", command=show_view_page, font=("Helvetica", 14), bg='lightgreen')
view_button.pack(pady=10)



# Register Page

usernameregister_label = tk.Label(register_page, text="Type in a Username", font=("Helvetica", 14), bg='lightblue')
usernameregister_label.pack(pady=10)

usernameregister_entry = tk.Entry(register_page, fg="black", bg="white", width=50, font=("Helvetica", 12))
usernameregister_entry.pack(pady=10)

passwordregister_label = tk.Label(register_page, text="Type in a Password", font=("Helvetica", 14), bg='lightblue')
passwordregister_label.pack(pady=10)

passwordregister_entry = tk.Entry(register_page, fg="black", bg="white", width=50, show="*", font=("Helvetica", 12))
passwordregister_entry.pack(pady=10)

registersubmit_button = tk.Button(register_page, text="Register", command=handle_register, font=("Helvetica", 14), bg='lightgreen')
registersubmit_button.pack(pady=10)

show_login_page()

window.mainloop()