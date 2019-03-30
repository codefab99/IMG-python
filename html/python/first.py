import mysql.connector
from mysql.connector import Error
import requests
import urllib3
from bs4 import BeautifulSoup

def decorator(func):
    def inner():
        try:
            mySQLconnection = mysql.connector.connect(host='localhost',
                                                    database='main',
                                                    user='bismita',
                                                    password='biscuit@7777')
            query = "SELECT * FROM user;"
            cursor = mySQLconnection.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            func(records)
            cursor.close()

        except Error as e:
            print("error in conn", e)
    return inner

def find_people(records):
    x = input("name of person to search- ")
    check= False
    for row in records:
        if x == row[0]:
            check = True
    if check:
        print(x,'exists')
    else:
        print('does not exist')

find_people = decorator(find_people)

class Person:
    def __init__(self, name, **kwargs):
        self.name = name
        self.work = kwargs['work']
        self.city = kwargs.get('city', "Roorkee")
    def show(self):

        print(f"My name is {self.name} and my current city is {self.city}")

hello = Person('Bismita')

def scrape(username):
    page = requests.get(f"https://www.facebook.com/{username}")
    soup = BeautifulSoup(page.content, 'html.parser')
    print("Current City:", end=" "),
    print(soup.find('span', class_='_2iel _50f7').get_text())
    print("Work:")
    print("[", end=" ")
    for tags in soup.find_all('div', class_='_2lzr _50f5 _50f7'):
        print(tags.find('a').contents[0], end=", ")
    print("]")
    print(end="\n")
    print("Favourites:")
    for tags in soup.find_all('tbody'):
        print(tags.find('th').get_text(), end=": ")
        print(tags.find('td').get_text())
        

name = input("Enter username: ")
scrape(name)

    