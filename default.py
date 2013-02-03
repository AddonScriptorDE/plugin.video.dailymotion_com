#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmcaddon,base64,socket,datetime,os

socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
xbox = xbmc.getCondVisibility("System.Platform.xbox")
addonID = 'plugin.video.dailymotion_com'
addon = xbmcaddon.Addon(addonID)
translation = addon.getLocalizedString
channelFavsFile=xbmc.translatePath("special://profile/addon_data/"+addonID+"/"+addonID+".favorites")

familyFilter=addon.getSetting("familyFilter")
filters=["on","off"]
familyFilter=filters[int(familyFilter)]

forceViewMode=addon.getSetting("forceViewMode")
if forceViewMode=="true": forceViewMode=True
else: forceViewMode=False
viewMode=str(addon.getSetting("viewMode"))

maxVideoQuality=addon.getSetting("maxVideoQuality")
qual=["480p","720p","1080p"]
maxVideoQuality=qual[int(maxVideoQuality)]

language=addon.getSetting("language")
languages=["en_EN","ar_ES","au_EN","be_FR","be_NL","br_PT","ca_EN","ca_FR","de_DE","es_ES","es_CA","gr_EL","fr_FR","in_EN","ie_EN","it_IT","mx_ES","ma_FR","nl_NL","at_DE","pl_PL","pt_PT","ru_RU","ro_RO","ch_FR","ch_DE","ch_IT","tn_FR","tr_TR","en_GB","en_US","vn_VI","jp_JP","cn_ZH"]
language=languages[int(language)]
lang=language[language.find("_")+1:].lower()
if language=="en_EN": lang=""

