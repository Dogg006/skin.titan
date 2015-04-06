import xbmcplugin
import xbmcgui
import xbmc
import xbmcaddon
import shutil
import xbmcaddon
import xbmcvfs
import os
import time
import urllib
import xml.etree.ElementTree as etree
from xml.dom.minidom import parse
import json
import random
import base64

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
import xml.etree.cElementTree as ET

doDebugLog = False

__language__ = xbmc.getLocalizedString

win = xbmcgui.Window( 10000 )
addon = xbmcaddon.Addon(id='script.titanskin.helpers')
addondir = xbmc.translatePath(addon.getAddonInfo('profile'))

def logMsg(msg, level = 1):
    if doDebugLog == True:
        xbmc.log(msg)

def sendClick(controlId):
    win = xbmcgui.Window( 10000 )
    time.sleep(0.5)
    xbmc.executebuiltin('SendClick('+ controlId +')')

def defaultSettings():
    # skins default settings for artist slideshow
    if xbmc.getCondVisibility("System.HasAddon(script.artistslideshow)"):
        __settings__ = xbmcaddon.Addon(id='script.artistslideshow')
        __settings__.setSetting('transparent', "true")
      
def musicSearch():
    xbmc.executebuiltin( "ActivateWindow(MusicLibrary)" )
    xbmc.executebuiltin( "SendClick(8)" )

def videoSearch():
    xbmc.executebuiltin( "ActivateWindow(VideoLibrary)" )
    xbmc.executebuiltin( "SendClick(8)" )    
    
def showWidget():
    win = xbmcgui.Window( 10000 )
    linkCount = 0
    xbmc.executebuiltin('Control.SetFocus(77777,0)')
    while linkCount !=10 and not xbmc.getCondVisibility("ControlGroup(77777).HasFocus"):
        time.sleep(0.1)
        if not xbmc.getCondVisibility("ControlGroup(77777).HasFocus"):
            xbmc.executebuiltin('Control.SetFocus(77777,0)')
        linkCount += 1
    
def setWidget(containerID):
    win = xbmcgui.Window( 10000 )
    win.clearProperty("activewidget")
    win.clearProperty("customwidgetcontent")
    skinStringContent = ""
    customWidget = False
    
    try:
        # workaround for numeric labels (get translated by xbmc)
        skinString = xbmc.getInfoLabel("Container(" + containerID + ").ListItem.Property(submenuVisibility)")
        skinString = skinString.replace("num-","")
        if xbmc.getCondVisibility("Skin.String(widget-" + skinString + ')'):
            skinStringContent = xbmc.getInfoLabel("Skin.String(widget-" + skinString + ')')
        
        # normal method by getting the defaultID
        if skinStringContent == "":
            skinString = xbmc.getInfoLabel("Container(" + containerID + ").ListItem.Property(defaultID)")
            if xbmc.getCondVisibility("Skin.String(widget-" + skinString + ')'):
                skinStringContent = xbmc.getInfoLabel("Skin.String(widget-" + skinString + ')')
           
        if skinStringContent != "":
     
            if "$INFO" in skinStringContent:
                skinStringContent = skinStringContent.replace("$INFO[Window(Home).Property(", "")
                skinStringContent = skinStringContent.replace(")]", "")
                skinStringContent = win.getProperty(skinStringContent)
                customWidget = True
            if "Activate" in skinStringContent:
                skinStringContent = skinStringContent.split(",",1)[1]
                skinStringContent = skinStringContent.replace(",return","")
                skinStringContent = skinStringContent.replace(")","")
                skinStringContent = skinStringContent.replace("\"","")
                customWidget = True
            if ":" in skinStringContent:
                customWidget = True
                
            if customWidget:
                 win.setProperty("customwidgetcontent", skinStringContent)
                 win.setProperty("activewidget","custom")
            else:
                win.clearProperty("customwidgetcontent")
                win.setProperty("activewidget",skinStringContent)

        else:
            win.clearProperty("activewidget")
        
        #also set spotlightwidget for enhancedhomescreen
        if xbmc.getCondVisibility("Skin.String(GadgetRows, enhanced)"):
            setSpotlightWidget(containerID)
    except: pass

