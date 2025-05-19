import os
import json
import pyodbc
from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management



server = 'apisrv.database.windows.net'
database = 'api01'
username = 'rakes'
password = 'Securi876'


# Azure Subscription and Resource details
subscription_id = ''
resource_group_name = 'apirg01'
region = 'East US'

# Set up the connection to Azure
credential = DefaultAzureCredential()
network_client = NetworkManagementClient(credential, subscription_id)

# Set up the connection to SQL database
def get_db_connection():
    conn = pyodbc.connect(
        f'Driver={{ODBC Driver 17 for SQL Server}};'
        f'Server={server};'
        f'Database={database};'
        f'Uid={username};'
        f'Pwd={password};'
    )
    return conn

# Route to register a user
@app.route('/register', methods=['POST'])
def register_user():
    # Get user data from the request
    user_data = request.get_json()

    username = user_data.get('username')
    password = user_data.get('password')
    email = user_data.get('email')

    if not username or not password or not email:
        return jsonify({"error": "All fields are required"}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Establish connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to insert user data
    insert_query = """
    INSERT INTO Users (username, password, email)
    VALUES (?, ?, ?)
    """

    try:
        cursor.execute(insert_query, (username, hashed_password, email))
        conn.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        conn.rollback()  # In case of an error, rollback the transaction
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Route to log in a user
@app.route('/login', methods=['POST'])
def login_user():
    # Get login data from the request
    login_data = request.get_json()

    username = login_data.get('username')
    password = login_data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Establish connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to find the user by username
    select_query = "SELECT password FROM Users WHERE username = ?"
    
    cursor.execute(select_query, (username,))
    user = cursor.fetchone()

    if user:
        stored_password = user[0]
        if check_password_hash(stored_password, password):
            session['user'] = username  # Store the user session
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401
    else:
        return jsonify({"error": "User not found"}), 404


# Route to create a VNet and subnets
@app.route('/create_vnet', methods=['POST'])
def create_vnet():
    if 'user' not in session:
        return jsonify({"error": "You must be logged in to create a VNet."}), 401

    vnet_data = request.get_json()
    
    vnet_name = vnet_data.get('vnet_name')
    subnets = vnet_data.get('subnets')

    if not vnet_name or not subnets:
        return jsonify({"error": "VNet name and subnets are required."}), 400

    # Create the VNet
    vnet_params = {
        'location': region,
        'address_space': {
            'address_prefixes': ['192.0.0.0/16']
        }
    }

    async_vnet_creation = network_client.virtual_networks.begin_create_or_update(
        resource_group_name,
        vnet_name,
        vnet_params
    )
    vnet_result = async_vnet_creation.result()

    # Create subnets
    for subnet in subnets:
        subnet_name = subnet.get('subnet_name')
        subnet_address = subnet.get('subnet_address')

        if not subnet_name or not subnet_address:
            return jsonify({"error": "Subnet name and address are required."}), 400

        subnet_params = {
            'address_prefix': subnet_address
        }

        async_subnet_creation = network_client.subnets.begin_create_or_update(
            resource_group_name,
            vnet_name,
            subnet_name,
            subnet_params
        )
        async_subnet_creation.result()

    # Store information of the created VNet and subnets in SQL Database
    store_vnet_info(vnet_name, subnets)

    return jsonify({"message": "VNet and subnets created successfully!"}), 201

# Store information of created VNet and subnets in the Azure SQL DB
def store_vnet_info(vnet_name, subnets):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Store VNet information in the Resources table
    insert_vnet_query = """
    INSERT INTO Resources (resource_name, resource_type)
    VALUES (?, ?)
    """
    cursor.execute(insert_vnet_query, (vnet_name, 'VNet'))

    # Store Subnet information in the Subnets table
    for subnet in subnets:
        subnet_name = subnet.get('subnet_name')
        subnet_address = subnet.get('subnet_address')
        insert_subnet_query = """
        INSERT INTO Subnets (subnet_name, subnet_address, vnet_name)
        VALUES (?, ?, ?)
        """
        cursor.execute(insert_subnet_query, (subnet_name, subnet_address, vnet_name))

    conn.commit()
    cursor.close()
    conn.close()

# Azure SQL connection parameters

driver = '{ODBC Driver 17 for SQL Server}'  # Ensure this is installed

# Function to fetch data
def fetch_data():
    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Subnets")  # Replace with your table
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        return {"error": str(e)}

# Flask route to expose data
@app.route('/api/subnets', methods=['GET'])
def get_data():
    data = fetch_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
