from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import credentials
import time # for sleep

service = ChromeService(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)

# login
email = credentials.email
password = credentials.pwd

# url = input("Your Form URL: ")
url = 'https://forms.gle/Z8rARWqQ4Wxc1kCt8'
url2 = 'https://forms.gle/nus7DZoHF9KXTLsx5'
driver.get(url2)
time.sleep(5)

# Just in case there are many types of containers
questions_class = 'Qr7Oae'
timecontainer = 'vEXS5c'
datecontainer = 'o7cIKf'
rowcontainer = 'gTGYUd'
optionbox = 'jgvuAb'
optionslist = 'OA0qNb'
question_word = 'M7eMe'

containers = [timecontainer,datecontainer,rowcontainer]
containers_name = ['Time', 'Date', 'Row']

# Sub-elements for rows container
checkboxrow = 'EzyPc'
radiorow = 'lLfZXe'

# Minified classes dict
minified = {
    'textinput':'whsOnd',
    'radio':'AB7Lab',
    'paragraph':'KHxj8b',
    'checkbox':'uHMk6b',
    'dropdown':'MocG8c',
    }

# Filling Forms
short_answer = 'Lorem ipsum dolor sit amet'
long_answer  = short_answer + ', consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
time_answer = '10'
date_answer = '01012020'
checkbox_answer = [0,1]
dropdown_answer = 1
radio_answer = 0

#Page Control
page = 1
buttons = ['//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div','//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span']
submitpath = buttons[0]

# Get current page questions container
def getQuestions(driver):
    q = driver.find_elements(By.CLASS_NAME,questions_class)
    return q


def getQuestionsTypes(questions):
    qtypes = []
    for num,question in enumerate(questions,1):
        #print('Question',num,end=' ')
        temp = []
        question_w = question.find_element(By.CLASS_NAME,question_word)
        print(question_w.text)
        for classname,name in zip(containers,containers_name):
            find = question.find_elements(By.CLASS_NAME,classname)
            if len(find) != 0:
                temp.append(name)
        if temp == []:
            temp.append(None)
        for key,value in zip(minified,minified.values()):
            find = question.find_elements(By.CLASS_NAME,value)
            if len(find) != 0:
                temp.append(key)
        if len(temp) < 2:
            temp.append(None)
        #temp[0] = question
        qtypes.append(tuple(temp))

    return qtypes

#print(questions_types)
def answer(questions,questions_types):
    for num in range(len(questions)):
        container = questions_types[num][0]
        qtype = questions_types[num][1]
        current = questions[num]
        if container == None:
            if qtype == 'textinput':
                ans = current.find_element(By.CLASS_NAME,minified['textinput'])
                ans.clear()
                ans.send_keys(short_answer)
            elif qtype == 'radio':
                ans = current.find_elements(By.CLASS_NAME,minified['radio'])
                ans[radio_answer].click()
            elif qtype == 'checkbox':
                ans = current.find_elements(By.CLASS_NAME,minified['checkbox'])
                for box in checkbox_answer:
                    ans[box].click()
            elif qtype == 'paragraph':
                ans = current.find_element(By.CLASS_NAME,minified['paragraph'])
                ans.clear()
                ans.send_keys(long_answer)
            elif qtype == 'dropdown':
                ans = current.find_element(By.CLASS_NAME,optionbox)
                ans.click()
                time.sleep(2)
                optionsbox = ans.find_element(By.CLASS_NAME,optionslist)
                options = optionsbox.find_elements(By.CLASS_NAME,minified['dropdown'])
                options[2].click()
                time.sleep(1)
        elif container == 'Row':
            if qtype == 'radio':
                ans = current.find_elements(By.CLASS_NAME,radiorow)
                for row in ans:
                    choices = row.find_elements(By.CLASS_NAME,minified['radio'])
                    choices[radio_answer].click()
            if qtype == 'checkbox':
                ans = current.find_element(By.CLASS_NAME,rowcontainer)
                cb_rows = ans.find_elements(By.CLASS_NAME,checkboxrow)
                for i in cb_rows:
                    choices = i.find_elements(By.CLASS_NAME,minified['checkbox'])
                    for j in choices:
                        j.click()
        elif container == 'Date':
            ans = current.find_element(By.CLASS_NAME,minified['textinput'])
            ans.send_keys(date_answer)
        elif container == 'Time':
            ans = current.find_elements(By.CLASS_NAME,timecontainer)
            for containers in ans:
                box = containers.find_element(By.CLASS_NAME,minified['textinput'])
                box.clear()
                box.send_keys(time_answer)
        else:
            pass
    sub = driver.find_element(By.XPATH,submitpath)
    sub.click()



def autoFill():
    questions = getQuestions(driver)
    questions_types = getQuestionsTypes(questions)
    answer(questions,questions_types)

def login(driver):
    e = driver.find_element(By.XPATH,"//input[@type='email']")
    e.clear()
    e.send_keys(email)
    e.send_keys(Keys.ENTER)
    time.sleep(4)

    p = driver.find_element(By.XPATH,"//input[@type='password']")
    p.clear()
    p.send_keys(password)
    p.send_keys(Keys.ENTER)
    time.sleep(7)

login(driver)
questions = getQuestions(driver)
while questions != []:
    autoFill()
    page += 1
    if page != 1:
        submitpath = buttons[1]
    time.sleep(3)



