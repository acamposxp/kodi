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


# BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import sys
import re
import urllib
import urllib2
import xbmc
import xbmcgui
import json
import xbmcplugin
import xbmcaddon
import urlresolver
from bs4 import BeautifulSoup


versao = '0.1'
addon_id ='plugin.video.cineflix'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'


USER_AGENT 	= 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'
ACCEPT 		= 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
URL = {}
URL['base'] = 'http://www.cineflixhd.net/'
URL['search'] = 'http://www.cineflixhd.net/search?q='
URL['newMovies'] = 'http://www.cineflixhd.net/search/label/2015'
sources = []
HTMLPattern = "<(.*?)>"
progress = xbmcgui.DialogProgress()

# MENUS############################################
def CATEGORIAS():
	addDir('Categorias', URL['base'], 2, 'http://i.imgur.com/tPuJW12.png')
	addDir('Filmes 2015', URL['newMovies'], 1, 'http://i.imgur.com/Hd8gmtS.png')
	addDir('Pesquisar', URL['base'], 3, 'http://i.imgur.com/awr7ArY.png')
	

# CATEGORIAS############################################
def CATEGORIES():
	dialog = xbmcgui.Dialog()
	addDir('[B]ANIMAÇÃO[/B]', 'http://www.cineflixhd.net/search/label/Anima%C3%A7%C3%A3o', 1,
		   'http://i.imgur.com/W2okuob.jpg')
	addDir('[B]AVENTURA[/B]', 'http://www.cineflixhd.net/search/label/Aventura', 1, 'http://i.imgur.com/WeLHJy9.jpg')
	addDir('[B]AÇÃO[/B]', 'http://www.cineflixhd.net/search/label/A%C3%A7%C3%A3o', 1, 'http://i.imgur.com/26HqBDB.jpg')
	addDir('[B]BIOGRAFIA[/B]', 'http://www.cineflixhd.net/search/label/Biografia', 1, 'http://i.imgur.com/VjHRh57.jpg')
	addDir('[B]CLÁSSICO[/B]', 'http://www.cineflixhd.net/search/label/Classico', 1, 'http://i.imgur.com/VhJ2j5d.jpg')
	addDir('[B]COMÉDIA[/B]', 'http://www.cineflixhd.net/search/label/Com%C3%A9dia', 1, 'http://i.imgur.com/PomZHty.jpg')
	addDir('[B]COMÉDIA ROMÂNTICA[/B]', 'http://www.cineflixhd.net/search/label/Com%C3%A9dia%20Rom%C3%A2ntica', 1,
		   'http://i.imgur.com/4Agolcp.jpg')
	addDir('[B]CRIME[/B]', 'http://www.cineflixhd.net/search/label/Crime', 1, 'http://i.imgur.com/qO3uivE.jpg')
	addDir('[B]DESENHOS[/B]', 'http://www.cineflixhd.net/search/label/Desenhos', 1, 'http://i.imgur.com/dRze8jm.jpg')
	addDir('[B]DRAMA[/B]', 'http://www.cineflixhd.net/search/label/Drama', 1, 'http://i.imgur.com/WpW1gqD.jpg')
	addDir('[B]DUBLADOS[/B]', 'http://www.cineflixhd.net/search/label/Dublados', 1, 'http://i.imgur.com/eXpspKo.jpg')
	addDir('[B]FAMÍLIA[/B]', 'http://www.cineflixhd.net/search/label/Fam%C3%ADla', 1, 'http://i.imgur.com/I5x7pdN.jpg')
	addDir('[B]FANTASIA[/B]', 'http://www.cineflixhd.net/search/label/Fantasia', 1, 'http://i.imgur.com/DGpMnRL.jpg')
	addDir('[B]FAROESTE[/B]', 'http://www.cineflixhd.net/search/label/Faroeste', 1, 'http://i.imgur.com/KazScUI.jpg')
	addDir('[B]FICÇÃO CIENTÍFICA[/B]', 'http://www.cineflixhd.net/search/label/Fic%C3%A7%C3%A3o', 1,
		   'http://i.imgur.com/i7hCgvV.jpg')
	addDir('[B]RELIGIOSOS[/B]', 'http://www.cineflixhd.net/search/label/Filmes%20Religioso', 1,
		   'http://i.imgur.com/PgeaIN6.jpg')
	addDir('[B]GUERRA[/B]', 'http://www.cineflixhd.net/search/label/Guerra', 1, 'http://i.imgur.com/eOK658J.jpg')
	addDir('[B]LANÇAMENTOS[/B]', 'http://www.cineflixhd.net/search/label/Lan%C3%A7amentos', 1,
		   'http://i.imgur.com/0WwoKZr.jpg')
	addDir('[B]LEGENDADOS[/B]', 'http://www.cineflixhd.net/search/label/Legendado', 1, 'http://i.imgur.com/deT1im1.jpg')
	addDir('[B]LUTA[/B]', 'http://www.cineflixhd.net/search/label/Luta', 1, 'http://i.imgur.com/0ugUGL9.jpg')
	addDir('[B]NACIONAL[/B]', 'http://www.cineflixhd.net/search/label/Nacional', 1, 'http://i.imgur.com/3TTKH4e.jpg')
	addDir('[B]POLICIAL[/B]', 'http://www.cineflixhd.net/search/label/Policial', 1, 'http://i.imgur.com/VgG7V15.jpg')
	addDir('[B]ROMANCE[/B]', 'http://www.cineflixhd.net/search/label/Romance', 1, 'http://i.imgur.com/Gz341un.jpg')
	addDir('[B]SHOW[/B]', 'http://www.cineflixhd.net/search/label/Show', 1, 'http://i.imgur.com/sIpnMfJ.jpg')
	addDir('[B]SUSPENSE[/B]', 'http://www.cineflixhd.net/search/label/Suspense', 1, 'http://i.imgur.com/bhVu5fU.jpg')
	addDir('[B]TERROR[/B]', 'http://www.cineflixhd.net/search/label/Terror', 1, 'http://i.imgur.com/uBYk5rh.jpg')
	xbmc.executebuiltin('Container.SetViewMode(500)')


