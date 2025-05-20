# Author: Dhaval Patel. Codebasics YouTube Channel

import mysql.connector
from mysql.connector import Error
global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0875",
    database="pandeyji_eatery"
)

# Function to call the MySQL stored procedure and insert an order item
def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()

        # Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        # Committing the changes
        cnx.commit()

        # Closing the cursor
        cursor.close()

        print("Order item inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1

# Function to insert a record into the order_tracking table
def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    cnx.commit()

    # Closing the cursor
    cursor.close()

def get_total_order_price(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to get the total order price
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    return result

# Function to get the next available order_id
def get_next_order_id():
    cursor = cnx.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1

# Function to fetch the order status from the order_tracking table
def get_order_status(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to fetch the order status
    query = f"SELECT status FROM order_tracking WHERE order_id = %s"
    cursor.execute(query, (order_id,))

    # Fetching the result
    result = cursor.fetchone()

    # Closing the cursor
    cursor.close()

    # Returning the order status
    if result:
        return result[0]
    else:
        return None

def insert_reservation(time: str, number_of_people: int):
    try:
        cursor = cnx.cursor()

        query = "INSERT INTO reservations (reservation_time, number_of_people) VALUES (%s, %s)"
        cursor.execute(query, (time, number_of_people))
        cnx.commit()

        table_id = cursor.lastrowid
        cursor.close()

        return table_id
    except Exception as e:
        print("❌ ERROR in insert_reservation():", str(e))
        return -1

if __name__ == "__main__":
    # print(get_total_order_price(56))
    # insert_order_item('Samosa', 3, 99)
    # insert_order_item('Pav Bhaji', 1, 99)
    # insert_order_tracking(99, "in progress")
    print(get_next_order_id())

""""
select * from pandeyji_eatery.food_items;

UPDATE pandeyji_eatery.food_items
SET price = 10
WHERE item_id =9

DELETE from pandeyji_eatery.food_items
where item_id=41;

UPDATE pandeyji_eatery.food_items
SET item_id =20
WHERE item_id=120;

INSERT INTO pandeyji_eatery.food_items VALUES(41,'Spring Roll',80);
INSERT INTO pandeyji_eatery.food_items VALUES(11, 'Noodles',80);
INSERT INTO pandeyji_eatery.food_items (item_id, name, price)VALUES(12, 'Rajma Chawal',80),(13, 'Chole Chawal',80),(14, 'Kadhi Chawal',80);
INSERT INTO pandeyji_eatery.food_items (item_id, name, price)VALUES(15, 'Momos',50),(16, 'Chilli Potato',100),(17, 'Pasta',100),(18, 'Thali',150),(19, 'Chaap',200),(120, 'Roti',10),(21, 'Naan',25);
INSERT INTO pandeyji_eatery.food_items (item_id, name, price)VALUES(22, 'Paneer Curry',200),(23, 'Fried Rice',100),(24, 'Cold Coffee',100),(25, 'Ice Cream',60),(26, 'Frech fries',60),(27, 'Burger',50),(28, 'Vada Pav',40);
INSERT INTO pandeyji_eatery.food_items (item_id, name, price)VALUES(29, 'Golgappe',40),(30, 'Salad',100),(31, 'Idli',100),(32, 'Sandwich',60),(33, 'Garlic Bread',80),(34, 'Roll',80),(35, 'Nachos',150);
INSERT INTO pandeyji_eatery.food_items (item_id, name, price)VALUES(36, 'Dal Makhni',150),(37, 'Jalebi',80),(38, 'Gulab Jamun',80),(39, 'Rasmalai',100),(40, 'Kachori',40);
"""