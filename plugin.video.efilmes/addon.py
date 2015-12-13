#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2015 acamposxp
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, HTMLParser, urlresolver
import xml.etree.ElementTree as ET
import jsunpack
from bs4 import BeautifulSoup

h = HTMLParser.HTMLParser()

versao = '0.0.2'
addon_id = 'plugin.video.efilmes'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
url_base = 'http://efilmesnarede.com/'


################################################## 

# MENUS############################################
def CATEGORIES():
    dialog = xbmcgui.Dialog()
    addDir('[B]Categorias[/B]',url_base,1,'http://i.imgur.com/W2okuob.jpg')
    addDir('[B]Lançamentos[/B]',url_base+'category/lancamentos/',2,'http://i.imgur.com/W2okuob.jpg')
    addDir('[B]Legendados[/B]',url_base+'category/legendados/',2,'http://i.imgur.com/W2okuob.jpg')
    addDir('[B]HD 720p[/B]',url_base+'category/blu-ray-720p/',2,'http://i.imgur.com/W2okuob.jpg')
    addDir('[B]Séries[/B]',url_base+'series-online',1,'http://i.imgur.com/W2okuob.jpg')
    addDir('[B]Animes[/B]',url_base+'http://www.animeson.tv',1,'http://i.imgur.com/W2okuob.jpg')	
    addDir('[B]Pesquisar[/B]', '-',3,'http://www.shoppingportaldaserra.com.br/2013/img/lupa.png')


###################################################################################
# FUNCOES

def listar_categorias(url):
    print url
    html = abrir_url(url)
    soup = BeautifulSoup(html)
    arquivo   = soup("ul",{"class":"m-cat"})[0]
    categorias = arquivo("li")
    total = len(categorias)
    for categoria in categorias:
            titulo = categoria.text.encode('utf-8')
            if not 'categoria' in titulo:
	                url = categoria.a["href"]
	                img = artfolder  + '.png'
	                addDir(titulo,url,2,img)
    xbmc.executebuiltin('Container.SetViewMode(515)')	
	
def listar_videos(url):
    print url
    html = abrir_url(url)
    soup = BeautifulSoup(html)
    arquivo = soup("div",{"class":"ib-miniaturas lista-miniaturas"})[0]
    filmes = soup("div",{"class":"ib-miniatura"})
    total = len(filmes)
    for filme in filmes:
        titulo = filme.img["alt"].replace('Assistir ','').replace('Filme ','')
        url = filme.a["href"]
        img = filme.img["src"].encode('utf-8')
        addDir("[B]"+titulo.encode('utf-8')+"[/B]",url,4,img,False,total)	
    try:
	    addDir('Página Seguinte >>','http://efilmesnarede.com/category/lancamentos/page/2/',1,"http://i.imgur.com/63Qyw7k.png")
    except:
	    pass
    xbmcplugin.setContent(int(sys.argv[1]), 'episodies')
    xbmc.executebuiltin('Container.SetViewMode(515)')
	

def pesquisa():
    keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa')  # Chama o keyboard do XBMC com a frase indicada
    keyb.doModal()  # Espera ate que seja confirmada uma determinada string
    if (keyb.isConfirmed()):  # Se a entrada estiver confirmada (isto e, se carregar no OK)
        search = keyb.getText()  # Variavel search fica definida com o conteudo do formulario
        parametro_pesquisa = urllib.quote(
        search)  # parametro_pesquisa faz o quote da expressao search, isto Ã©, escapa os parametros necessarios para ser incorporado num endereÃ§o url
        url = 'http://efilmesnarede.com/?s=' + (parametro_pesquisa)  # nova definicao de url. str forÃ§a o parametro de pesquisa a ser uma string
        listar_videos(url)  # chama a funÃ§Ã£o listar_videos com o url definido em cima


# Resolvers
def obtem_neodrive(url):
	codigo_fonte = abrir_url(url)
	
	try:
		url_video = re.findall(r'vurl.=."(.*?)";',codigo_fonte)[0]
		return [url_video,"-"]
	except:
		return ["-","-"]

def obtem_flashx(url):
    print url
    try:
		url_video = urlresolver.resolve(url)
		return [url_video, "-"]
    except:
		return ["-", "-"]

def obtem_openload(url):
	try:
		url_video = urlresolver.resolve(url)
		return [url_video, "-"]
	except:
		return ["-", "-"]

def obtem_videomega(url):
	try:
		url_video = urlresolver.resolve(url)
		return [url_video, "-"]
	except:
		return ["-", "-"]
		
def obtem_nowvideo(url):
    print url
    try:
		url_video = urlresolver.resolve(url)
		return [url_video, "-"]
    except:
		return ["-", "-"]		

###################################################################################
# FUNCOES JÁ FEITAS
def abrir_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link
	

