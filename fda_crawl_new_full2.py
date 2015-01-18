from urllib import urlopen
from lxml.html import fromstring
from nameparser.parser import HumanName
import csv

def last_and_first_name(name_list1, name_list2):

	name_listf = []
	name_listl = []
	name_list1f = []
	name_list1l = []
	name_list2f = []
	name_list2l = []

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
		name_list1f.append(first)	
		name_list1l.append(last)

       
	for name in name_list2:
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
		name_list2f.append(first)	
		name_list2l.append(last)
		
	# for item in name_list:
	# 	print item
	name_listf = name_list1f + name_list2f
	name_listl = name_list1l + name_list2l
	with open('output.csv', 'w') as csvfile:
		fieldnames = ['first_name', 'last_name']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writeheader()
		for row in zip(name_listf, name_listl):
			writer.writerow({'first_name': row[0], 'last_name':row[1]})


	return (name_list1f,name_list1l,name_list2f,name_list2l)



fda_gov_dict = {"names":[],"effective_date":[],"eod":[],"fr_date":[],"vol_page":[]}
ad_dict = {"names":[],"url":[],"center":[],"status":[],"date_of_status":[],"dt_nidpoe_issued":[],"dt_nooh_issued":[],"link_nidpoe":[],"link_nooh":[]}

# extractaion and cleaning for fda.gov
url = "http://www.fda.gov/ICECI/EnforcementActions/FDADebarmentList/default.htm"
html = urlopen(url).read()

tree = fromstring(html)
trs =  tree.xpath('//*[@class="table-responsive"]/table[1]//tr')
elements = [elem for elem in trs if any("," in s for s in elem.xpath('td[1]//text()')) or elem.xpath('td[1]//text()') == [u'\xa0']]


for tr in elements:
	fda_gov_dict["names"].append(tr.xpath('td[1]//text()')[0])
	fda_gov_dict["effective_date"].append(tr.xpath('td[2]//text()')[0])
	fda_gov_dict["eod"].append(tr.xpath('td[3]//text()')[0])
	fda_gov_dict["fr_date"].append(tr.xpath('td[4]//text()')[0])
	fda_gov_dict["vol_page"].append(tr.xpath('td[5]//text()')[0])


# extractaion and cleaning for accessdata.fda.gov
url2 = "http://www.accessdata.fda.gov/scripts/SDA/sdNavigation.cfm?sd=clinicalinvestigatorsdisqualificationproceedings&previewMode=true&displayAll=true"
html2 = urlopen(url2).read()

tree2 = fromstring(html2)
trs2 =  tree2.xpath("//table[1]//tr")

elements = [elem for elem in trs2 if not any("\r" in s for s in elem.xpath('td[1]//text()')) and not elem.xpath('td[1]//text()') == []]

for tr in elements:
	ad_dict["names"].append(tr.xpath('td[1]//text()')[1])
	ad_dict["url"].append(tr.xpath('td[1]//a/@href')[0])
	ad_dict["center"].append(tr.xpath('td[2]//text()')[0].strip())
	ad_dict["status"].append(tr.xpath('td[3]//text()')[0].strip())
	ad_dict["date_of_status"].append(tr.xpath('td[4]//text()')[0].strip())
	ad_dict["dt_nidpoe_issued"].append(tr.xpath('td[5]//text()')[0].strip())
	ad_dict["dt_nooh_issued"].append(tr.xpath('td[6]//text()')[0].strip())
	ad_dict["link_nidpoe"].append(tr.xpath("td[7]//a/@href"))
	ad_dict["link_nooh"].append(tr.xpath('td[8]//a/@href'))

name_list1f,name_list1l,name_list2f,name_list2l = last_and_first_name(fda_gov_dict["names"],ad_dict["names"])

for i in ad_dict["status"]:
	print i

with open('output_access.csv', 'w') as csvfile:
	fieldnames = ['first_name', 'last_name',"full_name","url","center","status","date_of_status","dt_nidpoe_issued","dt_nooh_issued","link_nidpoe","link_nooh"]
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for row in zip(name_list2f, name_list2l,ad_dict["names"],ad_dict["url"],ad_dict["center"],ad_dict["status"],ad_dict["date_of_status"],ad_dict["dt_nidpoe_issued"],ad_dict["dt_nooh_issued"],ad_dict["link_nidpoe"],ad_dict["link_nooh"]):
		writer.writerow({'first_name': row[0],'last_name':row[1],'full_name':row[2],'url':row[3],'center':row[4],'status':row[5].encode('utf8'),'date_of_status':row[6],'dt_nidpoe_issued':row[7],'dt_nooh_issued':row[8],'link_nidpoe':''.join(row[9]),'link_nooh':''.join(row[10])})
