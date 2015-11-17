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

import urllib, urllib2, re, cookielib, xbmcplugin, xbmcgui, xbmc, xbmcaddon, HTMLParser, urlresolver
import xml.etree.ElementTree as ET
import json
from resources.lib import control
from resources.lib import client
from resources.lib import jsunpack
from resources.lib import captcha
from resources.lib.BeautifulSoup import BeautifulSoup

addon_id    = 'plugin.video.efilmes'
selfAddon   = xbmcaddon.Addon(id=addon_id)
datapath    = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addonfolder = selfAddon.getAddonInfo('path')

icon   = addonfolder + '/icon.png'
fanart = addonfolder + '/fanart.jpg'

try    : os.mkdir(datapath)
except : pass

progress = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()

h = HTMLParser.HTMLParser()
urlopen = urllib2.urlopen
cj = cookielib.LWPCookieJar()
Request = urllib2.Request
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
headers = {'User-Agent': USER_AGENT,
           'Accept': '*/*',
           'Connection': 'keep-alive'}
openloadhdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

#sources =
################################################## 

# MENUS############################################
def CATEGORIES():
    dialog = xbmcgui.Dialog()
    addDir('[B]ANIMAÇÃO[/B]', 'http://efilmesnarede.com/category/animacao/', 1, 'http://i.imgur.com/W2okuob.jpg')
    addDir('[B]AVENTURA[/B]', 'http://efilmesnarede.com/category/aventura/', 1, 'http://i.imgur.com/WeLHJy9.jpg')
    addDir('[B]COMÉDIA[/B]', 'http://efilmesnarede.com/category/comedia/', 1, 'http://i.imgur.com/PomZHty.jpg')
    addDir('[B]COMÉDIA ROMÂNTICA[/B]', 'http://efilmesnarede.com/category/comedia-romantica/', 1,
           'http://i.imgur.com/4Agolcp.jpg')
    addDir('[B]DOCUMENTÁRIO[/B]', 'http://efilmesnarede.com/category/documentario/', 1,
           'http://i.imgur.com/VjHRh57.jpg')
    addDir('[B]DRAMA[/B]', 'http://efilmesnarede.com/category/drama/', 1, 'http://i.imgur.com/WpW1gqD.jpg')
    addDir('[B]FANTASIA[/B]', 'http://efilmesnarede.com/category/fantasia/', 1, 'http://i.imgur.com/DGpMnRL.jpg')
    addDir('[B]FAROESTE[/B]', 'http://efilmesnarede.com/category/faroeste/', 1, 'http://i.imgur.com/KazScUI.jpg')
    addDir('[B]FICÇÃO CIENTÍFICA[/B]', 'http://efilmesnarede.com/category/ficcao/', 1,
           'http://i.imgur.com/i7hCgvV.jpg')
    addDir('[B]GUERRA[/B]', 'http://efilmesnarede.com/category/guerra/', 1, 'http://i.imgur.com/eOK658J.jpg')
    addDir('[B]MUSICAL[/B]', 'http://efilmesnarede.com/category/musical/', 1, 'http://i.imgur.com/sIpnMfJ.jpg')
    addDir('[B]NACIONAL[/B]', 'http://efilmesnarede.com/category/nacional/', 1, 'http://i.imgur.com/3TTKH4e.jpg')
    addDir('[B]POLICIAL[/B]', 'http://efilmesnarede.com/category/policial/', 1, 'http://i.imgur.com/VgG7V15.jpg')
    addDir('[B]ROMANCE[/B]', 'http://efilmesnarede.com/category/romance/', 1, 'http://i.imgur.com/Gz341un.jpg')
    addDir('[B]SUSPENSE[/B]', 'http://efilmesnarede.com/category/suspense/', 1, 'http://i.imgur.com/bhVu5fU.jpg')
    addDir('[B]TERROR[/B]', 'http://efilmesnarede.com/category/terror/', 1, 'http://i.imgur.com/uBYk5rh.jpg')
    addDir('[B]THRILLER[/B]', 'http://efilmesnarede.com/category/thriller/', 1, 'http://i.imgur.com/bhVu5fU.jpg')
    addDir('[B]PESQUISAR[/B]', '-', 3, 'http://www.shoppingportaldaserra.com.br/2013/img/lupa.png')	
    xbmc.executebuiltin('Container.SetViewMode(500)')


