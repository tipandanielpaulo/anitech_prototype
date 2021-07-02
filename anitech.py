"""
Use this code to insert data from DHT22 to SQLite Database

"""
import sqlite3
from sqlite3 import Error
from datetime import datetime
import psycopg2

host = "ec2-35-168-145-180.compute-1.amazonaws.com"
dbname = "d39n6sb6mps83v"
user = "tlmojlfzsqvceh"
password = "c6d0b0a6ce827b5ab182a15ad863662628cdc4c159aa87ad1015e352d2659299"
sslmode = "require"
conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)

# Library for DHT22
import Adafruit_DHT

import I2C_LCD_driver
from time import sleep

import serial

# Initialize Sensor
DHT_SENSOR = Adafruit_DHT.DHT22
# Sensor GPIO
DHT_PIN = 4

auno_serial_speed = 9600
auno_serial_port = '/dev/ttyUSB0'
auno_ser = serial.Serial(auno_serial_port, auno_serial_speed)
auno_ser.flush

# File
filename = '/home/pi/rq_data/rq_' +'{:%Y-%m-%d}'.format(datetime.now())+'.csv'
file = open(filename,'a')


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        #conn = sqlite3.connect(db_file)
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

    except Error as e:
        print(e)
    return conn

def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO rq_table(id, date, co2x, o2xx, temp, humi, type)
                VALUES(%s,%s,%s,%s,%s,%s,%s) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid


def main():
	database = "/home/pi/anitech_prototype/database.db"
	humi, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
	date = datetime.today().strftime('%Y-%m-%d %H:%M')
	mylcd = I2C_LCD_driver.lcd()

	auno_ser.write(b'\x0101')
	sleep(.1)
	auno_data = auno_ser.readline().decode('utf-8')


    # create a database connection
	conn = create_connection(database)
	with conn:

		auno_data = auno_data.strip('\r\n')
		auno_processed_data = auno_data.split(",")
		if len(auno_processed_data) == 2:
			print(len(auno_processed_data))
		else:
			exit()
		o2xx = str(auno_processed_data[0])
		co2x = str(auno_processed_data[1])

       		# read dht
		temp = round(temp,3)
		humi = round(humi,3)
		dht = (date, temp, humi,co2x,o2xx)

		mylcd.lcd_display_string(date, 1)
		mylcd.lcd_display_string("CO2 in ppm: " + co2x, 2)
		mylcd.lcd_display_string("O2 in %vol: " + o2xx, 3)
		mylcd.lcd_display_string("Temp:" +str(temp) + " Hum:" + str(humi) , 4)


		co2s = str(co2x)
		o2ss = str(o2xx)

		file.write("{:%Y-%m-%d %H:%M},".format(datetime.now()))
		file.write(co2s + "," + o2ss + "," + str(temp) + "," + str(humi) )
		file.write("\n")
		file.flush()

		try:

			project_id = create_project(conn, dht)
			print(dht)
		except:
			pass


if __name__ == "__main__":
	main()
