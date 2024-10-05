import graphviz
from graphviz import Digraph
import os
import itertools

os.chdir("/Users/lakshanabhat/Documents/git/ER_Generator")

def generate_er_diagram(tables: dict, output_path: str):
    """
    Generates an ER diagram from a dictionary of tables and columns,
    including relationships based on shared columns, with a maximum of five relationships between two tables.
    Adds light translucent hue matching the table color, thickens edges, and enhances readability of labels.
    Reduces the distance between tables without making it congested and increases font size.
    :param tables: Dictionary where keys are table names and values are lists of columns
    :param output_path: Full path for the output ER diagram file (without extension)
    """
    dot = Digraph(comment='ER Diagram', format='png')

    # Set global attributes to reduce distance and increase font size, avoiding congestion
    dot.attr(splines='polyline', rankdir='LR', nodesep='0.1', ranksep='0.3')  # Minimize space between nodes
    dot.attr('node', fontsize='14', fontname='Helvetica')  # Increase font size for better readability

    # List of distinct colors to assign to different table pairs
    color_palette = ['#FF6666', '#66FF66', '#6666FF', '#FFCC66', '#CC66FF', '#66CCFF', '#FF66CC', '#66FFCC', '#FF6666', '#CCCCFF']
    color_cycle = itertools.cycle(color_palette)  # Cycles through colors

    # Function to generate lighter hues for a translucent-like effect
    def lighten_color(hex_color, factor=0.8):
        """Lightens the given hex color by multiplying its components by a factor."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        r = min(int(r + (255 - r) * factor), 255)
        g = min(int(g + (255 - g) * factor), 255)
        b = min(int(b + (255 - b) * factor), 255)
        
        return f'#{r:02x}{g:02x}{b:02x}'

    # Dictionary to store table-specific colors
    table_colors = {}

    # Create nodes for each table with color and translucent-like background
    for table, columns in tables.items():
        if table not in table_colors:
            table_colors[table] = next(color_cycle)  # Assign a unique color to each table
        
        table_color = table_colors[table]
        light_table_color = lighten_color(table_color)  # Generate a lighter hue for the background
        
        table_label = f'<b>{table}</b>'
        columns_label = '<br/>'.join(columns)
        label = f'<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4"><TR><TD BGCOLOR="{light_table_color}" PORT="table">{table_label}</TD></TR><TR><TD>{columns_label}</TD></TR></TABLE>>'
        dot.node(table, label=label, shape='plaintext')

    # Create relationships based on shared columns
    column_to_tables = {}
    for table, columns in tables.items():
        for column in columns:
            if column not in column_to_tables:
                column_to_tables[column] = []
            column_to_tables[column].append(table)

    # Track edges and limit relationships to a maximum of five per pair
    edge_count = {}  # To keep track of the number of relationships between pairs
    dummy_node_counter = 0
    table_pair_colors = {}  # Store assigned colors for table pairs

    for column, tables_with_common_column in column_to_tables.items():
        if len(tables_with_common_column) > 1:
            for i in range(len(tables_with_common_column)):
                for j in range(i + 1, len(tables_with_common_column)):
                    source = tables_with_common_column[i]
                    target = tables_with_common_column[j]
                    edge_pair = tuple(sorted([source, target]))  # Ensure same pair is treated consistently
                    
                    # Initialize count for this edge pair if not already present
                    if edge_pair not in edge_count:
                        edge_count[edge_pair] = 0
                    
                    # Assign color to the table pair if not already assigned
                    if edge_pair not in table_pair_colors:
                        table_pair_colors[edge_pair] = next(color_cycle)

                    # Add relationship if the edge count is less than 5
                    if edge_count[edge_pair] < 5:
                        # Create dummy node for merging lines
                        dummy_node = f'dummy_{dummy_node_counter}'
                        dummy_node_counter += 1
                        dot.node(dummy_node, shape='point', width='0', height='0', style='invisible')

                        # Color for this relationship (based on the table pair)
                        color = table_pair_colors[edge_pair]

                        # Add edges from source to dummy node, and from dummy node to target
                        dot.edge(source, dummy_node, color=color, fontcolor=color, arrowsize='1.5', style='dashed', penwidth='4.0')  # Thicker lines
                        dot.edge(dummy_node, target, label=column, color=color, fontcolor='black', fontsize='14', fontname='Helvetica bold', arrowsize='1.5', penwidth='4.0')  # Thicker lines and bold labels

                        edge_count[edge_pair] += 1

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(output_path)

    # Visualize the diagram
    dot.render(filename=output_path, cleanup=True)
    print(f'ER Diagram saved as {output_path}')

#Samle schema
banking_schema = {
    "Customer": [
        "customer_id",  # Primary Key
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "address",
        "date_of_birth",
        "created_at"
    ],
    "Account": [
        "account_id",  # Primary Key
        "customer_id",  # Foreign Key references Customer(customer_id)
        "account_type",  # (e.g., savings, checking)
        "balance",
        "created_at",
        "status"
    ],
    "Transaction": [
        "transaction_id",  # Primary Key
        "account_id",  # Foreign Key references Account(account_id)
        "transaction_type",  # (e.g., debit, credit)
        "amount",
        "transaction_date",
        "description"
    ],
    "Branch": [
        "branch_id",  # Primary Key
        "branch_name",
        "branch_address",
        "branch_phone",
        "manager_id"  # Foreign Key references Employee(employee_id)
    ],
    "Employee": [
        "employee_id",  # Primary Key
        "branch_id",  # Foreign Key references Branch(branch_id)
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "position",  # (e.g., manager, cashier)
        "salary",
        "date_hired"
    ],
    "Loan": [
        "loan_id",  # Primary Key
        "customer_id",  # Foreign Key references Customer(customer_id)
        "loan_amount",
        "interest_rate",
        "loan_type",  # (e.g., home loan, personal loan)
        "loan_start_date",
        "loan_end_date",
        "status"
    ],
    "CreditCard": [
        "card_id",  # Primary Key
        "customer_id",  # Foreign Key references Customer(customer_id)
        "card_number",
        "card_type",  # (e.g., Visa, Mastercard)
        "expiration_date",
        "credit_limit",
        "balance",
        "status"
    ],
    "Payment": [
        "payment_id",  # Primary Key
        "card_id",  # Foreign Key references CreditCard(card_id)
        "amount",
        "payment_date",
        "payment_method"  # (e.g., online, cheque)
    ],
    "ATM_Withdrawal": [
        "withdrawal_id",  # Primary Key
        "account_id",  # Foreign Key references Account(account_id)
        "atm_id",  # Foreign Key references ATM(atm_id)
        "withdrawal_amount",
        "withdrawal_date"
    ],
    "ATM": [
        "atm_id",  # Primary Key
        "location",
        "branch_id"  # Foreign Key references Branch(branch_id)
    ]
}

generate_er_diagram(tables=banking_schema
                    ,output_path="output_path.png")