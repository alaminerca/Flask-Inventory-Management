# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Initialize Flask application
app = Flask(__name__)

# Database configuration
DATABASE = 'flaskDB.db'

# Function to establish database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Function to execute database queries (insert, update, delete)
def execute_query(query, params=()):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return True  # Return True if query executed successfully
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False  # Return False if there's an error executing the query

# Function to execute database queries (select)
def fetch_query(query, params=()):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows  # Return query results
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return None  # Return None if there's an error executing the query

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    result = ''  # Initialize result variable
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        # Execute registration query
        if execute_query("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password)):
            result = 'Registration successful'
        else:
            result = 'Registration failed'
    return render_template('register.html', result=result)

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    result = ''  # Initialize result variable
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']
        # Check if user exists in database
        user = fetch_query("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        if user:
            result = 'Login successful'
            return redirect(url_for('dashboard'))  # Redirect to dashboard if login is successful
        else:
            result = 'Invalid email or password'
    return render_template('login.html', result=result)

# Route for dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Route for adding a product
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    result = ''  # Initialize result variable
    if request.method == 'POST':
        # Get form data
        name = request.form['input_pname']
        price = request.form['input_price']
        # Execute query to add product
        if execute_query("INSERT INTO products (pname, price) VALUES (?, ?)", (name, price)):
            result = 'Product added successfully'
        else:
            result = 'Failed to add product'
    return render_template('add.html', result=result)

# Route for deleting a product
@app.route('/delete', methods=['GET', 'POST'])
def delete_product():
    result = ''  # Initialize result variable
    if request.method == 'POST':
        # Get product ID from form data
        id = request.form['input_pid']
        # Execute query to delete product
        if execute_query("DELETE FROM products WHERE id = ?", (id,)):
            result = 'Product deleted successfully'
        else:
            result = 'Failed to delete product'
    return render_template('delete.html', result=result)

# Route for updating a product
@app.route('/update', methods=['GET', 'POST'])
def update_product():
    result = ''  # Initialize result variable
    product = None  # Initialize product variable
    if request.method == 'POST':
        # Get form data
        id = request.form['id']
        name = request.form['name']
        price = request.form['price']
        # Execute query to update product
        if execute_query("UPDATE products SET pname = ?, price = ? WHERE id = ?", (name, price, id)):
            result = 'Product updated successfully'
            # Fetch updated product details
            product = fetch_query("SELECT * FROM products WHERE id = ?", (id,))
        else:
            result = 'Failed to update product'
    return render_template('update.html', result=result, product=product)

# Route for viewing all products
@app.route('/view')
def view_products():
    # Fetch all products from the database
    products = fetch_query("SELECT * FROM products")
    if products:
        return render_template('view.html', products=products)
    else:
        return "No products found"

# Route for logging out
@app.route('/logout')
def logout():
    # Clear session data

    return redirect(url_for('index'))  # Redirect to home page after logout

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
