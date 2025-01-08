from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import smtplib,ssl
from email.message import EmailMessage


driver = webdriver.Firefox()
driver.get("https://rds2.northsouth.edu/index.php/common/showofferedcourses") # put here the adress of your page
searchBox = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/label/input") # put here the content you have put in Notepad, ie the XPath

select = Select(driver.find_element(By.NAME,'offeredCourseTbl_length'))

# select by value 
select.select_by_value('100')

numberOfCourses = input("Enter number of courses: ")
coursesArr = []
for i in range(int(numberOfCourses)):
    courseName = input("Enter course name: ")
    coursesArr.append(courseName)

coursesVacant = ""
notifiedCourses = []

def sendSeatNotif(recieverEmail, message):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "nsuadvisingassistant@gmail.com"  # Enter your address 
    message = """\
    """+message

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'SEATS AVAILABLE FOR COURSES!'
    msg['From'] = sender_email
    msg['To'] = recieverEmail
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, "kxyqpgagpyxbrkxi")
        server.send_message(msg)
        server.quit()





# Checking courses every minute
while True:
    message = ""
    for i in coursesArr:
        searchBox.clear()
        searchBox.send_keys(i)

        table = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody")
        try:
            for i in range(1,100):
                try:
                    if int(driver.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr["+str(i)+"]/td[7]").text)>0 and driver.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr["+str(i)+"]/td[1]").text not in notifiedCourses:
                        message += driver.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr["+str(i)+"]/td[1]").text + "\n" + driver.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr["+str(i)+"]/td[2]").text + "\nSection: " + driver.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr["+str(i)+"]/td[3]").text + "\nFaculty: " + driver.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr["+str(i)+"]/td[4]").text + "\nTime: " + driver.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr["+str(i)+"]/td[5]").text + "\nRoom: " + driver.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr["+str(i)+"]/td[6]").text + "\nSeat: " + driver.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr["+str(i)+"]/td[7]").text+"\n\n\n"
                        
                        notifiedCourses.append(driver.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr["+str(i)+"]/td[1]").text)
                except:
                    pass

        except Exception as e:
            print(e)
    if message != "":
        sendSeatNotif("abir.akhand@northsouth.edu", message)
    message = ""
    time.sleep(2) # wait 2 seconds before a new iteration of the loop