# FUNCOES############################################
def listar_videos(url):
	codigo_fonte = abrir_url(url)
	match_html_trunk = re.findall(
		'<a href="(.+?)" imageanchor="1".+?<div align="left" style="margin-left: 1em; margin-right: 1em; text-align: center;">(.*?)<span class=\'post-labels\'>',
		abrir_url(url), re.DOTALL)
	for imgfilme, html_trunk in match_html_trunk:
		nomefilme = re.compile('var x="(.+?)",').findall(html_trunk)[0]
		imagemfilme = imgfilme
		proximosite = re.compile('y="(.+?)",z').findall(html_trunk)[0]
		nomefilme = nomefilme.replace('&#8211;', "-").replace('&#8217;', "'")
		addDir(nomefilme, proximosite, 4, imgfilme)

	# Parte do codigo para o "link" da pagina seguinte
	# <a class='blog-pager-older-link' href='http://www.cinemaemcasa.pt/search/label/Anima%C3%A7%C3%A3o?updated-max=2015-03-21T13:00:00Z&amp;max-results=20&amp;start=15&amp;by-date=false' id='Blog1_blog-pager-older-link' title='Next Post'>Mais Filmes &#187;</a>
	page = re.compile("<a class=\'blog-pager-older-link\' href=\'(.+?)\' id=\'Blog1_blog-pager-older-link\'").findall(abrir_url(url))
	for prox_pagina in page:
		addDir('Página Seguinte >>', prox_pagina, 1, "http://i.imgur.com/63Qyw7k.png")
		break

	xbmc.executebuiltin("Container.SetViewMode(500)")


def obtem_url_google(url):

	html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)
dados = urllib2.unquote(soup('script')[4].prettify()).decode('unicode-escape')
ttsurls = re.findall(r',\["ttsurl","(.*?)"\]\s', dados)[0]
decoded = re.findall(r',\["url_encoded_fmt_stream_map","(.*?)"\]\s',dados)[0]
qualidade = []
url_video = []