def setSpotlightWidget(containerID):
    win = xbmcgui.Window( 10000 )
    win.clearProperty("spotlightwidgetcontent")
    skinStringContent = ""
    customWidget = False
    
    # workaround for numeric labels (get translated by xbmc)
    skinString = xbmc.getInfoLabel("Container(" + containerID + ").ListItem.Property(submenuVisibility)")
    skinString = skinString.replace("num-","")
    if xbmc.getCondVisibility("Skin.String(spotlightwidget-" + skinString + ')'):
        skinStringContent = xbmc.getInfoLabel("Skin.String(spotlightwidget-" + skinString + ')')
    
    # normal method by getting the defaultID
    if skinStringContent == "":
        skinString = xbmc.getInfoLabel("Container(" + containerID + ").ListItem.Property(defaultID)")
        if xbmc.getCondVisibility("Skin.String(spotlightwidget-" + skinString + ')'):
            skinStringContent = xbmc.getInfoLabel("Skin.String(spotlightwidget-" + skinString + ')')
       
    if skinStringContent != "":
 
        if "$INFO" in skinStringContent:
            skinStringContent = skinStringContent.replace("$INFO[Window(Home).Property(", "")
            skinStringContent = skinStringContent.replace(")]", "")
            skinStringContent = win.getProperty(skinStringContent)
        if "Activate" in skinStringContent:
            skinStringContent = skinStringContent.split(",",1)[1]
            skinStringContent = skinStringContent.replace(",return","")
            skinStringContent = skinStringContent.replace(")","")
            skinStringContent = skinStringContent.replace("\"","")

        win.setProperty("spotlightwidgetcontent", skinStringContent)

    else:
        win.clearProperty("spotlightwidgetcontent")        

def setSkinVersion():
    skin = xbmc.getSkinDir()
    skinLabel = xbmcaddon.Addon(id=skin).getAddonInfo('name')
    skinVersion = xbmcaddon.Addon(id=skin).getAddonInfo('version')
    win = xbmcgui.Window( 10000 )
    win.setProperty("skinTitle",skinLabel + " (v" + skinVersion + ")")
        
def setCustomContent(skinString):
    #legacy
    win = xbmcgui.Window( 10000 )
    skinStringContent = xbmc.getInfoLabel("Skin.String(" + skinString + ')')

    if "$INFO" in skinStringContent:
        skinStringContent = skinStringContent.replace("$INFO[Window(Home).Property(", "")
        skinStringContent = skinStringContent.replace(")]", "")
        skinStringContent = win.getProperty(skinStringContent)    

    if "Activate" in skinStringContent:
        skinStringContent = skinStringContent.split(",",1)[1]
        skinStringContent = skinStringContent.replace(",return","")
        skinStringContent = skinStringContent.replace(")","")
        skinStringContent = skinStringContent.replace("\"","")
           
        xbmc.executebuiltin("Skin.SetString(" + skinString + ','+ skinStringContent + ')')         

    win.setProperty("customwidgetcontent", skinStringContent)
        
def updatePlexlinks():
    win = xbmcgui.Window( 10000 )
    logMsg("update plexlinks started...")
    xbmc.executebuiltin('RunScript(plugin.video.plexbmc,skin)')
    linkCount = 0
    logMsg("updateplexlinks started...")
    
    #update plex window properties
    xbmc.sleep(3000)
    while linkCount !=10:
        plexstring = "plexbmc." + str(linkCount)
        link = win.getProperty(plexstring + ".title")
        logMsg(plexstring + ".title --> " + link)
        plexType = win.getProperty(plexstring + ".type")
        logMsg(plexstring + ".type --> " + plexType)            

        link = win.getProperty(plexstring + ".recent")
        logMsg(plexstring + ".recent --> " + link)
        link = link.replace("ActivateWindow(VideoLibrary, ", "")
        link = link.replace("ActivateWindow(VideoLibrary,", "")
        link = link.replace("ActivateWindow(MusicFiles,", "")
        link = link.replace("ActivateWindow(Pictures,", "")
        link = link.replace(",return)", "")
        win.setProperty(plexstring + ".recent.content", link)
        logMsg(plexstring + ".recent --> " + link)

        link = win.getProperty(plexstring + ".viewed")
        logMsg(plexstring + ".viewed --> " + link)
        link = link.replace("ActivateWindow(VideoLibrary, ", "")
        link = link.replace("ActivateWindow(VideoLibrary,", "")
        link = link.replace("ActivateWindow(MusicFiles,", "")
        link = link.replace("ActivateWindow(Pictures,", "")
        link = link.replace(",return)", "")
        win.setProperty(plexstring + ".viewed.content", link)
        logMsg(plexstring + ".viewed --> " + link)

        linkCount += 1
    
    xbmc.sleep(5000)
    updatePlexBackgrounds()   
        
