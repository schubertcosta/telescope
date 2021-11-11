#!/usr/bin/python

import sys
sys.path.insert(1, './stellarium_communication')
sys.path.insert(1, './telescope_control')
from application import Application

def main():
    Application()
    sys.stdout.flush()      

main()