urls = [l for l in decoded.split('url=') if 'mp4' in l and l.startswith('https')]
print urls
url_video = []
for u in urls:
	itags = {5:'Baixa Qualidade, 240p, FLV, 400x240',
			 17:'Baixa Qualidade, 144p, 3GP, 0x0',
			 18:'Media Qualidade, 480p, MP4, 480x360',
			 59:'Media Qualidade, 360p, MP4, 480x360',
			 22:'Alta Qualidade, 720p, MP4, 1280x720',
			 34:'Media Qualidade, 360p, FLV, 640x360',
			 35:'Standard Definition, 480p, FLV, 854x480',
			 36:'Baixa Qualidade, 240p, 3GP, 0x0',
			 37:'Alta Qualidade, 1080p, MP4, 1920x1080',
			 38:'Original Definition, MP4, 4096x3072',
			 43:'Media Qualidade, 360p, WebM, 640x360',
			 44:'Standard Definition, 480p, WebM, 854x480',
			 45:'Alta Qualidade, 720p, WebM, 1280x720',
			 46:'Alta Qualidade, 1080p, WebM, 1280x720',
			 82:'Media Qualidade 3D, 360p, MP4, 640x360',
			 84:'Alta Qualidade 3D, 720p, MP4, 1280x720',
			 100:'Media Qualidade 3D, 360p, WebM, 640x360',
			 102:'Alta Qualidade 3D, 720p, WebM, 1280x720'}
	q = 'quality='
	i = 'itag='
	quality = u[u.find(q) + len(q): u.find(',', u.find(q))]
	itag = u[u.find(i) + len(i): u.find('&', u.find(i))]
	#print "ORG qualitys: " + quality
	#print "ORG itag: " + itag
	try:
		quality = itags[int(itag)]
	except:
		pass
	qualidade.append(quality)
	url_video.append(u[:-1])
index = 0
index = xbmcgui.Dialog().select('Qualidade do vídeo:', qualidade)
if index == -1: return['-','-'] # Tive que alterar esta linha para corrigir um pequeno erro
return [url_video[index]]

#Urlresolver setttings
'''def ResolverSettings():
	urlresolver.display_settings()

# Videolinks

def VIDEOLINKS(url):
	Enable_Streamcloud = local.getSetting('Enable-Streamcloud')
	unrestrict_account = local.getSetting('unrestrict-account')
	unrestrict_regaccount = local.getSetting('unrestrict-regaccount')
	unrestrict_guestaccount = local.getSetting('unrestrict-guestaccount')
	similar = url
	arg = { 'x':'1'}
	encoded_arg = urllib.urlencode(arg)
	req = urllib2.Request(url, encoded_arg)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-GB; rv:1.8.1.18) Gecko/22082049 Firefox/2.0.0.18')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
        #addDir("[B][COLOR blue]Find Similar Movies[/COLOR][/B]",url,59,'',None,'')
        match=re.compile('[H](.+?)[L](.+?)\|(.+?)[U](.+?)[X]').findall(link) #'[H](.+?)[L].+?\|(.+?)[U](.+?)[X]'
        match2=re.compile('[H](.+?)[L](.+?)\|(.+?)\|(.+?)[U](.+?)[X]').findall(link)
        for name,sub,desc,url in match:
        	name = name.replace(']','')
        	name = name.replace('[','')
        	desc = desc.replace('[','')
        	desc = desc.replace('[','')
        	url = url.replace(']','')
        	url = url.replace('[','')
        	sub = sub.replace(']','')
        	sub = sub.replace('[','')
        	sub = sub.replace('&quot;','"')
                #List of allowed Hosters to show links for
                if Enable_Streamcloud == 'false':
                	hosters = ['Uptobox ','Ul','Billionuploads','Putlocker','Novamov','Sockshare','Filenuke','Movshare','Vidbux','Played','Movpod','Daclips','Movdivx','Vidhog','Vidbull','Divxstage','Zalaa','Movreel','Sharerepo','Uploadc','Sharesix','Watchfreeinhd','Videoweed','Vidxden','2gb-hosting']
                else:
                	hosters = ['Uptobox ','Vimeo','Ul','Dailymotion','Streamcloud','Billionuploads','Putlocker','Novamov','Sockshare','Filenuke','Movshare','Vidbux','Played','Movpod','Daclips','Movdivx','Vidhog','Vidbull','Divxstage','Zalaa','Movreel','Sharerepo','Uploadc','Sharesix','Watchfreeinhd','Videoweed','Vidxden','2gb-hosting']

                	if name in str(hosters):
                		if unrestrict_account == 'true':
                			unhosters = ['Uptobox ','Ul','Vimeo', 'Dailymotion ', 'Streamcloud', 'Putlocker', 'Sockshare']
                		elif unrestrict_regaccount == 'true':
                			unhosters = ['Uptobox ','Vimeo', 'Dailymotion ', 'Streamcloud', 'Putlocker', 'Sockshare']
                		elif unrestrict_guestaccount == 'true':
                			unhosters = ['Streamcloud']
                		else:
                			unhosters = 'Nope'
                			nono = ['']
                			if name not in str(nono):
                				un = "[B][COLOR purple]Unrestricted[/COLOR][/B]"
                				if name in str(unhosters):
                					addDir("%s : %s : %s"%(un,name,desc),url+'@'+sub,8,'',None,'')
                				else:
                					addDir("%s : %s"%(name,desc),url+'@'+sub,7,'',None,'')'''