def updatePlexBackgrounds():
    win = xbmcgui.Window( 10000 )
    logMsg("update plex backgrounds started...")        
    
    #update plex backgrounds
    linkCount = 0
    xbmc.sleep(5000)
    while linkCount !=10:
        plexstring = "plexbmc." + str(linkCount)
        randomNr = random.randrange(1,10+1)       
        plexType = win.getProperty(plexstring + ".type")
        randomimage = ""
        if plexType == "movie":
            randomimage = xbmc.getInfoLabel("Container(100" + str(linkCount) + ").ListItem(" + str(randomNr) + ").Art(fanart)")
            win.setProperty("plexfanartbg", randomimage)
        elif plexType == "artist":
            randomimage = xbmc.getInfoLabel("Container(100" + str(linkCount) + ").ListItem(" + str(randomNr) + ").Art(fanart)")
            if randomimage == "":
                randomimage = xbmc.getInfoLabel("Container(100" + str(linkCount) + ").ListItem(1).Art(fanart)")
            if randomimage == "":
                randomimage = "special://skin/extras/backgrounds/hover_my music.png"                
        elif plexType == "show":
            randomimage = xbmc.getInfoLabel("Container(100" + str(linkCount) + ").ListItem(" + str(randomNr) + ").Property(Fanart_Image)")
        elif plexType == "photo":
            randomimage = xbmc.getInfoLabel("Container(100" + str(linkCount) + ").ListItem(" + str(randomNr) + ").PicturePath")                

        if randomimage != "":
            win.setProperty(plexstring + ".background", randomimage)
            logMsg(plexstring + ".background --> " + randomimage)            

        linkCount += 1
               
def showInfoPanel():
    win = xbmcgui.Window( 10000 )
    tryCount = 0
    secondsToDisplay = "4"
    secondsToDisplay = xbmc.getInfoLabel("Skin.String(ShowInfoAtPlaybackStart)")
    while tryCount !=50 and not xbmc.getCondVisibility("Window.IsActive(fullscreeninfo)"):
        time.sleep(0.1)
        if not xbmc.getCondVisibility("Window.IsActive(fullscreeninfo)") and xbmc.getCondVisibility("Player.HasVideo"):
            xbmc.executebuiltin('Action(info)')
        tryCount += 1
    
    # close info again
    time.sleep(int(secondsToDisplay))
    if xbmc.getCondVisibility("Window.IsActive(fullscreeninfo)"):
        xbmc.executebuiltin('Action(info)')

def addShortcutWorkAround():
    win = xbmcgui.Window( 10000 )
    xbmc.executebuiltin('SendClick(301)')
    if xbmc.getCondVisibility("System.Platform.Windows"):
        xbmc.sleep(1000)
    else:
        xbmc.sleep(2500)
        if xbmc.getCondVisibility("System.Platform.Linux.RaspberryPi "):
            xbmc.sleep(1000)
    xbmc.executebuiltin('SendClick(401)')

def checkExtraFanArt():
        
    lastPath = None
    win = xbmcgui.Window( 10000 )
    
    try:
        efaPath = None
        efaFound = False
        liArt = None
        liPath = xbmc.getInfoLabel("ListItem.Path")
        containerPath = xbmc.getInfoLabel("Container.FolderPath")
        
        if (liPath != None and (xbmc.getCondVisibility("Container.Content(movies)") or xbmc.getCondVisibility("Container.Content(seasons)") or xbmc.getCondVisibility("Container.Content(episodes)") or xbmc.getCondVisibility("Container.Content(tvshows)")) and not "videodb:" in liPath):
                           
            if xbmc.getCondVisibility("Container.Content(episodes)"):
                liArt = xbmc.getInfoLabel("ListItem.Art(tvshow.fanart)")
            
            # do not set extra fanart for virtuals
            if (("plugin://" in liPath) or ("addon://" in liPath) or ("sources" in liPath) or ("plugin://" in containerPath) or ("sources://" in containerPath) or ("plugin://" in containerPath)):
                win.clearProperty("ExtraFanArtPath")
                lastPath = None
            else:

                if xbmcvfs.exists(liPath + "extrafanart/"):
                    efaPath = liPath + "extrafanart/"
                else:
                    pPath = liPath.rpartition("/")[0]
                    pPath = pPath.rpartition("/")[0]
                    if xbmcvfs.exists(pPath + "/extrafanart/"):
                        efaPath = pPath + "/extrafanart/"
                        
                if xbmcvfs.exists(efaPath):
                    dirs, files = xbmcvfs.listdir(efaPath)
                    if files.count > 1:
                        efaFound = True
                        
                if (efaPath != None and efaFound == True):
                    if lastPath != efaPath:
                        win.setProperty("ExtraFanArtPath",efaPath)
                        lastPath = efaPath
                        
                else:
                    win.clearProperty("ExtraFanArtPath")
                    lastPath = None
        else:
            win.clearProperty("ExtraFanArtPath")
            lastPath = None
    
    except:
        xbmc.log("Titan skin helper: error occurred in assigning extra fanart background")
          
