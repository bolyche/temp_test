import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np
import json
import os

def load_json_objects(filename):
    return [json.loads(line) for line in open(filename)]

def get_firstdictvalues(data,val):
    return [i.get(val) for i in data]

def get_user_properties(data,topval,val,finalval):
    d = [[s.get('value').get(finalval) for s in i.get(topval) if s.get('key') == val] for i in data]
    return [subitem if np.array(subitem).size == True else ['0'] for subitem in d]

def tidy_json_data(data):
    eventdate = get_firstdictvalues(data,'event_date')
    session_uuid = list(map(str, get_user_properties(data,'user_properties','session_uuid','string_value')))

    timeactive = get_user_properties(data,'event_params','engagement_time_msec','int_value')
    timeactive = list(map(int, [i for subi in timeactive for i in subi]))

    assert len(eventdate) == len(timeactive) == len(session_uuid)

    return eventdate, session_uuid, timeactive

def create_base_active_user_table(data):
    eventdate, session_uuid, timeactive =  tidy_json_data(data)
    d = {'date':eventdate,'session_uuid':session_uuid,'timeactive':timeactive}
    df = pd.DataFrame(d)
    df = df[df['timeactive'] > 3]
    df_grouped = df.groupby(['date','session_uuid']
                           ).agg({'session_uuid':'count'}
                                ).rename(columns={'session_uuid':'active_user_count'}
                                        ).reset_index(
                                            ).drop(['session_uuid'],axis=1
                                              ).groupby('date'
                                                       ).sum(
                                                        ).reset_index()
    return df_grouped

def db_connection(db_path):
    conn = None
    try:
        conn = sqlite3.connect(db_path+'/db.sqlite3')
        return conn
    except Error as e:
        print(e)

def create_table(conn, sql_to_run):
    try:
        cur = conn.cursor()
        cur.execute(sql_to_run)
    except Error as e:
        print(e)

def main(df):
    cwd = os.getcwd()
    sql_create_active_user_table = """ CREATE TABLE IF NOT EXISTS active_user_table (
                                        date DATE PRIMARY KEY,
                                        active_user_count INT NOT NULL
                                    ); """
    conn = db_connection(cwd)
    if conn is not None:
        create_table(conn, sql_create_active_user_table)
        conn.commit()
        df.to_sql('active_user_table', conn, if_exists='replace', index=False)
        print('Data in active_user_table:', conn.execute('SELECT * from active_user_table').fetchall())
    else:
        print("Error - Db connection not established")


if __name__ == '__main__':
    jsoninfo = load_json_objects('bq-results-sample-data.json')
    df_data =  create_base_active_user_table(jsoninfo)
    main(df_data)