def http_req(url, getCookie=False):
		req = urllib2.Request(url)
		req.add_header('User-Agent', USER_AGENT)
		req.add_header('Accept', ACCEPT)
		req.add_header('Cache-Control', 'no-transform')
		response = urllib2.urlopen(req)
		source = response.read()
		response.close()
		if getCookie:
			cookie = response.headers.get('Set-Cookie')
			return {'source': source, 'cookie': cookie}
			return source

def player(name,url,iconimage):
	win = xbmcgui.Window(10000)
	win.setProperty('cineflixhd.playing.name', name.lower())
	
	item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	item.setInfo(type = "Video", infoLabels = {"name": name})
	
	xbmc.Player().play(item=url, listitem=item)
	
	return True


# Odnoklassniki

def obtem_okru(url):
	
	def selectSource(url, title='', thumbnail=''):
		progress = xbmcgui.DialogProgress()
		progress.create('Carregando', 'Aguarde...')
		progress.update(1, "", "Fontes de Vídeo...", "")
	
		sources = []
	
		progress.close()
	
		if not sources:
			return xbmcgui.Dialog().ok("", "Nenhuma fonte encontrada.")
	
		labels = []
	
		for item in sources:
			labels.append(item['name'])
	
		dialog = xbmcgui.Dialog()
	
		index = dialog.select('Selecione a fonte do vídeo', labels)
		if index > -1:
			playStream(sources[index]['url'], title, thumbnail)
		else:
			return
	
	sources = []
	
	rawhtml = http_req(url)
	params = {}
	
	try:
		re.search(r'_([0-9a-z]+).html?', url).group(1)
		
	except:
		html = BeautifulSoup(rawhtml).find_all('script', {'type': 'text/javascript'})
		html = "".join(line.strip() for line in str(html).split("\n"))
		html = re.findall(r'\$\.ajax\({.+?data: {(.+?)}', html)
		html = html[1].replace('"', '').split(',')

		for parameter in html:
			key, value = parameter.split(':')
			params[key] = value.strip()

			mirrors = []

			multiMirrors = re.findall(r'<img src=".+?templates/s[1-9].png"', rawhtml)

			if(len(multiMirrors) != 0):
				for i in range(len(multiMirrors)):
					mirrors.append('%sajax.php?p=custom&do=requestmirror&vid=%s&mirror=%s' % (URL['base'], params['vid'], i+1))
				else:
					mirrors.append('%sajax.php?p=video&do=getplayer&vid=%s' % (URL['base'], params['vid']))

					mirrors.reverse()

					for mirror in mirrors:
						try:
							mirrorUrl = BeautifulSoup(http_req(mirror)).find('iframe').attrs['src']
							mirrorUrl = re.sub(r'https?:\/\/(?:www\.)?.+?\.li/?\??', '', mirrorUrl)
						except:
							mirrorUrl = ''

							if(re.search(r'ok.ru', mirrorUrl)):
								try:
									id = re.search('\d+', mirrorUrl).group(0)
									jsonUrl = 'http://ok.ru/dk?cmd=videoPlayerMetadata&mid=' + id
									jsonSource = json.loads(http_req(jsonUrl))

									for source in jsonSource['videos']:
										name = '%s %s' % ('[ok.ru]', (source['name']))
										link = '%s|User-Agent=%s&Accept=%s&Referer=%s'
										link = link % (source['url'], HEADERS['User-Agent'], HEADERS['Accept'], urllib.quote_plus(URL['base']))

										item = {'name': name, 'url': link}
										sources.append(item)
								except: pass
								return sources


