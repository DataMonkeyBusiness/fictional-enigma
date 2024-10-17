# ER Diagram Generator

This Python script generates an Entity-Relationship (ER) diagram based on a dictionary of tables and columns. It enhances readability by applying custom colors, adjusting table spacing, and adding relationships between tables based on shared columns. The diagram is saved as a PNG image.

## Key Features

- Automatically generates ER diagrams from table schemas.
- Highlights tables with unique colors and adds translucent backgrounds.
- Thickens edges and displays relationships based on shared columns, with a maximum of five relationships between two tables.
- Enhances label readability with increased font size and bold styling.
- Reduces node separation for a more compact diagram layout without causing congestion.

## Dependencies

- `graphviz`: A graph visualization tool for generating diagrams.

## How to Use

1. Install the necessary library:
    ```bash
    pip install graphviz
    ```

2. Define your table schema in a dictionary format, where the keys are table names, and the values are lists of columns.

3. Call the `generate_er_diagram()` function, providing the schema and the desired output path for the PNG file.

## Function

### `generate_er_diagram(tables: dict, output_path: str)`

Generates an ER diagram based on the provided schema.

- **Parameters:**
    - `tables` (dict): A dictionary where keys are table names and values are lists of columns.
    - `output_path` (str): Full path (without extension) for saving the ER diagram as a PNG.

- **Example:**
    ```python
    banking_schema = {
        "Customer": ["customer_id", "first_name", "last_name"],
        "Account": ["account_id", "customer_id", "account_type", "balance"]
    }

    generate_er_diagram(tables=banking_schema, output_path="er_diagram")
    ```

## Sample Schema

The example schema represents a banking system, containing entities like `Customer`, `Account`, `Transaction`, `Branch`, `Employee`, etc., along with their respective attributes and relationships.

## Diagram Customizations

- **Color Palette:** A set of predefined colors is assigned to table pairs for relationship visualization.
- **Translucent Backgrounds:** Each table's node has a translucent background matching its color.
- **Font Size & Style:** Increased font size for better readability and bold labels for table relationships.

## Output

The script saves the ER diagram as a PNG image in the specified `output_path`.
