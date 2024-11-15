import mysql.connector
import csv

try:
    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',    # Replace with your actual host
        user='Alex', # Replace with your actual username
        password='1234', # Replace with your actual password
        database='catalogue_of_life'  # Replace with your actual database name
    )

    # Create a cursor object
    cursor = connection.cursor()

    # SQL query to join the three tables and filter the required data
    sql_query = """
    SELECT cn.common_name, sn.species, sn.genus, f.family, f.order, f.class, f.phylum
    FROM common_names cn
    JOIN scientific_names sn ON cn.name_code = sn.name_code
    JOIN families f ON sn.family_id = f.record_id
    WHERE f.kingdom = 'Animalia' 
      AND f.phylum = 'Chordata'
      AND f.class != 'Actinopterygii' 
      AND cn.is_infraspecies = 0
      AND cn.language = 'English'  -- Ensure common name is in English
      AND cn.common_name IS NOT NULL;  -- Ensure there is a common name
    """

    # Execute the SQL query
    cursor.execute(sql_query)

    # Fetch all results
    results = cursor.fetchall()

    # Specify the output CSV file name
    output_csv_file = "filtered_chordate_species.csv"

    # Write the results to a new CSV file
    with open(output_csv_file, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the header (column names)
        csv_writer.writerow(["Common Name", "Species", "Genus", "Family", "Order", "Class", "Phylum"])

        # Write each row of filtered data
        for row in results:
            csv_writer.writerow(row)

    print(f"Filtered data written to {output_csv_file} successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # Close the cursor and connection if they were created
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
