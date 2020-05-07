#!/usr/bin/python3
import sys
import re
def print_usage():
    print("Usage: read_heap.py pid")
    exit(1)
def overwrite_heap(pid, search_string, replace_string):
    mem_perm = 'rw'
    maps_filename = "/proc/{}/maps".format(pid)
    mem_filename = "/proc/{}/mem".format(pid)
    i=0
    try:
        with open(maps_filename, 'r') as maps_file:
            i = i+1
            with open(mem_filename, 'rb+', 0) as mem_file:
                i = i+1
                for line in maps_file.readlines():
                    addr_perm = r'([0-9A-Fa-f]+)-([0-9A-Fa-f]+) ([-r][-w])'
                    m = re.search(addr_perm, line)
                    h = re.search(r'(\[heap\])', line)
                    if m.group(3) == mem_perm and h and h.group(0) == "[heap]":
                        start_addr = int(m.group(1), 16)
                        end_addr = int(m.group(2), 16)
                        mem_file.seek(start_addr)
                        heap = mem_file.read(end_addr - start_addr)
                        #print(''.join(chr(i) for i  in heap))
                        start_pos = heap.find(bytes(search_string,"ASCII"))  
                        i = i+1                      
                        if start_pos:                            
                            mem_file.seek(start_addr + start_pos)                            
                            adjusted_str = replace_string.ljust(len(search_string))                            
                            mem_file.write(bytes(adjusted_str, "ASCII"))
                            i = i+1                            
                            heap.write(bytes(adjusted_str,"ASCII"))
                            
                        else:
                            print("%s is not found in the heap",search_string)
    except IOError as e:
        print("[ERROR] Can not open file {}:".format(i))
        print("        I/O error({}): {}".format(e.errno, e.strerror))
        exit(1)
try:
    print("length of arguments:",len(sys.argv))
    if len(sys.argv) != 4:
        print_usage()
    pid = int(sys.argv[1])
    search_string = sys.argv[2]
    replace_string = sys.argv[3]
    if(len(search_string) == 0 or len(replace_string) == 0):
        help()
    overwrite_heap(pid,search_string,replace_string)
except Exception as e:
    print_usage()

'''
#/usr/bin/python3

import sys
import re

def help():
    print("overwrite_heap.py pid")
    exit(1)

def overwrite_heap(pid):
    memory_permission = 'rw'
    maps = "/proc/{}/maps".format(pid)
    mem = "/proc/{}/mem".format(pid)

    try:
        with open(maps,'r') as maps_file:
           with open(mem,'rb+',0) as mem_file:
              for line in maps.readlines():
                 addr_perm = r'([0-9A-Fa-f]+)-([0-9A-Fa-f]+) ([-r][-w])'
                 m = re.search(addr_perm,line) 
                 h = re.search(r'(\[heap\])', line)
                 if m.group(3) == mem_perm and h and h.group(0) == "[heap]":
                    starting_addr = int(m.group(1),16)
                    end_addr = int(m.group(2),16)
                    mem_file.seek(starting_addr)
                    heap_mem = mem_file.read(end_addr = starting_addr)
                    print(''.join(chr(i) for i in heap_mem))
    except IOError as e:
        print("Error: Cannot open the file",e.errno,e.strerror)
        exit(1)
 
try:
    print("checl") 
    print("length of arguments:",len(sys.argv))
    if len(sys.argv) != 2:
        help()
        print("entered help check")
    pid = int(sys.argv[1])
    print("entered help check")
    overwrite_heap(pid)
except Exception as e:
    print("Error: Cannot open the file",e.errno,e.strerror)
    help() 


'''