def index():
        addDir(translation(30004),"",'listMovieCats',"")
        addDir(translation(30006),"",'listChannels',"")
        addDir(translation(30007),"http://www.dailymotion.com/users/1",'sortUsers1',"")
        addDir(translation(30002),"",'search',"")
        addDir(translation(30003),"http://www.dailymotion.com/visited-today/live/1",'listVideos',"")
        addDir("3D","http://www.dailymotion.com/3d/1",'sortChannels1',"")
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def favoriteUsers():
        xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
        if os.path.exists(channelFavsFile):
          fh = open(channelFavsFile, 'r')
          all_lines = fh.readlines()
          for line in all_lines:
            user=line[line.find("###USER###=")+11:]
            user=user[:user.find("#")]
            thumb=line[line.find("###THUMB###=")+12:]
            thumb=thumb[:thumb.find("#")]
            addUserFavDir(user,"http://www.dailymotion.com/user/"+user+"/1",'sortChannels1',thumb,user)
          fh.close()
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def listChannels():
        content = getUrl("http://www.dailymotion.com/channels/1")
        content = content[content.find('<div class="dmco_box channels_menu column span-12 last">'):]
        content = content[:content.find('<div class="dmco_clear">')]
        match=re.compile('<a class="foreground" href="(.+?)">(.+?)</a>', re.DOTALL).findall(content)
        for url, title in match:
          if url.find("/channel/")>=0:
            id = url[url.find("/channel/")+9:]
            if id.find("/")>0:
              id=id[:id.find("/")]
            addDir(title,"http://www.dailymotion.com/"+lang+"/channel/"+id+"/1",'sortChannels1',"")
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def listMovieCats():
        addDir("cracklemovies","http://www.dailymotion.com/user/cracklemovies/1",'listVideos',"")
        addDir("crazedigitalmovies","http://www.dailymotion.com/user/crazedigitalmovies/1",'listVideos',"")
        addDir("BFIfilms","http://www.dailymotion.com/user/BFIfilms/1",'listVideos',"")
        addDir("Documentaries","http://www.dailymotion.com/visited/group/DM_Documentaries/1",'listVideos',"")
        addDir("Independent","http://www.dailymotion.com/visited/group/DM_Independent_film/1",'listVideos',"")
        addDir("Vintage","http://www.dailymotion.com/visited/group/DM_Vintage/1",'listVideos',"")
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def sortChannels1(url):
        addDir(translation(30008),url,'listVideos',"")
        if url.find("/channel/")>0:
          addDir(translation(30009),url.replace("/channel/","/visited/channel/"),'sortChannels2',"")
          addDir(translation(30010),url.replace("/channel/","/rated/channel/"),'sortChannels2',"")
        elif url.find("/user/")>0:
          addDir(translation(30009),url.replace("/user/","/visited/user/"),'sortChannels2',"")
          addDir(translation(30010),url.replace("/user/","/rated/user/"),'sortChannels2',"")
        else:
          addDir(translation(30009),url.replace("/1","/visited/1"),'sortChannels2',"")
          addDir(translation(30010),url.replace("/1","/rated/1"),'sortChannels2',"")
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def sortChannels2(url):
        addDir(translation(30011),url.replace("/visited/","/visited-today/").replace("/rated/","/rated-today/"),'listVideos',"")
        addDir(translation(30012),url.replace("/visited/","/visited-week/").replace("/rated/","/rated-week/"),'listVideos',"")
        addDir(translation(30013),url.replace("/visited/","/visited-month/").replace("/rated/","/rated-month/"),'listVideos',"")
        addDir(translation(30014),url,'listVideos',"")
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def sortUsers1(url):
        addDir(translation(30024),"","favoriteUsers","")
        addDir(translation(30015),url,'sortUsers2',"")
        addDir(translation(30016),url.replace("/users/","/users/featured/"),'sortUsers2',"")
        addDir(translation(30017),url.replace("/users/","/users/official/"),'sortUsers2',"")
        addDir(translation(30018),url.replace("/users/","/users/creative/"),'sortUsers2',"")
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def sortUsers2(url):
        addDir(translation(30008),url,'listUsers',"")
        addDir(translation(30019),url.replace("/users/","/users/popular/"),'listUsers',"")
        addDir(translation(30020),url.replace("/users/","/users/commented/"),'listUsers',"")
        addDir(translation(30021),url.replace("/users/","/users/rated/"),'listUsers',"")
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def listVideos(url):
        content = getUrl(url)
        spl=content.split('<div class="sd_video_wv3item')
        for i in range(1,len(spl),1):
            entry=spl[i]
            match=re.compile('title="(.+?)"', re.DOTALL).findall(entry)
            title=match[0]
            title=cleanTitle(title)
            match=re.compile('data-id="(.+?)"', re.DOTALL).findall(entry)
            id=match[0]
            match=re.compile('<span class="name">(.+?)</span>', re.DOTALL).findall(entry)
            user=match[0]
            match=re.compile('<div class="dmco_date">(.+?)</div>', re.DOTALL).findall(entry)
            date=""
            if len(match)>0:
              date=match[0]
            match=re.compile('<div class="duration">(.+?) </div>', re.DOTALL).findall(entry)
            duration=""
            if len(match)>0:
              duration=match[0]
            match=re.compile('<div class="dmpi_video_description foreground">(.+?)</div>', re.DOTALL).findall(entry)
            desc=""
            if entry.find('<div class="dmpi_video_description foreground"></div>')==-1:
              desc=match[0]
            match=re.compile('data-src="(.+?)"', re.DOTALL).findall(entry)
            thumb=match[0]
            desc=str(translation(30023))+": "+date+"\n"+desc
            if user=="cracklemovies":
              addLink(title,id,'playCrackle',thumb,desc,duration)
            elif user=="hulu":
              addLink(title,id,'playHulu',thumb,desc,duration)
            elif user=="ARTEplus7":
              addLink(title,id,'playArte',thumb,desc,duration)
            else:
              addLink(title,id,'playVideo',thumb,desc,duration)
        if content.find('<div class="next">')>=0:
          content=content[content.find('<div class="next">'):]
          content=content[:content.find('</div>')]
          match=re.compile('href="(.+?)"', re.DOTALL).findall(content)
          if len(match)>0:
            addDir(translation(30001),"http://www.dailymotion.com"+match[0],'listVideos',"")
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def listUsers(url):
        content = getUrl(url)
        spl=content.split('<a class="avatar image_border"')
        for i in range(1,len(spl),1):
            entry=spl[i]
            match=re.compile('<a class="name" href="/(.+?)">(.+?)</a>', re.DOTALL).findall(entry)
            title=match[0][0]
            match=re.compile('<a href="/user/(.+?)">(.+?)</a>', re.DOTALL).findall(entry)
            oTitle=title
            if len(match)>0:
              vids=match[0][1]
              title=title+" ("+vids+")"
            match=re.compile('src="(.+?)"', re.DOTALL).findall(entry)
            thumb=match[0]
            addUserDir(title,"http://www.dailymotion.com/user/"+title+"/1",'sortChannels1',thumb,oTitle)
        if content.find('<div class="next">')>=0:
          content=content[content.find('<div class="next">'):]
          content=content[:content.find('</div>')]
          match=re.compile('href="(.+?)"', re.DOTALL).findall(content)
          if len(match)>0:
            addDir(translation(30001),"http://www.dailymotion.com"+match[0],'listUsers',"")
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def search():
        keyboard = xbmc.Keyboard('', translation(30002))
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
          search_string = keyboard.getText().replace(" ","+")
          listVideos('http://www.dailymotion.com/relevance/search/'+search_string+'/1')

