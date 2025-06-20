# Definitions for phex

import glob
from decimal import *
import csv


class Hexnum():

    # a HexNum is a Hexnum(Decimal, Int, Int) and has a
    # - value of the number
    # - a list of colors that the powers of val land in
    # - boolean if it rolls a double
    # - number indicating at which power it rolled a double
    def __init__(self, val, pow_limit, prec):
        self.val = val
        self.powers = power_list(val, pow_limit, prec)
        self.colors = []
        self.roll_double = False
        self.roll_double_pow = 0

    def add_color(self, c):
        self.colors.append(c)

    def set_roll_double(self):
        self.roll_double = self.did_roll_double()

    #set_roll_double: set the roll double field based on the pows/colors list
    def did_roll_double(self):
        #colors = [x[1] for x in pows/colors]
        for i in range(1, len(self.colors)):
            if self.colors[i] == self.colors[i-1]:
                self.roll_double_pow = i+1
                return True

        return False


# power-list: Decimal(number) Number -> [Listof Decimal(number)]
# num raised from powers 1 to p
# p cannot be zero
def power_list(num, power, precision):
    getcontext().prec = precision
    pows = []
    for p in range(1,power+1):
        #print( Decimal(Decimal(num) ** p) )
        pows.append( Decimal(Decimal(num) ** p) )
    return pows


# A [Maybe X] is one of:
# - None
# - X

# get_spin_nums : Number File -> [Maybe (Number, Number)]
# spin numbers of the input number
def get_spin_nums(num, pfile):
    c_line = pfile.readline().split()
    n_line = pfile.readline().split()
    #current line and next line
    c_nums = [Decimal(i) for i in c_line]
    n_nums = [Decimal(i) for i in n_line]

    #print (pfile.name)

    if(c_nums[0] > num):
        return (1, 1)

    while (c_nums != []):
        if(n_nums == []):
            break
        elif(num >= c_nums[0] and num < n_nums[0]):
            return (int(c_nums[1]), int(c_nums[2]))

        c_nums = n_nums
        n_line = pfile.readline().split()
        if n_line == []:
            break
        n_nums = [Decimal(i) for i in n_line]

    #reached the end of the file
    return None


# mapping numbers to spin color
spin = {  (1,  1) : "blue",
          (2, -1) : "blue",
          (2,  1) : "purple",
          (3, -1) : "purple",
          (3,  1) : "red",
          (4, -1) : "red",
          (4,  1) : "yellow",
          (5, -1) : "yellow",
          (5,  1) : "green",
          (0, -1) : "green",
          (0,  1) : "cyan",
          (1, -1) : "cyan"
        }


# list of paths to prime-list files
plists = glob.glob('user_data/ft_client/test_client/prime_lists/*.txt')

# lowest primes in each file
lowest_primes = [int(p[44:-4]) for p in plists]

# Maximum of the numbers
# Will change later to be dynamic
MAX = 49999991


# find_plist : Number -> Number
# return the index of the correct file in plists
def find_plist(n):
    if n > MAX:
        return None

    index = lowest_primes.index(5)
    for i in range(0,len(lowest_primes)):
        if (n > lowest_primes[i]) and (lowest_primes[i] > lowest_primes[index]):
            index = i
    return index


#Get vals and colors
def get_val_spin(num):
    if None in num.colors:
        return "%s %s Limit Reached" % (num.val, ', '.join([str(c) for c in num.colors]))
    else:
        return "%s %s" % (num.val, ', '.join([str(c) for c in num.colors]))

def set_optimize_flags(params, param):
    for section in params.values():
        if isinstance(section, dict):
            for key, value in section.items():
                if isinstance(value, dict) and "optimize" in value:
                    value["optimize"] = (key == param)
    return params

def set_params(params, param, fibbo):
    strat_params = fibbo.get("params", {})

    for section_name, section in params.items():
        strat_section = strat_params.get(section_name, {})

        for param_name, param_data in section.items():
            # Step 1: Set optimize flags
            if isinstance(param_data, dict) and "optimize" in param_data:
                param_data["optimize"] = (param_name == param)

            # Step 2: Set default values (except ROI, handled separately below)
            if section_name != "roi" and param_name in strat_section:
                if isinstance(param_data, dict) and "default" in param_data:
                    param_data["default"] = strat_section[param_name]

    # Special handling for ROI
    if "roi" in strat_params and "roi" in params:
        roi_keys = sorted(map(int, strat_params["roi"].keys()), reverse=True)
        for i, k in enumerate(roi_keys):
            param_name = f"roi_p{i+1}"
            if param_name in params["roi"]:
                params["roi"][param_name]["default"] = strat_params["roi"][str(k)]

    return params
