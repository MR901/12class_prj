
import time
import random
import datetime 
''' ## Download and install MySql from 
https://dev.mysql.com/downloads/
https://stackoverflow.com/questions/10577374/mysql-command-not-found-in-os-x-10-7
https://stackoverflow.com/questions/10299148/mysql-error-1045-28000-access-denied-for-user-billlocalhost-using-passw

Installation Steeps
    pip3 install mysql-connector-python
    if doesn't work: pip3 install mysql-connector-python-rf
    export PATH=${PATH}:/usr/local/mysql/bin
    
'''
import mysql.connector


## MODULE TO CHECK MYSQL CONNECTIVITY
def connect_to_mysql_db(username, password, db_name='HotelManagementSystem'):
    ''' Connect to MySql'''
    try:
        ## create connection
        connect = mysql.connector.connect(
            host='localhost', user=username, passwd=password, 
            auth_plugin='mysql_native_password'
        )
        
        ## create DB if not present
        cursor = connect.cursor()
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db_name}')
        cursor.execute('COMMIT')
        cursor.close()
        
        ## create connection with db
        connect = mysql.connector.connect(
            host='localhost', user=username, passwd=password, 
            database=db_name,
            auth_plugin='mysql_native_password'
        )
        print('Connection to MySql is Established. "{}" db initialized.'.format(
            connect.database))
        
        return connect
    except mysql.connector.Error as err:
        print('Connection Failed. Something went wrong: {}'.format(err))
        print('Exiting.')
        exit()

