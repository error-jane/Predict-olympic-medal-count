import csv
import numpy as np
import matplotlib.pyplot as plt

#ฟังก์ชั้นสำหรับอ่านไฟล์ตามปีที่เลือก
def readFile(year):
    PrizeOfCountry = {}#เก็บข้อมูลจำนวนเหรียญของแต่ละประเทศทุกปี

    #เปิดไฟล์เพื่ออ่านข้อมูลจากไฟล์สกุล csv หรือไฟล์ excel
    with open('Summer-Olympic-medals-1976-to-2008.csv','r')as csv_f:
        data = list(csv.reader(csv_f))
        data.pop(0) #ลบหัวข้อตารางออกเพื่อจะเอาแต่ข้อมูล
        PrizeOfCountry["All"] = {"Country_Code":"All","Country":"All","Silver":0, "Bronze":0,"Gold":0,"Total":0}

        #วนลูปเพื่อเก็บข้อมูลแต่ละบรรทัด
        for row in data:

            #ถ้าบรรทัดนี้เป็นประเทศที่ยังไม่เคยเก็บข้อมูล
            if(PrizeOfCountry.get(row[7]) == None and row[-1] != "" and int(row[1]) == year):

                #เก็บชื่อย่อชื่อเต็มของประเทศ
                #เก็บข้อมูลรางวัลที่ได้รับ
                prizeData = {"Country_Code":row[7],"Country":row[8],"Silver":0, "Bronze":0,"Gold":0,"Total":1}
                prizeData[row[-1]] = 1
                PrizeOfCountry[row[7]] = prizeData
                
                PrizeOfCountry["All"][row[-1]] += 1
                PrizeOfCountry["All"]["Total"] += 1

            #ถ้าบรรทัดนี้เป็นประเทศที่เคยเก็บข้อมูล
            elif(row[-1] != "" and int(row[1]) == year):

                #เก็บข้อมูลรางวัลที่ได้รับของแต่ละประเทศ
                prizeData = PrizeOfCountry.get(row[7])
                prizeData[row[-1]] += 1
                prizeData["Total"] += 1

                #เก็บข้อมูลโดยรวมไม่แยกประเทศ
                PrizeOfCountry["All"][row[-1]] += 1
                PrizeOfCountry["All"]["Total"] += 1
    return (PrizeOfCountry)


#ฟังก์ชันเขียนไฟล์excelข้อมูลเหรียญที่ได้ของแต่ละประเทศ        
def writeMainDataFile(PrizeOfCountry, year):
    
    #เปิดไฟล์เพื่อเขียนข้อมูลลงไฟล์สกุล csv หรือไฟล์ excel        
    with open('Summer-Olympic-medals-prize_file'+str(year)+'.csv', 'w', newline='') as prize_file:

        #หัวข้อของแต่ละอัน
        fieldnames =['Country_Code', 'Country', 'Gold', 'Bronze', 'Silver','Total']
        file_writer = csv.DictWriter(prize_file, fieldnames = fieldnames)
        
        allCountry = PrizeOfCountry.values()
        file_writer.writeheader()
        
        #วนลูปเพื่อนำข้อมูลชนิด dict เขียนลงไฟล์
        for country in allCountry:
            if(country['Country_Code'] != "All"):
                file_writer.writerow(country)

                
#ฟังก์ชั่นสำหรับเขียนไฟล์ Excel เกี่ยวกับโอกาสได้เหรียญของแต่ละประเทศ และคืนค่าข้อมูลที่มีแต่ชื่อกับจำนวนเหรียญ
def writAVRdataFile(PrizeOfCountry, year):
    #เปิดไฟล์เพื่อเขียนข้อมูลลงไฟล์สกุล csv หรือไฟล์ excel        
    with open('Summer-Olympic-medals-AVR_prize_'+str(year)+'.csv', 'w', newline='') as prize_file:

        #หัวข้อของแต่ละอัน
        fieldnames =['Country_Code', 'Country', 'Gold', 'Bronze', 'Silver','Total']
        file_writer = csv.DictWriter(prize_file, fieldnames = fieldnames)

        AllTo = PrizeOfCountry.get('All')
        PrizeOfCountry.pop('All')
        
        allCountry = PrizeOfCountry.values()
        file_writer.writeheader()
        
        #วนลูปเพื่อนำข้อมูลชนิด dict เขียนลงไฟล์
        for country in allCountry:

            #หาค่าเฉลี่ยของแต่ละเหรียญที่เคยได้รับ
            country['Silver'] = "%.2f"%((country['Silver']/AllTo['Silver'])*100)
            country['Bronze'] = "%.2f"%((country['Bronze']/AllTo['Bronze'])*100)
            country['Gold'] = "%.2f"%((country['Gold']/AllTo['Gold'])*100)
            country['Total'] = "%.2f"%((country['Total']/AllTo['Total'])*100)
            file_writer.writerow(country)

    return (PrizeOfCountry)

#หาโอกาสที่ได้เหรียญของแต่ละปีแล้วเก็บไว้ใน Excel
def fileOfYear():
    
    #เริ่มหาจากปีแรกสุดในข้อมูล จนถึงปีสุดท้าย
    for year in range(1976,2009,4):   
        PrizeOfCountry = readFile(year)            
        writeMainDataFile(PrizeOfCountry, year)
        PrizeOfCountry = writAVRdataFile(PrizeOfCountry, year)
        plotGraph(PrizeOfCountry,year)


#เขียนกราฟของแต่ละปี
def plotGraph(dataDict,year):
    plt.figure(year)  
    keys = dataDict.keys()
    for name in keys:
        if(float(dataDict[name]['Total'])>2.5):
            plt.plot(['Silver', 'Bronze', 'Gold','Total'],
                     [float(dataDict[name]['Silver']),float(dataDict[name]['Bronze']),
                      float(dataDict[name]['Gold']),float(dataDict[name]['Total'])],
                      label = dataDict[name]['Country'])
        else:
            plt.plot(['Silver', 'Bronze', 'Gold','Total'],
                     [float(dataDict[name]['Silver']),float(dataDict[name]['Bronze']),
                      float(dataDict[name]['Gold']),float(dataDict[name]['Total'])],
                      'C7')
    plt.xlabel('Megals')
    plt.ylabel('Chance to medal')
    plt.title('Summer-Olympic-medals-'+str(year))
    plt.legend(bbox_to_anchor=(0., 1.05, 1., .102), loc=4, ncol=4,
               mode="expand", borderaxespad=0.)
    plt.show()




fileOfYear()


























