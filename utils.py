import glob

DATA_DIRECTORY = '/Volumes/nighoodam/vesselsdata/data'

def get_files(dir_path, extension):
    files_list = glob.glob(dir_path+'/*.'+extension)
    return files_list