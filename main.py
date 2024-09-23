import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.stats as st
import scipy.signal as signal

#air pollution data
num=np.arange(1440)
arr=np.random.uniform(50,200,1440)

#noise data
noise=np.random.random(1440)*2
noise_arr=arr+noise

#filter
fs=1
cutoff=0.05
b,a= signal.butter(4,cutoff,fs=fs,btype='lowpass')
smooth=signal.filtfilt(b,a,noise_arr)

#danger zone of air pollution(>150)
def danger():
    d_val=[]
    d_idx=[]
    for i in range(0,1440):
        if smooth[i]>=150:
            d_val.append(smooth[i])
            d_idx.append(i)
    return [d_val,d_idx]

d_val,d_idx=danger()[0],danger()[1]   

def conti(smooth):
    count=0
    idx=0
    c_idx=[]
    v_idx=[]
    for i in range(0,1440,10):
        idx+=1
        if smooth[i]>150:
            count+=1
        
        elif count==10:
            c_idx.append(i)
            v_idx.append(smooth[i])
    
        elif idx==10:
            idx=0
            count=0
        
    return [c_idx,v_idx]

c_idx,v_idx=conti(smooth)[0],conti(smooth)[1]

#graphs of air pollution
plt.figure(figsize=(12,9))
plt.subplot(2,1,1)
plt.title("Air Pollution")

plt.plot(num,arr,label="Data")
plt.plot(num,noise_arr,label="Data+Noise")
plt.plot(num,smooth,label="Smooth")
plt.plot(d_idx,d_val,"o",label="Danger")
if c_idx:
    plt.plot(c_idx,v_idx,"*",label="Conti")
    
plt.xlabel("Minutes")
plt.ylabel("PM")
plt.legend()

#average value of air pollution(hourly)
def avg(smooth):
    avg_hour=[np.mean(smooth[i:i+60]) for i in range(0,len(num),60)]
    return avg_hour

hour=np.arange(24)
avg_hour=avg(smooth)

plt.subplot(2,1,2)
plt.title("Average Air Polution(hour)")
plt.plot(hour,avg_hour)
plt.xlabel("Hour")
plt.ylabel("Avg")
plt.show()

    
