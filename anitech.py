"""
Use this code to insert data from DHT22 to SQLite Database

"""
import sqlite3
from sqlite3 import Error
from datetime import datetime
# Library for DHT22
import Adafruit_DHT

import I2C_LCD_driver
from time import *

import serial

# Initialize Sensor
DHT_SENSOR = Adafruit_DHT.DHT22
# Sensor GPIO
DHT_PIN = 4

auno_serial_speed = 9600
auno_serial_port = '/dev/ttyUSB0'
auno_ser = serial.Serial(auno_serial_port, auno_serial_speed)
auno_ser.flush


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
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
    sql = ''' INSERT INTO dht(date,temp,humi,co2x,o2xx)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid


def main():
    database = "/home/pi/anitech/database.db"
    humi, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    date = datetime.today().strftime('%Y-%m-%d %H:%M')
    mylcd = I2C_LCD_driver.lcd()

    auno_ser.write("m")
	time.sleep(.1)
	auno_data = auno_ser.readline()

    try:
        # Get arduino uno data
		auno_data = auno_data.strip('\r\n')
		auno_processed_data = auno_data.split(",")

        co2x = str(auno_processed_data[0])
		o2xx = str(auno_processed_data[1])

    # create a database connection
    conn = create_connection(database)
    with conn:
        # read dht
        temp = round(temp,3)
        humi = round(humi,3)
        dht = (date, temp, humi,co2x,o2xx);
        project_id = create_project(conn, dht)
        print(dht)

        mylcd.lcd_display_string("Date: " + date, 1)
        mylcd.lcd_display_string("Date: " + date, 2)
        mylcd.lcd_display_string("Temperature: " + temp, 3)
        mylcd.lcd_display_string("Humidity: " + humi, 4)


if __name__ == '__main__':
    main()
