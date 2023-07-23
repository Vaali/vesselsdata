import sqlite3
import pandas as pd
dbname = "aisdata_new.db"

def create_table():
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    #MMSI	BaseDateTime	LAT	LON	SOG	COG	Heading	VesselName	IMO	CallSign	VesselType	Status	Length	Width	Draft	Cargo	TransceiverClass
    # Create a table in the database
    cursor.execute('''CREATE TABLE IF NOT EXISTS vessels (
                    id Integer,
                    datetime DATETIME,
                    lat REAL,
                    long REAL,
                    sog REAL,
                    cog REAL,
                    heading REAL,
                    vessel_name TEXT,
                    imo TEXT,
                    call_sign TEXT,
                    vessel_type Integer,
                    status Integer,
                    length Integer,
                    width Integer,
                    draft Integer,
                    cargo Integer,
                    transreceiver_class Text
                )''')
    conn.commit()
    conn.close()

def push_data(data):
    conn = sqlite3.connect(dbname)
    # cursor = conn.cursor()
    table_name = "vessels"
    #              MMSI         BaseDateTime       LAT       LON  SOG    COG  Heading           VesselName         IMO 
    # CallSign  VesselType  Status  Length  Width  Draft  Cargo TransceiverClass
    column_mapping = {'MMSI': 'id',
                  'BaseDateTime': 'datetime',
                  'LAT':'lat',
                  'LON':'long',
                  'SOG':'sog',
                  'COG':'cog',
                  'Heading':'heading',
                  'VesselName':'vessel_name',
                  'IMO':'imo',
                  'CallSign':'call_sign',
                  'VesselType':'vessel_type',
                  'Status':'status',
                  'Length':'length',
                  'Width':'width',
                  'Draft':'draft',
                  'Cargo':'cargo',
                  'TransceiverClass':'transreceiver_class'  
                  }
    data = data.rename(columns=column_mapping)
    data.to_sql(table_name, conn, if_exists='append', index=False)
    # placeholders = ','.join(['?'] * len(row))
    # sql = f'INSERT INTO {table_name} (id, datetime,lat,long,sog,cog,heading,\
    #             vessel_name,imo,call_sign,vessel_type,status,length,width,\
    #             draft,cargo,transreceiver_class) VALUES ({placeholders})'
    # cursor.execute(sql, row)
    # conn.commit()
    conn.close()

def get_data(date):
   conn = sqlite3.connect(dbname)
   table_name = "vessels"
   # Execute SQL query and retrieve data into a list of tuples
   cursor = conn.cursor()
   cursor.execute('SELECT vessel_name,lat,long,DATE(datetime) as date, time(datetime) as time FROM '+table_name +' where date like "'+date+'"')
   rows = cursor.fetchall()
   
   # Get column names from the cursor's description
   columns = [desc[0] for desc in cursor.description]
   # Close the cursor and the database connection
   cursor.close()
   conn.close()
   return (columns,rows)