"""
Pickle file handler
@auth: Yu-Hsiang Fu
@date  2014/10/05
"""


# read pickle file：
def read_pickle_file(file_path):
    import pickle
    import os
    import os.path

    # read file
    try:
        # check "isfile" and "access"
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            return pickle.load(open(file_path, 'rb'))
        else:
            raise
    except:
        print('[Error] The file can not be read ...')
        print('[Error] Please check this: ' + str(file_path))


# write pickle
def write_pickle_file(file_path, data):
    import pickle

    try:
        pickle.dump(data, open(file_path, 'wb'))
    except:
        print('[Error] The file can not be writed ...')
        print('[Error] Please check this: ' + str(file_path))
