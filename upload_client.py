import requests
from bs4 import BeautifulSoup

def upload(username, password, host,filename="LICENSE") :
	zimbra = requests.session()
	k = zimbra.get(host, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},allow_redirects=True,stream=True)
	if "503" in str(k):
		return "Servidor caído";
	elif "404" in str(k):
		return "Servidor no encontrado";
	elif "403" in str(k):
		return "Acceso denegado"
	else:
		soup = BeautifulSoup(k.text, "html.parser")
		token = soup.find("input", attrs={"name": "login_csrf"})["value"]
		params = {'loginOp':'login','login_csrf':token,'username':username, 'password':password,'zrememberme':'1','client':'standard'}
		s = zimbra.post(host, params,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},allow_redirects=True,stream=True)
		tok = zimbra.get(host+"/m/zmain", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},allow_redirects=True,stream=True)
		cook = s.cookies.get_dict()
		s = zimbra.get(host,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},cookies=cook,allow_redirects=True,stream=True)
		if "404" in str(s):
			return "Página no encontrada"
		else:
			if "403" in str(s):
				return "Sin permiso de acceso, use un proxy"
			else:
				if "login_csrf" in s.text:
					return "Usuario incorrecto"
				else:
					datos = zimbra.get(host+"/h/search?st=briefcase", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},cookies=cook,allow_redirects=True,stream=True)
					soup = BeautifulSoup(datos.text, "html.parser")
					crumb = soup.find("input", attrs={"name":"crumb"})["value"]
					sc = soup.find("a", attrs={"id": "NEW_UPLOAD"})["href"].replace("?si=0&amp;so=0&amp;sc=","").replace("&amp;st=briefcase&amp;action=compose","")
					files = {"fileUpload": open(filename, "rb")}
	
					data = {"actionAttachDone":"Hecho","doBriefcaseAction":"1","sendUID":""}
					web = host+"/h/search?si=0&so=0&sc="+sc+"&sfi=16&st=briefcase&crumb="+crumb+"&action=newbrief&lbfums="
					post = zimbra.post(web,data=data,files=dict(files),headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},cookies=cook,allow_redirects=True,stream=True)
					briefcase = zimbra.get(host+"/h/search?st=briefcase&sfi=16", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},cookies=cook,allow_redirects=True,stream=True)
					if "caducado" in post.text:
						return "Caduco"
					else:
						if filename in briefcase.text:
							returnvar = filename+' SUBIDO: \n\n <a href="https://correo.uclv.edu.cu/home/'+username+'/Briefcase/'+filename+'?auth=co">DESCARGAR</a>'
							return returnvar
						else:
							return 'Error al subir'
#TechDev @techdev_pro