import requests
from bs4 import BeautifulSoup
import re
import json
import csv
import time

# web url links
urls=''

# load url
contor=0
with open('sample_websites.csv', 'r') as f:
    #csv_reader = csv.reader(csv_file)

    for line in f.read():
        urls+= str(line)
urls=list(filter(None, urls.split('\n')))
#print(urls)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

#loop over urls
for url in urls:
#    print(url)
#   HTTP REQUEST
    res=requests.get('http://'+url)
    print('crawled base URL:', res.url)
    
    content=BeautifulSoup(res.text, 'lxml')
#    print(content)
    email_homepage=re.findall(r'[\w\.-]+@[\w\.-]+', content.get_text())
    phones_homepage=re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', content.get_text())




    #print('\nEmail home', email_homepage)
    #print('\nPhone home', phone_homepage)

    #data stocare extrageri
    contacte={
        'website': res.url,
        'email_homepage': ', '.join(email_homepage),
        'phones_homepage': ', '.join(phones_homepage),
        'email': '',
        'phone': ''
        }
    
    try:
    #extract contact link if available
        contact=content.find('a', text=re.compile('contact', re.IGNORECASE))['href']
        if 'http' in contact:
            contact_url=contact
        else:
            contact_url=res.url[0:-1] + contact
        
        res_contact=requests.get(contact_url)
        contact_content=BeautifulSoup(res_contact.text, 'lxml').get_text()
        #print(contact_content.url)
        print('crawled contact URL:', res_contact.url)
        #email=re.findall('(\w+@\w+\.\w+\.\w+)', contact_content)
        email=re.findall(r'[\w\.-]+@[\w\.-]+', contact_content)
        phones=re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', contact_content)
        if (email or email_homepage) or (phones_homepage or phones):
            contor+=1
        #print('\nEMAIL:', email)
        #print('\nPhone:', phones)
        
        #adaugare
        contacte['email']=', '.join(email)
        contacte['phone']=', '.join(phones)
        if contor>100:
            break
    except:
        pass

    print('\n\n', json.dumps(contacte, indent=2))
    
    with open('contacts.csv', 'a', newline='') as file:
        writer=csv.DictWriter(file, fieldnames=contacte.keys())
        #writer.writeheader()
        writer.writerow(contacte)
        #file.write("%s,%s\n"%(i, contacte[i]))



            