###################################################################################
# FUNCOES

def listar_videos(url):
    codigo_fonte = abrir_url(url)
    grupo = re.findall(
        '<div class="titulo"><a href="(.+?)" title="(.+?)">.+?<img src="(.+?)" width="135" height="169"/>',
        abrir_url(url), re.DOTALL)
    for link, nomefilme, imgfilme in grupo:
        nomefilme = nomefilme.replace('Assistir', "").replace('Filme',"").replace('&#8211;',"")
        addDirPlayer(nomefilme, link, 100, imgfilme, False)
    # Parte do codigo para o "link" da pagina seguinte
    # <a class='blog-pager-older-link' href='http://www.cinemaemcasa.pt/search/label/Anima%C3%A7%C3%A3o?updated-max=2015-03-21T13:00:00Z&amp;max-results=20&amp;start=15&amp;by-date=false' id='Blog1_blog-pager-older-link' title='Next Post'>Mais Filmes &#187;</a>
    page = re.compile('<a class="nextpostslink" rel="next" href="(.+?)">»</a>').findall(abrir_url(url))
    for prox_pagina in page:
        addDir('Página Seguinte >>', prox_pagina, 1, "http://i.imgur.com/63Qyw7k.png")
        break

    xbmc.executebuiltin("Container.SetViewMode(500)")
	

def pesquisa():
    keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa')  # Chama o keyboard do XBMC com a frase indicada
    keyb.doModal()  # Espera ate que seja confirmada uma determinada string
    if (keyb.isConfirmed()):  # Se a entrada estiver confirmada (isto e, se carregar no OK)
        search = keyb.getText()  # Variavel search fica definida com o conteudo do formulario
        parametro_pesquisa = urllib.quote(
            search)  # parametro_pesquisa faz o quote da expressao search, isto Ã©, escapa os parametros necessarios para ser incorporado num endereÃ§o url
        url = 'http://efilmesnarede.com/?s=' + str(
            parametro_pesquisa)  # nova definicao de url. str forÃ§a o parametro de pesquisa a ser uma string
        listar_videos(url)  # chama a funÃ§Ã£o listar_videos com o url definido em cima


# Resolvers

def obtem_OpenLoad(url):
    link = client.request(url)
    url = 'https://api.openload.io/1/file/dlticket?file=%s' % id

    result = client.request(url)
    result = json.loads(result)

    cap = result['result']['captcha_url']

    if  not cap == None : cap = captcha.keyboard(cap)

    time.sleep(result['result']['wait_time'])

    url = 'https://api.openload.io/1/file/dl?file=%s&ticket=%s' % (id, result['result']['ticket'])

    if not cap == None : url += '&captcha_response=%s' % urllib.quote(cap)

    result = client.request(url)
    result = json.loads(result)

    urlVideo = result['result']['url'] + '?mime=true'

    return [urlVideo]

def obtem_neodrive(url):
    codigo_fonte = abrir_url(url)

    try:
        url_video = re.findall(r'vurl.=."(.*?)";',codigo_fonte)[0]
        return [url_video,"-"]
    except:
        return ["-","-"]


def obtem_neodrive2(url):
    codigo_fonte = abrir_url(url)

    try:
        url_video = re.findall(r'vurl.=."(.*?)";',codigo_fonte)[0]
        return [url_video,"-"]
    except:
        return ["-","-"]


def obtem_videopw(url):
    codigo_fonte = abrir_url(url)

    try:
        url_video = re.findall(r'var vurl2 = "(.*?)";',codigo_fonte)[0]
        return [url_video,"-"]
    except:
        return ["-","-"]


def obtem_videopw2(url):
    codigo_fonte = abrir_url(url)

    try:
        url_video = re.findall(r'var vurl2 = "(.*?)";',codigo_fonte)[0]
        return [url_video,"-"]
    except:
        return ["-","-"]



def obtem_url_dropvideo(url):
    codigo_fonte = abrir_url(url)
    try:
        soup = BeautifulSoup(codigo_fonte)
        lista = soup.findAll('script')
        js = str(lista[9]).replace('<script>',"").replace('</script>',"")
        sUnpacked = jsunpack.unpack(js)
        print sUnpacked
        url_video = re.findall(r'var vurl2="(.*?)";', sUnpacked)
        url_video = str(url_video).replace("['","").replace("']","")
        return [url_video,"-"]
    except:
        pass


