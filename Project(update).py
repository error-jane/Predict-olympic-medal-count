import csv
import numpy as np
import matplotlib.pyplot as plt

#ฟังก์ชั้นสำหรับอ่านไฟล์ตามปีที่เลือก
def readFile(year):
    PrizeOfCountry = {}#เก็บข้อมูลจำนวนเหรียญของแต่ละประเทศทุกปี

    #เปิดไฟล์เพื่ออ่านข้อมูลจากไฟล์สกุล csv หรือไฟล์ excel
    with open('Summer-Olympic-medals-1976-to-2008.csv','r',encoding = 'cp850')as csv_f:
        data = list(csv.reader(csv_f))
        data.pop(0) #ลบหัวข้อตารางออกเพื่อจะเอาแต่ข้อมูล
        PrizeOfCountry["All"] = {"Country_Code":"All","Country":"All","Silver":0, "Bronze":0,"Gold":0,"Total":0}
        #วนลูปเพื่อเก็บข้อมูลแต่ละบรรทัด
        for row in data:

            #ถ้าบรรทัดนี้เป็นประเทศที่ไม่เคยเก็บข้อมูล
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
    return (PrizeOfCountry) #return data in PrizeOfCountry


#ฟังก์ชันเขียนไฟล์excelข้อมูลเหรียญที่ได้ของแต่ละประเทศ        
def writeMainDataFile(PrizeOfCountry, year):#write new excel for every year
    
    #เปิดไฟล์เพื่อเขียนข้อมูลลงไฟล์สกุล csv หรือไฟล์ excel        
    with open('Summer-Olympic-medals-prize_file'+str(year)+'.csv', 'w', newline='') as prize_file:

        #หัวข้อของแต่ละอัน
        fieldnames =['Country_Code', 'Country', 'Gold', 'Bronze', 'Silver','Total']#collum
        file_writer = csv.DictWriter(prize_file, fieldnames = fieldnames)
        
        allCountry = PrizeOfCountry.values()

        file_writer.writeheader()#write 'Country_Code', 'Country', 'Gold', 'Bronze', 'Silver','Total' to collum
        
        #วนลูปเพื่อนำข้อมูลชนิด dict เขียนลงไฟล์
        for country in allCountry:
            if(country['Country_Code'] != "All"):
                file_writer.writerow(country)#write row

                
#ฟังก์ชั่นสำหรับเขียนไฟล์ Excel เกี่ยวกับโอกาสได้เหรียญของแต่ละประเทศ และคืนค่าข้อมูลที่มีแต่ชื่อกับจำนวนเหรียญ
def writAVRdataFile(PrizeOfCountry, year):
    data_list = {}
    #เปิดไฟล์เพื่อเขียนข้อมูลลงไฟล์สกุล csv หรือไฟล์ excel        
    with open('Summer-Olympic-medals-AVR_prize_'+str(year)+'.csv', 'w', newline='') as prize_file:

        #หัวข้อของแต่ละอัน
        fieldnames =['Country_Code', 'Country', 'Gold', 'Bronze', 'Silver','Total']
        file_writer = csv.DictWriter(prize_file, fieldnames = fieldnames)

        AllTo = PrizeOfCountry.get('All')#get all of every medal
        PrizeOfCountry.pop('All')
        
        allCountry = PrizeOfCountry.values()#get only value not get key
        file_writer.writeheader()#write collum
        
        #วนลูปเพื่อนำข้อมูลชนิด dict เขียนลงไฟล์
        for country in allCountry:

            #หาค่าเฉลี่ยของแต่ละเหรียญที่เคยได้รับ
            country['Silver'] = "%.2f"%((country['Silver']/AllTo['Silver'])*100)
            country['Bronze'] = "%.2f"%((country['Bronze']/AllTo['Bronze'])*100)
            country['Gold'] = "%.2f"%((country['Gold']/AllTo['Gold'])*100)
            country['Total'] = "%.2f"%((country['Total']/AllTo['Total'])*100)
            data_list[country['Country_Code']] = country
            file_writer.writerow(country)

    return (data_list)

#หาโอกาสที่ได้เหรียญของแต่ละปีแล้วเก็บไว้ใน Excel
def fileOfYear():
    #เริ่มหาจากปีแรกสุดในข้อมูล จนถึงปีสุดท้าย
    year_olympic = {}
    country = {}
    country_result = {}
    allCountry = set()
    for year in range(1976,2009,4):   
        PrizeOfCountry = readFile(year)            
        writeMainDataFile(PrizeOfCountry, year)
        data_avg = writAVRdataFile(PrizeOfCountry, year)
        year_olympic[year] = data_avg

    for i in year_olympic:
        x = set(year_olympic[i].keys())

        allCountry.update(x)
        
    for con in allCountry:
        country[con] = {}
        list_con = []
        list_g = []
        list_s = []
        list_b = []
        for year in year_olympic:#{}
            if(con in year_olympic[year]):
                list_con.append(year)
                list_g.append(year_olympic[year][con]['Gold'])
                list_s.append(year_olympic[year][con]['Silver'])
                list_b.append(year_olympic[year][con]['Bronze'])
        country[con]['year'] = list_con
        country[con]['Gold'] = list_g
        country[con]['Silver'] = list_s
        country[con]['Bronze'] = list_b
                
    for con in country:
        if(len(country[con]['year']) == 9):
            plotGraph(con,country[con])
        
        
        
            
    

#เขียนกราฟของแต่ละปี
def createLinerModel(year,data):
    x_ = sum(year)/len(year)
    y_ = sum(data)/len(data)
    print('x_ = ',x_)
    print('y_ = ',y_)
    n = len(year)
    Ex2 = sum([x**2 for x in year])
    Exy = sum([data[i]*year[i] for i in range(n)])
    b1 = (Exy - n*x_*y_)/(Ex2 - n*(x_**2))
    b0 = y_ - b1*x_
    result = "Y = %.2f + (%.2f*X)"%(b0,b1)
    return result
    
        
def plotGraph(country,data):
    #print(country,data)
    x = data['Gold']
    y = data['Silver']
    z = data['Bronze']
    gold = []
    silver = []
    bronze = []
    
    for i in x:
        gold.append(float(i))
    
    for i in y:
        silver.append(float(i))
    
    for i in z:
        bronze.append(float(i))

    #print(createLinerModel(data['year'],gold))

    
    #print(gold)
    #print(data['year'])
    plt.plot(data['year'],gold,label = 'Gold')
    plt.plot(data['year'],silver,label = 'Silver')
    plt.plot(data['year'],bronze,label = 'Bronze')

    plt.xlabel('year\n'+"Gold Medal model "+createLinerModel(data['year'],gold)+
               "Silver Medal model "+createLinerModel(data['year'],silver)+
               "\nBronze Medal model "+createLinerModel(data['year'],bronze))
    plt.ylabel('rate for get medals(100%)')
    plt.title(country)
    plt.legend()
    plt.show()
    
    
    
    
    

    



fileOfYear()


