def playVideo(id):
        content = getUrl("http://www.dailymotion.com/sequence/"+id)
        if content.find('"statusCode":410')>0 or content.find('"statusCode":403')>0:
          xbmc.executebuiltin('XBMC.Notification(Info:,'+str(translation(30022))+' (DailyMotion)!,5000)')
        else:
          matchFullHD=re.compile('"hd1080URL":"(.+?)"', re.DOTALL).findall(content)
          matchHD=re.compile('"hd720URL":"(.+?)"', re.DOTALL).findall(content)
          matchHQ=re.compile('"hqURL":"(.+?)"', re.DOTALL).findall(content)
          matchSD=re.compile('"sdURL":"(.+?)"', re.DOTALL).findall(content)
          matchLive=re.compile('"customURL":"(.+?)"', re.DOTALL).findall(content)
          if len(matchFullHD)>0 and maxVideoQuality=="1080p":
            url=urllib.unquote_plus(matchFullHD[0]).replace("\\","")
          elif len(matchHD)>0 and (maxVideoQuality=="720p" or maxVideoQuality=="1080p"):
            url=urllib.unquote_plus(matchHD[0]).replace("\\","")
          elif len(matchHQ)>0:
            url=urllib.unquote_plus(matchHQ[0]).replace("\\","")
          elif len(matchSD)>0:
            url=urllib.unquote_plus(matchSD[0]).replace("\\","")
          elif len(matchLive)>0:
            url=urllib.unquote_plus(matchLive[0]).replace("\\","")
            url=getUrl(url)
          listitem = xbmcgui.ListItem(path=url)
          return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def playCrackle(id):
        try:
          content = getUrl("http://www.dailymotion.com/video/"+id)
          match=re.compile('swf\\?id=(.+?)&', re.DOTALL).findall(content)
          id=match[0]
          content = getUrl("http://api.crackle.com/Service.svc/details/media/"+id+"/US?format=json")
          match=re.compile('"Thumbnail_Wide":"http:\\\/\\\/images-us-am.crackle.com\\\/(.+?)_tnw.jpg', re.DOTALL).findall(content)
          url="http://media-us-am.crackle.com/"+match[0].replace("\\","")+"_480p_1mbps.mp4"
          listitem = xbmcgui.ListItem(path=url)
          return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
        except:
          xbmc.executebuiltin('XBMC.Notification(Info:,'+str(translation(30022))+' (Crackle)!,5000)')

def playHulu(id):
        try:
          content = getUrl("http://www.dailymotion.com/video/"+id)
          match=re.compile('<link rel="video_src" href="http://player.hulu.com/express/(.+?)"', re.DOTALL).findall(content)
          contentID=match[0]
          #Where to get videoID/eID
          videoID=""
          eID=""
          if xbox==True:
            url = 'plugin://video/Hulu/?mode="TV_play"&url="'+contentID+'"&videoid="'+videoID+'"&eid="'+eID+'"'
          else:
            url = 'plugin://plugin.video.hulu/?mode="TV_play"&url="'+contentID+'"&videoid="'+videoID+'"&eid="'+eID+'"'
          listitem = xbmcgui.ListItem(path=url)
          return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
        except:
          xbmc.executebuiltin('XBMC.Notification(Info:,'+str(translation(30022))+' (Hulu)!,5000)')

