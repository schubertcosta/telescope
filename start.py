import sys

sys.path.insert(1, './stellarium_communication')
sys.path.insert(1, './telescope_control')

def main(argv):
    param = argv[1] if len(argv) > 1 else None
    if(param == "-a"):
        from analysis import Analysis
        Analysis()
    else:
        from application import Application
        Application()
    sys.stdout.flush()      

if __name__ == '__main__':
    main(sys.argv)