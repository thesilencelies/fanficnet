#script to scrape fanfiction from websites and save them to the target text file

import argparse
import urllib.request
import re

#function to parse AO3 fic
def AO3_parse(url):
        print("not yet implimented")
        #some regex based search to slice the input html body

#function to parse FanFiction.net fic
def fan_fic_net_parse(url):
        #containter for the result
        res = ""
        
        #create the main regexes
        splitter = re.compile(r"</?div[^>]*>")
        formatter = r"<[^>]*>|\\x[\w]{2}"
        apostrophyCorrection = r"\\'"
        nextcheck = re.compile(r"<button class=btn TYPE=BUTTON onClick=[^>]*>Next")
        urleditor = r'(\/s\/\d+\/)(\d+)\/'
        
        while True:
                try:
                        raw = str(urllib.request.urlopen(url).read())
                        
                        #strip out the actual text and append it to the url
                        split = splitter.split(raw)
                        
                        #the actual text will be the biggest of the cuts
                        ind = 0
                        maxlen = 0
                        for i in range(0,len(split)):
                                if len(split[i]) > maxlen:
                                        maxlen = len(split[i])
                                        ind = i
                        
                        #remove the formatting we don't want
                        split[ind] = re.sub(formatter, " ", split[ind])
                        split[ind] = re.sub(apostrophyCorrection, "'", split[ind])
                        
                        #append the text to the output
                        res = res + split[ind]
                        
                        #check for a next button, and then attempt to incriment the url
                        next = nextcheck.search(raw)
                        if next :
                                #iterate the url check
                                newind = int(re.search(urleditor, url).group(2)) + 1
                                url = re.sub(urleditor, r'\g<1>' + str(newind) + "/", url)
                        else:
                                return res
                        
                except Exception as err:
                        print("exception whilst attempting to parse url: " + url)
                        print("error: {0}".format(err))
                        return res
                        
#turns the main search term into a list of urls
def generate_ffnet_search_res(url):
        res = []
        urlIterRgex = r"(&p=)(\d)"
        hrefRgx = r"href=[^>]*(/s/\d*/1/[^\"]*)"
        #check for a &p= term and if there is not, add it
        if not re.search(urlIterRgex, url):
                url = url + "&p=1"
        
        while True:
                try:
                        raw = str(urllib.request.urlopen(url).read())
                        #parse out the urls
                        new_urls = re.finditer(hrefRgx, raw)
                        for u in new_urls:
                                res.append("https://www.fanfiction.net/" + u.group(1))
                        
                        #iterate the url
                        newind = int(re.search(urlIterRgex, url).group(2)) + 1
                        url = re.sub(urlIterRgex, r'\g<1>' + str(newind) + "/", url)
                
                except Exception as err:
                        print("exception whilst attempting to parse url: " + url)
                        print("error: {0}".format(err))
                        return res
                

#main run function
def run(args):
        urls = generate_ffnet_search_res(args.url)
        with open(args.destination, "w") as f:
            f.write( fan_fic_net_parse(u) )
			f.write("|")#Special character for end of story



if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("-a3", help="toggles the function to parse Ao3 rather than fanfiction.net", action="store_true")
        parser.add_argument("url", nargs='?', default="https://www.fanfiction.net/book/Harry-Potter/?&srt=1&lan=1&r=103&len=1&p=1", help="base url to scrape from")
        parser.add_argument("destination", nargs='?', default="train_1.txt", help="file to save to, eg. train_1.txt")
        
        args = parser.parse_args()
        run(args)