# Player

'''def player(name,url,iconimage):
	google = r'src="(.*?google.*?/preview)"'
	okru = r'src=(.*?ok.?/videoembed)"'
	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('CineflixHD', 'Resolvendo link','Por favor aguarde...')
	mensagemprogresso.update(33)
	
	links = []
	hosts = []
	matriz = []
	codigo_fonte = abrir_url(url)
	
	try:
		links.append(re.findall(google, codigo_fonte)[0])
		hosts.append('Gdrive')
	except:
		pass

		try:
			links.append(re.findall(okru, codigo_fonte)[0])
			hosts.append('Ok.ru')
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
					if 'google' in url_video:
						matriz = obtem_url_google(url_video)
					if 'okru' in url_video:
						matriz = obtem_url_okru(url_video)
					else:
						print "Falha: " + str(url_video)
						print matriz
						url = matriz[0]
						print url
						if url=='-': return
						legendas = matriz[1]
						print "Url do gdrive: " + str(url_video)
	#print "Legendas: " + str(legendas)
	
	mensagemprogresso.update(100)
	mensagemprogresso.close()
	
	listitem = xbmcgui.ListItem() # name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png"
	listitem.setPath(url)
	listitem.setProperty('mimetype','video/mp4')
	listitem.setProperty('IsPlayable', 'true')
	listitem.setProperty('isfolder', 'false')
	#try:
	xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	xbmcPlayer.play(url)
	#if legendas != '-':
		if 'timedtext' in legendas:
			legenda = xmltosrt.convert(legendas)
			try:
				import os.path
				sfile = os.path.join(xbmc.translatePath("special://temp"),'sub.srt')
				sfile_xml = os.path.join(xbmc.translatePath("special://temp"),'sub.xml')#timedtext
				sub_file_xml = open(sfile_xml,'w')
				sub_file_xml.write(urllib2.urlopen(legendas).read())
				sub_file_xml.close()
				print "Sfile.srt : " + sfile_xml
				xmltosrt.main(sfile_xml)
				xbmcPlayer.setSubtitles(sfile)
			except:
				pass
		else:
			xbmcPlayer.setSubtitles(legendas)'''
			


'''def player(name,url,iconimage):

	def set_sub(url):
		while not xbmc.Player().isPlaying():
			time.sleep(1)

			try:
				import os.path
				sfile = os.path.join(xbmc.translatePath('special://temp'), 'sub.srt')
				if 'mail.ru' in subtitles_url:
					referer = 'https://cloud.mail.ru/public/' + subtitles_url.split('/get/')[1]
					req = urllib2.Request(subtitles_url)
					req.add_header('Referer', referer)
					resp = urllib2.urlopen(req)
					content = resp.read()
					sub_file = open(sfile, 'w')
					sub_file.write(content)
					sub_file.close()
					xbmc.Player().setSubtitles(sfile)
				else:
					sub_file = open(sfile, 'w')
					sub_file.write(urllib2.urlopen(subtitles_url).read())
					sub_file.close()
					xbmc.Player().setSubtitles(sfile)
				except:
					pass

					if url is not None and url != '':
						print 'Freeflix sub/play: ' + subtitles_url
						if 'google' in url:
							try:
								Url = obtem_url_google[0]
							except:
								dialog = xbmcgui.Dialog()
								dialog.ok('Indisponivel', ' Conteudo Insdisponivel! ')
								xbmcplugin.endOfDirectory(int(sys.argv[1]))
								return

							elif '|putlocker|' in url:
								Url = simple_putlocker.ret(url.replace('|putlocker|', ''))
							elif '|bitcasa|' in url:
								Url = simple_bitcasa.ret(url.replace('|bitcasa|', ''))
							elif '|uptobox|' in url:
								Url = simple_uptobox.ret(url.replace('|uptobox|', ''))
							elif '|shared|' in url:
								Url = obtem_shared(url.replace('|shared|', ''))
							elif '|mailru|' in url:
								Url = simple_mailru.ret(url.replace('|mailru|', ''))
								if not subtitles_url:
									try:
										import os
										try:
											Url2 = Url.split('|')[0]
										except:
											Url2 = Url

											path = os.path.splitext(Url2)[0]
											print 'Freeflix sub/pre/mailru: ' + path + '.srt'
											subtitles_url = path + '.srt'
											print 'Freeflix sub/mailru: ' + subtitles_url
										except:
											pass

										elif '|megashares|' in url:
											Url = simple_megashares.ret(url.replace('|megashares|', ''))
										elif '|1fichier|' in url:
											Url = simple_1fichier.ret(url.replace('|1fichier|', ''))
										else:
											Url = url
											try:
												import os
												path = os.path.splitext(Url)[0]
												urllib2.urlopen('http://freetv.96.lt/static/srt/%s.srt' % path.split('/')[len(path.split('/')) - 1]).read()
												subtitles_url = 'http://freetv.96.lt/static/srt/%s.srt' % path.split('/')[len(path.split('/')) - 1]
											except:
												pass

												if not litem:
													litem = xbmcgui.ListItem(name, path=str(Url))
													litem.setThumbnailImage(thumbnail)
													litem.setInfo(type='video', infoLabels={'title': name})
													if '.mp4' in url:
														litem.setProperty('mimetype', 'video/mp4')
														if '.mkv' in url:
															litem.setProperty('mimetype', 'video/x-matroska')
															if subtitles_url:
																print 'Freeflix sub/play/thread: ' + subtitles_url
																thread.start_new_thread(set_sub, (subtitles_url,))
																print Url
																ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=str(Url), listitem=litem)
																xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, litem)
																return'''

