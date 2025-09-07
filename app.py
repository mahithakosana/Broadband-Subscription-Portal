# Import necessary libraries for the application
import streamlit as st  # Main web application framework
import pandas as pd  # Data manipulation and analysis
import numpy as np  # Numerical computations
import plotly.express as px  # Data visualization library
import plotly.graph_objects as go  # Advanced graph creation
from datetime import datetime, timedelta  # Date and time manipulation
import time  # For adding delays in the UI
import hashlib  # For password hashing (security)
import base64  # For encoding/decoding (available but not currently used)

# Configure the Streamlit page settings
st.set_page_config(
    page_title="Broadband Subscription Portal",  # Title shown in browser tab
    page_icon="🌐",  # Icon shown in browser tab
    layout="wide",  # Use wide layout for better screen utilization
    initial_sidebar_state="expanded"  # Sidebar starts expanded
)

# Define function to set background image and custom CSS styles
def set_bg_image():
    # Use Streamlit's markdown with HTML and CSS for styling
    st.markdown(
        """
        <style>
        /* Set background image for the entire app */
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1542744173-8e7e53415bb0?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1770&q=80");
            background-size: cover;  /* Cover the entire area */
            background-position: center;  /* Center the image */
        }
        
        /* Style for main header text */
        .main-header {
            font-size: 3rem;  /* Large font size */
            color: white;  /* White text color */
            text-align: center;  /* Center alignment */
            margin-bottom: 2rem;  /* Bottom margin */
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);  /* Text shadow for better visibility */
        }
        
        /* Container for login/signup forms */
        .login-container {
            background-color: rgba(255, 255, 255, 0.95);  /* Semi-transparent white background */
            padding: 30px;  /* Internal spacing */
            border-radius: 15px;  /* Rounded corners */
            box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);  /* Shadow effect */
        }
        
        /* Style for text inside login container */
        .login-container h2, .login-container label, .login-container p {
            color: #000000 !important;  /* Force black text color */
        }
        
        /* Style for all input fields */
        .stTextInput input, .stNumberInput input, .stTextArea textarea, .stSelectbox select {
            background-color: #000000 !important;  /* Black background */
            color: white !important;  /* White text */
            border: 1px solid #444444 !important;  /* Dark gray border */
        }
        
        /* Style for input field labels */
        .stTextInput label, .stNumberInput label, .stTextArea label, .stSelectbox label {
            color: white !important;  /* White text for labels */
        }
        
        /* Style for sub-headers */
        .sub-header {
            font-size: 1.5rem;  /* Medium font size */
            color: #0D47A1;  /* Dark blue color */
            margin-bottom: 1rem;  /* Bottom margin */
        }
        
        /* Style for plan cards */
        .plan-card {
            border-radius: 10px;  /* Rounded corners */
            padding: 20px;  /* Internal spacing */
            margin: 10px 0;  /* Vertical margin */
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);  /* Shadow effect */
            transition: 0.3s;  /* Smooth transition for hover effect */
            background-color: white;  /* White background */
        }
        
        /* Hover effect for plan cards */
        .plan-card:hover {
            box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);  /* Enhanced shadow on hover */
        }
        
        /* Style for metric cards */
        .metric-card {
            background-color: #E3F2FD;  /* Light blue background */
            border-radius: 10px;  /* Rounded corners */
            padding: 15px;  /* Internal spacing */
            text-align: center;  /* Center text alignment */
            margin: 10px 0;  /* Vertical margin */
        }
        
        /* Style for all buttons */
        .stButton>button {
            width: 100%;  /* Full width buttons */
            border-radius: 5px;  /* Slightly rounded corners */
        }
        
        /* Container for tabs */
        .tab-container {
            display: flex;  /* Use flexbox layout */
            flex-direction: column;  /* Vertical arrangement */
            width: 100%;  /* Full width */
        }
        
        /* Container for tab buttons */
        .tab-buttons {
            display: flex;  /* Use flexbox layout */
            margin-bottom: 1rem;  /* Bottom margin */
        }
        
        /* Style for individual tab buttons */
        .tab-button {
            padding: 10px 20px;  /* Internal spacing */
            margin-right: 5px;  /* Right margin between buttons */
            background-color: #f0f0f0;  /* Light gray background */
            border: none;  /* No border */
            border-radius: 5px 5px 0 0;  /* Rounded top corners only */
            cursor: pointer;  /* Pointer cursor on hover */
        }
        
        /* Style for active tab button */
        .tab-button.active {
            background-color: #1E88E5;  /* Blue background for active tab */
            color: white;  /* White text */
        }
        
        /* Container for data usage progress bar */
        .usage-progress {
            height: 20px;  /* Fixed height */
            background-color: #f0f0f0;  /* Light gray background */
            border-radius: 10px;  /* Rounded corners */
            margin: 10px 0;  /* Vertical margin */
        }
        
        /* Style for the progress bar itself */
        .usage-progress-bar {
            height: 100%;  /* Full height of container */
            border-radius: 10px;  /* Rounded corners */
            text-align: center;  /* Center text alignment */
            line-height: 20px;  /* Vertical centering of text */
            color: white;  /* White text color */
        }
        
        /* Style for customer table */
        .customer-table {
            width: 100%;  /* Full width */
            border-collapse: collapse;  /* Collapse borders */
            margin: 15px 0;  /* Vertical margin */
        }
        
        .customer-table th, .customer-table td {
            border: 1px solid #ddd;  /* Light gray border */
            padding: 8px;  /* Internal spacing */
            text-align: left;  /* Left alignment */
        }
        
        .customer-table th {
            background-color: #1E88E5;  /* Blue background for headers */
            color: white;  /* White text */
        }
        
        .customer-table tr:nth-child(even) {
            background-color: #f2f2f2;  /* Zebra striping */
        }
        
        .customer-table tr:hover {
            background-color: #ddd;  /* Hover effect */
        }
        </style>
        """,
        unsafe_allow_html=True  # Allow HTML rendering in markdown
    )

