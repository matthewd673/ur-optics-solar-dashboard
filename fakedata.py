# fakedata.py
# run `py fakedata.py` to generate a file full of fake data for testing

import random

def generateFakeLine(year, doy, mst):
    out = '0,' + str(year) + ',' + str(doy) + ',' + str(mst) + ','
    for i in range(12):
        out += str(random.randint(40, 60))
        if (i < 11):
            out += ','
    return out

def main():
    fake = ',Year,DOY,MST,Global Horizontal [W/m^2],Direct Normal [W/m^2],Diffuse Horizontal [W/m^2],PR1 Temperature [deg C],PH1 Temperature [deg C],Pressure [mBar],Zenith Angle [degrees],Azimuth Angle [degrees],RaZON Status,RaZON Time [hhmm],Logger Battery [VDC],Logger Temp [deg C]\n'
    
    mst = 0
    doy = 0
    for i in range(14400):
        #increment mst and doy
        if mst == 2359:
            doy += 1
            mst = 0
        else:
            if str(mst).endswith('59'): #gross but i don't care
                mst += 41
            else:
                mst += 1
        fake += generateFakeLine(2021, doy, mst) + '\n'
    
    f = open('fake.csv', 'w', newline='')
    f.write(fake)
    f.close()

    print('Done - check fake.csv')

if __name__ == '__main__':
    main()