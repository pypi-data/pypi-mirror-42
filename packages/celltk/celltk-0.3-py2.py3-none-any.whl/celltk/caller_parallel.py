'''
Call this function if you want to multiprocess using PARENT_INPUT argument 
(see input_fireworks.yml). 
If you simply want to pass multiple input files, use caller.py.
'''
from __future__ import print_function
import os
import sys
from os.path import join, basename, exists, dirname
celltkroot = dirname(dirname(os.path.abspath(__file__)))
sys.path.append(join(celltkroot, 'celltk'))
# sys.path.insert(0, join(celltkroot, 'celltk'))
from caller import parse_args, load_yaml, call_operations
import yaml
import collections
import multiprocessing


def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


def parallel_call(contents):
    contents = convert(contents)
    call_operations(contents)


def multi_call(inputs):
    contents = load_yaml(inputs)
    pin = contents['PARENT_INPUT']
    pin = pin[:-1] if pin.endswith('/') or pin.endswith('\\') else pin
    input_dirs = [join(pin, i) for i in os.listdir(pin)]
    contents_list = []
    for subfolder in input_dirs:
        conts = eval(str(contents).replace('$INPUT', subfolder))
        conts['OUTPUT_DIR'] = join(conts['OUTPUT_DIR'], basename(subfolder))
        contents_list.append(conts)
    return contents_list


def main():
    args = parse_args()
    contents_list = multi_call(args.input[0])

    num_cores = args.cores
    print(str(num_cores) + ' started parallel')
    pool = multiprocessing.Pool(num_cores, maxtasksperchild=1)
    pool.map(parallel_call, contents_list, chunksize=1)
    pool.close()


if __name__ == "__main__":
    main()
