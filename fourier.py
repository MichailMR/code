import numpy as np
from scipy.fft import fft, fftfreq
import scipy.io.wavfile as wavfile
import openpyxl
import math
import random
import os

os.chdir('..')

TOTALBINSNO = 100
    
def fourier_transform_parse(sampleRate, tone, samplesNo):
    soundFrequencies = fftfreq(samplesNo, 1 / sampleRate)
    occurancesNos = fft(tone)

    xlsxFilePath = "fourier.xlsx"
    workbook = openpyxl.load_workbook(xlsxFilePath)
    
    sheet = workbook.active
    sheet.delete_cols(1,2)
    
    print('Binning data')
    writeDataToXlsx(soundFrequencies, occurancesNos, sheet, samplesNo)
    
    print('Saving to xlsx file')
    workbook.save(xlsxFilePath)

def writeDataToXlsx(soundFrequencies, occurancesNos, sheet, samplesNo):
    bins = dict(list(enumerate([0]*(TOTALBINSNO+1))))
    
    binSize = round(soundFrequencies.max() / TOTALBINSNO)
    print('Binsize:', binSize)
    
    for i, frequency in enumerate(soundFrequencies):
        binNo = 0
        while frequency > (binNo+1) * binSize:
            binNo += 1
        
        if random.choice(range(samplesNo)) < samplesNo/10000000: print(round(i / samplesNo * 100), 'percent')
        
        bins[binNo] += int(np.abs(occurancesNos[i].real[0]))
    
    print('Writing to data sheet')
    
    for bin in bins.items():
        sheet.cell(row = bin[0]+1, column = 1).value = bin[0]
        sheet.cell(row = bin[0]+1, column = 2).value = (math.log(bin[1], 10) if bin[1] > 0 else 0)

print('reading file')
sampleRate, tone = wavfile.read('B305.wav')
samplesNo = tone.shape[0]

fourier_transform_parse(sampleRate, tone, samplesNo)