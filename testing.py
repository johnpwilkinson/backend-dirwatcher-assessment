# def search(magic_text):
#     with open('test.txt') as f:
#         datafile = f.readlines()
#         for line in datafile:
#             if 'morty' in line:
#                 print("true")
#                 return True
#             else:
#                 print('false')
#                 return False
   
# search('morty')
   
import os 

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    # start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
       for file in files:
           if file not in dir.keys():
               dir[file] = []
        
    print(dir)
    return dir

get_directory_structure('/Users/john/Documents/Kenzie-Projects/Q3/backend-dirwatcher-assessment/example')