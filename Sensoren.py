import Adafruit_DHT
import spidev
import time
import math
import RPi._GPIO as GPIO
from DbClass import DbClass
import datetime
from decimal import Decimal
import mysql.connector as mc

# Define Variables

delay = 0.5
ldr_channel = 0

#Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)

def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data
def bereken(bitwaarde):
    voltage = bitwaarde/1023*3.3
    exp = (voltage-4.284289202)/-0.178003
    ppm = math.e**exp
    return ppm

def CO_inlezen():
    waarde =  readadc(1)
    if(waarde < 750):
        return "geen CO"
    else:
        return "Gevaar!"

def schakelaar_inlezen():
    stand1 = GPIO.input(25)
    stand2 = GPIO.input(24)
    stand3 = GPIO.input(23)
    stand4 = GPIO.input(18)
    if((stand1 == False) and (stand2 == True) and (stand3 == True) and (stand4 == True)):
        CO2_stand = "CO2_stand"
        return CO2_stand
    elif((stand1 == True) and (stand2 == False) and (stand3 == True) and (stand4 == True)):
        CO_stand = "CO_stand"
        return CO_stand
    elif((stand1 == True) and (stand2 == True) and (stand3 == False) and (stand4 == True)):
        hum_stand = "hum_stand"
        return hum_stand
    elif ((stand1 == True) and (stand2 == True) and (stand3 == True) and (stand4 == False)):
        temp_stand = "temp_stand"
        return temp_stand
    return

def CO2_quality(waardeppm):
    if(waardeppm < 1200):
        Quality_CO2 = "GOOD"
        ID = 1
        return Quality_CO2,ID
    elif((waardeppm <= 2500) and (waardeppm >= 1200)):
        Quality_CO2 = "AVERAGE"
        ID = 2
        return Quality_CO2,ID
    elif(waardeppm>2500):
        Quality_CO2 = "BAD"
        ID = 3
        return Quality_CO2,ID

def humidity_quality(waardeProcent):
    if (waardeProcent < 30):
        hum_qual = "BAD"
        hum_qual_ID = 3
        return hum_qual,hum_qual_ID
    elif(waardeProcent >= 30) and (waardeProcent <= 55):
        hum_qual = "AVERAGE"
        hum_qual_ID = 2
        return hum_qual,hum_qual_ID
    elif(waardeProcent > 55):
        hum_qual = "GOOD"
        hum_qual_ID = 1
        return hum_qual,hum_qual_ID

def relay230V(always_on,gas_on,CO2,CO):
    if ((always_on == "1")) or ((gas_on == "1") and ((CO2 > 2000) or (CO != "geen CO"))):
        GPIO.output(12,GPIO.HIGH)
    else:
        GPIO.output(12,GPIO.LOW)
    return

def relayVentilator(ventWaarde):
    if ((ventWaarde == "1")):
        GPIO.output(17,GPIO.HIGH)
    else:
        GPIO.output(17,GPIO.LOW)
    return




RS = 16
RW = 20
E = 21

D4 = 6
D5 = 13
D6 = 19
D7 = 26
GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

