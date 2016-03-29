##单图博下载
url为图博地址

	url = r'https://quyu.tuchong.com/12728263/'
	t = Tuchong(url = url)
	t.download_blog()

##个人下载
###使用id号
例如个人主页为：https://tuchong.com/386025/
则id号为386025

    uid = 24935
    t = Tuchong(uid = uid)
    t.download_person()

###直接使用个人主页链接下载
部分个人主页使用二级域名，如https://leon870526.tuchong.com/
无法使用id号下载，则可以直接使用链接下载

    uid = r'https://leon870526.tuchong.com/'
    t = Tuchong(uid = uid)
    t.download_person()