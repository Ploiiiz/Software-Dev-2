from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time # for sleep
import random as rd

service = ChromeService(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)

# url = input("Your Form URL: ")
url = 'https://forms.gle/m1m9AFg5rp9LTYnZ8'
url2 = 'https://forms.gle/nus7DZoHF9KXTLsx5'
driver.get(url2)

# Just in case there are many types of containers
questions_class = 'Qr7Oae'
timecontainer = 'vEXS5c'
datecontainer = 'o7cIKf'
rowcontainer = 'gTGYUd'
optionbox = 'jgvuAb'
optionslist = 'OA0qNb'

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
    'other' : 'Hvn9fb'
    }

def checkboxAnsRD(current):
    g = []
    ans = current.find_elements(By.CLASS_NAME,minified['checkbox'])
    # for box in checkbox_answer: ##in g
    #     ans[box].click()
    rdcheckbox = rd.randint(1,len(ans))#สุ่มจำนวนติ๊ก
    for i in range(rdcheckbox):
        n = rd.randint(0,len(ans)-1)
        if( n not in g ):
            g.append(n)   
    
    # print(g)
    for box in g:
        if box == 5 :
            ans[box].click()
            ansother = current.find_elements(By.CLASS_NAME,minified['other'])
            ansother[0].clear()
            ansother[0].send_keys('hi')        
        else:
            ans[box].click()


def radioAnsRD(anss):  
     
    rdradio = rd.randint(0,len(anss)-1) 
    
    # print(rdradio)
        
    anss[rdradio].click()

def dropdownAnsRD(option):       
    rdradio = rd.randint(1,len(option))     
    # print(rdradio)        
    # option[rdradio].click()
    return rdradio
    
def shortNameAnsRD():       
    list_name = ['กิ่งดาว ดารณี', 'กชกร ส่งแสงเติม', 'กุลณัฐ ปรียะวัฒน์', 'กัญญา รัตนเพชร์', 'กัญญารัตน์ พงศ์กัมปนาท', 'กัญญาวีร์ สองเมือง', 'กันยรินทร์ นิธินพรัศม์', 'กาญจนา จินดาวัฒน์', 'กาญจน์เกล้า ด้วยเศียรเกล้า', 'กุณฑีรา สัตตบงกช', 'กุลธิดา พริ้งเกษมชัย', 'เกวลิน คอตแลนด์', 'เกวลิน พูลภีไกร', 'เกวลิน ศรีวรรณา', 'เกศริน เอกธวัชกุล', 'เกศรินทร์ น้อยผึ้ง', 'เก็จมณี วรรธนะสิน', 'แก่นใจ มีนะกนิษฐ์', 'แก้วมณี วัฒนวรากุล', 'กัญญ์ณรัณ วงศ์ขจรไกล', 'กุลฑีรา ยอดช่าง', 'กรณิศ เล้าสุบินประเสริฐ', 'กรองทอง อำนวยสวัสดิ์', 'กรองทอง รัชตะวรรณ', 'เขมนิจ จามิกรณ์', 'เขมิศรา พลเดช', 'เข็มอัปสร สิริสุขะ', 'เขมสรณ์ หนูขาว', 'โขมพัสตร์ อรรถยา', 'ขวัญตา บัวเปลี่ยนสี', 'คริส หอวัง', 'คามิลล่า กิตติวัฒน์', 'คัคกิ่งรักส์ คิคคิคสะระณัง', 'คัทลียา แมคอินทอช', 'คลาวเดีย จักรพันธุ์', 'คะนึงนิจ จักรสมิทธานนท์', 'แคทรียา อิงลิช', 'คิมเบอร์ลี แอน เทียมศิริ', 'คริษฐา สังสะโอภาส', 'จริญญา ศิริมงคลสกุล', 'จรินทร์พร จุนเกียรติ', 'จริยา แอนโฟเน่', 'จรรยา ธนาสว่างกุล', 'จารุณี สุขสวัสดิ์', 'จามจุรี เชิดโฉม', 'จารุวรรณ ปัญโญภาส', 'จารุศิริ ภูวนัย', 'จิรกิติยา บุญครองทรัพย์', 'จิระวดี อิศรางกูร ณ อยุธยา', 'จิรวรรณ เตชะหรูวิจิตร', 'จีรนันท์ มะโนแจ่ม', 'เจนี่ อัลภาชน์ ณ ป้อมเพชร', 'เจมี่ บูเฮอร์', 'เจสสิกา ภาสะพันธุ์', 'เจสสิก้า เอสพินเนอร์', 'จิดาภา ศิริบัญชาวรรณ', 'จุรี โอศิริ', 'ฉัตรฑริกา สิทธิพรม', 'ฉันทนา ธาราจันทร์', 'ฉัตรดาว สิทธิผล', 'ชไมพร จตุรภุช', 'ชนานา นุตาคม', 'โชติกา วงศ์วิลาศ', 'ชาลิดา วิจิตรวงศ์ทอง', 'ชญานิษฐ์ ชาญสง่าเวช', 'ชฎาพร วชิระปราณี', 'ชฎาพร รัตนากร', 'ชิดจันทร์ รุจิพรรณ', 'ชาร์เลท วาศิตา แฮเมเนา', 'ชมพู่ ก่อนบ่ายคลายเครียด', 'ชนัญญา เลิศวัฒนามงคล', 'ชนม์ทิดา อัศวเหม', 'ชาเคอลีน มึ้นช์', 'ชนิกานต์ ตังกบดี', 'ชนิดาภา พงศ์ศิลป์พิพัฒน์', 'ชุติมณฑน์ จึงเจริญสุขยิ่ง', 'ซาร่า ผุงประเสริฐ', 'เฌอปราง อารีย์กุล', 'เฌอมาลย์ บุญยศักดิ์']
     
    rdname = rd.randint(0,len(list_name)-1) 

    return list_name[rdname]
    
