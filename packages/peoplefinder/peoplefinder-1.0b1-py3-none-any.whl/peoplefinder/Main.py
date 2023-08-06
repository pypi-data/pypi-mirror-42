import os
import random
import shelve
import sys

from selenium import webdriver

from .SaveData import savedata
from .GetPhoto import get_photo
from .TelegramUpload import telegram_upload

if __name__ == "__main__":

    while True:
        try:
            _ = shelve.open('../Shelve/peopleData')  # import data
        except:
            os.makedirs('../Shelve')
            continue
        else:
            break

    data = shelve.open('../Shelve/peopleData')  # import or creates data

    driver = webdriver.Chrome()
    driver.get('https://web.whatsapp.com')

    input('Press enter once you have logged in... ')
    try:
        i = data['last_indice']  # pic indice
    except KeyError:
        i = 1
    else:
        pass

    j = sys.argv[1]  # quantity of independent loops
    send = sys.argv[2]  # choose between send and no send the pics
    ddd = sys.argv[3]  # phone ddd
    k = 0  # counter to reach j
    numbers = list()

    while k < int(j):
        print('{0}/{1} => {2:.1f}%'.format(str(k + 1), j, (k + 1) / int(j) * 100))
        number = '55{1}999{0}'.format(random.randint(100000, 999999), ddd)
        # number = '1010' #used for tests
        control = get_photo(driver, number)
        if control is not None:
            i += 1
            k += 1
            numbers.append(number)
        else:
            k += 1

    savedata(data, numbers, i)

    driver.close()

    if int(send) == 1:
        telegram_upload(data['temp_numbers'])
        data['temp_numbers'] = list()
    else:
        pass

    data.close()
