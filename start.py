import sys

sys.path.insert(1, './stellarium_communication')
sys.path.insert(1, './telescope_control')
from analysis import Analysis
from application import Application

def main(argv):
    param = argv[1]
    print(param)
    if(param == "-a"):
        Analysis()
    else:
        Application()
    sys.stdout.flush()      

main()