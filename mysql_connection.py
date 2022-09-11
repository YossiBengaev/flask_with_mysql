import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
import yaml


def connection_attendace_csv_to_mysql():
    empdata = pd.read_csv('C:\\Users\\Yossi\\Desktop\\b\\flask-mysql\\venv\\attendance.csv', index_col=False, delimiter = ',')
    df_names_avarges = empdata[['names', 'average']].copy()
    df = pd.DataFrame()
    try:
        db = yaml.safe_load(open('db.yaml'))
        conn = msql.connect(host=db['mysql_host'], user=db['mysql_user'],
                                    password=db['mysql_password'], database=db['mysql_db'])
        ################ for first time to create thh database
    #     if conn.is_connected():
    #         cursor = conn.cursor()
    #         cursor.execute("CREATE DATABASE attendance")
    #         print("Database is created")
    # except Error as e:
    #     print("Error while connecting to MySQL", e)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database()")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.execute('DROP TABLE IF EXISTS attendance_data;')
            print('Creating table....')
        # in the below line please pass the creation table statement which you want #to create
            cursor.execute("CREATE TABLE attendance_data(Names VARCHAR(20), average VARCHAR(20))")
            print("Table is created....")
            #loop through the data frame
            for i,row in df_names_avarges.iterrows():
                #here %S means string values
                sql = "INSERT INTO attendance.attendance_data VALUES (%s, %s)"
                cursor.execute(sql, tuple(row))
                #print("Record inserted")
                # the connection is not auto committed by default, so we must commit to save our changes
                conn.commit()

        query = "SELECT * FROM attendance.attendance_data;"
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.read_sql(query, conn)
        # for row in rows:
        #     for col in row:
        #        print(col, end=" ")
        #     print()
        conn.close()
    except Error as e:
                print("Error while connecting to MySQL", e)
    return df




# if __name__ == "__main__":
#     connection_attendace_csv_to_mysql()