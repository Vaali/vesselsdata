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
    qr = qr.query(" VesselType >= 90 or Cargo >= 90")
    db.push_data(qr)
    print("processing file done",file)


def main():
    db.create_table()
    files_list = utils.get_files(utils.DATA_DIRECTORY,"csv")
    # for file in files_list:
    #     extract_and_push(file)
    with multiprocessing.Pool(processes=4) as pool:
        pool.map(extract_and_push, files_list)
        pool.close()
        pool.join()



if __name__ == "__main__":
    main()