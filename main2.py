from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import traceback
import smtplib,ssl
from email.message import EmailMessage

courseWanted = input("Enter the course you want to take: ")
print("Please let Firefox do its thing and keep an eye on your email for seat availabilty updates. We will update you once a seat is vacant for "+courseWanted)

driver = webdriver.Firefox()
driver.get("https://rds3.northsouth.edu/index.php")
usernameBox = driver.find_element(By.NAME, "username") 
usernameBox.send_keys("2221699")
nextBtn = driver.find_element(By.NAME, "commit") 
nextBtn.click();
time.sleep(2)

passwordBox = driver.find_element(By.NAME, "password")
passwordBox.send_keys("---")

captchaImg = driver.find_element(By.XPATH, '//*[@id="main-container"]/div/div[2]/div/div/div[1]/div[2]/form/div[3]/div[2]/img')
screenshot_path = 'screenshot.png'
captchaImg.screenshot(screenshot_path)

driver2 = webdriver.Firefox()
driver2.get("https://www.imagetotext.info/")

imgUpBtn = driver2.find_element(By.NAME, "file")
imgUpBtn.send_keys(os.path.dirname(os.path.abspath(__file__))+"\\screenshot.png")
submitBtn = driver2.find_element(By.ID, 'jsShadowRoot')
submitBtn.click()

time.sleep(20)
div_element = driver2.find_element(By.XPATH, '//*[@id="result-sec"]/div[1]')

div_text = div_element.text

div_text_cleaned = div_text.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ','')

driver2.close()

captchaBox = driver.find_element(By.NAME, "captcha")
captchaBox.send_keys(div_text_cleaned)

loginBtn = driver.find_element(By.NAME, "commit")
loginBtn.click()



driver.get("https://rds3.northsouth.edu/index.php/students/advising")
courseSearchBox = driver.find_element(By.NAME, 'searchText')
courseSearchBox.send_keys(courseWanted)

table = driver.find_element(By.XPATH, '//*[@id="courseList"]')

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



while True:
    driver.get("https://rds3.northsouth.edu/index.php/students/advising")
    try:
        list(notifiedCourses)
        for i in range(1,100):
            try:
                if driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}{str(i)}"]/td[1]').text in notifiedCourses:
                    pass
                else:
                    if driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}{str(i)}"]/td[1]').text.split(".",1)[0] == courseWanted and int(driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}{str(i)}"]/td[2]').text.split("(",1)[0]) < int(driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}{str(i)}"]/td[2]').text.split("(",1)[1].replace(')','')) and driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}{str(i)}"]/td[1]').text not in notifiedCourses:
                        seatsVacant = int(driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}{str(i)}"]/td[2]').text.split("(",1)[1].replace(')','')) - int(driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}{str(i)}"]/td[2]').text.split("(",1)[0])
                        indivCourse = courseWanted + " - Section: " + driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}{str(i)}"]/td[1]').text.split(".",1)[1] + ", Available Seats: "+str(seatsVacant)
                        coursesVacant = coursesVacant + indivCourse + "\n "
                        notifiedCourses.append(driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}{str(i)}"]/td[1]').text)
                
                if driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}L{str(i)}"]/td[1]').text in notifiedCourses:
                    pass
                else:   
                    if driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}L{str(i)}"]/td[1]').text.split(".",1)[0] == courseWanted+'L' and int(driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}L{str(i)}"]/td[2]').text.split("(",1)[0]) < int(driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}L{str(i)}"]/td[2]').text.split("(",1)[1].replace(')','')) and driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}L{str(i)}"]/td[1]').text not in notifiedCourses:
                        seatsVacant = int(driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}L{str(i)}"]/td[2]').text.split("(",1)[1].replace(')','')) - int(driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}L{str(i)}"]/td[2]').text.split("(",1)[0])
                        indivCourse = courseWanted+'L' + " - Section: " + driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}L{str(i)}"]/td[1]').text.split(".",1)[1] + ", Available Seats: "+str(seatsVacant)
                        coursesVacant = coursesVacant + indivCourse + "\n"
                        notifiedCourses.append(driver.find_element(By.XPATH, f'//*[@id="clist{courseWanted}L{str(i)}"]/td[1]').text)

            except Exception as e:
                pass

        if coursesVacant != "":
            sendSeatNotif('abir.akhand@northsouth.edu', coursesVacant)
        coursesVacant = ""
        

    except Exception as e:
        print(traceback.format_exc())


