import sqlite3
db_name = "measurements.db"
def get_connection():
    return sqlite3.connect(db_name)
def create_table():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""create table if not exists measurements(date text, fasting_glucose real, water_glasses integer, steps integer, carbs integer)""")
        cursor.execute("""create table if not exists hba1c(date text, value real)""")
        cursor.execute("""create table if not exists weight(date text, kg real)""")
def welcome():
    name = input("Enter your name: ")
    print(f"\nHello, {name}!")
def add():
    date = input("Add date(YYYY-MM-DD):")
    fasting_glucose = float(input("Add glucose value:"))
    water_glasses = int(input("Add water glasses:"))
    steps = int(input("How many steps today:"))
    carbs = int(input("How much grams of carbs:"))
    if any(x <= 0 for x in [fasting_glucose,water_glasses,steps,carbs]):
        print("Invalid value")
        return
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""insert into measurements(date, fasting_glucose, water_glasses, steps, carbs)values(?, ?, ?, ?, ?)""",(date,fasting_glucose,water_glasses,steps,carbs))
def add_hba1c():
    date = input("Enter date YYYY-MM-DD(once in 3 months): ")
    while True:
        try:
            value = float(input("Enter HbA1c value: "))
            break
        except ValueError:
            print("Invalid value")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""insert into hba1c(date,value) values(?, ?)""",(date,value))
def add_weight():
    date = input("Enter date YYYY-MM-DD(once a month): ")
    while True:
        try:
            kg = float(input("Enter weight: "))
            break
        except ValueError:
            print("Invalid value")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""insert into weight(date,kg) values(?, ?)""",(date,kg))
def glycemia_state(fasting_glucose):
    if fasting_glucose < 70:
        return "Hipoglycemia"
    elif fasting_glucose <=130:
        return "Normal"
    else:
        return "Hyperglycemia"
def hba1c_state(value):
    if value <= 7:
        return "Good control"
    else:
        return "Consult your doctor"
def display():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("select * from measurements")
        results = cursor.fetchall()
        pretty_print(results)
        if not results:
            print("No measurements found")
def display_hba1c():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("select * from hba1c")
        results = cursor.fetchall()
        pretty_print_hba1c(results)
def display_weight():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("select * from weight")
        results = cursor.fetchall()
        pretty_print_weight(results)
def get_all(table):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"select * from {table}")
        return cursor.fetchall()
def delete_record(table):
    results = get_all(table)
    for r in results:
        print(r)   
    date = input("What record do you want to delete?")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"delete from {table} where trim(date) = ?",(date,))
        print(cursor.rowcount)
        if cursor.rowcount > 0:
            print("Deleted successfully")
        else:
            print("No record found")
def modify():
    display()
    date = input("What measurement you want to modify?")
    with get_connection() as conn:
        cursor = conn.cursor()
        record = cursor.execute("select * from measurements where date = ?",(date, )).fetchone()
        new_fasting_glucose = input("New glucose:")
        new_water_glasses = input("New water glasses:")
        new_steps = input("New steps:")
        new_carbs = input("New carbs:")
        fasting_glucose = float(new_fasting_glucose) if new_fasting_glucose else record[1]
        water_glasses = int(new_water_glasses) if new_water_glasses else record[2]
        steps = int(new_steps) if new_steps else record[3]
        carbs = int(new_carbs) if new_carbs else record[4]
        cursor.execute("""update measurements set fasting_glucose = ?, water_glasses = ?, steps = ?, carbs = ? where date = ?""",(fasting_glucose,water_glasses,steps,carbs,date))
        if cursor.rowcount > 0:
            print("Updated successfully")
        else:
            print("No record found")
def modify_hba1c():
    display_hba1c()
    date = input("What record do you want to modify?")
    with get_connection() as conn:
        cursor = conn.cursor()
        record = cursor.execute("select * from hba1c where date = ?",(date,)).fetchone()
        if not record:
            print("No record found")
            return
        new_value = input("New HbA1c value:")
        while True:
            try:
                value = float(new_value) if new_value else record[1]
                break
            except ValueError:
                print("Invalid value")
        cursor.execute("update hba1c set value = ? where date = ?",(value,date))
        if cursor.rowcount > 0:
            print("Updated successfully")
        else:
            print("No record found")