def create_table_and_assign_some_dummy_data(connect):
    ##. create table if not exist
    ## Table 1: Booking
    create_table_query = '''CREATE TABLE IF NOT EXISTS BOOKING_DETAILS( 
        NAME VARCHAR(255), PHONE_NO VARCHAR(255), ADDRESS VARCHAR(255), 
        CHECK_IN_DATE VARCHAR(255), CHECK_OUT_DATE VARCHAR(255), 
        ROOM_TYPE VARCHAR(255), DAYS_STAY VARCHAR(255), COST_PER_DAY VARCHAR(255), 
        ROOM_NO VARCHAR(255), BOOKING_ID VARCHAR(255) ) '''
    cursor = connect.cursor()
    cursor.execute(create_table_query)
    cursor.close()
    
    ## Table 2: Restraurant
    # create_table_query = ''''''
    # cursor = connect.cursor()
    # cursor.execute(create_table_query)
    # cursor.close()
    
    ## adding some data
    insert_query_b = '''INSERT INTO BOOKING_DETAILS VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    values = (
        'Mohit', '9898912345', 'Chandi Chowk, Delhi 110006', '01/03/2021',
        '01/04/2021', 'Standard AC', '31', '4000', '404', '89121778449'
        )
    cursor = connect.cursor()
    cursor.execute(insert_query_b, values)
    cursor.close()

    values = (
        'Bhanu', '9845612345', 'Punjabi Bagh, Delhi', '05/03/2021',
        '05/04/2021', 'Standard AC', '31', '4000', '302', '98667535722'
        )
    cursor = connect.cursor()
    cursor.execute(insert_query_b, values)
    cursor.close()

    values = (
        'Madhu', '9898574345', 'Dilshad Colony, Delhi', '05/03/2021',
        '10/03/2021', '3-Bed Non-AC', '5', '4500', '208', '58182823965'
        )
    cursor = connect.cursor()
    cursor.execute(insert_query_b, values)
    cursor.close()

    values = (
        'Sumit', '8935912345', 'Model Town, Delhi', '02/03/2021',
        '19/03/2021', 'Standard AC', '17', '4000', '310', '11190965021'
        )
    cursor = connect.cursor()
    cursor.execute(insert_query_b, values)
    cursor.close()

    values = (
        'Neelam', '9898912345', 'Rajiv Chowk, Delhi', '02/03/2021',
        '07/03/2021', '3-Bed Non-AC', '5', '4500', '205', '59888180311'
        )
    cursor = connect.cursor()
    cursor.execute(insert_query_b, values)
    cursor.close()


## 1. option
def is_date_valid(date_str):
    ''' date_str format: dd/mm/yyyy 
    '01/02/2021', '1/02/2021', '1/2/2021' > are okay
    '1/22/2021' > is not
    '''
    try:
        datetime.datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except:
        print(date_str)
        return False

def is_date2_after_date1(date1_str, date2_str):
    ''' date_str format: dd/mm/yyyy 
        '01/02/2021', '01/02/2021' > True (same day checkout is acceptable)
        '01/02/2021', '01/03/2021' > True
        '01/03/2021', '01/02/2021' > False
    '''
    difference = ( datetime.datetime.strptime(date2_str, '%d/%m/%Y') - 
                  datetime.datetime.strptime(date1_str, '%d/%m/%Y'))
    return difference.days >= 0, difference.days
    
def get_booking_information(): 
    '''  '''
    print('-'*93)
    print('\tBOOKING ROOMS') 
    print('-'*93)
    print()
    print('Please Enter')
    
    ## getting "Name"
    while True: 
        booking_name = input('\n\tName: ')
        if booking_name!="":
            break
        else:
            print('\t"Name" cannot be empty. Please re-enter.')
    
    ## getting "Phone No."
    while True: 
        booking_ph = input('\n\tPhone No.: ')
        for c in booking_ph:
            valid = c in ' +0123456789'
                
        if len(booking_ph)>=8 and (valid is True):
            break
        elif len(booking_ph)>=8 and (valid is False):
            print('\t"Phone No." is not Valid. Please re-enter.')
        else:
            print('\t"Phone No." seems to be missing some digits. Please re-enter.')
            
    ## getting "Address"
    while True: 
        booking_add = input('\n\tAddress: ')
        if booking_add!="":
            break
        else:
            print('\t"Address" cannot be empty. Please re-enter.')
    
    ## getting "Check-In"
    while True: 
        booking_ch_in = input('\n\tCheck-In date in dd/mm/yyyy format: ')
        if is_date_valid(booking_ch_in):
            break
        else:
            print('\t"Check-In date" is not valid. Please re-enter.')

    ## getting "Check-Out"
    while True: 
        booking_ch_out = input('\n\tCheck-Out date in dd/mm/yyyy format: ')
        if is_date_valid(booking_ch_out):
            is_date_allowed, days_stay = is_date2_after_date1(booking_ch_in, booking_ch_out)
            if is_date_allowed:
                break
            else:
                print('\t"Check-Out" date is should be either same for after "Check-in" date. Please re-enter.')
        else:
            print('\t"Check-Out" date is not valid. Please re-enter.')
            
    ## get Room Type
    li = [ 
        ('Details on Room', None), 
        ('Standard Non-AC (Cost: Rs. 3500 per day)', 3500),
        ('Standard AC (Cost: Rs. 4000 per day)', 4000), 
        ('3-Bed Non-AC (Cost: Rs. 4500 per day)', 4500), 
        ('3-Bed AC (Cost: Rs. 5000 per day)', 5000)
    ]
    print('\n\tSelect Room Type from the following option.')
    for i in range(len(li)):
        print('\tPress '+ str(i)+' for '+ li[i][0])
    while True:
        choice=input('\tType the respective key and hit Enter:')
        if (len(choice)!=1) or (choice[0] not in '01234'):
            print('\tWrong Input provided. Please Re-Enter.')
        elif (len(choice)==1) and (choice[0]=='0'):
            rooms_info()
            print('\n\tSelect Room Type from the following option.')
            for i in range(len(li)):
                print('\t\tPress '+ str(i)+' for '+ li[i])
        else:
            booking_room_type, cost = li[int(choice[0])]
            print('\tSelected Room Type: {} for {} days at Rs {} per day'.format(booking_room_type, days_stay, cost))
            break
    
    print('\nRedirecting to Payment Screen...')
    time.sleep(3)
    print('-'*93) 
    
    return booking_name, booking_ph, booking_add, booking_ch_in, booking_ch_out, days_stay, cost, booking_room_type

def get_room_and_booking_id(booked_rooms=[], booking_ids=[]):
    ''' '''
    print('-'*95)
    print('\t Room has been Booked Succsfully.')
    print('-'*95)
    
    ## randomly generating room no. and booking id
    while True:
        booked_room = 100*random.randint(1,6) + random.randint(0,30) # 1-6 floor and 30 rooms on each
        if booked_room not in booked_rooms:
            break
    while True:
        booking_id = random.randint(10**10, 10**11)
        if booking_id not in booking_ids:
            break
    
    print('Allotted Room No. :', booked_room) 
    print('Booking ID        :', booking_id) 
    
    return booked_room, booking_id

## 2. option
def rooms_info(): 
    print()
    print('-'*93) 
    print('\tHOTEL ROOMS INFO') 
    print('-'*93) 
    print('''
    1. Standard Non-AC:  
       The Standard Non-AC Rooms  Provides  you the  Economic  way  of  the  accommodation. 
       The economic class also gives you  the pleasant experience, with greater facilities. 
       These  rooms are  more spacious  laid  out neatly  with a simple  decor  give  more 
       comfortable. The bathroom is designed more spacious and complete amenities make this 
       room more elegant.
       Room amenities include: 
           - 1 Double Bed, 
           - Television, 
           - Telephone, 
           - Double-Door Cupboard, 
           - 1 Coffee table with 2 sofa, 
           - Balcony and
           - an attached washroom with hot/cold water.
       ''')
    print('''
    2. Standard AC:
       Each Standard Ac Room is appointed with great facilities. The rooms are  moderately 
       designed with all essentialities to make a comfortable accommodation. They are calm, 
       peaceful and well ventilated. Snug and cozy, they have amenities like AC, telephone, 
       TV and cane swing.
       Room amenities include: 
           - 1 Double Bed, 
           - Television, 
           - Telephone, 
           - Double-Door Cupboard, 
           - 1 Coffee table with 2 sofa, 
           - Balcony,
           - an attached washroom with hot/cold water and
           - Window/Split AC.
       ''') 
    print('''
    3. 3-Bed Non-AC:  
       The Standard Non-AC Rooms Provides you the  Economic  way  of  the  accommodation. 
       The economic class also gives you the pleasant experience, with greater facilities. 
       These  rooms are  more spacious  laid  out neatly  with a simple  decor  give  more 
       comfortable. The bathroom is designed more spacious and complete amenities make this 
       room more elegant. With Extra Bed.
       Room amenities include: 
           - 1 Double Bed, 
           - Television, 
           - Telephone, 
           - Double-Door Cupboard, 
           - 1 Coffee table with 2 sofa, 
           - Balcony and
           - an attached washroom with hot/cold water.
       ''')
    print('''
    4. 3-Bed AC:
       Each Standard Ac Room is appointed with great facilities. The rooms are  moderately 
       designed with all essentialities to make a comfortable accommodation. They are calm, 
       peaceful and well ventilated. Snug and cozy, they have amenities like AC, telephone, 
       TV and cane swing. With Extra Bed.
       Room amenities include: 
           - 1 Double Bed, 
           - Television, 
           - Telephone, 
           - Double-Door Cupboard, 
           - 1 Coffee table with 2 sofa, 
           - Balcony,
           - an attached washroom with hot/cold water and
           - Window/Split AC.
       ''')
    print('-'*93) 

## 4 option
def show_qr_code():
    ''' dummy '''
    print('\tPlease Scan this code to make payment. Waiting for receiving payment.\n')
    char = '!#*+=-:}{[|@]&^%~>?'
    for i in range(15):
        temp_li = []
        for j in range(30):
            temp_li.append(char[random.randint(0,len(char)-1)])
        print('\t\t|', ''.join(temp_li), '|')
    time.sleep(10)

def payment(bill_recipt, final_amount):
    ''' for_what: 'room_booking', 'restaurant' '''
    print()
    print('-'*93) 
    print('\tPAYMENT SCREEN')
    print('-'*93)
    
    print('\t  Bill Receipt')
    print('\t','-'*40)
    print(bill_recipt)
    print('\t','-'*40)
    print('\t  Total Amount:', final_amount)
    print('\t','-'*40)
    
    print('\n\tPlease Select Mode of Payment')
    li = [ 'Credit/Debit Card', 'Netbanking', 'UPI', 'Cash']
    for i in range(len(li)):
        print('\t\tPress '+ str(i+1)+' for '+ li[i])
    
    ## get input
    while True:
        choice=input('\t\tType the respective key and hit Enter: ')
        print()
        if (len(choice)!=1) or (choice[0] not in '1234'):
            print('\t\tWrong Input provided. Please Re-Enter.')
        elif (len(choice)==1) and (choice[0] in '12'):
            print('\t\tThis service is not available at the moment. Please re-select.')
        else:
            break
    
    if choice[0]=='3':
        show_qr_code()
    elif choice[0]=='4':
        print('\tPlease hand over the money to cashier.')
    
    print('\tWaiting for payment to be made.')
    time.sleep(7)    
    
    ## random
    if random.randint(1,15) >= 2:
        print('\n\n\tPayment Received. Thank You.')
        print('\tProceding... ') 
        time.sleep(4)
        print('-'*93) 
        return True ## payment sucessful
    else:
        print('\n\n\tPayment Failed. Redirecting ...')
        time.sleep(4)
        print('-'*93) 
        return False

## 5 option
def show_restaurant_menu():
    ''' '''
    print('\t-------------------------------------------------------------------------') 
    print('\t                        Restaurant Menu Card') 
    print('\t-------------------------------------------------------------------------') 
    print('\n\t BEVARAGES                             26 Dal Fry................ 180.00') 
    print('\t----------------------------------     27 Dal Makhani............ 180.00') 
    print('\t  1 Regular Tea............. 20.00     28 Dal Tadka.............. 180.00') 
    print('\t  2 Masala Tea.............. 25.00') 
    print('\t  3 Coffee.................. 25.00     ROTI') 
    print('\t  4 Cold Drink.............. 25.00    -----------------------------------') 
    print('\t  5 Bread Butter............ 30.00     29 Plain Roti.............. 15.00') 
    print('\t  6 Bread Jam............... 30.00     30 Butter Roti............. 20.00') 
    print('\t  7 Veg. Sandwich........... 60.00     31 Tandoori Roti........... 25.00') 
    print('\t  8 Veg. Toast Sandwich..... 60.00     32 Butter Naan............. 25.00') 
    print('\t  9 Cheese Toast Sandwich... 70.00') 
    print('\t 10 Grilled Sandwich........ 70.00     RICE') 
    print('\t                                      -----------------------------------') 
    print('\t SOUPS                                 33 Plain Rice............. 100.00') 
    print('\t----------------------------------     34 Jeera Rice............. 120.00') 
    print('\t 11 Tomato Soup............ 130.00     35 Veg Pulao.............. 150.00') 
    print('\t 12 Hot & Sour............. 130.00     36 Peas Pulao............. 150.00') 
    print('\t 13 Veg. Noodle Soup....... 130.00') 
    print('\t 14 Sweet Corn............. 130.00     SOUTH INDIAN') 
    print('\t 15 Veg. Munchow........... 130.00    -----------------------------------') 
    print('\t                                       37 Plain Dosa............. 100.00') 
    print('\t MAIN COURSE                           38 Onion Dosa............. 110.00') 
    print('\t----------------------------------     39 Masala Dosa............ 130.00') 
    print('\t 16 Shahi Paneer........... 140.00     40 Paneer Dosa............ 130.00') 
    print('\t 17 Kadai Paneer........... 140.00     41 Rice Idli.............. 130.00') 
    print('\t 18 Handi Paneer........... 160.00     42 Sambhar Vada........... 140.00') 
    print('\t 19 Palak Paneer........... 160.00') 
    print('\t 20 Chilli Paneer.......... 180.00     ICE CREAM') 
    print('\t 21 Matar Mushroom......... 180.00    -----------------------------------') 
    print('\t 22 Mix Veg................ 180.00     43 Vanilla................. 80.00') 
    print('\t 23 Jeera Aloo............. 180.00     44 Strawberry.............. 80.00') 
    print('\t 24 Malai Kofta............ 180.00     45 Pineapple............... 90.00') 
    print('\t 25 Aloo Matar............. 180.00     46 Butter Scotch........... 90.00') 
    print('\t-------------------------------------------------------------------------') 
    print('\tType 0x0 to return to Home Screen ') 
    
    menu_li = [
        (1, 'Regular Tea', 20.0),
        (2, 'Masala Tea', 25.0),
        (3, 'Coffee', 25.0),
        (4, 'Cold Drink', 25.0),
        (5, 'Bread Butter', 30.0),
        (6, 'Bread Jam', 30.0),
        (7, 'Veg. Sandwich', 60.0),
        (8, 'Veg. Toast Sandwich', 60.0),
        (9, 'Cheese Toast Sandwich', 70.0),
        (10, 'Grilled Sandwich', 70.0),
        (11, 'Tomato Soup', 130.0),
        (12, 'Hot & Sour', 130.0),
        (13, 'Veg. Noodle Soup', 130.0),
        (14, 'Sweet Corn', 130.0),
        (15, 'Veg. Munchow', 130.0),
        (16, 'Shahi Paneer', 140.0),
        (17, 'Kadai Paneer', 140.0),
        (18, 'Handi Paneer', 160.0),
        (19, 'Palak Paneer', 160.0),
        (20, 'Chilli Paneer', 180.0),
        (21, 'Matar Mushroom', 180.0),
        (22, 'Mix Veg', 180.0),
        (23, 'Jeera Aloo', 180.0),
        (24, 'Malai Kofta', 180.0),
        (25, 'Aloo Matar', 180.0),
        (26, 'Dal Fry', 180.0),
        (27, 'Dal Makhani', 180.0),
        (28, 'Dal Tadka', 180.0),
        (29, 'Plain Roti', 15.0),
        (30, 'Butter Roti', 20.0),
        (31, 'Tandoori Roti', 25.0),
        (32, 'Butter Naan', 25.0),
        (33, 'Plain Rice', 150.0),
        (34, 'Jeera Rice', 150.0),
        (35, 'Veg Pulao', 150.0),
        (36, 'Peas Pulao', 150.0),
        (37, 'Plain Dosa', 100.0),
        (38, 'Onion Dosa', 110.0),
        (39, 'Masala Dosa', 130.0),
        (40, 'Paneer Dosa', 130.0),
        (41, 'Rice Idli', 130.0),
        (42, 'Sambhar Vada', 140.0),
        (43, 'Vanilla', 80.0),
        (44, 'Strawberry', 80.0),
        (45, 'Pineapple', 90.0),
        (46, 'Butter Scotch', 90.0),
    ]
    return menu_li

def get_order_from_restaurant():
    ''' ''' 
    menu = show_restaurant_menu()
    while True:
        choice=input('Type the respective key x quantity seperated by blankspace. eg 1x1 4x1 5x3 \nand hit Enter: ')
        try:
            choice = [ (int(e.split('x')[0]), int(e.split('x')[1])) for e in choice.split() if len(e)>0 ]
            if (len(choice)==0):
                print('Wrong Input provided. Please Re-Enter.')
            elif max([ m_id for m_id, quantity in choice ])>46:
                print('Wrong Input provided. Please Re-Enter.')
            else:
                break
        except:
            print('Wrong Input provided. Please Re-Enter.')

    if (0,0) in choice:
        print('Redirecting to Home Screen...')
        time.sleep(3)

    ## calculating the order
    receipt = 'Order Summary from the restaurant.'
    cost = 0
    for m,name,cost in menu:
        for i in range(len(choice)):
            if m == choice[i][0]:
                receipt += '\n\tItem: '+name+'\t\tPrice: '+str(cost)+'\t\tQuantity: '+str(choice[i][1])
                cost += cost * choice[i][1]
    return receipt, cost

## 6 option
def show_record(connect): 
    
    print('-'*93) 
    print('\tHOTEL RECORDS') 
    print('-'*93) 
    
    li = [ 'to show all records', 'Name', 'Phone No.', 'Booking ID']
    print('\n\tSearch records based on')
    for i in range(len(li)):
        print('\tPress '+ str(i)+' for '+ li[i])
    while True:
        choice=input('\tType the respective key and hit Enter:')
        if (len(choice)!=1) or (choice[0] not in '0123'):
            print('\tWrong Input provided. Please Re-Enter.')
        else:
            break
    if choice[0]!='0':
        value = input('\tEnter the values for search:')
    if choice[0]=='0':
        condition = ''
    elif choice[0]=='1':
        condition = ' WHERE NAME="{}"'.format(value)
    elif choice[0]=='2':
        condition = ' WHERE PHONE_NO="{}"'.format(value)
    elif choice[0]=='3':
        condition = ' WHERE BOOKING_ID="{}"'.format(value)
    
    select_query = '''SELECT * FROM BOOKING_DETAILS {}'''.format(condition)
    print('---|', select_query)
    cursor = connect.cursor()
    cursor.execute(select_query)
    results = cursor.fetchall()
    cursor.close()
    
    # checks if any record exists or not 
    if len(results)==0:
        print('No Records Found')
    else: 
        print('| Name\t | Phone No. | Address\t\t | Check-In | Check-Out\t | Room Type\t | Price\t | DAYS STAY\t | Cost per day | Room No\t | Booking Id |') 
        print('-'*83) 
        for record in results: 
            print('|%s \t| %s \t| %s \t\t| %s \t| %s \t| %s \t| %s \t| %s \t| %s \t| %s'%record)
        print('-'*83) 


## main
def home_screen(connect): 
    
    ## Printing Msg
    print('\n\n')
    print('-'*93) 
    print('\t\t\tWELCOME TO HOTEL') 
    print('-'*93) 
    print()
    
    print('Please from the following options to proceed.')
    li = [ 'Room Booking', 'Rooms Info', 'Room Service(Menu Card)', 'Additional Tip Payment', 'Record', 'Exit']
    for i in range(len(li)):
        print('Press '+ str(i+1)+' for '+ li[i])
    
    ## get input
    while True:
        choice=input('Type the respective key and hit Enter: ')
        print()
        print('-'*93) 
        print()
        if (len(choice)!=1) or (choice[0] not in '123456'):
            # print('Wrong input provided. Hence Exiting.')
            # time.sleep(5); exit()
            print('Wrong Input provided. Please Re-Enter.')
        else:
            break
    
    ## Performing Task
    if choice[0]=='1':
        occupied_rooms = [] ## get this from db
        alloted_booking_ids = [] ## get this from db
        b_name, b_ph, b_add, b_ch_in, b_ch_out, b_stay, cost, b_room_type = get_booking_information() 
        if b_stay == 0:
            print('\tNote: Same day checkout will also incure the cost of single day.')
            b_stay = 1 
        bill_recipt = f'''
        Booking Details:
            Name           : {b_name}
            Phone No.      : {b_ph}
            Address        : {b_add}
            Check-in Date  : {b_ch_in}
            Check-out Date : {b_ch_out}
            Stay Duration  : {b_stay} days
            Room Type      : {b_room_type} 
            Cost of Room   : Rs. {cost} per day'''
        room_final_amount = b_stay * cost
        payment_success = payment(bill_recipt, room_final_amount)
        
        ## get data from DB
        select_query = '''SELECT ROOM_NO FROM BOOKING_DETAILS'''
        cursor = connect.cursor()
        cursor.execute(select_query)
        myresult1 = cursor.fetchall()
        cursor.close()
        select_query = '''SELECT BOOKING_ID FROM BOOKING_DETAILS'''
        cursor = connect.cursor()
        cursor.execute(select_query)
        myresult2 = cursor.fetchall()
        cursor.close()
        booked_rooms = [ e[0] for e in myresult1 ]
        booking_ids = [ e[0] for e in myresult2 ]
        booked_rooms, booking_ids = [], []
        
        if payment_success:
            b_room, b_id = get_room_and_booking_id(booked_rooms, booking_ids)
        else:
            ## retry
            payment_success = payment(bill_recipt, room_final_amount)
            if payment_success:
                b_room, b_id = get_room_and_booking_id(booked_rooms=[], booking_ids=[])
            else:
                print('There\'s some error, Restarting from Home Screen.')
                home_screen()
        print('\t HAPPY STAY')
        
        ## Add entry to DB
        insert_query_b = '''INSERT INTO BOOKING_DETAILS VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        values = ( b_name, b_ph, b_add, b_ch_in, b_ch_out, b_room_type, b_stay, cost, b_room, b_id)
        cursor = connect.cursor()
        cursor.execute(insert_query_b % values)
        cursor.close()
        home_screen(connect)
        
    elif choice[0]=='2': 
        rooms_info() 
        home_screen(connect)
        
    elif choice[0]=='3': 
        receipt, cost = get_order_from_restaurant() 
        payment_success = payment(receipt, cost)
        if payment_success:
            print('Enjoy your Meal.')
        else:
            ## retry
            payment_success = payment(receipt, cost)
            if payment_success:
                print('Enjoy your Meal.')
            else:
                print('There\'s some error, Restarting from Home Screen.')
        home_screen(connect)

    elif choice[0]=='4': 
        ## tip
        while True:
            try:
                amount = float(input('Please Enter the Amount you want to tip'))
                break
            except:
                print('Please re-enter the amount in digits')
            
        payment('\t\tTip Amount: {}'.format(amount), amount) 
        home_screen(connect)

    elif choice[0]=='5': 
        show_record(connect)
        home_screen(connect)

    elif choice[0]=='6': 
        print('Exiting the portal. ')
        time.sleep(3); exit()


if __name__=="__main__":
    ## Connect to DB        
    print('-'*93) 
    print('LOGIN TO DB')
    print('-'*93) 
    while True:
        try:
            username = input('\n Enter MySql Server\'s Username : ')
            password = input('\n Enter MySql Server\'s Password : ')
            # username, password = 'root::admin@123'.split('::')
            connect = connect_to_mysql_db(username, password, 'hotelmanagement')

            ## Clean Table
            select_query = '''DROP TABLE BOOKING_DETAILS'''
            cursor = connect.cursor()
            cursor.execute(select_query)
            cursor.close()

            ## Creating Table and adding somee dummy data
            create_table_and_assign_some_dummy_data(connect)
            break
        except:
            print('Unable to connect. Please re-enter the details.')
    print()
    print('-'*93) 
    print()
    home_screen(connect)