def obtem_url_dropvideo2(url):
    codigo_fonte = abrir_url(url)
    try:
        soup = BeautifulSoup(codigo_fonte)
        lista = soup.findAll('script')
        js = str(lista[9]).replace('<script>',"").replace('</script>',"")
        sUnpacked = jsunpack.unpack(js)
        print sUnpacked
        url_video = re.findall(r'var vurl2="(.*?)";', sUnpacked)
        url_video = str(url_video).replace("['","").replace("']","")
        return [url_video,"-"]
    except:
        pass

###################################################################################
# FUNCOES JÁ FEITAS
def abrir_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link

def getHtml(url, referer, hdr=None, NoCookie=None):
    if not hdr:
        req = Request(url, '', headers)
    else:
        req = Request(url, '', hdr)
    if len(referer) > 1:
        req.add_header('Referer', referer)
    response = urlopen(req, timeout=60)
    data = response.read()
    if not NoCookie:
        cj.save(cookiePath)
    response.close()
    return data
#
def addLink(name, url, iconimage):
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setProperty('fanart_image', addonfolder + artfolder + 'fanart.png')
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
    return ok


#

def addDir(name, url, mode, iconimage, pasta=True):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=pasta)
    return ok
	
def addDirPlayer(name, url, mode, iconimage, pasta=False):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=pasta)
    return ok	
	
