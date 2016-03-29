#coding : utf-8
import requests
import re
from bs4 import BeautifulSoup
import os
import json
import time

class Tuchong(object):
	def __init__(self, url = None, uid = None):
		self.url = url
		self.uid = uid
		self.num = 20

	def download_blog(self, url = None, path = r'./img/'):
		if path == r'./img/':
			url = self.url
		else:
			path = self.author_path

		try:
			os.mkdir(path)
		except:
			pass

		if url == None:
			print u'Error: URL is None!'
			return False

		try:
			response = requests.get(url)
		except:
			print u'Request error!'

		text = response.text
		soup = BeautifulSoup(text, 'lxml')

		title = soup.h1.text
		if title == u'\u6b64\u56fe\u535a\u9700\u8981\u767b\u9646\u540e\u67e5\u770b':
			return False
		l = list(r'\/:*?"<>|')
		for i in l:
			if i in title:
				title = title.replace(i, '_')

		try:
			article = soup.article.text
		except:
			article = u'-------- None --------'
		author = soup.hgroup.a.attrs['title']
		href = soup.hgroup.a.attrs['href']
		post_time = soup.hgroup.time.attrs['datetime']

		imglist = re.findall(r'<img src="(.*)" class=.*alt="" />',text)

		try:
			os.mkdir(path + title + r'/')
		except:
			pass

		file_path = path + title + r'/'
		print 'All: %d' % len(imglist)
		print file_path.encode('gbk')
		with open(file_path + 'info.txt', 'w') as f:
			f.write(author.encode('utf8')), f.write('\t')
			f.write(href), f.write('\n')

			f.write(title.encode('utf8')), f.write('\t')
			f.write(url), f.write('\n')

			f.write(article.encode('utf8')), f.write('\n')
			f.write(post_time.encode('utf8')), f.write('\n')

		for i in range(len(imglist)):
			try:
				response = requests.get(imglist[i])
			except:
				time.sleep(5)
				response = requests.get(imglist[i])
			img_path = file_path + title + r'_' + str(i+1) + r'.jpg'
			try:
				with open(img_path, 'rb') as f:
					print img_path + ' is OK!'
			except:
				print img_path.encode('gbk'),
				with open(img_path, 'wb') as f:
					f.write(response.content)
				print '\t%d/%d' % (i+1, len(imglist))
	
	def get_json(self, published_time):
		blog_list = []
		if type(self.uid) is str:
			url = self.uid
		else:
			url = r'https://tuchong.com/%d/' % self.uid
		print url

		r = requests.get(url)
		text = r.text
		soup = BeautifulSoup(text, 'lxml')

		if type(self.uid) is str:
			f_img = soup.find('img', attrs={'class':'profile-icon'})
			temp_id = f_img.attrs['src'].split('/')[5]
			self.uid = int(temp_id)

		meta = soup.select(r'meta[name="author"]')[0]
		author = meta.attrs['content']
		l = list(r'\/:*?"<>|')
		for i in l:
			if i in author:
				author = author.replace(i, '_')
		self.author_path = r'./' + author + r'/'

		last_published_at = published_time
		url_json = r'https://tuchong.com/rest/sites/%d/posts/' % (self.uid) + last_published_at + '?limit=%d' % self.num
		response = requests.get(url_json)
		data = json.loads(response.text)
		if data['result'] == u'ERROR':
			print 'Error!'
			return False,False
		posts = data['posts']
		if posts:
			for i in range(len(posts)):
				post = posts[i]
				url = post['url']
				blog_list.append(url)
				published_at = post['published_at']
				if i == (len(posts)-1):
					last_published_at = published_at
		else:
			return False,False

		return (blog_list, last_published_at)

	def download_person(self):
		now = time.localtime()
		published_time = '%d-%d-%d %d:%d:%d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
		blog_list, last_published_at = self.get_json(published_time)
		while blog_list:
			for i in blog_list:
				print i
				try:
					self.download_blog(url = i, path = self.author_path)
				except:
					continue
			blog_list, last_published_at = self.get_json(last_published_at)


if __name__ == '__main__':
	# uid = 24935
	# t = Tuchong(uid = uid)
	# t.download_person()
	
	# url = r'https://quyu.tuchong.com/12728263/'
	# t = Tuchong(url = url)
	# t.download_blog()
	
	uid = r'https://tuchong.com/490455/'
	t = Tuchong(uid = uid)
	t.download_person()