def focusEpisode():
    
    totalItems = 0
    curView = xbmc.getInfoLabel("Container.Viewmode") 
    viewId = int(getViewId(curView))
    
    wid = xbmcgui.getCurrentWindowId()
    window = xbmcgui.Window( wid )        
    control = window.getControl(int(viewId))
    totalItems = int(xbmc.getInfoLabel("Container.NumItems"))
    
    #only do a focus if we're on top of the list, else skip to prevent bouncing of the list
    if not int(xbmc.getInfoLabel("Container.Position")) > 1:
        if (xbmc.getCondVisibility("Container.SortDirection(ascending)")):
            curItem = 0
            control.selectItem(0)
            xbmc.sleep(250)
            while ((xbmc.getCondVisibility("Container.Content(episodes)") or xbmc.getCondVisibility("Container.Content(seasons)")) and totalItems >= curItem):
                if (xbmc.getInfoLabel("Container.ListItem(" + str(curItem) + ").Overlay") != "OverlayWatched.png" and xbmc.getInfoLabel("Container.ListItem(" + str(curItem) + ").Label") != ".." and not xbmc.getInfoLabel("Container.ListItem(" + str(curItem) + ").Label").startswith("*")):
                    if curItem != 0:
                        control.selectItem(curItem)
                    break
                else:
                    curItem += 1
        
        elif (xbmc.getCondVisibility("Container.SortDirection(descending)")):
            curItem = totalItems
            control.selectItem(totalItems)
            xbmc.sleep(250)
            while ((xbmc.getCondVisibility("Container.Content(episodes)") or xbmc.getCondVisibility("Container.Content(seasons)")) and curItem != 0):
                
                if (xbmc.getInfoLabel("Container.ListItem(" + str(curItem) + ").Overlay") != "OverlayWatched.png"):
                    control.selectItem(curItem-1)
                    break
                else:    
                    curItem -= 1
            

def getViewId(viewString):
    # get all views from views-file
    viewId = None
    skin_view_file = os.path.join(xbmc.translatePath('special://skin/extras'), "views.xml")
    tree = etree.parse(skin_view_file)
    root = tree.getroot()
    for view in root.findall('view'):
        if viewString == __language__(int(view.attrib['languageid'])):
            viewId=view.attrib['value']
    
    return viewId
    
    