#	
def gethtml(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    soup = BeautifulSoup(link)
    return soup	


#
def addLink(name, url, iconimage):
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setProperty('fanart_image', addonfolder + artfolder + 'fanart.png')
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
    return ok


#	
def addDir(name,url,mode,iconimage,pasta=True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	contextMenuItems = []
	contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
	liz.addContextMenuItems(contextMenuItems, replaceItems=True)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

	
#
def player(name,url,iconimage):	
	
	try:
		neomega = r'src=".*?neodrive.*?id=(.*?)"'
		flashx = r'src=".*?efilmesnarede.*?/nplayer/flashx.*?id=(.+?)"'
		openload = r'src=".*?openload.co/embed/(.+?)"'
		videomega = r'src=".*?videomega.tv/view.*?ref=(.+?)"'		
		nowvideo = r'src=".*?/nplayer/nowvideo.*?id=(.+?)"'
		
		mensagemprogresso = xbmcgui.DialogProgress()
		mensagemprogresso.create('Armagedon Pirata', 'A resolver link','Por favor aguarde...')
		mensagemprogresso.update(33)
		links = []
		hosts = []
		matriz = []
		codigo_fonte = abrir_url(url)
			
		try:
			links.append('http://videomega.tv/view.php?ref='+re.findall(videomega, codigo_fonte)[0])
			hosts.append('Videomega')
		except:
			pass
			
		try:
			links.append('http://embed.nowvideo.sx/embed.php?v='+re.findall(nowvideo, codigo_fonte)[0])
			hosts.append('Nowvideo')
		except:
			pass			
		
		try:
			links.append('http://neodrive.co/embed/'+re.findall(neomega, codigo_fonte)[0])
			hosts.append('Neodrive')
		except:
			pass	
			
		try:
			links.append('http://www.flashx.tv/embed-'+re.findall(flashx, codigo_fonte)[0]+'.html')
			hosts.append('Flashx')
		except:
			pass			
			
		try:
			links.append('https://openload.co/embed/'+re.findall(openload, codigo_fonte)[0])
			hosts.append('Openload')
		except:
			pass			
			
		if not hosts:
			return
		
		index = xbmcgui.Dialog().select('Selecione um dos hosts suportados :', hosts)
		
		if index == -1:
			return
		
		url_video = links[index]
		mensagemprogresso.update(66)
		
		print 'Player url: %s' % url_video
		if 'neodrive' in url_video:
			matriz = obtem_neodrive(url_video)
		elif 'nowvideo' in url_video:
			matriz = obtem_nowvideo(url_video)
		elif 'flashx.tv' in url_video:
			matriz = obtem_flashx(url_video)		
		elif 'openload.co/embed' in url_video:
			matriz = obtem_openload(url_video)	
		elif 'videomega' in url_video:
			matriz = obtem_videomega(url_video)				
		else:
			print "Falha: " + str(url_video)
		print matriz
		url = matriz[0]
		print url
		if url=='-': return
		legendas = matriz[1]
		print "Url do gdrive: " + str(url_video)
		print "Legendas: " + str(legendas)
		
		mensagemprogresso.update(100)
		mensagemprogresso.close()
		
		playlist = xbmc.PlayList(1)
		playlist.clear()
		
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage) # name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png"
		listitem.setPath(url)
		listitem.setProperty('mimetype','video/mp4')
		listitem.setProperty('IsPlayable', 'true')
		playlist.add(url,listitem)
		#try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
		if legendas != '-':
			if 'timedtext' in legendas:
				#legenda = xmltosrt.convert(legendas)
				#try:
					import os.path
					sfile = os.path.join(xbmc.translatePath("special://temp"),'sub.srt')
					sfile_xml = os.path.join(xbmc.translatePath("special://temp"),'sub.xml')#timedtext
					sub_file_xml = open(sfile_xml,'w')
					sub_file_xml.write(urllib2.urlopen(legendas).read())
					sub_file_xml.close()
					print "Sfile.srt : " + sfile_xml
					xmltosrt.main(sfile_xml)
					xbmcPlayer.setSubtitles(sfile)
				#except:
				#	pass
			else:
				xbmcPlayer.setSubtitles(legendas)
		#except:
		#	dialog = xbmcgui.Dialog()
		#	dialog.ok(" Erro:", " Impossível abrir vídeo! ")
		#	pass
	except:
		print "erro ao abrir o video"
		print url_video
		pass
	
############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################

def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


params = get_params()
url = None
name = None
mode = None
iconimage = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass

try:
    iconimage = urllib.unquote_plus(params["iconimage"])
except:
    pass

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "Iconimage: " + str(iconimage)


###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################


if mode == None or url == None or len(url) < 1:
    print ""
    CATEGORIES()
	
elif mode == 1:
    print ""
    listar_categorias(url)	

elif mode == 2:
    print ""
    listar_videos(url)

elif mode == 3:
    print ""
    pesquisa()

elif mode == 4:
    print ""
    player(name,url,iconimage)
	

xbmcplugin.endOfDirectory(int(sys.argv[1]))