# Importing the library
import os
import psutil
import time

#---------------------------------------Variables to set-------------------------------------------------------



csv = "./test.csv" #path of the CSV file will be save
bench_time = 2.0 #time in secs



#--------------------------------------------------------------------------------------------------------------

class Benchmark():
    def __init__(self):
        self.time = []
        self.CPU_freqs = []
        self.CPU_percents = []
        self.CPU_time_percentages = []
        self.RAM_percentages = []
        self.RAM_used = []
        self.RAM_percentages_used = []

    def bench_raw(self,start):
        #time
        self.time.append(time.time()-start)
        #CPU FREQ
        self.CPU_freqs.append(psutil.cpu_freq().current)

        #CPU%
        self.CPU_percents.append(psutil.cpu_percent(interval= 0.1,percpu=True))

        #
        self.CPU_time_percentages.append(psutil.cpu_times_percent())

        # Getting % usage of virtual_memory ( 3rd field)
        self.RAM_percentages.append(psutil.virtual_memory()[2])
        # Getting usage of virtual_memory in GB ( 4th field)
        self.RAM_used.append(psutil.virtual_memory()[3]/1000000000)

        # Getting all memory using os.popen()
        total_memory, used_memory, free_memory = map(
            int, os.popen('free -t -m').readlines()[-1].split()[1:])
        
        # Memory usage
        self.RAM_percentages_used.append(round((used_memory/total_memory) * 100, 2))


    def write_csv(self,filename):
        csvFormat = "time;CPU_freqs;CPU_percents1;CPU_percents2;CPU_percents3;CPU_percents4;CPU_time_percentages_user;CPU_time_percentages_system;CPU_time_percentages_idle;RAM_percentages;RAM_used;RAM_percentages_used\n"
        for i in range(len(self.time)):
            csvFormat = csvFormat + str(self.time[i])+";"+str(self.CPU_freqs[i])+";" +str(self.CPU_percents[i][0]) +";" +str(self.CPU_percents[i][1]) +";" +str(self.CPU_percents[i][2]) +";" +str(self.CPU_percents[i][3]) +";" +str(self.CPU_time_percentages[i].user)+";" +str(self.CPU_time_percentages[i].system)+";" +str(self.CPU_time_percentages[i].idle)+";" + str(self.RAM_percentages[i])+";" + str(self.RAM_used[i])+";" + str(self.RAM_percentages_used[i])+"\n"
        print(csvFormat)

        f = open(filename, "w")
        f.write(csvFormat)
        f.close()    

if __name__ == '__main__':
    obj = Benchmark()
    start = time.time()
    while(time.time()-start <= bench_time):
        obj.bench_raw(start)
    obj.write_csv(csv)




    