class LCD:

    def __init__(self,par_RS,par_RW,par_E,par_DB4,par_DB5,par_DB6,par_DB7):
        self.__RS = par_RS
        self.__RW = par_RW
        self.__E = par_E
        self.__DB4 = par_DB4
        self.__DB5 = par_DB5
        self.__DB6 = par_DB6
        self.__DB7 = par_DB7

        allpins = [self.__RS,self.__RW,self.__E, self.__DB4, self.__DB5, self.__DB6, self.__DB7]

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for pin in allpins:
            GPIO.setup(pin, GPIO.OUT)


        self.__pins = [par_DB7,par_DB6,par_DB5,par_DB4]
        self.__delay_instructie = 0.005


    def __eHoogInstructie(self):
        GPIO.output(self.__E, 1)
        GPIO.output(self.__RS, 0)
        GPIO.output(self.__RW, 0)

    def __eLaagInstructie(self):
        GPIO.output(self.__E, 0)
        GPIO.output(self.__RS, 0)
        GPIO.output(self.__RW, 0)

    def __eHoogData(self):
        GPIO.output(self.__E, 1)
        GPIO.output(self.__RS, 1)
        GPIO.output(self.__RW, 0)

    def __eLaagData(self):
        GPIO.output(self.__E, 0)
        GPIO.output(self.__RS, 1)
        GPIO.output(self.__RW, 0)

    def FunctionSet(self):
        self.__eHoogInstructie()
        GPIO.output(self.__RS, GPIO.LOW)
        GPIO.output(self.__RW, GPIO.LOW)
        GPIO.output(self.__DB7, GPIO.LOW)
        GPIO.output(self.__DB6, GPIO.LOW)
        GPIO.output(self.__DB5, GPIO.HIGH)
        GPIO.output(self.__DB4, GPIO.LOW)
        self.__eLaagInstructie()
        time.sleep(self.__delay_instructie)

    def Display_On(self):
        self.__eHoogInstructie()
        GPIO.output(self.__RS, GPIO.LOW)
        GPIO.output(self.__RW, GPIO.LOW)
        GPIO.output(self.__DB7, GPIO.LOW)
        GPIO.output(self.__DB6, GPIO.LOW)
        GPIO.output(self.__DB5, GPIO.LOW)
        GPIO.output(self.__DB4, GPIO.LOW)
        self.__eLaagInstructie()
        self.__eHoogInstructie()
        GPIO.output(self.__DB7, GPIO.HIGH)
        GPIO.output(self.__DB6, GPIO.HIGH)
        GPIO.output(self.__DB5, GPIO.HIGH)
        GPIO.output(self.__DB4, GPIO.HIGH)
        self.__eLaagInstructie()
        time.sleep(self.__delay_instructie)

    def Clear_Display(self):
        self.__eHoogInstructie()
        GPIO.output(RS, GPIO.LOW)
        GPIO.output(self.__RW, GPIO.LOW)
        GPIO.output(self.__DB7, GPIO.LOW)
        GPIO.output(self.__DB6, GPIO.LOW)
        GPIO.output(self.__DB5, GPIO.LOW)
        GPIO.output(self.__DB4, GPIO.LOW)
        self.__eLaagInstructie()
        self.__eHoogInstructie()
        GPIO.output(self.__DB7, GPIO.LOW)
        GPIO.output(self.__DB6, GPIO.LOW)
        GPIO.output(self.__DB5, GPIO.LOW)
        GPIO.output(self.__DB4, GPIO.HIGH)
        self.__eLaagInstructie()
        time.sleep(self.__delay_instructie)

    def Reset(self):
        self.__eHoogInstructie()
        GPIO.output(self.__RS, GPIO.LOW)
        GPIO.output(self.__RW, GPIO.LOW)
        GPIO.output(self.__DB7, GPIO.LOW)
        GPIO.output(self.__DB6, GPIO.LOW)
        GPIO.output(self.__DB5, GPIO.HIGH)
        GPIO.output(self.__DB4, GPIO.HIGH)
        self.__eLaagInstructie()
        self.__eHoogInstructie()
        GPIO.output(self.__DB7, GPIO.HIGH)
        GPIO.output(self.__DB6, GPIO.LOW)
        GPIO.output(self.__DB5, GPIO.HIGH)
        GPIO.output(self.__DB4, GPIO.HIGH)
        self.__eLaagInstructie()

    def __setGPIODataBits(self,data, instructie):
        x = data
        deel1 = x & 0xF0
        filter = 0x80

        if instructie:
            self.__eHoogInstructie()
        else:
            self.__eHoogData()

        for i in range(0, 4):
            deel1 = data & filter
            GPIO.output(self.__pins[i], deel1)
            filter >>= 1

        if instructie:
            self.__eLaagInstructie()
        else:
            self.__eLaagData()

        deel2 = x & 0x0F
        deel2 = deel2 << 4

        if instructie:
            self.__eHoogInstructie()
        else:
            self.__eHoogData()

        for i in range(0, 4):
            deel2 = data & filter
            GPIO.output(self.__pins[i], deel2)
            filter >>= 1

        if instructie:
            self.__eLaagInstructie()
        else:
            self.__eLaagData()

    def __set_DDRAM(self,plaats):
        self.__setGPIODataBits(0x80 | plaats, 1)

    def WriteText(self,text):
        i = 1
        for letter in text:
            # 2 keer doorklokken
            number = ord(letter)
            self.__setGPIODataBits(number, 0)
            time.sleep(self.__delay_instructie)
            if i == 16:
                print("JA")
                self.__set_DDRAM(0x40)
            i += 1

    def WriteCO2Waarde(self,waarde):
        i = 1
        self.__set_DDRAM(0x00)
        CO2 = "CO2: "
        CO2 += str(waarde)
        CO2 += " ppm"
        for letter in CO2:
            number = ord(letter)
            self.__setGPIODataBits(number, 0)
            time.sleep(self.__delay_instructie)

    def WriteTempWaarde(self,waarde):
        i = 1
        self.__set_DDRAM(0x00)
        temp = "Temp C: "
        temp += str(waarde)
        temp += " C"
        for letter in temp:
            number = ord(letter)
            self.__setGPIODataBits(number, 0)
            time.sleep(self.__delay_instructie)

    def WriteLuchtvochtigheidWaarde(self,waarde):
        i = 1
        self.__set_DDRAM(0x00)
        luchtvochtigheid = "hum.: "
        luchtvochtigheid += str(waarde)
        luchtvochtigheid += " %"
        for letter in luchtvochtigheid:
            number = ord(letter)
            self.__setGPIODataBits(number, 0)
            time.sleep(self.__delay_instructie)

    def WriteCoWaarde(self,waarde):
        i = 1
        self.__set_DDRAM(0x00)
        comfortniveau = "CO: "
        comfortniveau += str(waarde)
        for letter in comfortniveau:
            number = ord(letter)
            self.__setGPIODataBits(number, 0)
            time.sleep(self.__delay_instructie)

    def WriteQualityWaarde(self,waarde):
        i = 1
        self.__set_DDRAM(0x40)
        quality = ""
        quality += str(waarde)
        for letter in quality:
            number = ord(letter)
            self.__setGPIODataBits(number, 0)
            time.sleep(self.__delay_instructie)

    def WriteTempF(self,waarde):
        i = 1
        self.__set_DDRAM(0x40)
        quality = "Temp F: "
        quality += str(waarde)
        quality += " F"
        for letter in quality:
            number = ord(letter)
            self.__setGPIODataBits(number, 0)
            time.sleep(self.__delay_instructie)

