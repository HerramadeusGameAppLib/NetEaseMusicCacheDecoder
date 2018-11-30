#-------------------------------------------------------------
#-------------------------------------------------------------

class UrlChecker:

    def IsValidUrl(self, url):
        return NotImplemented

#-------------------------------------------------------------

class KeywordSongChecker(UrlChecker):

    def IsValidUrl(self, url):

        if url.rfind("song") >= 0 :
            return True

        print("Invalid Url: No Keyword: \"song\"")
        return False

#-------------------------------------------------------------

class NetEaseMusicLinkChecker(UrlChecker):
    
    def IsValidUrl(self, url):

        if url.find("music.163.com") >= 0 :
            return True

        print("Invalid Url: Not A Netease Cloud Music Link")
        return False

#-------------------------------------------------------------
#-------------------------------------------------------------

class MusicIDGetter:
    
    url_checkers = None

    def GetMusicID(self, url):

        if None != self.url_checkers:
            for checker in self.url_checkers:
                if False == checker.IsValidUrl(url):
                    return None

        music_id_str = str(url).rpartition("id=")[2]
        if(id(music_id_str) == id(url)):
            print("Invalid Url: No Keyword: \"id\"")
            return None

        if(0 == len(music_id_str)):
            print("Invalid Url: No Valid ID")
            return None

        print("Music ID: " + music_id_str)
        return music_id_str

#-------------------------------------------------------------
#-------------------------------------------------------------

class OutLinkUrlGetter:
    
    out_link_url_head = "http://music.163.com/song/media/outer/url?id="
    out_link_url_tail = ".mp3"

    def GetOutLinkUrl(self, music_id_str):
        
        if None == music_id_str or 0 == len(music_id_str):
            print("Invalid Music ID")
            return None

        return self.out_link_url_head+music_id_str+self.out_link_url_tail

#-------------------------------------------------------------
#-------------------------------------------------------------

import urllib
import urllib.request

class ActualUrlGetter:

    def GetActualUrl(self, outlink_url):

        result = None
        res = None

        try:
            req = urllib.request.Request(url=outlink_url, method="GET")
            req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)")

            res = urllib.request.urlopen(req)
            result = res.geturl()

        except Exception as ex:
            print("Cannot Get Actual Url: " + str(ex))

        finally:
            if None != res:
                res.close()

        return result

#-------------------------------------------------------------
#-------------------------------------------------------------

class ActualUrl_404_Checker(UrlChecker):

    url_of_404 = "404"

    def IsValidUrl(self, url):
        if str(url).rfind(self.url_of_404) + 3 < len(url):
            return True

        print("Not An Downloadable Url: Actual Url is 404")

#-------------------------------------------------------------        
#-------------------------------------------------------------

class MusicDataWriter:
    
    def Write(self, path_to_write, data):
        return NotImplemented

#-------------------------------------------------------------

class SimpleMusicDataWriter(MusicDataWriter):

    def Write(self, path_to_write, data):

        result = False
        try:
            write_file = open(path_to_write, "wb")
            write_file.write(data)
            result = True
        except ex:
            print("Cannot Write Music Data: " + str(ex))

        finally:
            if None != write_file:
                write_file.close()

        return result

#-------------------------------------------------------------
#-------------------------------------------------------------

class Downloader:
    def Download(self, url, path_to_write):
        return NotImplemented

#-------------------------------------------------------------

class HttpDownloader(Downloader):

    music_data_writer = None

    def __init__(self, *args, **kwargs):

        self.music_data_writer = SimpleMusicDataWriter()
        return super().__init__(*args, **kwargs)

    def Download(self, url_to_download, path_to_write):

        result = False
        try:
            req = urllib.request.urlopen(url_to_download)
            data = req.read()
            self.music_data_writer.Write(path_to_write, data)
            result = True

        except ex:
            print("Cannot Download: " + str(ex))

        finally:
            if None != req:
                req.close()

        return result

#-------------------------------------------------------------
#-------------------------------------------------------------

import sys
class DownloadPerformer:

    music_id_getter = None
    outlink_url_getter = None

    actual_url_getter = None
    actual_url_404_checker = None

    downloader = None

    def __init__(self, *args, **kwargs):
        self.music_id_getter = MusicIDGetter()
        self.music_id_getter.url_checkers = [KeywordSongChecker(), NetEaseMusicLinkChecker()]

        self.outlink_url_getter = OutLinkUrlGetter()
        self.actual_url_getter = ActualUrlGetter()
        self.actual_url_404_checker = ActualUrl_404_Checker()
        self.downloader = HttpDownloader()

    def  Run(self):
        music_url = input("\nInput Music Url:")

        print("Getting Music ID...")
        music_id = self.music_id_getter.GetMusicID(music_url)
        if None == music_id:
            return

        print("Getting Outlink Url...")
        outlink_url = self.outlink_url_getter.GetOutLinkUrl(music_id)
        if None == outlink_url:
            return

        print("Getting Actual Url...")
        actual_url = self.actual_url_getter.GetActualUrl(outlink_url)
        if None == actual_url:
            return

        if not self.actual_url_404_checker.IsValidUrl(actual_url):
            return

        #-------------------------------------------------------------

        print("Actual Url Is:\n\n" + actual_url)
        print("\nStart Downloading...\n")

        path_to_write = sys.path[0]+"\\"+music_id+".mp3"
        if self.downloader.Download(actual_url, path_to_write):
            print("Download Completed At:\n" + path_to_write + "\n")

#-------------------------------------------------------------
#-------------------------------------------------------------

download_performer = DownloadPerformer()
while(True):
    download_performer.Run()