'''def PLAYVIDEO(url, name, download=None):
    progress.create('Play video', 'Searching videofile.')
    progress.update( 10, "", "Loading video page", "" )
    videosource = getHtml(url, url)
    playvideo(videosource, name, download, url)

def playvideo(videosource, name, download=None, url=None):
    videosource = getHtml(url, url)
    hosts = []
    if re.search('videomega\.tv/', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('VideoMega')
    if re.search('openload\.', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('OpenLoad')
    if re.search('streamin.to', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('Streamin')
    if re.search('www.flashx.tv', videosource, re.DOTALL | re.IGNORECASE):
        hosts.append('FlashX')
    if len(hosts) == 0:
        progress.close()
        dialog.ok('Oh oh','Couldn\'t find any video')
        return
    elif len(hosts) > 1:
        if addon.getSetting("dontask") == "true":
            vidhost = hosts[0]
        else:
            vh = dialog.select('Videohost:', hosts)
            vidhost = hosts[vh]
    else:
        vidhost = hosts[0]

    if vidhost == 'VideoMega':
        progress.update( 40, "", "Loading videomegatv", "" )
        if re.search("videomega.tv/iframe.js", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile("""javascript["']>ref=['"]([^'"]+)""", re.DOTALL | re.IGNORECASE).findall(videosource)
        elif re.search("videomega.tv/iframe.php", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile(r"iframe\.php\?ref=([^&]+)&", re.DOTALL | re.IGNORECASE).findall(videosource)
        elif re.search("videomega.tv/view.php", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile(r'view\.php\?ref=([^"]+)', re.DOTALL | re.IGNORECASE).findall(videosource)
        elif re.search("videomega.tv/cdn.php", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile(r'cdn\.php\?ref=([^"]+)', re.DOTALL | re.IGNORECASE).findall(videosource)
        elif re.search("videomega.tv/\?ref=", videosource, re.DOTALL | re.IGNORECASE):
            hashref = re.compile(r'videomega.tv/\?ref=([^"]+)', re.DOTALL | re.IGNORECASE).findall(videosource)
        else:
            hashkey = re.compile("""hashkey=([^"']+)""", re.DOTALL | re.IGNORECASE).findall(videosource)
            if not hashkey:
                dialog.ok('Oh oh','Couldn\'t find playable videomega link')
                return
            if len(hashkey) > 1:
                i = 1
                hashlist = []
                for x in hashkey:
                    hashlist.append('Video ' + str(i))
                    i += 1
                vmvideo = dialog.select('Multiple videos found', hashlist)
                hashkey = hashkey[vmvideo]
            else: hashkey = hashkey[0]
            hashpage = getHtml('http://videomega.tv/validatehash.php?hashkey='+hashkey, url)
            hashref = re.compile('ref="([^"]+)', re.DOTALL | re.IGNORECASE).findall(hashpage)
        progress.update( 80, "", "Getting video file from Videomega", "" )
        videopage = getHtml('http://videomega.tv/view.php?ref='+hashref[0], url)
        videourl = re.compile('<source src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
        videourl = videourl[0]
    elif vidhost == 'OpenLoad':
        progress.update( 40, "", "Loading Openload", "" )
        openloadurl = re.compile(r"//(?:www\.)?openload\.(?:co|io)?/(?:embed|f)/([0-9a-zA-Z-_]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        openloadlist = list(set(openloadurl))
        if len(openloadlist) > 1:
            i = 1
            hashlist = []
            for x in openloadlist:
                hashlist.append('Video ' + str(i))
                i += 1
            olvideo = dialog.select('Multiple videos found', hashlist)
            openloadurl = openloadlist[olvideo]
        else: openloadurl = openloadurl[0]

        openloadurl1 = 'http://openload.co/embed/%s/' % openloadurl

        try:
            openloadsrc = getHtml(openloadurl1, '', openloadhdr)
            progress.update( 80, "", "Getting video file from OpenLoad", "")
            videourl = decodeOpenLoad(openloadsrc)
        except:
            dialog.ok('Oh oh','Couldn\'t find playable OpenLoad link')
    elif vidhost == 'Streamin':
        progress.update( 40, "", "Loading Streamin", "" )
        streaminurl = re.compile('<iframe.*?src="(http://streamin\.to[^"]+)"', re.DOTALL | re.IGNORECASE).findall(videosource)
        streaminsrc = getHtml2(streaminurl[0])
        videohash = re.compile('h=([^"]+)', re.DOTALL | re.IGNORECASE).findall(streaminsrc)
        videourl = re.compile('image: "(http://[^/]+/)', re.DOTALL | re.IGNORECASE).findall(streaminsrc)
        progress.update( 80, "", "Getting video file from Streamin", "" )
        videourl = videourl[0] + videohash[0] + "/v.mp4"
    elif vidhost == 'FlashX':
        progress.update( 40, "", "Loading FlashX", "" )
        flashxurl = re.compile(r"//(?:www\.)?flashx\.tv/(?:embed-)?([0-9a-zA-Z]+)", re.DOTALL | re.IGNORECASE).findall(videosource)
        flashxurl = 'http://flashx.tv/embed-%s-670x400.html' % flashxurl[0]
        flashxsrc = getHtml2(flashxurl)
        progress.update( 60, "", "Grabbing video file", "" )
        flashxurl2 = re.compile('<a href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(flashxsrc)
        flashxsrc2 = getHtml2(flashxurl2[0])
        progress.update( 70, "", "Grabbing video file", "" )
        flashxjs = re.compile("<script type='text/javascript'>([^<]+)</sc", re.DOTALL | re.IGNORECASE).findall(flashxsrc2)
        progress.update( 80, "", "Getting video file from FlashX", "" )
        flashxujs = beautify(flashxjs[0])
        videourl = re.compile(r'\[{\s+file: "([^"]+)",', re.DOTALL | re.IGNORECASE).findall(flashxujs)
        videourl = videourl[0]
    progress.close()
    playvid(videourl, name, download)'''

def player(name, url, iconimage):
    try:
        import urlresolver
    except:
        addon.log_error("Failed to import script.module.urlresolver")
        xbmcgui.Dialog().ok("Import Failure", "Failed to import URLResolver", "A component needed by this addon is missing on your system", "Please visit www.xbmc.org for support")

        sources = []
        html = GET_HTML(url)

    if 'DROPVIDEO' in hoster:
        html = GET_HTML(hoster)
        r = re.compile('src=".*?drop.*?id=(.*?)"').findall(str(html))
        for id in r:
            hosted_media = urlresolver.HostedMediaFile(url='http://www.dropvideo.com/embed/'+ id, title='Dropvideo')
            sources.append(hosted_media)

    if 'VIDEOTT' in hoster:
        html = GET_HTML(hoster)
        r = re.compile('src=".*?drop.*?id=(.*?)"').findall(str(html))
        for id in r:
            hosted_media = urlresolver.HostedMediaFile(url='http://video.tt/e/'+ id, title='Videott')
            sources.append(hosted_media)

    if 'OPENLOAD' in hoster:
        html = GET_HTML(hoster)
        r = re.compile('src=".*?video.*?/e/(.*?)"').findall(str(html))
        for id in r:
            hosted_media = urlresolver.HostedMediaFile(url='https://openload.co/embed/'+ id, title='Openload')
            sources.append(hosted_media)

        source = urlresolver.choose_source(sources)
