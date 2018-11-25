
#-------------------------------------------------------------

class UrlChecker:

    def IsValidUrl(self, url, error_message):
        return NotImplemented

#-------------------------------------------------------------

class KeywordSongChecker(UrlChecker):

    def IsValidUrl(self, url, error_message):

        if url.rfind("song") >= 0 :
            return True

        error_message = "no keyword: \"song\""
        return False

#-------------------------------------------------------------

class NeteaseCloudMusicLinkChecker(UrlChecker):
    
    def IsValidUrl(self, url, error_message):

        if url.find("music.163.com") >= 0 :
            return True

        error_message = "not a Netease music link"
        return False

#-------------------------------------------------------------

class MusicIDGetter:
    
    url_checkers = None

    def GetMusicID(self, url, error_message):

        if None != self.url_checkers:
            for checker in self.url_checkers:
                if False == checker.IsValidUrl(url, error_message):
                    return None

        music_id_str = str(url).rpartition("id=")[2]
        if(id(music_id_str) == id(url)):
            error_message = "no keyword: \"id\""
            return None

        if(0 == len(music_id_str)):
            error_message = "no valid id"
            return None

        print("Music ID: " + music_id_str)
        return music_id_str

#-------------------------------------------------------------

class OutLinkUrlGetter:
    
    out_link_url_head = "http://music.163.com/song/media/outer/url?id="
    out_link_url_tail = ".mp3"

    def GetOutLinkUrl(self, music_id_str, error_message):
        
        if None == music_id_str or 0 == len(music_id_str):
            error_message = "invalid music id"
            return None

        return self.out_link_url_head+music_id_str+self.out_link_url_tail

#-------------------------------------------------------------

import urllib
import urllib.request

class ActualUrlGetter:

    def GetActualUrl(self, outlink_url, error_message):

        result = None
        try:
            req = urllib.request.Request(url=outlink_url, method="GET")
            req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)")

            res = urllib.request.urlopen(req)
            result = res.geturl()

        except Exception as ex:
            error_message = str(ex)
        
        return result
        
#-------------------------------------------------------------

class Downloader:
    def Download(self, url, path_to_write):
        return NotImplemented

class HttpDownloader(Downloader):

    def Download(self, url_to_download, path_to_write):

        data = urllib.request.urlopen(url_to_download).read()
        
        with open(path_to_write, "wb") as write_file:
            write_file.write(data)

#-------------------------------------------------------------

import sys
class DownloadPerformer:

    music_id_getter = None
    outlink_url_getter = None
    actual_url_getter = None
    downloader = None

    def __init__(self, *args, **kwargs):
        self.music_id_getter = MusicIDGetter()
        self.music_id_getter.url_checkers = [KeywordSongChecker(), NeteaseCloudMusicLinkChecker()]

        self.outlink_url_getter = OutLinkUrlGetter()
        self.actual_url_getter = ActualUrlGetter()
        self.downloader = HttpDownloader()

    def  Run(self):
        music_url = input("Input Music Url:")
        error_message = ""

        music_id = self.music_id_getter.GetMusicID(music_url, error_message)
        if None == music_id:
            print("Invalid Song ID: " + error_message)
            print("\n")
            return

        outlink_url = self.outlink_url_getter.GetOutLinkUrl(music_id, error_message)
    
        if None == outlink_url:
            print("Invalid Outlink: " + error_message)
            print("\n")
            return

        actual_url = self.actual_url_getter.GetActualUrl(outlink_url, error_message)
        print("Actual Url Is:\n")
        print(actual_url)
        print("\nStart Downloading...\n")

        path_to_write = sys.path[0]+"\\"+music_id+".mp3"
        self.downloader.Download(actual_url, path_to_write)

        print("Download Completed At:\n")
        print(path_to_write)
        print("\n")

#-------------------------------------------------------------

download_performer = DownloadPerformer()
while(True):
    download_performer.Run()


