from urllib import urlopen
from lxml.html import fromstring
from nameparser.parser import HumanName
import csv

def last_and_first_name(name_list1, name_list2):

	name_listf = []
	name_listl = []
	i = 1 

	for name in name_list1:
		first = ""
		last = ""
		#extra logic needed for those first names which are put in suffix part of name
		if "." in HumanName(name).suffix:
		    na = HumanName(name).suffix.split(',')[1]
		    first = na.split()[0]
		    last = HumanName(name).first
		else:
			first = HumanName(name).first
			last = HumanName(name).last


		name_listf.append(first)	
		name_listl.append(last)

       
	for name in name_list2:
		first = ""
		last = ""
		
		#extra logic needed for those first names which are put in suffix part of name
		if "." in HumanName(name).suffix:
			na = HumanName(name).suffix.split(',')[1]
			first = na.split()[0]
			last = HumanName(name).first
			name_listf.append(first)	
			name_listl.append(last)
		   
		else:
			first = HumanName(name).first
			last = HumanName(name).last
			name_listf.append(first)	
			name_listl.append(last)
		

	# for item in name_list:
	# 	print item

	with open('output.csv', 'w') as csvfile:
	    fieldnames = ['first_name', 'last_name']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	    writer.writeheader()
	    for row in zip(name_listf, name_listl):
	        writer.writerow({'first_name': row[0], 'last_name':row[1]})




name_list1 = []
name_list2 = []


# extractaion and cleaning for fda.gov
url = "http://www.fda.gov/ICECI/EnforcementActions/FDADebarmentList/default.htm"
html = urlopen(url).read()

tree = fromstring(html)
trs =  tree.xpath('//*[@class="table-responsive"]/table[1]//tr')

for tr in trs:
	ls = tr.xpath('td[1]//text()')
	if any("," in s for s in ls):
		if ls:
			name_list1.append(ls[0])
			# print ls[0] #name    


# extractaion and cleaning for accessdata.fda.gov
url2 = "http://www.accessdata.fda.gov/scripts/SDA/sdNavigation.cfm?sd=clinicalinvestigatorsdisqualificationproceedings&previewMode=true&displayAll=true"
html2 = urlopen(url2).read()

tree2 = fromstring(html2)
trs2 =  tree2.xpath("//table[1]//tr")

for tr in trs2:
	ls = tr.xpath('td[1]//text()')
	if not any("\r" in s for s in ls):
		if ls:
			name_list2.append(ls[1])
			# print ls[1] #name


last_and_first_name(name_list1,name_list2)








    