# Initialize application data
def init_data():
    # Create users dictionary if it doesn't exist in session state
    if 'users' not in st.session_state:
        st.session_state.users = {
            # Pre-defined admin user
            'admin': {'password': 'admin123', 'role': 'admin', 'name': 'System Administrator'},
            # Pre-defined customer user with sample data
            'customer1': {'password': 'customer1', 'role': 'customer', 'name': 'John Doe', 
                         'subscriptions': [{'plan': 'Premium', 'status': 'active', 'start_date': '2023-01-15', 'end_date': '2024-01-14', 'data_used': 850, 'data_limit': 1000}],
                         'usage': {'daily': np.random.randint(5, 20, 30).tolist()},
                         'personal_details': {'email': 'john@example.com', 'phone': '123-456-7890', 'address': '123 Main St'}},
            # Additional sample customers
            'customer2': {'password': 'customer2', 'role': 'customer', 'name': 'Alice Smith', 
                         'subscriptions': [{'plan': 'Standard', 'status': 'active', 'start_date': '2023-03-10', 'end_date': '2024-03-09', 'data_used': 450, 'data_limit': 1000}],
                         'usage': {'daily': np.random.randint(3, 15, 30).tolist()},
                         'personal_details': {'email': 'alice@example.com', 'phone': '234-567-8901', 'address': '456 Oak St'}},
            'customer3': {'password': 'customer3', 'role': 'customer', 'name': 'Bob Johnson', 
                         'subscriptions': [{'plan': 'Basic', 'status': 'active', 'start_date': '2023-05-20', 'end_date': '2024-05-19', 'data_used': 300, 'data_limit': 500}],
                         'usage': {'daily': np.random.randint(2, 10, 30).tolist()},
                         'personal_details': {'email': 'bob@example.com', 'phone': '345-678-9012', 'address': '789 Pine St'}}
        }
    
    # Create plans list if it doesn't exist in session state
    if 'plans' not in st.session_state:
        st.session_state.plans = [
            # Basic plan
            {'name': 'Basic', 'speed': '50 Mbps', 'price': 29.99, 'data_cap': '500 GB', 'description': 'For light browsing and streaming'},
            # Standard plan
            {'name': 'Standard', 'speed': '100 Mbps', 'price': 49.99, 'data_cap': '1 TB', 'description': 'For families and remote work'},
            # Premium plan
            {'name': 'Premium', 'speed': '1 Gbps', 'price': 79.99, 'data_cap': 'Unlimited', 'description': 'For gaming and 4K streaming'}
        ]
    
    # Create subscriptions list if it doesn't exist in session state
    if 'subscriptions' not in st.session_state:
        # Generate sample subscription data
        subscriptions = []  # Empty list to store subscriptions
        statuses = ['active', 'expired', 'cancelled']  # Possible subscription statuses
        plans = ['Basic', 'Standard', 'Premium']  # Available plans
        
        # Create 100 sample subscriptions
        for i in range(100):
            # Random start date within the past year
            sub_date = datetime.now() - timedelta(days=np.random.randint(1, 365))
            # End date one year after start date
            end_date = sub_date + timedelta(days=365)
            # Random status with weighted probabilities
            status = np.random.choice(statuses, p=[0.7, 0.2, 0.1])
            # Random plan selection
            plan_name = np.random.choice(plans)
            
            # Get the price for the selected plan
            plan_price = next((p['price'] for p in st.session_state.plans if p['name'] == plan_name), 29.99)
            
            # Add subscription to list
            subscriptions.append({
                'user_id': f'user_{i}',  # Unique user ID
                'plan': plan_name,  # Plan name
                'status': status,  # Subscription status
                'start_date': sub_date.strftime('%Y-%m-%d'),  # Formatted start date
                'end_date': end_date.strftime('%Y-%m-%d'),  # Formatted end date
                'price': plan_price  # Plan price
            })
        
        # Store subscriptions in session state
        st.session_state.subscriptions = subscriptions
        
    # Initialize admin tab state if it doesn't exist
    if 'admin_tab' not in st.session_state:
        st.session_state.admin_tab = "Dashboard"  # Default to Dashboard tab
        
    # Initialize customer tab state if it doesn't exist
    if 'customer_tab' not in st.session_state:
        st.session_state.customer_tab = "My Subscriptions"  # Default to My Subscriptions tab
    
    # Initialize upgrade subscription index state if it doesn't exist
    if 'upgrade_sub_index' not in st.session_state:
        st.session_state.upgrade_sub_index = None  # No upgrade in progress
        
    # Initialize renew subscription index state if it doesn't exist
    if 'renew_sub_index' not in st.session_state:
        st.session_state.renew_sub_index = None  # No renewal in progress
    
    # Initialize revenue data if it doesn't exist
    if 'revenue_data' not in st.session_state:
        st.session_state.revenue_data = calculate_revenue()  # Calculate initial revenue