# Filling Forms
# short_answer = 'Lorem ipsum dolor sit amet'
short_answer = shortNameAnsRD()
long_answer  = short_answer + ', consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
time_answer = '10'
date_answer = '01012020'
checkbox_answer = [0,1]
dropdown_answer = 1
radio_answer = 2

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
                radioAnsRD(ans)
                # ans = current.find_elements(By.CLASS_NAME,minified['radio'])
                # ans[radio_answer].click()
            elif qtype == 'checkbox':       
                checkboxAnsRD(current)
                # ans = current.find_elements(By.CLASS_NAME,minified['checkbox'])
                # for box in checkbox_answer:
                #     ans[box].click()
            elif qtype == 'paragraph':     
                ans = current.find_element(By.CLASS_NAME,minified['paragraph'])
                ans.clear()
                ans.send_keys(long_answer)
            elif qtype == 'dropdown':     
                ans = current.find_element(By.CLASS_NAME,optionbox)
                ans.click()
                time.sleep(1)
                optionsbox = ans.find_element(By.CLASS_NAME,optionslist)
                options = optionsbox.find_elements(By.CLASS_NAME,minified['dropdown'])
                # dropdownAnsRD(options)
                rdAns = dropdownAnsRD(options)
                options[rdAns].click()
                time.sleep(1)
        elif container == 'Row':
            if qtype == 'radio':
                ans = current.find_elements(By.CLASS_NAME,radiorow)
                for row in ans:
                    choices = row.find_elements(By.CLASS_NAME,minified['radio'])
                    radioAnsRD(choices)
                    
                    # choices[radio_answer].click()
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

questions = getQuestions(driver)
def autoFill():
    questions = getQuestions(driver)
    questions_types = getQuestionsTypes(questions)
    answer(questions,questions_types)

while questions != []:
    autoFill()
    page += 1
    if page != 1:
        submitpath = buttons[1]


