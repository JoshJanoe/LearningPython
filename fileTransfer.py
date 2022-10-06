#!/apps/python_3.7/bin/python3.7 
# incomplete and untested File Transfer script

import smtplib
import pysftp as sftp
from email.message import EmailMessage

dataDict = {
	"mailSubject":"<SUBJECT>",
	"mailFrom":"<FROM>",
	"mailTo":"<TO>",
	"mailBody":"<BODY>",
	#"mailUsername":"<USERNAME>",
	#"mailPassword":"<PASSWORD>",
	"companyHost":"<HOST>", 
	"companyServer":"<company-SERVER>",
	"companyUsername":"<USERNAME>",
	"companyPassword":"<PASSWORD>",
	"clientServer":"<CLIENT-SERVER>",
	"targetFilename":"<FILENAME>",
	"targetFile":"<FILE>"
	}

def getFile():
	print("Getting file...")
	s = sftp.Connection(host=dataDict.get("companyHost"), username=dataDict.get("companyUsername"), password=dataDict.get("companyPassword"))

	remotepath = dataDict.get("companyServer") 
	localpath = dataDict.get("targetFilename")
	s.get(remotepath,localpath)
	dataDict["targetFile"] = s.getfo(remotepath, localpath)

	s.close()
	print('{} retrieved from {}'.format(localpath,remotepath))



def sendToSFTP():
	print("Sending file to SFTP...")
	s = sftp.Connection(host=dataDict.get("companyHost"), username=dataDict.get("companyUsername"), password=dataDict.get("companyPassword"))

	remotepath = dataDict.get("clientServer") 
	localpath = dataDict.get("targetFilename")
	s.put(localpath,remotepath)
	
	s.close()
	print('{} sent to {}'.format(localpath,remotepath))



def sendEmail():
	print("Sending file as email attachment...")
	msg = EmailMessage()
	msg['Subject'] = dataDict.get("mailSubject")
	msg['From'] = dataDict.get("mailFrom")
	msg['To'] = dataDict.get("mailTo")
	msg.set_content(dataDict.get("mailBody"))
	
	with open(dataDict.get("targetFilename"), 'rb') as f:
		file_data = f.read()
		file_name=f.name

	msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

	with smtplib.SMTP_SSL('smtp.company.com', 465) as smtp:
		smtp.login(dataDict.get("companyUsername"), dataDict.get("companyPassword"))
		smtp.send_message(msg)

	print('Email containing {} sent to {}'.format(file_name, dataDict.get("mailTo")))

print("Beginning file transfer process")
getFile()
sendToSFTP()
sendEmail()
