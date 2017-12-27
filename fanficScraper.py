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

#main run function
def run(args):
	data = fan_fic_net_parse(args.url)
	with open(args.destination, "w") as f:
		f.write(data)


	#load the initial search terms
	
	#iterate through all the links in the search and attempt to scrape the results from it
	


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", help="toggles the function to pars fanfiction.net rather than AO3", action="store_true")
	parser.add_argument("url", nargs='?', default="https://www.fanfiction.net/s/12672741/1/renascentia", help="base url to scrape from")
	parser.add_argument("destination", nargs='?', default="train_1.txt", help="file to save to, eg. train_1.txt")
	
	args = parser.parse_args()
	run(args)