def playArte(id):
        try:
          content = getUrl("http://www.dailymotion.com/video/"+id)
          match=re.compile('<a class="link" href="http://videos.arte.tv/(.+?)/videos/(.+?).html">', re.DOTALL).findall(content)
          lang=match[0][0]
          vid=match[0][1]
          url="http://videos.arte.tv/"+lang+"/do_delegate/videos/"+vid+",view,asPlayerXml.xml"
          content = getUrl(url)
          match=re.compile('<video lang="'+lang+'" ref="(.+?)"', re.DOTALL).findall(content)
          url=match[0]
          content = getUrl(url)
          match1=re.compile('<url quality="hd">(.+?)</url>', re.DOTALL).findall(content)
          match2=re.compile('<url quality="sd">(.+?)</url>', re.DOTALL).findall(content)
          urlNew=""
          if len(match1)==1:
            urlNew=match1[0]
          elif len(match2)==1:
            urlNew=match2[0]
          listitem = xbmcgui.ListItem(path=urlNew+" swfVfy=1 swfUrl=http://videos.arte.tv/blob/web/i18n/view/player_23-3188338-data-4993762.swf")
          return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
        except:
          xbmc.executebuiltin('XBMC.Notification(Info:,'+str(translation(30022))+' (Arte)!,5000)')

def cleanTitle(title):
        title=title.replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("&#039;","'").replace("&quot;","\"").replace("&szlig;","ß").replace("&ndash;","-")
        title=title.replace("&Auml;","Ä").replace("&Uuml;","Ü").replace("&Ouml;","Ö").replace("&auml;","ä").replace("&uuml;","ü").replace("&ouml;","ö")
        title=title.strip()
        return title

def getUrl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/14.0')
        req.add_header('Cookie',"lang="+language+"; family_filter="+familyFilter)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

def parameters_string_to_dict(parameters):
        ''' Convert parameters encoded in a URL to a dict. '''
        paramDict = {}
        if parameters:
            paramPairs = parameters[1:].split("&")
            for paramsPair in paramPairs:
                paramSplits = paramsPair.split('=')
                if (len(paramSplits)) == 2:
                    paramDict[paramSplits[0]] = paramSplits[1]
        return paramDict

def addLink(name,url,mode,iconimage,desc,duration):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": desc, "Duration": duration } )
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addUserDir(name,url,mode,iconimage,oTitle):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        playListInfos="###MODE###=ADD###USER###="+oTitle+"###THUMB###="+iconimage+"###END###"
        liz.addContextMenuItems([(translation(30028), 'XBMC.RunScript(special://home/addons/'+addonID+'/favs.py,'+urllib.quote_plus(playListInfos)+')',)])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addUserFavDir(name,url,mode,iconimage,oTitle):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        playListInfos="###MODE###=REMOVE###REFRESH###=TRUE###USER###="+oTitle+"###THUMB###="+iconimage+"###END###"
        liz.addContextMenuItems([(translation(30029), 'XBMC.RunScript(special://home/addons/'+addonID+'/favs.py,'+urllib.quote_plus(playListInfos)+')',)])
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

params=parameters_string_to_dict(sys.argv[2])
mode=params.get('mode')
url=params.get('url')
if type(url)==type(str()):
  url=urllib.unquote_plus(url)

if mode == 'listVideos':
    listVideos(url)
elif mode == 'listUsers':
    listUsers(url)
elif mode == 'listChannels':
    listChannels()
elif mode == 'favoriteUsers':
    favoriteUsers()
elif mode == 'listMovieCats':
    listMovieCats()
elif mode == 'sortChannels1':
    sortChannels1(url)
elif mode == 'sortChannels2':
    sortChannels2(url)
elif mode == 'sortUsers1':
    sortUsers1(url)
elif mode == 'sortUsers2':
    sortUsers2(url)
elif mode == 'playVideo':
    playVideo(url)
elif mode == 'playCrackle':
    playCrackle(url)
elif mode == 'playHulu':
    playHulu(url)
elif mode == 'playArte':
    playArte(url)
elif mode == 'search':
    search()
else:
    index()
