# http requests
import requests
# web scraping
from bs4 import BeautifulSoup
# send the mail
import smtplib
# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# system date and time manipulation
import datetime
now = datetime.datetime.now()

# email content placeholder
content = ''

# extract Hacker News Stories
def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt += ('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class':'title', 'valign': ''})):
        if tag.text != 'More':
            cnt += (str(i+1) + ' :: ' + tag.text + '\n' + '<br>')
        else:
            cnt += ''
    return cnt

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>----------<br>')
content += ('<br><br>End of Message')

# send email
print("Composing Email...")

# update email details
SERVER = 'smtp.gmail.com' # your smtp server
PORT = 587  # port number for gmail
FROM = ''  # your email id
TO = ''  # can be a list of email ids
PASS = ''  # your email account password

msg = MIMEMultipart()

msg['Subject'] = 'Top Stories HN [Automated Email]' + ' ' + str(now.day) + '-' \
                 + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print("Email Sent...")

server.quit()