LCD = LCD(RS,RW,E,D4,D5,D6,D7)
temperatuur_oud = 0
temp_fahrenheit_oud = 0
humidity_oud = 0
CO2_valueppm_oud = 0
CO_oud = 0


try:
    while True:
        connection = mc.connect(host="localhost", user="Air-checker", passwd="root", db="AirChecker")
        cursor = connection.cursor()
        q5 = "SELECT minutes FROM time_between WHERE ID= '1'"
        cursor.execute(q5)
        tijd = cursor.fetchone()
        tijd = tijd[0]
        Tijd_ertussen = float(tijd * 21.4285714286)
        Tijd_ertussen = int(Tijd_ertussen)
        connection.commit()
        i=0

        while(i< Tijd_ertussen):
            i+=1
            q5 = "SELECT minutes FROM time_between WHERE ID= '1'"
            cursor.execute(q5)
            tijd = cursor.fetchone()
            tijd = tijd[0]
            Tijd_ertussen = float(tijd * 21.4285714286)
            Tijd_ertussen = int(Tijd_ertussen)
            connection.commit()

            q6 = "SELECT state FROM relay WHERE relay = '230V_GAS'"
            cursor.execute(q6)
            relay_gas = cursor.fetchone()
            relay_gas = relay_gas[0]
            connection.commit()
            q7 = "SELECT state FROM relay WHERE relay = '230V_ALWAYS'"
            cursor.execute(q7)
            relay_always = cursor.fetchone()
            relay_always = relay_always[0]
            connection.commit()
            q8 = "SELECT state FROM relay WHERE relay = 'MOTOR'"
            cursor.execute(q8)
            relay_motor = cursor.fetchone()
            relay_motor = relay_motor[0]
            relay_motor
            connection.commit()
            LCD.FunctionSet()
            LCD.Display_On()
            LCD.Clear_Display()
            stand = schakelaar_inlezen()
            CO2_value = readadc(0)
            CO2_valueppm = bereken(float(CO2_value))
            CO = CO_inlezen()
            luchtvochtigheid, temperatuur = Adafruit_DHT.read(22, 22)
            while ((temperatuur == None) or (luchtvochtigheid == None)):
                luchtvochtigheid, temperatuur = Adafruit_DHT.read(22, 22)
            temp_fahrenheit = (float(temperatuur) * (9 / 5)) + 32
            temp_fahrenheit = Decimal(temp_fahrenheit)
            relay230V(relay_always, relay_gas, CO2_valueppm, CO)
            relayVentilator(relay_motor)
            if (stand == "CO2_stand"):
                LCD.WriteCO2Waarde(round(CO2_valueppm, 2))
                LCD.WriteQualityWaarde(CO2_quality(CO2_valueppm)[0])
                time.sleep(2)
                stand = schakelaar_inlezen()
                LCD.Clear_Display()

            elif (stand == "temp_stand"):
                LCD.WriteTempWaarde(round(temperatuur, 2))
                LCD.WriteTempF(round(temp_fahrenheit,2))
                time.sleep(3)
                stand = schakelaar_inlezen()
                LCD.Clear_Display()


            elif (stand == "hum_stand"):
                LCD.WriteLuchtvochtigheidWaarde(round(luchtvochtigheid, 2))
                LCD.WriteQualityWaarde(humidity_quality(luchtvochtigheid)[0])
                time.sleep(3)
                stand = schakelaar_inlezen()
                LCD.Clear_Display()

            elif (stand == "CO_stand"):
                LCD.WriteCoWaarde(CO)
                time.sleep(3)
                LCD.Clear_Display()
            LCD.Reset()
            verschil_CO2 = CO2_valueppm - CO2_valueppm_oud
            CO2_valueppm_oud = CO2_valueppm
            verschil_CO2 = Decimal(verschil_CO2)
            CO2_valueppm = Decimal(CO2_valueppm)
            CO2_kwal = CO2_quality(CO2_valueppm)
            CO2_kwal_ID = CO2_kwal[1]
            hum_kwal_ID = humidity_quality(luchtvochtigheid)[1]
            if (CO == "Gevaar!"):
                CO_kwal = 3
            else:
                CO_kwal = 1
            verschil_hum = luchtvochtigheid - humidity_oud
            humidity_oud = luchtvochtigheid
            verschil_temp_C = temperatuur - temperatuur_oud
            temperatuur_oud = temperatuur
            verschil_temp_F = temp_fahrenheit - temp_fahrenheit_oud
            temp_fahrenheit_oud = temp_fahrenheit

        q1 = "INSERT INTO co2 (Date,Time,Waarde_ppm,Stijging_daling_ppm,relatieve_kwaliteit_ID) VALUES (CURDATE(),CURTIME(),'{param1}','{param2}','{param3}')"
        q1 = q1.format(param1=CO2_valueppm, param2=verschil_CO2, param3=CO2_kwal_ID)
        cursor.execute(q1)
        connection.commit()
        q2 = "INSERT INTO co (Date,Time,CO_aanwezig,Relatieve_kwaliteit_ID) VALUES (CURDATE(),CURTIME(),'{param1}','{param2}')"
        q2 = q2.format(param1=CO, param2=CO_kwal)
        cursor.execute(q2)
        connection.commit()
        q3 = "INSERT INTO luchtvochtigheid (Date,Time,Waarde_procent,Stijging_daling_procent,Relatieve_kwaliteit_ID) VALUES (CURDATE(),CURTIME(),'{param1}','{param2}','{param3}')"
        q3 = q3.format(param1=luchtvochtigheid, param2=verschil_hum, param3=hum_kwal_ID)
        cursor.execute(q3)
        connection.commit()
        q4 = "INSERT INTO temperatuur (Date,Time,Waarde_celcius,Stijging_daling_C,waarde_fahrenheit,stijging_daling_fahrenheit) VALUES (CURDATE(),CURTIME(),'{param1}','{param2}','{param3}','{param4}')"
        q4 = q4.format(param1=temperatuur, param2=verschil_temp_C, param3=temp_fahrenheit, param4=verschil_temp_F)
        cursor.execute(q4)
        connection.commit()
        print("opgeslagen")

except KeyboardInterrupt:
    connection.close()