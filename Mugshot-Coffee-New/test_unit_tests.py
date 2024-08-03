import pytest

def remove_sens_data(input_data_list : list,sens_data_keys:list):
    try:
        for dicts in input_data_list:
            for key in sens_data_keys:
                if key in dicts:
                    del dicts[key]
    except:
        raise TypeError("invalid inputs use lists")

def split_date_time(input_data_list : list):
    try:
        for dicts in input_data_list:
            dt_temp = dicts["Date and time"]
            date = dt_temp[0:10]
            time = dt_temp[11:16]
            dicts["date"] = date
            dicts["time"] = time
            del dicts["Date and time"]
    except:
        raise TypeError("invalid inputs use lists")

def split_order(input_data_list : list):
    for dicts in input_data_list:
        split_order_list = dicts["Order"].split(", ")
        order_list = []
        for orders in split_order_list:
            order_list.append(orders.split(" - "))
        dicts["Order_list"] = order_list
        del dicts["Order"]

def test_remove_sens_data_raises_typeerror():
    with pytest.raises(Exception):
        remove_sens_data(1,1)

def test_remove_sens_data():
    data =[{'date_time' : "09/05/2023 09:00","location" :"Leeds",'name' : "Jerome Soper",'order' :"Regular Iced americano - 2.15, Large Hot Chocolate - 1.70, Regular Iced americano - 2.15, Large Filter coffee - 1.80",'total' : 7.8,'payment_type' :"CARD",'card_number' : 7925280230207247}]
    expected = [{'date_time' : "09/05/2023 09:00","location" :"Leeds",'order' :"Regular Iced americano - 2.15, Large Hot Chocolate - 1.70, Regular Iced americano - 2.15, Large Filter coffee - 1.80",'total' : 7.8,'payment_type' :"CARD"}]
    #act 
    actual = data
    remove_sens_data(actual,["card_number","name"])
    #assert pass
    print(actual)
    print(expected)
    assert actual == expected

def test_split_date_time_raises_typeerror():
    with pytest.raises(Exception):
        split_date_time(1)

def test_split_date_time():
    actual =[{'Date and time' : "09/05/2023 09:00","location" :"Leeds",'name' : "Jerome Soper",'order' :"Regular Iced americano - 2.15, Large Hot Chocolate - 1.70, Regular Iced americano - 2.15, Large Filter coffee - 1.80",'total' : 7.8,'payment_type' :"CARD",'card_number' : 7925280230207247}]
    expeted =[{"date": "09/05/2023","time": "09:00","location" :"Leeds",'name' : "Jerome Soper",'order' :"Regular Iced americano - 2.15, Large Hot Chocolate - 1.70, Regular Iced americano - 2.15, Large Filter coffee - 1.80",'total' : 7.8,'payment_type' :"CARD",'card_number' : 7925280230207247}]
    

    split_date_time(actual)

    assert actual == expeted

def test_split_order_raises_typeerror():
    with pytest.raises(Exception):
        split_order(1)

def test_split_order():
    actual =[{'Date and time' : "09/05/2023 09:00","location" :"Leeds",'name' : "Jerome Soper",'order' :"Regular Iced americano - 2.15, Large Hot Chocolate - 1.70, Regular Iced americano - 2.15, Large Filter coffee - 1.80",'total' : 7.8,'payment_type' :"CARD",'card_number' : 7925280230207247}]
    expeted =[{"date": "09/05/2023","time": "09:00","location" :"Leeds",'name' : "Jerome Soper",'order' :"Regular Iced americano - 2.15, Large Hot Chocolate - 1.70, Regular Iced americano - 2.15, Large Filter coffee - 1.80",'total' : 7.8,'payment_type' :"CARD",'card_number' : 7925280230207247}]


test_remove_sens_data_raises_typeerror()
test_remove_sens_data()
test_split_date_time()    
test_split_date_time_raises_typeerror()
test_split_order_raises_typeerror()
#Unit test for loading the data from csv
filename1 = 'Data/test_data.csv'
keys1 = ('Name', 'Colour', 'Age')
with open (filename1, 'r') as data:
    reader = csv.DictReader(data,keys1)
    test = list()
    for row in reader:
        test.append(row)
print(test)