# Calculate revenue from all active subscriptions
def calculate_revenue():
    revenue_data = {}  # Empty dictionary to store revenue by plan
    
    # Calculate revenue for each plan
    for plan in st.session_state.plans:
        # Find all active subscriptions for this plan
        plan_subs = [s for s in st.session_state.subscriptions if s['plan'] == plan['name'] and s['status'] == 'active']
        # Calculate total revenue for this plan
        revenue = len(plan_subs) * plan['price']
        # Store revenue for this plan
        revenue_data[plan['name']] = revenue
    
    # Calculate total revenue across all plans
    revenue_data['Total'] = sum(revenue_data.values())
    # Return the revenue data
    return revenue_data

# Hash a password for security
def make_hashes(password):
    # Create SHA256 hash of the password
    return hashlib.sha256(str.encode(password)).hexdigest()

# Check if a password matches its hash
def check_hashes(password, hashed_text):
    # Compare hash of input password with stored hash
    return make_hashes(password) == hashed_text

# Authenticate a user login attempt
def login_user(username, password):
    # Check if username exists in users dictionary
    if username in st.session_state.users:
        # Check if password matches
        if st.session_state.users[username]['password'] == password:
            return True  # Authentication successful
    return False  # Authentication failed

# Register a new user
def signup_user(username, password, role='customer'):
    # Check if username already exists
    if username in st.session_state.users:
        return False  # Username already taken
        
    # Create new user account
    st.session_state.users[username] = {
        'password': password,  # Store password (in plain text for demo - not secure for production)
        'role': role,  # User role (default is customer)
        'name': username,  # User's name (defaults to username)
        'subscriptions': [],  # Empty subscriptions list
        'usage': {'daily': []},  # Empty usage data
        'personal_details': {}  # Empty personal details
    }
    return True  # Registration successful

# Create a custom tab navigation component
def custom_tabs(tabs, key_prefix, default_index=0):
    # Create a container for the tab buttons
    tab_container = st.container()
    with tab_container:
        # Create columns for each tab button
        cols = st.columns(len(tabs))
        # Start with default tab selected
        selected_index = default_index
        
        # Create a button for each tab
        for i, tab in enumerate(tabs):
            # If button is clicked, select this tab
            if cols[i].button(tab, key=f"{key_prefix}_{i}", use_container_width=True):
                selected_index = i  # Update selected index
                # Update the session state with selected tab
                if key_prefix == "admin":
                    st.session_state.admin_tab = tab  # Set admin tab
                else:
                    st.session_state.customer_tab = tab  # Set customer tab
                
        # Add CSS to highlight the active tab
        st.markdown(f"""
        <style>
            div[data-testid="column"]:nth-of-type({selected_index + 1}) button {{
                background-color: #1E88E5;  /* Blue background for active tab */
                color: white;  /* White text */
            }}
        </style>
        """, unsafe_allow_html=True)  # Allow HTML rendering
    
    # Return the index of the selected tab
    return selected_index

# Display the login/signup page
def login_page():
    set_bg_image()  # Apply background image and styles
    # Display main header
    st.markdown("<h1 class='main-header'>Broadband Subscription Portal</h1>", unsafe_allow_html=True)
    
    # Create a container for the login/signup forms
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)  # Start login container
        
        # Login form header
        st.markdown("<h2 style='color: black;'>Login</h2>", unsafe_allow_html=True)
        # Create login form
        login_form = st.form("Login")
        # Username input field
        username = login_form.text_input("Username")
        # Password input field (hidden text)
        password = login_form.text_input("Password", type="password")
        
        # When login button is clicked
        if login_form.form_submit_button("Login"):
            # Attempt to authenticate user
            if login_user(username, password):
                # Set login state and user information
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = st.session_state.users[username]['role']
                st.success("Logged in successfully!")  # Success message
                time.sleep(1)  # Brief delay
                st.rerun()  # Refresh the page
            else:
                st.error("Invalid username or password")  # Error message
        
        # Separator between login and signup forms
        st.markdown("---")
        # Signup form header
        st.markdown("<h3 style='color: black;'>Don't have an account? Sign up below.</h3>", unsafe_allow_html=True)
        
        # Create signup form
        signup_form = st.form("Sign Up")
        # New username input
        new_username = signup_form.text_input("Choose a username")
        # New password input (hidden text)
        new_password = signup_form.text_input("Choose a password", type="password")
        # Password confirmation input
        confirm_password = signup_form.text_input("Confirm password", type="password")
        
        # When signup button is clicked
        if signup_form.form_submit_button("Sign Up"):
            # Check if passwords match
            if new_password != confirm_password:
                st.error("Passwords don't match")  # Error message
            # Attempt to create new account
            elif signup_user(new_username, new_password):
                st.success("Account created successfully! Please log in.")  # Success message
            else:
                st.error("Username already exists")  # Error message
                
        st.markdown('</div>', unsafe_allow_html=True)  # End login container