def getImageFromPath(path):
    
    logMsg("getting images for path " + path)
    if "$INFO" in path:
        path = path.replace("$INFO[Window(Home).Property(", "")
        path = path.replace(")]", "")
        path = win.getProperty(path)    

    if "Activate" in path:
        path = path.split(",",1)[1]
        path = path.replace(",return","")
        path = path.replace(")","")
        path = path.replace("\"","")
    
    #safety check: does the config directory exist?
    if not xbmcvfs.exists(addondir + os.sep):
        xbmcvfs.mkdir(addondir)
    
    #first check if this link is blacklisted
    blacklistPath = os.path.join(addondir,"blacklist.txt")
    blackListed = False
    if (xbmcvfs.exists(blacklistPath) and os.path.getsize(blacklistPath) > 0):
        blfile = open(blacklistPath, 'r')
        if path in blfile.read():
            logMsg("path blacklisted - skipping for path " + path)
            blfile.close()
            return None
        logMsg("path is NOT blacklisted (or blacklist file error) - continuing for path " + path)
        blfile.close()

    #no blacklist so read cache and/or path
    images = list()
    txtPath = base64.urlsafe_b64encode(path)
    txtPath = os.path.join(addondir,txtPath + ".txt")
    
    #delete existing cache file if cache expired
    if xbmcvfs.exists(txtPath) and win.getProperty(txtPath) != "loaded":
        logMsg("cache file outdated, deleting... " + txtPath)
        xbmcvfs.delete(txtPath)
    
    #cache file exists and cache is not expired, load cache file
    if (xbmcvfs.exists(txtPath) and os.path.getsize(txtPath) > 0) and win.getProperty(txtPath) == "loaded":
        txtfile = open(txtPath, 'r')
        logMsg("get images from the cache file... " + path)
        for line in txtfile.readlines():
            if not "skip" in line:
                logMsg("found image in cache... " + line)
                images.append(line)
        txtfile.close()
        if images != []:
            random.shuffle(images)
            logMsg("loading done setting image from cache... " + images[0])
            return images[0]
        else:
            logMsg("cache file empty...skipping...")
    else:
        #no cache file so try to load images from the path
        logMsg("get images from the path or plugin... " + path)
        if path.startswith("plugin://"):
            media_type = "files"
        else:
            media_type = "video"
        media_array = None
        media_array = getJSON('Files.GetDirectory','{ "properties": ["title","art"], "directory": "' + path + '", "media": "' + media_type + '", "limits": {"end":50}, "sort": { "order": "ascending", "method": "random", "ignorearticle": true } }')
        
        if(media_array != None and media_array.has_key('files')):
            for media in media_array['files']:
                if media.has_key('art'):
                    if media['art'].has_key('fanart'):
                        images.append(media['art']['fanart'])
                    if media['art'].has_key('tvshow.fanart'):
                        images.append(media['art']['tvshow.fanart'])
        else:
            logMsg("media array empty or error so add this path to blacklist..." + path)
            blacklistPath = os.path.join(addondir,"blacklist.txt")
            blfile = open(blacklistPath, 'a')
            blfile.write(path + '\n')
            blfile.close()
            return None
    
    #all is fine, we have some images to randomize and return one
    txtfile = open(txtPath, 'w')
    image = None
    if images != []:
        for image in images:
            txtfile.write(image + '\n')
        random.shuffle(images)
        image = images[0]
        logMsg("setting random image.... " + image)
    else:
        logMsg("image array empty so skipping this path until next restart - " + path)
        win.setProperty(txtPath,"loaded")
        txtfile.write('skip')
    
    win.setProperty(txtPath,"loaded")
    txtfile.close()
    return image

    
def UpdateBackgrounds():
    win = xbmcgui.Window( 10000 )

    #get all playlists
    if xbmc.getCondVisibility("Skin.HasSetting(SmartShortcuts.playlists)"):
        playlistCount = 0
        path = "special://profile/playlists/video/"
        if xbmcvfs.exists( path ):
            dirs, files = xbmcvfs.listdir(path)
            for file in files:
                if file.endswith(".xsp"):
                    playlist = path + file
                    label = file.replace(".xsp","")
                    image = getImageFromPath(playlist)
                    if image != None:
                        playlist = "ActivateWindow(Videos," + playlist + ",return)"
                        win.setProperty("playlist." + str(playlistCount) + ".image", image)
                        win.setProperty("playlist." + str(playlistCount) + ".label", label)
                        win.setProperty("playlist." + str(playlistCount) + ".action", playlist)
                        playlistCount += 1
    
    #get favorites
    if xbmc.getCondVisibility("Skin.HasSetting(SmartShortcuts.favorites)"):
        favoritesCount = 0
        fav_file = xbmc.translatePath( 'special://profile/favourites.xml' ).decode("utf-8")
        if xbmcvfs.exists( fav_file ):
            doc = parse( fav_file )
            listing = doc.documentElement.getElementsByTagName( 'favourite' )
            
            for count, favourite in enumerate(listing):
                name = favourite.attributes[ 'name' ].nodeValue
                path = favourite.childNodes [ 0 ].nodeValue
                if (path.startswith("ActivateWindow(Videos") or path.startswith("ActivateWindow(10025")) and not "script://" in path:
                    image = getImageFromPath(path)
                    if image != None:
                        win.setProperty("favorite." + str(favoritesCount) + ".image", image)
                        win.setProperty("favorite." + str(favoritesCount) + ".label", name)
                        win.setProperty("favorite." + str(favoritesCount) + ".action", path)
                        favoritesCount += 1
            
    media_array = None
    
    #get in progress movies  
    win.setProperty("InProgressMovieBackground",getImageFromPath("special://skin/extras/widgetplaylists/inprogressmovies.xsp"))

    #get recent and unwatched movies
    win.setProperty("RecentMovieBackground",getImageFromPath("videodb://recentlyaddedmovies/"))
    
    #unwatched movies
    win.setProperty("UnwatchedMovieBackground",getImageFromPath("special://skin/extras/widgetplaylists/unwatchedmovies.xsp"))
  
    #get in progress tvshows
    win.setProperty("InProgressShowsBackground",getImageFromPath("library://video/inprogressshows.xml"))

    #get recent episodes
    win.setProperty("RecentEpisodesBackground",getImageFromPath("videodb://recentlyaddedepisodes/"))

