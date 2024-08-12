#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: Ashrusha Khatiwada
Semester: "Enter Summer 2024

The python code in this file is original work written by
Ashrusha Khatiwada. No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: I Ashrusha Khatiwada is writing this code (Version A)that show the memory usage of the linux system.
I am using fedora vm to do this assignment

'''

import argparse
import os, sys

def parse_command_args() -> object:
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",epilog="Copyright 2023")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("-H", "--human-readable", action="store_true", help="Prints sizes in human-readable format")
    # add argument for "human-readable". USE -H, don't use -h! -h is reserved for --help which is created automatically.
    # check the docs for an argparse option to store this as a boolean.
    parser.add_argument("program", type=str, nargs='?', help="if a program is specified, show memory use of all associated processes. Show only total use is not.")
    args = parser.parse_args()
    return args
# create argparse function
# -H human readable
# -r running only

def percent_to_graph(percent: float, length: int=20) -> str:
    """turns a percent 0.0 - 1.0 into a bar graph
    making a graph with ###"""
    ...
    num_hashes = int(percent * length)
    num_spaces = length - num_hashes
    return '#' * num_hashes + ' ' * num_spaces

def get_sys_mem() -> int:
    """return total system memory (used or available) in kB
    get total sys mem"""
    file_path = '/proc/meminfo' 
    try:
        with open(file_path, 'r') as file:  #open file
            for entry in file:  # read all line
                if 'MemTotal:' in entry: #look for MemTotal in lines
                    memory_total = int(entry.split()[1])
                    return memory_total  
    except: #except error
        return 0 #return 0 if error

def get_avail_mem() -> int:
    """return total memory that is available
    get available mem"""
    file_path = '/proc/meminfo'
    try:
        mem_file = open(file_path, 'r') #open file
        lines = mem_file.readlines() # read line
        mem_file.close() # close file
        for line in lines: #look for memtotal line in each line
            if 'MemAvailable:' in line:
                available_mem = int(line.split()[1])
                return available_mem
    except : #ecpect error and return 0 if error
        return 0

def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    try:
        pid_command = f'pidof {app_name}' #get pids command
        pid_output = os.popen(pid_command).read().strip() #runing command reading output
        if pid_output: #if output
            pid_list = pid_output.split() #split the output
        else:
            pid_list = [] #if no output empty list
        return pid_list
    except: #if error
        print(f"Error getting PIDs for {app_name}")
        return []

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the resident memory used, zero if not found"
    try:
        f = open(f'/proc/{proc_id}/status', 'r') #open the status file
        for line in f: #real line
                if 'VmRSS:' in line: #look for VmRSS line
                    return int(line.split()[1])  
    except ValueError: #if error
        return 0

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()
    
    total_mem = get_sys_mem()
    avail_mem = get_avail_mem()
    used_mem = total_mem - avail_mem
    used_percent = used_mem / total_mem
    
    if not args.program: #if no program
        graph = percent_to_graph(used_percent, args.length) #make graph
        percentage = int(used_percent * 100)
        if args.human_readable: #if human readable is asked
            used_mem_str = bytes_to_human_r(used_mem)#convert to human readable
            total_mem_str = bytes_to_human_r(total_mem)
        else:
            used_mem_str = str(used_mem) #keep default
            total_mem_str = str(total_mem) #keep default
        
        print(f"Memory         [{graph} | {percentage}%] {used_mem_str}/{total_mem_str}")
    else: #if app specified
        pid_list = pids_of_prog(args.program) #get list of pids
        if not pid_list: #if not found
            print(f"{args.program} not found.")
        
        total_program_mem = 0 #initialize total program mem
        for pid in pid_list: 
            pid_mem = rss_mem_of_pid(pid)
            total_program_mem += pid_mem
            pid_mem_percent = pid_mem / total_mem #calculate percentage
            graph = percent_to_graph(pid_mem_percent, args.length) #make bar graph
            pid_percentage = int(pid_mem_percent * 100)
            
            if args.human_readable: #if human readable needed
                pid_mem_str = bytes_to_human_r(pid_mem) #convert to human readable
                total_mem_str = bytes_to_human_r(total_mem)
            else:
                pid_mem_str = str(pid_mem)
                total_mem_str = str(total_mem)
                
            print(f"{pid}         [{graph} | {pid_percentage}%] {pid_mem_str}/{total_mem_str}")
        
        total_program_percent = total_program_mem / total_mem
        graph = percent_to_graph(total_program_percent, args.length)
        program_percentage = int(total_program_percent * 100)
        
        if args.human_readable:
            total_program_mem_str = bytes_to_human_r(total_program_mem)
            total_mem_str = bytes_to_human_r(total_mem)
        else:
            total_program_mem_str = str(total_program_mem)
            total_mem_str = str(total_mem)
        
        print(f"{args.program}        [{graph} | {program_percentage}%] {total_program_mem_str}/{total_mem_str}")
    # process args
    # if no parameter passed, 
    # open meminfo.
    # get used memory
    # get total memory
    # call percent to graph
    # print

    # if a parameter passed:
    # get pids from pidof
    # lookup each process id in /proc
    # read memory used
    # add to total used
    # percent to graph
    # take total our of total system memory? or total used memory? total used memory.
    # percent to graph.