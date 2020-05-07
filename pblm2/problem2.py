import sys
import time

def read_file(file_name):
    f = open(file_name,"r")    
    return f.readlines()

def print_processortype():
    f = read_file("/proc/cpuinfo")
    for x in f:
        #print(x)
        lines = x.split(":",1)
        if len(lines) > 0 and lines[0].replace(" ","").rstrip() == "modelname" :
            print(lines[1])
            break

def print_kernel_version():
    f = read_file("/proc/version")
    for x in f:
        print(x)
	
def print_memory_configuration():
    f = read_file("/proc/meminfo")
    print(f[0])

def print_lastboot_time():
    f = read_file("/proc/uptime")
    print("Uptime:",f[0])

def cpu_times():
    f = read_file("/proc/stat")
    cpu_times_list = []
    context_switch = 0
    processes_created = 0

    for x in f:
        #print(x)
        lines = x.split(" ")
        if len(lines) > 0 and lines[0].replace(" ","").rstrip() == "cpu" :
            #print(lines)
            for i in range(2,len(lines)-1):
                cpu_times_list.append(int(lines[i]))

        if len(lines) > 0 and lines[0].replace(" ","").rstrip() == "ctxt":
            context_switch = int(lines[1])

        if len(lines) > 0 and lines[0].replace(" ","").rstrip() == "processes":
            processes_created = int(lines[1])
    
    return cpu_times_list,context_switch,processes_created

def calculate_cpushare_precentages(prev_cpu_times,cpu_time):
    cur_cpu_times = [0]*len(cpu_time)
    total_cpu_times = 0
    cpu_mode_rates = []
    for j in range(0,len(cpu_time)):
        cur_cpu_times[j] = cpu_time[j] - prev_cpu_times[j]
        total_cpu_times = total_cpu_times+cur_cpu_times[j]
    
    cpu_mode_rates.append(((cur_cpu_times[0]+cur_cpu_times[1])/total_cpu_times)*100)
    cpu_mode_rates.append((cur_cpu_times[2]/total_cpu_times)*100)
    cpu_mode_rates.append((cur_cpu_times[3]/total_cpu_times)*100)
    return cpu_mode_rates

def calculate_context_switches(prev_context_switch,context_switch):
    return context_switch-prev_context_switch

def calculate_processes_created(prev_processes_created,processes_created):
    return processes_created-prev_processes_created

def memory_calculation():
    f = read_file("/proc/meminfo")
    mem_total = 0
    mem_free = 0
    mem_available = 0

    for x in f:
        lines = x.split(":",1)
        if len(lines) > 0 and lines[0].replace(" ","").rstrip() == "MemTotal" :
            line = lines[1].split(" ")
            #print(line)
            mem_total = int(line[len(line)-2].replace(" ","").rstrip())

        if len(lines) > 0 and lines[0].replace(" ","").rstrip() == "MemFree":
            line = lines[1].split(" ")
            #print(line)
            mem_free =  int(line[len(line)-2].replace(" ","").rstrip())

        if len(lines) > 0 and lines[0].replace(" ","").rstrip() == "MemAvailable":
            line = lines[1].split(" ")
            mem_available =  int(line[len(line)-2].replace(" ","").rstrip())

    return mem_available, (mem_available/(mem_available+mem_total+mem_free))*100

def disk_read_write_stats():
    f = read_file("/proc/diskstats")
    disk_reads = 0
    read_time = 0

    disk_writes = 0
    write_time = 0

    for x in f:
        lines = x.split(" ")
        if len(lines) ==  25 and lines[9] == "nvme0n1":
            disk_reads = int(lines[12])
            read_time = int(lines[13])
            disk_writes = int(lines[16])
            write_time = int(lines[17])
            return disk_reads/read_time,disk_writes/write_time

def main():

    if len(sys.argv) > 1:
        read_rate = int(sys.argv[1])
        printout_rate = int(sys.argv[2])
        prev_cpu_times,prev_context_switch,prev_processes_created = cpu_times()
       
        while True:
            context_switch_count = 0
            process_created_Count = 0
            cpu_mode_percentages_count = [0]*3
            disk_read_rate_count = 0
            disk_write_rate_count = 0
            time.sleep(read_rate)  
            for i in range(0,int(printout_rate/read_rate)):
                cpu_time,context_switch,processes_created = cpu_times()
                cpu_mode_percentages = calculate_cpushare_precentages(prev_cpu_times,cpu_time)
                for i in range(0,len(cpu_mode_percentages)):
                    cpu_mode_percentages_count[i] = cpu_mode_percentages_count[i] + cpu_mode_percentages[i]
                prev_cpu_times = cpu_time
                context_switch_count = context_switch_count + calculate_context_switches(prev_context_switch,context_switch)
                prev_context_switch = context_switch
                process_created_Count = process_created_Count + calculate_processes_created(prev_processes_created,processes_created)
                prev_processes_created = processes_created
                # print(cpu_time)
                # print(context_switch)
                # print(processes_created)
                
                time.sleep(read_rate)  
                read_count, write_count = disk_read_write_stats()
                disk_read_rate_count = disk_read_rate_count + read_count
                disk_write_rate_count = disk_write_rate_count + write_count
            print("---------------------------------STATITICS-------------------------------------------------------")
            print("User Space CPU Time:",cpu_mode_percentages_count[0]/(int(printout_rate/read_rate)))
            print("Kernel Space CPU Time:",cpu_mode_percentages_count[1]/int(printout_rate/read_rate))
            print("Idle CPU Time:",cpu_mode_percentages_count[2]/int(printout_rate/read_rate))
            print("Context Switch Rate:",context_switch_count/int(printout_rate/read_rate))
            print("Process Creation Rate:",process_created_Count/int(printout_rate/read_rate))
            mem_available, mem_available_percentage = memory_calculation()
            print("Memory Available: {}  Memory Available Percentage: {}".format(mem_available,mem_available_percentage))
            print("Disk Read rate:",disk_read_rate_count/(int(printout_rate/read_rate)))
            print("Disk Write rate:",disk_write_rate_count/(int(printout_rate/read_rate)))
            print("-------------------------------------------------------------------------------------------------\n")
        #print("read_rate:",read_rate,"p_rate:",printout_rate)
        pass
    else:
        print_processortype()
        print_kernel_version()
        print_memory_configuration()
        print_lastboot_time()
    
if __name__ == "__main__":
    main()