try:
    if source: stream_url = source.resolve()
    else: stream_url = ''
    liz=xbmcgui.ListItem(linkback, iconImage='',thumbnailImage=img)
    liz.setInfo('Video', {'Title': linkback} )
    liz.setProperty("IsPlayable","true")
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=stream_url,isFolder=False,listitem=liz)#; Addon.resolve_url(stream_url)
    xbmc.Player().play(stream_url,liz)


'''def player(name, url, iconimage):
    try:
        import urlresolver
    except:
        addon.log_error("Failed to import script.module.urlresolver")
        xbmcgui.Dialog().ok("Import Failure", "Failed to import URLResolver", "A component needed by this addon is missing on your system", "Please visit www.xbmc.org for support")

    videott = r'src=".*?video.*?/e/(.*?)"'
    openload = r'data-src=".*?openload.*?/embed/(.*?)"'
    dropmega = r'src=".*?drop.*?id=(.*?)"'
    videopw = r'src=".*?videopw.*?/e/(.*?)"'
    mensagemprogresso = xbmcgui.DialogProgress()
    mensagemprogresso.create('eFilmesnaRede', 'A resolver link', 'Por favor aguarde...')
    mensagemprogresso.update(33)
    links = []
    hosts = []
    matriz = []
    codigo_fonte = abrir_url(url)
    # try: url_video = re.findall(r'<iframe src="(.*?)" width="738" height="400" frameborder="0"></iframe></li>',codigo_fonte)[0]
    # <iframe src="(.*?)" width="738" height="400" frameborder="0"></iframe></li>
    # except: return
    try:
        links.append(re.findall(cloudzilla_e, codigo_fonte)[0])  # http://www.cloudzilla.to/embed/%s
        hosts.append('CloudZilla')
    except:
        pass
    try:
        links.append('http://www.cloudzilla.to/embed/%s' % re.findall(cludzilla_s, codigo_fonte)[0])  # http://www.cloudzilla.to/embed/%s
        hosts.append('CloudZilla')
    except:
        pass
    try:
        links.append('http://vidigvideo.com/embed-%s-885x660.html' % re.findall(vidig_s, codigo_fonte)[0])
        hosts.append('Vidig')
    except:
        pass
    try:
        links.append('https://openload.co/embed/%s' % re.findall(openload, codigo_fonte)[0])
        hosts.append('Openload')
    except:
        pass
    try:
        links.append(re.findall(vidig, codigo_fonte)[0])
        hosts.append('Vidig')
    except:
        pass
    try:
        links.append(re.findall(okru, codigo_fonte)[0])
        hosts.append('Odnoklassniki')
    except:
        pass
    try:
        links.append(re.findall(videomail, codigo_fonte)[0])
        hosts.append('Videomail')
    except:
        pass
    try:
        links.append('http://neodrive.co/embed/'+re.findall(neomega, codigo_fonte)[0])
        hosts.append('Neodrive')
    except:
        pass
    try:
        links.append('http://video.tt/e/%s'+re.findall(videott, codigo_fonte)[0])
        hosts.append('Videott')
    except:
        pass
    try:
        links.append('http://neodrive.co/embed/'+re.findall(neomega2, codigo_fonte)[0])
        hosts.append('Neodrive2')
    except:
        pass		
    try:
        links.append(re.findall(videomega, codigo_fonte)[0])
        hosts.append('Videomega')
    except:
        pass
    try:
        links.append(re.findall(flashx, codigo_fonte)[0])
        hosts.append('Flashx')
    except:
        pass
    try:
        links.append('http://videopw.com/e/'+re.findall(videopw, codigo_fonte)[0])
        hosts.append('Videopw')
    except:
        pass
    try:
        links.append('http://videopw.com'+re.findall(videopw2, codigo_fonte)[0])
        hosts.append('Videopw2')
    except:
        pass		
    try:
        links.append(re.findall(vidzi, codigo_fonte)[0])
        hosts.append('Vidzi')
    except:
        pass
    try:
        links.append(re.findall(videobis, codigo_fonte)[0])
        hosts.append('VideoBis')
    except:
        pass
    try:
        links.append(re.findall(picasa, codigo_fonte)[0])
        hosts.append('Picasa')
    except:
        pass
    try:
        links.append(re.findall(google, codigo_fonte)[0])
        hosts.append('Gdrive')
    except:
        pass
    try:
        links.append(re.findall(dropvideo, codigo_fonte)[0])
        hosts.append('Dropvideo')
    except:
        pass
    try:
        links.append('http://www.dropvideo.com/embed/'+re.findall(dropmega, codigo_fonte)[0])
        hosts.append('Dropvideo')
    except:
        pass
    try:
        links.append('http://www.dropvideo.com/embed/'+re.findall(dropmega2, codigo_fonte)[0])
        hosts.append('Dropvideo2')
    except:
        pass		
    try:
        links.append('http://www.cloudzilla.to/embed/' + re.findall(cloudzilla, codigo_fonte)[0])
        hosts.append('CloudZilla')
    except:
        pass
    try:
        links.append('http://www.cloudzilla.to/embed/' + re.findall(cloudzilla_t, codigo_fonte)[0])
        hosts.append('CloudZilla(Legendado)')
    except:
        pass

    if not hosts:
        mensagemprogresso.update(100)
        mensagemprogresso.close()
        return

    index = xbmcgui.Dialog().select('Selecione um dos hosts suportados :', hosts)

    if index == -1:
        return

    url_video = links[index]
    mensagemprogresso.update(66)

    if 'google' in url_video:
        matriz = obtem_url_google(url_video)
    elif 'dropvideo.com/embed' in url_video:
        matriz = obtem_url_dropvideo(url_video)   # esta linha está a mais
    elif 'dropvideo.com/embed' in url_video:
        matriz = obtem_url_dropvideo2(url_video)   # esta linha está a mais		
    elif 'filmesonlinebr.info/player' in url_video:
        matriz = obtem_url_picasa(url_video)
    elif 'videott' in url_video:
        if source:
            stream_url = source.resolve()
            addon.resolve_url(stream_url)
        else:
            addon.resolve_url(False)
    elif 'openload' in url_video:
        matriz = obtem_OpenLoad(url_video)
    elif 'vk.com/video_ext' in url_video:
        matriz = obtem_url_vk(url_video)
    elif 'neodrive' in url_video:
        matriz = obtem_neodrive(url_video)
    elif 'neodrive' in url_video:
        matriz = obtem_neodrive2(url_video)		
    elif 'http://ok.ru' in url_video:
        matriz = obtem_okru(url_video)
    elif 'vodlocker.com' in url_video:
        matriz = obtem_url_vodlocker(url_video)
    elif 'firedrive.com/embed' in url_video:
        matriz = obtem_url_firedrive(url_video)
    elif 'cloudzilla' in url_video:
        matriz = obtem_cloudzilla(url_video)
    elif 'videobis.net' in url_video:
        matriz = obtem_videobis(url_video)  # video.pw
    elif 'videopw' in url_video:
        matriz = obtem_videopw(url_video)  # video.pw
    elif 'videopw2' in url_video:
        matriz = obtem_videopw2(url_video)  # video.pw		
    elif 'vidzi.tv' in url_video:
        matriz = obtem_vidig(url_video)
    elif 'mail.ru' in url_video:
        matriz = obtem_videomail(url_video)
    elif 'videomega.tv' in url_video:
        matriz = videomega_resolver(url_video)
    else:
        print "Falha: " + str(url_video)

    url = matriz[0]

    if url == '-':
        mensagemprogresso.update(100)
        mensagemprogresso.close()
        return

    mensagemprogresso.update(100)
    mensagemprogresso.close()

    listitem = xbmcgui.ListItem()  # name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png"
    listitem.setPath(url)
    listitem.setProperty('mimetype', 'video/mp4')
    listitem.setProperty('IsPlayable', 'true')
    # try:
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(url)
    return'''
        
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
    listar_videos(url)

elif mode == 3:
    print ""
    pesquisa()

elif mode == 100:
    PLAYVIDEO(url, name)

elif mode == 4:
    print ""
    player(name, url)
	

xbmcplugin.endOfDirectory(int(sys.argv[1]))