# Display the admin dashboard
def admin_dashboard():
    # Welcome message in sidebar
    st.sidebar.markdown(f"### Welcome, {st.session_state.users[st.session_state.username]['name']}")
    # Logout button in sidebar
    if st.sidebar.button("Logout"):
        # Clear session state and return to login page
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.admin_tab = "Dashboard"
        st.rerun()  # Refresh the page
    
    # Admin dashboard tabs (added Customer Management tab)
    tabs = ["Dashboard", "Customer Management", "Manage Plans"]
    
    # Get the current tab from session state
    current_tab = st.session_state.admin_tab
    # Set default index based on current tab
    default_index = tabs.index(current_tab) if current_tab in tabs else 0
    
    # Display custom tabs and get selected index
    selected_index = custom_tabs(tabs, "admin", default_index)
    
    # Dashboard tab content
    if tabs[selected_index] == "Dashboard":
        # Dashboard header
        st.markdown("<h2 class='sub-header'>Admin Dashboard</h2>", unsafe_allow_html=True)
        
        # Calculate metrics for dashboard
        # Count active subscriptions
        active_subs = [s for s in st.session_state.subscriptions if s['status'] == 'active']
        # Count expired subscriptions
        expired_subs = [s for s in st.session_state.subscriptions if s['status'] == 'expired']
        # Count cancelled subscriptions
        cancelled_subs = [s for s in st.session_state.subscriptions if s['status'] == 'cancelled']
        
        # Update revenue data
        st.session_state.revenue_data = calculate_revenue()
        
        # Count total customers (users with customer role)
        total_customers = len([user for username, user in st.session_state.users.items() if user.get('role') == 'customer'])
        
        # Display metrics in columns
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        # Total subscriptions metric
        col1.metric("Total Subscriptions", len(st.session_state.subscriptions))
        # Active subscriptions metric
        col2.metric("Active Subscriptions", len(active_subs))
        # Expired subscriptions metric
        col3.metric("Expired Subscriptions", len(expired_subs))
        # Cancelled subscriptions metric
        col4.metric("Cancelled Subscriptions", len(cancelled_subs))
        # Total customers metric
        col5.metric("Total Customers", total_customers)
        # Total revenue metric (formatted as currency)
        col6.metric("Total Revenue", f"${st.session_state.revenue_data['Total']:,.2f}")
        
        # Revenue by plan chart
        st.markdown("#### Revenue by Plan")
        # Create DataFrame for revenue data
        revenue_df = pd.DataFrame({
            'Plan': [plan for plan in st.session_state.revenue_data.keys() if plan != 'Total'],
            'Revenue': [st.session_state.revenue_data[plan] for plan in st.session_state.revenue_data.keys() if plan != 'Total']
        })
        
        # Create bar chart of revenue by plan
        fig_rev = px.bar(revenue_df, x='Plan', y='Revenue', title="Revenue by Plan")
        # Display the chart
        st.plotly_chart(fig_rev, use_container_width=True)
        
        # Subscription distribution by plan chart
        st.markdown("#### Subscriptions by Plan")
        # Count subscriptions by plan
        plan_counts = pd.DataFrame(st.session_state.subscriptions)['plan'].value_counts()
        # Create pie chart of subscription distribution
        fig1 = px.pie(values=plan_counts.values, names=plan_counts.index, title="Subscription Distribution by Plan")
        # Display the chart
        st.plotly_chart(fig1, use_container_width=True)
        
        # Subscription status distribution chart
        st.markdown("#### Subscription Status Distribution")
        # Count subscriptions by status
        status_counts = pd.DataFrame(st.session_state.subscriptions)['status'].value_counts()
        # Create bar chart of status distribution
        fig2 = px.bar(x=status_counts.index, y=status_counts.values, 
                     labels={'x': 'Status', 'y': 'Count'}, title="Subscription Status")
        # Display the chart
        st.plotly_chart(fig2, use_container_width=True)
        
        # Daily new subscriptions chart
        st.markdown("#### Daily New Subscriptions (Last 30 Days)")
        # Generate dates for the last 30 days
        dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]
        # Generate random new subscription counts
        new_subs = np.random.randint(0, 10, 30).tolist()
        # Create line chart of daily new subscriptions
        fig3 = px.line(x=dates, y=new_subs, labels={'x': 'Date', 'y': 'New Subscriptions'})
        # Display the chart
        st.plotly_chart(fig3, use_container_width=True)
        
        # Revenue distribution by plan chart
        st.markdown("#### Revenue Distribution by Plan")
        revenue_data = []  # Empty list to store revenue data
        # Calculate revenue for each plan
        for plan in st.session_state.plans:
            # Find active subscriptions for this plan
            plan_subs = [s for s in st.session_state.subscriptions if s['plan'] == plan['name'] and s['status'] == 'active']
            # Calculate total revenue
            revenue = len(plan_subs) * plan['price']
            # Add to revenue data list
            revenue_data.append({'Plan': plan['name'], 'Revenue': revenue})
        
        # Create DataFrame from revenue data
        revenue_df = pd.DataFrame(revenue_data)
        # Create pie chart of revenue distribution
        fig4 = px.pie(revenue_df, values='Revenue', names='Plan', title="Revenue Distribution by Plan")
        # Display the chart
        st.plotly_chart(fig4, use_container_width=True)
    
    # Customer Management tab content
    elif tabs[selected_index] == "Customer Management":
        # Customer Management header
        st.markdown("<h2 class='sub-header'>Customer Management</h2>", unsafe_allow_html=True)
        
        # Search box for filtering customers
        search_term = st.text_input("Search Customers", placeholder="Enter customer name or username")
        
        # Get all customer users
        customers = {username: user for username, user in st.session_state.users.items() if user.get('role') == 'customer'}
        
        # Filter customers based on search term
        if search_term:
            customers = {username: user for username, user in customers.items() 
                        if search_term.lower() in username.lower() or 
                        search_term.lower() in user.get('name', '').lower()}
        
        # Display customer count
        st.markdown(f"**Total Customers: {len(customers)}**")
        
        # Check if there are any customers
        if not customers:
            st.info("No customers found matching your search criteria.")
        else:
            # Create a list to store customer data for the table
            customer_data = []
            
            # Process each customer
            for username, user in customers.items():
                # Get active subscription if exists
                active_sub = next((sub for sub in user.get('subscriptions', []) if sub['status'] == 'active'), None)
                
                # Get personal details
                personal_details = user.get('personal_details', {})
                
                # Add customer data to list
                customer_data.append({
                    'Username': username,
                    'Name': user.get('name', ''),
                    'Email': personal_details.get('email', ''),
                    'Phone': personal_details.get('phone', ''),
                    'Address': personal_details.get('address', ''),
                    'Current Plan': active_sub['plan'] if active_sub else 'None',
                    'Plan Status': active_sub['status'] if active_sub else 'None',
                    'Start Date': active_sub['start_date'] if active_sub else 'N/A',
                    'End Date': active_sub['end_date'] if active_sub else 'N/A'
                })
            
            # Create DataFrame from customer data
            customer_df = pd.DataFrame(customer_data)
            
            # Display customer table
            st.markdown("### Customer Details")
            st.dataframe(customer_df, use_container_width=True)
            
            # Option to download customer data as CSV
            csv = customer_df.to_csv(index=False)
            st.download_button(
                label="Download Customer Data as CSV",
                data=csv,
                file_name="customers.csv",
                mime="text/csv"
            )
            
            # Display customer details in expandable sections
            st.markdown("### Detailed Customer View")
            for username, user in customers.items():
                # Get active subscription if exists
                active_sub = next((sub for sub in user.get('subscriptions', []) if sub['status'] == 'active'), None)
                
                # Get personal details
                personal_details = user.get('personal_details', {})
                
                # Create expandable section for each customer
                with st.expander(f"{user.get('name', '')} ({username})"):
                    # Two-column layout for customer details
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Personal Information")
                        st.write(f"**Name:** {user.get('name', '')}")
                        st.write(f"**Email:** {personal_details.get('email', 'Not provided')}")
                        st.write(f"**Phone:** {personal_details.get('phone', 'Not provided')}")
                        st.write(f"**Address:** {personal_details.get('address', 'Not provided')}")
                    
                    with col2:
                        st.markdown("#### Subscription Information")
                        if active_sub:
                            st.write(f"**Current Plan:** {active_sub['plan']}")
                            st.write(f"**Status:** {active_sub['status']}")
                            st.write(f"**Start Date:** {active_sub['start_date']}")
                            st.write(f"**End Date:** {active_sub['end_date']}")
                            
                            # Calculate days remaining
                            end_date = datetime.strptime(active_sub['end_date'], '%Y-%m-%d')
                            days_remaining = (end_date - datetime.now()).days
                            status_color = "green" if days_remaining > 30 else "orange" if days_remaining > 7 else "red"
                            st.write(f"**Days Remaining:** <span style='color:{status_color};'>{days_remaining}</span>", unsafe_allow_html=True)
                        else:
                            st.warning("No active subscription")
                    
                    # Action buttons for customer management
                    st.markdown("#### Actions")
                    action_col1, action_col2, action_col3 = st.columns(3)
                    
                    with action_col1:
                        if st.button("View Usage", key=f"usage_{username}"):
                            st.session_state.selected_customer = username
                            st.info(f"Viewing usage data for {user.get('name', '')}")
                    
                    with action_col2:
                        if st.button("Contact", key=f"contact_{username}"):
                            st.info(f"Contacting {user.get('name', '')} at {personal_details.get('email', 'No email available')}")
                    
                    with action_col3:
                        if st.button("Suspend Account", key=f"suspend_{username}"):
                            st.warning(f"Account suspension functionality would be implemented here for {username}")
    
    # Manage Plans tab content
    elif tabs[selected_index] == "Manage Plans":
        # Manage Plans header
        st.markdown("<h2 class='sub-header'>Manage Subscription Plans</h2>", unsafe_allow_html=True)
        
        # Display current plans
        st.markdown("#### Current Plans")
        # Loop through each plan
        for i, plan in enumerate(st.session_state.plans):
            # Create expandable section for each plan
            with st.expander(f"{plan['name']} - ${plan['price']}/month"):
                # Two-column layout for plan details
                col1, col2 = st.columns(2)
                with col1:
                    # Display plan speed
                    st.write(f"**Speed:** {plan['speed']}")
                    # Display data cap
                    st.write(f"**Data Cap:** {plan['data_cap']}")
                with col2:
                    # Display plan price
                    st.write(f"**Price:** ${plan['price']}")
                    # Display plan description
                    st.write(f"**Description:** {plan['description']}")
                
                # Delete plan button
                if st.button(f"Delete {plan['name']}", key=f"del_{i}"):
                    # Remove plan from list
                    st.session_state.plans.pop(i)
                    # Success message
                    st.success(f"Removed {plan['name']} plan")
                    # Update revenue after deletion
                    st.session_state.revenue_data = calculate_revenue()
                    st.rerun()  # Refresh the page
        
        # Add new plan form
        st.markdown("#### Add New Plan")
        # Create form for adding new plans
        with st.form("add_plan_form"):
            # Two-column layout for form fields
            col1, col2 = st.columns(2)
            with col1:
                # Plan name input
                new_name = st.text_input("Plan Name")
                # Plan speed input
                new_speed = st.text_input("Speed")
            with col2:
                # Plan price input (numeric)
                new_price = st.number_input("Price ($)", min_value=0.0, step=0.01)
                # Data cap input
                new_data_cap = st.text_input("Data Cap")
            
            # Plan description text area
            new_description = st.text_area("Description")
            
            # When Add Plan button is clicked
            if st.form_submit_button("Add Plan"):
                # Validate that all required fields are filled
                if new_name and new_speed and new_price and new_data_cap:
                    # Add new plan to the list
                    st.session_state.plans.append({
                        'name': new_name,
                        'speed': new_speed,
                        'price': new_price,
                        'data_cap': new_data_cap,
                        'description': new_description
                    })
                    # Success message
                    st.success(f"Added {new_name} plan")
                    # Update revenue after adding new plan
                    st.session_state.revenue_data = calculate_revenue()
                    st.rerun()  # Refresh the page
                else:
                    # Error message if validation fails
                    st.error("Please fill all required fields")