def pesquisa():
	keyb = xbmc.Keyboard('', 'Escreva o parametro de pesquisa')  # Chama o keyboard do XBMC com a frase indicada
	keyb.doModal()  # Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()):  # Se a entrada estiver confirmada (isto e, se carregar no OK)
		search = keyb.getText()  # Variavel search fica definida com o conteudo do formulario
		parametro_pesquisa = urllib.quote(
			search)  # parametro_pesquisa faz o quote da expressao search, isto Ã©, escapa os parametros necessarios para ser incorporado num endereÃ§o url
		url = 'http://www.cineflixhd.net/search?q=' + str(
			parametro_pesquisa)  # nova definicao de url. str forÃ§a o parametro de pesquisa a ser uma string
		listar_videos(url)  # chama a função listar_videos com o url definido em cima


# FUNCOES JÃ FEITAS############################################

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent',
				   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	return link


def clearCache():
	if plugin.clearCache():
		xbmcgui.Dialog().ok('', 'O cache foi limpo.')
	else:
		xbmcgui.Dialog().ok('', 'Erro. Tente novamente.')


def addLink(name, url, iconimage):
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + artfolder + 'fanart.png')
	liz.setInfo(type="Video", infoLabels={"Title": name})
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
	return ok


def addDir(name, url, mode, thumbnail='', folder=True):
	ok = True
	params = {'name': name, 'mode': mode, 'url': url, 'thumbnail': thumbnail}

	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)

	if not folder:
		liz.setProperty('isPlayable', 'true')
		liz.setProperty('resumetime', str(0))
		liz.setProperty('totaltime', str(1))

	liz.setInfo(type="Video", infoLabels = {"title": name})

	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = set_params(params), listitem = liz, isFolder = folder)
	return ok


# PARÂMETROS############################################

def set_params(dict):
	out = {}
	for key, value in dict.iteritems():
		if isinstance(value, unicode):
			value = value.encode('utf8')
		elif isinstance(value, str):
			value.decode('utf8')
		out[key] = value
	return sys.argv[0] + '?' + urllib.urlencode(out)


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




# MODOS############################################

if mode == None or url == None or len(url) < 2:
	print ""
	CATEGORIAS()

elif mode == 1:
	print ""
	listar_videos(url)

elif mode == 2:
	print ""
	CATEGORIES()

elif mode == 3:
	print ""
	pesquisa()

elif mode == 4:
	print ""
	player(name,url,iconimage)

elif mode == 5:
	clearCache()

elif mode == 6:
	urlresolver.display_settings()

elif mode==7:
        print ""+url
        STREAM(url)

elif mode==8:
        UNSTREAM(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
