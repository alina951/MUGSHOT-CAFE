
import csv
import pprint
import connect
import pandas as pd

#loading data into a dataframe
filename = 'Data/leeds_09-05-2023_09-00-00.csv'
keys = ('Date and time', 'Location','Name', 'Order', 'Total', 'Payment Type', 'Card Number')
with open (filename, 'r') as data:
    reader = csv.DictReader(data,keys)
    mugshot = list()
    for row in reader:
        mugshot.append(row)

# filename = 'Data/leeds_09-05-2023_09-00-00.csv'
# keys = ('Date and time', 'Location','Name', 'Order', 'Total', 'Payment Type', 'Card Number')
# mugshot = pd.read_csv(filename,names = keys)
# print(mugshot)

# #transform stage
# #Removing sensative data
# mugshot = mugshot.drop(columns=['Name', 'Card Number'])

# print(mugshot)
#Splitting Date and Time
# mugshot['Date'] = pd.to_datetime(mugshot['Date and time']).dt.date
# mugshot['Time'] = pd.to_datetime(mugshot['Date and time']).dt.time
# #Dropping the redundant 'Date and time' column
# mugshot = mugshot.drop(columns=['Date and time'])
# print(mugshot)

#
def remove_sens_data(input_data_list : list,sens_data_keys:list):
    for dicts in input_data_list:
        for key in sens_data_keys:
            if key in dicts:
                del dicts[key]

def split_date_time(input_data_list : list):
    for dicts in input_data_list:
        dt_temp = dicts["Date and time"]
        date = dt_temp[0:10]
        time = dt_temp[11:16]
        dicts["Date"] = date
        dicts["Time"] = time
        del dicts["Date and time"]
#Splitting orders into name , price and quantity

def split_order(input_data_list : list):
    for dicts in input_data_list:
        product_dupe_tag = 0
        order_dicts_list=[]
        split_order_list = dicts["Order"].split(", ")
        for orders in split_order_list:
            product_dupe_tag = 0
            #order_list.append(orders.split(" - "))
            templist = orders.split(" - ")
            if len(templist)>2:
                price = templist[len(templist)-1]
                name = ""
                for items in templist:  
                    if items != price:
                        name += items
                    name +=" "
                    name.rstrip()
            else:
                name = templist[0]
                price = templist[1]
            for products in order_dicts_list:
                if products["Name"] == name:
                    products["Quantity"] = products["Quantity"] + 1
                    product_dupe_tag=1
            if product_dupe_tag !=1:
                quantity = 1
                order_dicts_list.append({"Name":name,"Price":price,"Quantity":quantity})
                product_dupe_tag = 0

        dicts["Order_dict"] = order_dicts_list
        del dicts["Order"]
def insert_data_into_db(connection, transactions_data):
    #try:
        with connection.cursor() as cursor:
            for index,transaction in transactions_data.iterrows():
                # insert into transactions table
                insert_transaction_sql = """
                INSERT INTO transactions (date, time, city, total_cost, payment_method)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_transaction_sql, (
                    transaction.get('Date'),
                    transaction.get('Time'),
                    transaction.get('Location'),
                    transaction.get('Total'),
                    transaction.get('Payment Type')
                ))
                #connection.commit()
                # Retrieve the transaction_id of the newly inserted transaction
                select_transaction_sql = "SELECT transaction_id FROM transactions WHERE date = %s and time = %s"
                cursor.execute(select_transaction_sql, (transaction.get("Date"),transaction.get('Time'),))
                transaction_id = cursor.fetchone()

                for product in transaction.get('Order_dict'):
                    product_name = product.get('Name')
                    product_price = product.get('Price')
                    product_quantity = product.get('Quantity')

                    # check if the product already exists in products table
                    select_product_sql = "SELECT product_id FROM products WHERE product_name = %s"
                    try: 
                        cursor.execute(select_product_sql, (product_name,))
                        result = cursor.fetchone()
                    except Exception as e:
                        print(f'Error {e}')
                        print('error here')
                        connection.rollback()

                    if result:
                        product_id = result[0]
                        

                    else:
                        # Insert product into products table
                        insert_product_sql = "INSERT INTO products (product_name, product_price) VALUES (%s, %s)"
                        cursor.execute(insert_product_sql, (product_name, product_price))
                        select_product_id_sql = "SELECT product_id FROM products WHERE product_name = %s and product_price = %s"
                        cursor.execute(select_product_id_sql, (product_name,product_price))
                        product_id = cursor.fetchone()
                        

                    # Insert into order_items table
                    insert_order_item_sql = """
                    INSERT INTO order_items (transaction_id, product_id, product_quantity)
                    VALUES (%s, %s, %s)
                    """
                    try:
                        cursor.execute(insert_order_item_sql, [transaction_id, product_id, product_quantity])
                    except:
                        print("key already exists")

                connection.commit()
                print(f"Transaction {transaction_id} successfully inserted into database.")

connection = connect.connect()

if connection:
    
    remove_sens_data(mugshot,['Name','Card Number'])
    split_date_time(mugshot)
    split_order(mugshot)
    df = pd.DataFrame(mugshot)
    
    print(df[["Date"]])
    print(df.loc[0][["Date"]])
    insert_data_into_db(connection, df)
    #for index, transaction in df.iterrows():
    #    for product in transaction.get('Order_dict'):
    #        i = product.get('Name')
    #        print(i)
    
    # Close the database connection
    connection.close()
#remove_sens_data(mugshot,['Name','Card Number'])
#split_date_time(mugshot)
#split_order(mugshot)
#df = pd.DataFrame(mugshot)
#print(df)