# Display the customer dashboard
def customer_dashboard():
    # Get current user's data
    user_data = st.session_state.users[st.session_state.username]
    # Welcome message in sidebar
    st.sidebar.markdown(f"### Welcome, {user_data['name']}")
    # Logout button in sidebar
    if st.sidebar.button("Logout"):
        # Clear session state and return to login page
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.customer_tab = "My Subscriptions"
        st.session_state.upgrade_sub_index = None
        st.session_state.renew_sub_index = None
        st.rerun()  # Refresh the page
    
    # Customer dashboard tabs
    tabs = ["My Subscriptions", "Browse Plans", "Usage Analytics", "Personal Details"]
    
    # Get the current tab from session state
    current_tab = st.session_state.customer_tab
    # Set default index based on current tab
    default_index = tabs.index(current_tab) if current_tab in tabs else 0
    
    # Display custom tabs and get selected index
    selected_index = custom_tabs(tabs, "customer", default_index)
    
    # My Subscriptions tab content
    if tabs[selected_index] == "My Subscriptions":
        # My Subscriptions header
        st.markdown("<h2 class='sub-header'>My Subscriptions</h2>", unsafe_allow_html=True)
        
        # Check if user has any subscriptions
        if not user_data.get('subscriptions'):
            # Message for users with no subscriptions
            st.info("You don't have any subscriptions yet. Browse our plans to get started!")
        else:
            # Loop through each subscription
            for i, sub in enumerate(user_data['subscriptions']):
                # Set color based on subscription status
                status_color = "green" if sub['status'] == 'active' else "gray"
                # Display subscription card
                st.markdown(f"""
                <div class="plan-card">
                    <h3>{sub['plan']} Plan <span style="color: {status_color}; font-size: 0.8em;">({sub['status']})</span></h3>
                    <p><strong>Start Date:</strong> {sub['start_date']} | <strong>End Date:</strong> {sub['end_date']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show action buttons for active subscriptions only
                if sub['status'] == 'active':
                    # Three-column layout for action buttons
                    col1, col2, col3 = st.columns(3)
                    # Renew button
                    if col1.button("Renew", key=f"renew_{i}"):
                        # Set renewal mode and switch to Browse Plans tab
                        st.session_state.renew_sub_index = i
                        st.session_state.customer_tab = "Browse Plans"
                        st.rerun()  # Refresh the page
                    
                    # Upgrade button
                    if col2.button("Upgrade", key=f"upgrade_{i}"):
                        # Set upgrade mode and switch to Browse Plans tab
                        st.session_state.upgrade_sub_index = i
                        st.session_state.customer_tab = "Browse Plans"
                        st.rerun()  # Refresh the page
                    
                    # Cancel button
                    if col3.button("Cancel", key=f"cancel_{i}"):
                        # Mark subscription as cancelled
                        user_data['subscriptions'][i]['status'] = 'cancelled'
                        # Warning message
                        st.warning(f"Cancelled {sub['plan']} plan!")
                        st.rerun()  # Refresh the page
    
    # Browse Plans tab content
    elif tabs[selected_index] == "Browse Plans":
        # Browse Plans header
        st.markdown("<h2 class='sub-header'>Browse Plans</h2>", unsafe_allow_html=True)
        
        # Check if we're in upgrade or renew mode
        upgrade_mode = st.session_state.upgrade_sub_index is not None
        renew_mode = st.session_state.renew_sub_index is not None
        
        # Show upgrade message if in upgrade mode
        if upgrade_mode:
            current_sub = user_data['subscriptions'][st.session_state.upgrade_sub_index]
            st.info(f"You are upgrading from your current {current_sub['plan']} plan. Select a new plan below.")
        
        # Show renewal options if in renew mode
        if renew_mode:
            current_sub = user_data['subscriptions'][st.session_state.renew_sub_index]
            st.info(f"You are renewing your {current_sub['plan']} plan. Select renewal options below.")
            
            # Two-column layout for renewal options
            col1, col2 = st.columns(2)
            with col1:
                # Slider for selecting renewal duration
                months = st.slider("Months to renew", 1, 24, 12)
            with col2:
                # Spacer for alignment
                st.write("")  
                st.write("")  
                # Confirm renewal button
                if st.button("Confirm Renewal"):
                    # Calculate new end date
                    current_end = datetime.strptime(current_sub['end_date'], '%Y-%m-%d')
                    new_end = current_end + timedelta(days=30*months)
                    # Update subscription end date
                    user_data['subscriptions'][st.session_state.renew_sub_index]['end_date'] = new_end.strftime('%Y-%m-%d')
                    # Success message
                    st.success(f"Renewed your plan for {months} months!")
                    # Exit renewal mode
                    st.session_state.renew_sub_index = None
                    time.sleep(1)  # Brief delay
                    st.rerun()  # Refresh the page
        
        # Show plan recommendations if not in upgrade or renew mode
        if not upgrade_mode and not renew_mode:
            st.markdown("#### Recommended For You")
            # Simple recommendation logic (always recommends Standard plan)
            rec_plan = st.session_state.plans[1]
            # Display recommended plan card
            st.markdown(f"""
            <div class="plan-card" style="border: 2px solid #1E88E5;">
                <h3>🌟 {rec_plan['name']} Plan (Recommended)</h3>
                <p><strong>Speed:</strong> {rec_plan['speed']} | <strong>Data Cap:</strong> {rec_plan['data_cap']}</p>
                <p><strong>Price:</strong> ${rec_plan['price']}/month</p>
                <p>{rec_plan['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Subscribe to recommended plan button
            if st.button("Subscribe to Recommended Plan", key="sub_rec"):
                # Add subscription to user
                start_date = datetime.now().strftime('%Y-%m-%d')
                end_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
                
                # Add to user's subscriptions
                user_data['subscriptions'].append({
                    'plan': rec_plan['name'],
                    'status': 'active',
                    'start_date': start_date,
                    'end_date': end_date,
                    'data_used': 0,
                    'data_limit': 1000 if rec_plan['data_cap'] == '1 TB' else (500 if rec_plan['data_cap'] == '500 GB' else float('inf'))
                })
                
                # Also add to global subscriptions for revenue tracking
                st.session_state.subscriptions.append({
                    'user_id': st.session_state.username,
                    'plan': rec_plan['name'],
                    'status': 'active',
                    'start_date': start_date,
                    'end_date': end_date,
                    'price': rec_plan['price']
                })
                
                # Update revenue
                st.session_state.revenue_data = calculate_revenue()
                
                # Success message
                st.success(f"Subscribed to {rec_plan['name']} plan!")
                time.sleep(1)  # Brief delay
                st.rerun()  # Refresh the page
        
        # Display all available plans
        st.markdown("#### All Available Plans")
        # Loop through each plan
        for plan in st.session_state.plans:
            # Display plan card
            st.markdown(f"""
            <div class="plan-card">
                <h3>{plan['name']} Plan</h3>
                <p><strong>Speed:</strong> {plan['speed']} | <strong>Data Cap:</strong> {plan['data_cap']}</p>
                <p><strong>Price:</strong> ${plan['price']}/month</p>
                <p>{plan['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show appropriate button based on mode
            if upgrade_mode:
                # Upgrade button for upgrade mode
                if st.button(f"Upgrade to {plan['name']}", key=f"upg_{plan['name']}"):
                    # Upgrade the subscription
                    user_data['subscriptions'][st.session_state.upgrade_sub_index]['plan'] = plan['name']
                    user_data['subscriptions'][st.session_state.upgrade_sub_index]['data_limit'] = 1000 if plan['data_cap'] == '1 TB' else (500 if plan['data_cap'] == '500 GB' else float('inf'))
                    # Success message
                    st.success(f"Upgraded to {plan['name']} plan!")
                    # Exit upgrade mode
                    st.session_state.upgrade_sub_index = None
                    time.sleep(1)  # Brief delay
                    st.rerun()  # Refresh the page
            elif not renew_mode:
                # Subscribe button for normal mode
                if st.button(f"Subscribe to {plan['name']}", key=f"sub_{plan['name']}"):
                    # Add subscription to user
                    start_date = datetime.now().strftime('%Y-%m-%d')
                    end_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
                    
                    # Add to user's subscriptions
                    user_data['subscriptions'].append({
                        'plan': plan['name'],
                        'status': 'active',
                        'start_date': start_date,
                        'end_date': end_date,
                        'data_used': 0,
                        'data_limit': 1000 if plan['data_cap'] == '1 TB' else (500 if plan['data_cap'] == '500 GB' else float('inf'))
                    })
                    
                    # Also add to global subscriptions for revenue tracking
                    st.session_state.subscriptions.append({
                        'user_id': st.session_state.username,
                        'plan': plan['name'],
                        'status': 'active',
                        'start_date': start_date,
                        'end_date': end_date,
                        'price': plan['price']
                    })
                    
                    # Update revenue
                    st.session_state.revenue_data = calculate_revenue()
                    
                    # Success message
                    st.success(f"Subscribed to {plan['name']} plan!")
                    time.sleep(1)  # Brief delay
                    st.rerun()  # Refresh the page
        
        # Cancel button for upgrade or renew mode
        if upgrade_mode or renew_mode:
            if st.button("Cancel", key="cancel_action"):
                # Exit upgrade/renew mode
                if upgrade_mode:
                    st.session_state.upgrade_sub_index = None
                if renew_mode:
                    st.session_state.renew_sub_index = None
                st.rerun()  # Refresh the page
        
        # Plan finder tool (only shown in normal mode)
        if not upgrade_mode and not renew_mode:
            st.markdown("#### Find the Right Plan for You")
            # Two-column layout for plan finder inputs
            col1, col2 = st.columns(2)
            with col1:
                # Usage intensity selector
                usage = st.select_slider("Usage Intensity", options=["Light", "Moderate", "Heavy"])
                # Number of devices slider
                devices = st.slider("Number of devices", 1, 10, 3)
            with col2:
                # Budget slider
                budget = st.slider("Budget ($/month)", 20, 100, 50)
                # Primary activities multi-select
                activities = st.multiselect("Primary activities", ["Browsing", "Streaming", "Gaming", "Working"])
            
            # Find My Plan button
            if st.button("Find My Plan"):
                # Simple recommendation algorithm
                if usage == "Light" or budget < 40:
                    rec_idx = 0  # Basic plan
                elif usage == "Moderate" or budget < 70:
                    rec_idx = 1  # Standard plan
                else:
                    rec_idx = 2  # Premium plan
                    
                # Display recommendation
                st.success(f"We recommend the {st.session_state.plans[rec_idx]['name']} plan for you!")
    
    # Usage Analytics tab content
    elif tabs[selected_index] == "Usage Analytics":
        # Usage Analytics header
        st.markdown("<h2 class='sub-header'>Usage Analytics</h2>", unsafe_allow_html=True)
        
        # Check if user has active subscription
        active_subs = [sub for sub in user_data.get('subscriptions', []) if sub['status'] == 'active']
        if not active_subs:
            # Message for users with no active subscriptions
            st.info("You don't have any active subscriptions to show usage data.")
            return  # Exit the function
        
        # Get the first active subscription
        current_sub = active_subs[0]
        
        # Generate sample usage data if not exists
        if not user_data['usage']['daily']:
            user_data['usage']['daily'] = np.random.randint(5, 20, 30).tolist()
        
        # Data usage progress visualization
        if current_sub.get('data_limit', float('inf')) != float('inf'):
            # Get data usage and limit
            data_used = current_sub.get('data_used', 0)
            data_limit = current_sub['data_limit']
            # Calculate usage percentage
            usage_percent = (data_used / data_limit) * 100
            
            # Display data usage header
            st.markdown(f"#### Data Usage: {data_used} GB / {data_limit} GB")
            # Create progress bar with color coding
            st.markdown(f"""
            <div class="usage-progress">
                <div class="usage-progress-bar" style="width: {usage_percent}%; background-color: {'#4CAF50' if usage_percent < 80 else '#FF9800' if usage_percent < 95 else '#F44336'};">
                    {usage_percent:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show appropriate message based on usage level
            if usage_percent > 95:
                st.error("You've almost reached your data limit! Consider upgrading your plan.")
            elif usage_percent > 80:
                st.warning("You're approaching your data limit. Monitor your usage carefully.")
            else:
                st.success(f"You have {data_limit - data_used} GB remaining this month.")
        else:
            # Message for unlimited data plans
            st.info("Your current plan has unlimited data usage.")
        
        # Daily usage chart
        # Generate dates for the last 30 days
        dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]
        # Get usage data
        usage_data = user_data['usage']['daily']
        
        # Create line chart of daily usage
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=usage_data, mode='lines+markers', name='Daily Usage (GB)'))
        fig.update_layout(title="Your Data Usage (Last 30 Days)", xaxis_title="Date", yaxis_title="Data Used (GB)")
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Usage statistics in three columns
        col1, col2, col3 = st.columns(3)
        # Average daily usage metric
        col1.metric("Average Daily Usage", f"{np.mean(usage_data):.1f} GB")
        # Maximum daily usage metric
        col2.metric("Max Daily Usage", f"{np.max(usage_data)} GB")
        # Total monthly usage metric
        col3.metric("Total Monthly Usage", f"{np.sum(usage_data)} GB")
        
        # Data cap warnings (for limited plans only)
        if current_sub.get('data_limit', float('inf')) != float('inf'):
            data_cap = current_sub['data_limit']
            # Check if user has exceeded data cap
            if np.sum(usage_data) > data_cap:
                st.error(f"You've exceeded your monthly data cap of {data_cap} GB!")
            # Check if user is approaching data cap
            elif np.sum(usage_data) > 0.8 * data_cap:
                st.warning(f"You're approaching your monthly data cap of {data_cap} GB.")
    
    # Personal Details tab content
    elif tabs[selected_index] == "Personal Details":
        # Personal Details header
        st.markdown("<h2 class='sub-header'>Personal Details</h2>", unsafe_allow_html=True)
        
        # Get personal details or empty dict if none exists
        personal_details = user_data.get('personal_details', {})
        
        # Create form for editing personal details
        with st.form("personal_details_form"):
            # Two-column layout for form fields
            col1, col2 = st.columns(2)
            with col1:
                # Full name input (pre-filled with current value)
                name = st.text_input("Full Name", value=user_data.get('name', ''))
                # Email input (pre-filled with current value)
                email = st.text_input("Email", value=personal_details.get('email', ''))
            with col2:
                # Phone input (pre-filled with current value)
                phone = st.text_input("Phone", value=personal_details.get('phone', ''))
                # Address input (pre-filled with current value)
                address = st.text_input("Address", value=personal_details.get('address', ''))
            
            # Save Details button
            if st.form_submit_button("Save Details"):
                # Update user data with new values
                user_data['name'] = name
                user_data['personal_details'] = {
                    'email': email,
                    'phone': phone,
                    'address': address
                }
                # Success message
                st.success("Personal details updated successfully!")

# Main application logic
def main():
    init_data()  # Initialize application data
    
    # Initialize login state if it doesn't exist
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
    
    # Show login page if not logged in, otherwise show appropriate dashboard
    if not st.session_state.logged_in:
        login_page()  # Show login/signup page
    else:
        if st.session_state.role == 'admin':
            admin_dashboard()  # Show admin dashboard
        else:
            customer_dashboard()  # Show customer dashboard

# Entry point of the application
if __name__ == "__main__":
    main()  # Run the main function