def getJSON(method,params):
    json_response = xbmc.executeJSONRPC('{ "jsonrpc" : "2.0" , "method" : "' + method + '" , "params" : ' + params + ' , "id":1 }')

    jsonobject = json.loads(json_response.decode('utf-8','replace'))
   
    if(jsonobject.has_key('result')):
        return jsonobject['result']
    else:
        xbmc.log("no result " + str(jsonobject),xbmc.LOGDEBUG)
        return None

    
def setView(containerType,viewId):

    if viewId=="00":
        win = xbmcgui.Window( 10000 )

        curView = xbmc.getInfoLabel("Container.Viewmode")
        viewId = getViewId(curView)
        
    else:
        viewId=viewId    

    if xbmc.getCondVisibility("System.HasAddon(plugin.video.netflixbmc)"):
        __settings__ = xbmcaddon.Addon(id='plugin.video.netflixbmc')

        if containerType=="MOVIES":
            __settings__.setSetting('viewIdVideos', viewId)
        elif containerType=="SERIES":
            __settings__.setSetting('viewIdEpisodesNew', viewId)
        elif containerType=="SEASONS":
            __settings__.setSetting('viewIdEpisodesNew', viewId)
        elif containerType=="EPISODES":
            __settings__.setSetting('viewIdEpisodesNew', viewId)
        else:
            __settings__.setSetting('viewIdActivity', viewId)
            
    if xbmc.getCondVisibility("System.HasAddon(plugin.video.xbmb3c)"):
        __settings__ = xbmcaddon.Addon(id='plugin.video.xbmb3c')
        if __settings__.getSetting(xbmc.getSkinDir()+ '_VIEW_' + containerType) != "disabled":
            __settings__.setSetting(xbmc.getSkinDir()+ '_VIEW_' + containerType, viewId)

def checkNotifications(notificationType):
    
    if notificationType == "weather":
        win = xbmcgui.Window(12600)
        if (win.getProperty("Alerts.RSS") != "" and win.getProperty("Current.Condition") != ""):
            dialog = xbmcgui.Dialog()
            dialog.notification(xbmc.getLocalizedString(31294), win.getProperty("Alerts"), xbmcgui.NOTIFICATION_WARNING, 8000)
    
    if notificationType == "nextaired":
        win = xbmcgui.Window(10000)
        if (win.getProperty("NextAired.TodayShow") != ""):
            dialog = xbmcgui.Dialog()
            dialog.notification(xbmc.getLocalizedString(31295), win.getProperty("NextAired.TodayShow"), xbmcgui.NOTIFICATION_WARNING, 8000)    
            
            
def showSubmenu(showOrHide,doFocus):

    win = xbmcgui.Window( 10000 )
    submenuTitle = xbmc.getInfoLabel("Container(300).ListItem.Label")
    submenu = win.getProperty("submenutype")
    submenuloading = ""
    if xbmc.getCondVisibility("Skin.HasSetting(AutoShowSubmenu)"):
        submenuloading = win.getProperty("submenuloading")

    # SHOW SUBMENU    
    if showOrHide == "SHOW":
        if submenuloading != "loading":
            if submenu != "":
                win.setProperty("submenu", "show")
                if doFocus != None:
                    win.setProperty("submenuTitle", submenuTitle)
                    xbmc.executebuiltin('Control.SetFocus('+ doFocus +',0)')
                    time.sleep(0.2)
                    xbmc.executebuiltin('Control.SetFocus('+ doFocus +',0)')
            else:
                win.setProperty("submenu", "hide")
        else:
            win.setProperty("submenuloading", "")

    #HIDE SUBMENU
    elif showOrHide == "HIDE":
        win.setProperty("submenuloading", "loading")
        win.setProperty("submenu", "hide")
        if doFocus != None:
            win.setProperty("submenu", "show")
            xbmc.executebuiltin('Control.SetFocus('+ doFocus +',0)')
            time.sleep(0.5)
            xbmc.executebuiltin('Control.SetFocus('+ doFocus +',0)')
            win.setProperty("submenuloading", "loading")
            win.setProperty("submenu", "hide")
            
