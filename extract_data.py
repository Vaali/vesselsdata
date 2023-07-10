import pandas as pd
import utils
import database as db
import multiprocessing

def extract_and_push(file):
    print("processing file ",file)
    df = pd.read_csv(file)
    east_coast_df = df[(df['LAT'] >= 36.5) & (df['LAT'] <= 46.0) &
                (df['LON'] >= -87.0) & (df['LON'] <= -65.0)]
    qr = east_coast_df[(east_coast_df['Status'] == 3 )]
    '''
    select distinct(vessel_name),call_sign,vessel_type,cargo,length,width from vessels where cargo != 55 
    and cargo != 52 and ( cargo < 30 or cargo > 37) and cargo != 0 and (cargo >69 or cargo <60 ) 
    and cargo != 51 and ( vessel_type > 69 or vessel_type <60 ) and vessel_name not like '%CG %';
    
    '''
    qr = qr.query(" VesselType >= 90 or Cargo >= 90 or VesselType == 70")
    qr = qr.query(" VesselType > 69 or VesselType < 60 ")
    qr = qr.query(" (Cargo < 51 or Cargo > 55 ) and Cargo != 58 and (Cargo > 69 or Cargo <60 ) and ( Cargo < 30 or Cargo > 37) ")
    qr = qr.query('not VesselName.str.contains("CG ")')

    db.push_data(qr)
    print("processing file done",file)


def main():
    db.create_table()
    files_list = utils.get_files(utils.DATA_DIRECTORY,"csv")
    #files_list = ["../data/AIS_2023_01_01.csv"]
    # for file in files_list:
    #     extract_and_push(file)
    with multiprocessing.Pool(processes=4) as pool:
        pool.map(extract_and_push, files_list)
        pool.close()
        pool.join()



if __name__ == "__main__":
    main()