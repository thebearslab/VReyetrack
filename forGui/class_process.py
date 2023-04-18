################################################
## 1.convert xml to hitting points with csv file
################################################

import pandas as pd
import sys
import os
import xml.etree.ElementTree as ET
import math
from sphere import Sphere
# geom3 adopted from https://github.com/phire/Python-Ray-tracer
from geom3 import Vector3, Point3, Ray3, dot, unit
from math import sqrt
import numpy  as np
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # <--- This is important for 3d plotting
# from sphere_to_cubemap.angles import *
from PIL import Image
import csv

class XmlToHittingPoints:
    print("do this")