def modify_weight():
    display_weight()
    date = input("What record you want to modify?")
    with get_connection() as conn:
        cursor = conn.cursor()
        record = cursor.execute("select * from weight where date = ?",(date,)).fetchone()
        if not record:
            print("No record found")
            return
        new_kg = input("Enter new weight:")
        while True:
            try:
                kg = float(new_kg) if new_kg else record[1]
                break
            except ValueError:
                print("Invalid value")
        cursor.execute("update weight set kg = ? where date = ?",(kg,date))
        if cursor.rowcount > 0:
            print("Updated successfully")
        else:
            print("No record found")
def highest_glucose():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("select max(fasting_glucose) from measurements")
        result = cursor.fetchone()
        print(f" Highest glucose:{result}")
def carbs_steps():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("select fasting_glucose from measurements where carbs = (select max(carbs) from measurements) and steps = (select min(steps) from measurements)")
        result = cursor.fetchone()
        print(result)
def avg_glucose():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("select avg(fasting_glucose) from measurements")
        result = cursor.fetchone()
        print(f"Average glucose: {result[0]}")
def hba1c_trend():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("select value from hba1c order by date desc limit 2")
        results = cursor.fetchall()
        if len(results) < 2:
            print("Not enough data")
            return
        last = results[0][0]
        previous = results[1][0]
        print(f"Last HbA1c:{last}%")
        print(f"Previous HbA1c:{previous}%")
        if last > previous:
            print("HbA1C increasing")
        elif last < previous:
            print("HbA1c improving")
        else:
            print("No change")
def weight_trend():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("select kg from weight order by date desc limit 2")
        results = cursor.fetchall()
        if len(results) < 2:
            print("Not enough data")
            return
        last = results[0][0]
        previous = results[1][0]
        print(f"Last weight :{last}kg")
        print(f"Previous weight:{previous}kg")
        if last > previous:
            print("Watch your weight")
        elif last < previous:
            print("Weight decreasing")
        else:
            print("No change")
def pretty_print(results):
    if not results:
        print("No data found")
        return
    for r in results:
        state = glycemia_state(r[1])
        print(f"""Date:{r[0]}|Glucose:{r[1]}mg/dl|Water:{r[2]}glasses|Steps:{r[3]}|Carbs:{r[4]}g""")
        if state != "Normal":
            print("Please consult your doctor\n")
            print("---------------------------")
def pretty_print_hba1c(results):
    if not results:
        print("No data found")
        return
    for r in results:
        state = hba1c_state(r[1])
        print(f"Date:{r[0]}|HbA1c:{r[1]}%|{state}")
def pretty_print_weight(results):
    if not results:
        print("No data found")
        return
    for r in results:
        print(f"Date:{r[0]}|Weight:{r[1]}kg")
create_table()
welcome()
while True:
    print(f"\n--- Diabetes Tracker ---")
    print(f"\n--- Measurements ---")
    print(f"\n1. Add measurements")
    print(f"2. Display measurements")
    print("3. Delete measurements")
    print(f"4. Modify measurements")
    print(f"\n--- HbA1c ---")
    print(f"5. Add HbA1c(once in 3 months)")
    print(f"6. Display HbA1c")
    print(f"7. Modify HbA1c")
    print(f"8. Delete HbA1c")
    print(f"\n--- Weight ---")
    print(f"9. Add weight(once a month)")
    print(f"10. Display weight")
    print(f"11. Modify weight")
    print(f"12. Delete weight")
    print(f"\n--- Analysis ---")
    print(f"13. Display highest glucose value")
    print(f"14. Display glucose when carbs are high and steps are low")
    print(f"15. Average glucose")
    print(f"16. HbA1c trend")
    print(f"17. Weight trend")
    print(f"0. Exit")
    option = input("Choose option:")
    if option == "1":
        add()
    elif option =="2":
        display()
    elif option == "3":
        delete_record("measurements")
    elif option == "4":
        modify()
    elif option == "5":
        add_hba1c()    
    elif option == "6":
        display_hba1c()
    elif option == "7":
        modify_hba1c()
    elif option == "8":
        delete_record("hba1c")
    elif option == "9":
        add_weight()
    elif option == "10":
        display_weight()
    elif option == "11":
        modify_weight()
    elif option == "12":
        delete_record("weight")
    elif option == "13":
        highest_glucose()
    elif option == "14":
        carbs_steps()
    elif option == "15":
        avg_glucose()
    elif option == "16":
        hba1c_trend()
    elif option == "17":
        weight_trend()
    elif option == "0":
        break
    else:
        print("Invalid option")





 