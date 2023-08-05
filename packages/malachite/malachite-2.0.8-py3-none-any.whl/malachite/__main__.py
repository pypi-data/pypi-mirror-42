#!/usr/bin/python

from __future__ import print_function
from os.path import join, dirname, abspath
import os
import sys
import re
import ast
# from cmndline import *
# from cmndPhase2 import *
from collections import Counter
import csv
import mechanize
from bs4 import BeautifulSoup as BS
import requests
import urllib
import xlrd
import requests
import json
# from mech import mechanizer

def main():
# pwd = os.getcwd()
    print('Number of arguments:', len(sys.argv), 'arguments.')
    inputFile = sys.argv[1]
    inputType = str(sys.argv[2])
    categories = sys.argv[3]
    indiv_output = sys.argv[4]
    concat_output = sys.argv[5]
    print("INPUT FILES: "+inputFile)
    print("INPUT TYPE: "+inputType)
    print("CATEGORIES: "+categories)
    print("INITIAL TOPPGENE OUTPUT PATH: "+indiv_output)
	# print("NAME FOR OUTPUT: "+name_for_output)
    print("CONCATENATED RESULTS OUTPUT PATH: "+concat_output)
    cmndline(inputFile, inputType, categories, indiv_output)
    cmndPhase2(indiv_output, categories, concat_output)

def cmndline(path_in, input_type, category, indiv_output):
	# path_in = sys.argv[1]
    # inputfile = join(dirname(dirname(abspath(__file__))), '', file_in)
	# list_of_files = getFiles(path_in)
	# if '.DS_Store' in list_of_files:
	#     list_of_files.remove('.DS_Store')

	# input_type = sys.argv[2]
	# category = sys.argv[3]
	pval_method = 'HYPER_PMF'
	# output_name = str(sys.argv[4])

	topgen(path_in, input_type, category, pval_method, indiv_output)

def cmndPhase2(indiv_output, categor, path_out):
	# path_in = str(sys.argv[1])

	list_of_files = getFiles(indiv_output)
	if '.DS_Store' in list_of_files:
	    list_of_files.remove('.DS_Store')

	numof = len(list_of_files)

	# CATEGORY
	category = ast.literal_eval(categor)

	# OUTPUT PATH NAME
	# name = str(name)

	# OUTPUT PATH
	path_out = str(path_out)

	toppDict = {"GeneOntologyMolecularFunction": "GO: Molecular Function", "GeneOntologyBiologicalProcess": "GO: Biological Process", "GeneOntologyCellularComponent":"GO: Cellular Component", "HumanPheno":"Human Phenotype","MousePheno":"Mouse Phenotype","Domain":"Domain", "Pathway":"Pathway","Pubmed":"Pubmed","Interaction":"Interaction","Cytoband":"Cytoband","TFBS":"Transcription Factor Binding Site","GeneFamily":"Gene Family","Coexpression":"Coexpression","CoexpressionAtlas":"Coexpression Atlas","Computational":"Computational","MicroRNA":"MicroRNA","Drug":"Drug","Disease":"Disease"}

	print("currently running part (1/2), please wait.")
	dcount(indiv_output, numof, list_of_files, path_out, category, toppDict)
	print("currently running part (2/2), please wait.")
	dcount2(indiv_output, numof, list_of_files, path_out, category, toppDict)
	print("done.")

def dcount(path_in, numof, list_of_files,  path_out, category, toppDict):
    # master = []
    # totalCanc = []
    # totalDrugs = []
    for cat in category:
        master = []
        totalCanc = []
        totalDrugs = []
        print("CURRENT CATEGORY: "+str(cat))
        z = 0
        for oo in range(0, numof):
            master = []
            totalTemp = []
            title = str(path_in) + str(list_of_files[oo])
            print(title)
            symbolfile = open(title)

            symbolslist = symbolfile.read()

            num_lines = sum(1 for line in open(title))
            print("NUMLINES: "+str(num_lines))

            array = []
            j=0
            while j<num_lines:
                b = symbolslist.split('\n')[j]
                array.append(b)
                j+=1
                if j%1000 == 0:
                    print("CurrentLine: "+str(j)+" out of "+str(num_lines))
            tempDrugList = []
            for i in range(0, len(array)):
                if toppDict[cat] in array[i]:
                    tempDrugList.append(array[i].split('\t')[2])
                    # print("ARRAY[i]: "+array[i].split('\t')[2])

            # Remove duplicates in list of drugs
            tempDrugList = set(tempDrugList)
            tempDrugList = list(tempDrugList)

            tempDrugList1 = []

            sep = ' ['
            sep2 = '; '
            for word in tempDrugList:
                if '[' in word:
                    rest = word.split(sep,1)[0]
                    tempDrugList1.append(str(rest))
                elif ';' in word:
                    rest = word.split(sep2,1)[0]
                    tempDrugList1.append(str(rest))
                else:
                    tempDrugList1.append(word)
            tempDrugList = tempDrugList1

            count = len(tempDrugList)

            totalTemp.extend(tempDrugList)

            totalTemp = [str(x).lower() for x in tempDrugList]

            totalTemp = set(totalTemp)
            totalTemp = list(totalTemp)
            master.extend(totalTemp)

            # titleCount is a list of patient and corresponding number of drugs
            titleCount = []
            titleCount.append([title, count])

            # Converts to tuple with drug/number of occurences
            c = Counter(master)
            # Sorts into most common first
            mc = c.most_common()
            # print mc

            cancgov = []
            html = requests.get('https://www.cancer.gov/about-cancer/treatment/drugs')
            soup = BS(html.text, "lxml")
            for d in soup.find_all("ul", {"class": "no-bullets no-description"}):
                for b in d.find_all('li'):
                    element = b.string
                    if ((element) != None):
                        cancgov.append(element.encode('utf-8').strip())
            cancgov = set(cancgov)
            cancgov = list(cancgov)

            cancgovNew = []
            cancgovNew = [str(item).lower() for item in cancgov]

            masterNew = []
            masterNew = [str(x).lower() for x in master]

            # q is list of drugs found in https://www.cancer.gov/about-cancer/treatment/drugs
            # checks to see if is substring of words in the list
            q = []
            for mas in masterNew:
                m = [s for s in cancgovNew if mas in s]
                if not m:
                    pass
                else:
                    q.append(mas)
                m = []

            q = list(set(q))

            totalCanc.extend(q)

            totalDrugs.extend(masterNew)

            z = z+1
            if cat == "Drug":
                file = open(str(path_out) +str(cat)+ "--" +str(list_of_files[oo]) + str(z),"w")
                file.write("Cancer Drugs:")
                file.write("\n")
                file.write("\n")
                file.write(str(q))
                file.write("\n")
                file.write("\n")

                file.write("All Drugs:")
                file.write("\n")
                file.write("\n")
                file.write(str(masterNew))
            else:
                file = open(str(path_out) +str(cat)+ "--" +str(list_of_files[oo]) + str(z),"w")
                file.write(str(cat) +": ")
                file.write("\n")
                file.write("\n")
                file.write(str(masterNew))
                file.write("\n")
                file.write("\n")


            # master = []
            # totalCanc = []
            # totalDrugs = []

def dcount2(path_in, numof, list_of_files,  path_out, category, toppDict):
    for cat in category:
        master = []
        totalCanc = []
        totalDrugs = []
        print("CURRENT CATEGORY: "+str(cat))
        z = 0
        for y in range(0, numof):
            master = []
            totalTemp = []
            title = str(path_in) + str(list_of_files[y])
            print(title)
            symbolfile = open(title)

            symbolslist = symbolfile.read()

            num_lines = sum(1 for line in open(title))

            array = []
            j=0
            while j<num_lines:
                b = symbolslist.split('\n')[j]
                array.append(b)
                j+=1



            tempDrugList = []
            for i in range(0, len(array)):
                if toppDict[cat] in array[i]:
                    # print("ARRAY[i]: "+array[i])
                    tempDrugList.append(array[i].split('\t')[2])

            # Remove duplicates in list of drugs
            tempDrugList = set(tempDrugList)
            tempDrugList = list(tempDrugList)
            # print("CHECK",len(tempDrugList))
            # print("CHECK",len(tempDrugList))
            tempDrugList1 = []
            # print("TEMPDRUGLIST:", tempDrugList)
            sep = ' ['
            sep2 = '; '
            for word in tempDrugList:
                # print("WORD:", word)
                if '[' in word:
                    # print("TRUE")
                    rest = word.split(sep,1)[0]
                    # print("Rest:", rest)
                    tempDrugList1.append(str(rest))
                elif ';' in word:
                    # print("TRUE")
                    rest = word.split(sep2,1)[0]
                    # print("Rest:", rest)
                    tempDrugList1.append(str(rest))
                else:
                    tempDrugList1.append(word)
            tempDrugList = tempDrugList1

            # print("TEMPDRUGLIST1:", tempDrugList1)
            # print("TEMPDRUGLIST:", tempDrugList)
            # number of drugs
            count = len(tempDrugList)
            # print(len(tempDrugList))
            # print("CHECK",len(tempDrugList))
            totalTemp.extend(tempDrugList)

            # print("CHECK",len(tempDrugList))
            # print("CHECK",len(totalTemp))

            totalTemp = [str(x).lower() for x in tempDrugList]

            # print("CHECK",len(tempDrugList))
            # print("CHECK",len(totalTemp))
            totalTemp = set(totalTemp)
            totalTemp = list(totalTemp)
            # print("CHECK",len(totalTemp))
            master.extend(totalTemp)
            # print("CHECK",len(master))

            # titleCount is a list of patient and corresponding number of drugs
            titleCount = []
            titleCount.append([title, count])

            # writes to csv as Patient, #number of drugs
            # fd = open('individidualcount.csv','a')
            # for row in titleCount:
            #     fd.write(str(row) + "\n")



            # Checks to see if cancer.gov request is working
            # r = requests.post("https://www.cancer.gov/about-cancer/treatment/drugs")
            # print(r.status_code, r.reason)
            # print(r.content)

            # print(master)
            # Converts to tuple with drug/number of occurences
            c = Counter(master)
            # Sorts into most common first
            mc = c.most_common()
            # print mc

            cancgov = []
            html = requests.get('https://www.cancer.gov/about-cancer/treatment/drugs')
            soup = BS(html.text, "lxml")
            for d in soup.find_all("ul", {"class": "no-bullets no-description"}):
                for b in d.find_all('li'):
                    element = b.string
                    if ((element) != None):
                        cancgov.append(element.encode('utf-8').strip())
            cancgov = set(cancgov)
            cancgov = list(cancgov)

            cancgovNew = []
            cancgovNew = [str(item).lower() for item in cancgov]

            masterNew = []
            masterNew = [str(x).lower() for x in master]

            # q is list of drugs found in https://www.cancer.gov/about-cancer/treatment/drugs
            # checks to see if is substring of words in the list
            q = []
            for mas in masterNew:
                m = [s for s in cancgovNew if mas in s]
                if not m:
                    pass
                else:
                    q.append(mas)
                m = []
            # q = [e for e in masterNew if e in cancgovNew]
            q = list(set(q))
            # print(len(q))

            totalCanc.extend(q)
            # print(len(q))
            # print(len(totalCanc))
            # print(totalCanc)
            totalDrugs.extend(masterNew)
            # print(masterNew)

            # if "gemcitabine" in masterNew:
            #     print("TRUE")
            # else:
            #     print("FALSE")
            # if "gemcitabine hydrochloride" in cancgovNew:
            #     print("TRUE")
            # else:
            #     print("FALSE")
            # if "gemcitabine" in q:
            #     print("TRUE")
            # else:
            #     print("FALSE")
            # print(len(masterNew))
            # print(len(cancgovNew))
            # print(len(q))

            # z = z+1
            # file = open("/Users/Gershkowitz/Desktop/HowTo/Phase2/Results/LuadTotal"+str(z),"w")
            # file.write("Cancer Drugs:")
            # file.write("\n")
            # file.write("\n")
            # file.write(str(q))
            # file.write("\n")
            # file.write("\n")

            # file.write("All Drugs:")
            # file.write("\n")
            # file.write("\n")
            # file.write(str(masterNew))


        # Converts to tuple with drug/number of occurences
        canc1 = Counter(totalCanc)
        # Sorts into most common first
        canc2 = canc1.most_common()

        mast1 = Counter(totalDrugs)
        # Sorts into most common first
        mast2 = mast1.most_common()
        # print("Cancer Drugs:"+str(canc2))
        # print("Total Drugs:"+str(mast2))
        #
        # file = open(str(path_out) +str(cat)+ "--" +name +"Total.txt","w")
        # print(str(str(path_out) +str(cat)+ "--" +name +"Total.txt"))
        # file.write("Cancer Drugs:")
        # file.write("\n")
        # file.write("\n")
        # file.write(str(canc2))
        # file.write("\n")
        # file.write("\n")
        #
        # file.write("All Drugs:")
        # file.write("\n")
        # file.write("\n")
        # file.write(str(mast2))

        if cat == "Drug":
            file = open(str(path_out) +str(cat)+ "--Total.txt","w")
            file.write("Cancer Drugs:")
            file.write("\n")
            file.write("\n")
            file.write(str(canc2))
            file.write("\n")
            file.write("\n")

            file.write("All Drugs:")
            file.write("\n")
            file.write("\n")
            file.write(str(mast2))
        else:
            file = open(str(path_out) +str(cat)+ "--Total.txt","w")
            file.write(str(cat) +": ")
            file.write("\n")
            file.write("\n")
            file.write(str(mast2))
            file.write("\n")
            file.write("\n")

def mechanizer(title, entrez, input_type, category, pval_method, indiv_output):
    # print("ENTREZZZ: "+str(entrez))
    # Parses topgene TOPPFUN
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open('https://toppgene.cchmc.org/enrichment.jsp')
    br.select_form(nr=0) # Select first form

    # Set entry type to Entrez ID
    br.form['type'] = [input_type]
    # print("ENTREZZZ: "+str(entrez))
    br.form['training_set'] = entrez
    r = br.submit()

    data = r.read()
    soup = BS(data, "lxml")
    # "userid" is custom ID assigned to user by topgene
    userid = soup.input["value"]
    br.open('https://toppgene.cchmc.org/input_enrichment.jsp?userdata_id='+str(userid))

    br.select_form(nr=0)
    br.form['pvaluemethod'] = [pval_method]

    # Set feature disease to True, everything else to false
    print("USERID: "+ userid)
    options = br.find_control("category").items
    # print("OPTIONS: "+ str(options))
    for i in range(0, len(options)):
        if options[i].name in category:
            options[i].selected=True
            print("True: "+ options[i].name)
        else:
            options[i].selected=False
            print("False: "+ options[i].name)
    br.submit()

    # Get results
    url = 'https://toppgene.cchmc.org/download.jsp?userdata_id=' + str(userid)
    r = requests.get(url, allow_redirects=True)
    # Write results to text file
    # print("CONTENT:::::::::::::"+str(r.content))
    open(indiv_output+"resultFor_"+str(title), 'wb').write(r.content)

def topgen(path_in, input_type, category, pval_method, indiv_output):

    current = 0

    # tempFileName = str(list_of_files[i])
    fname = join(dirname(dirname(abspath(__file__))), 'test_data', str(path_in))

    # Open the workbook
    print("FNAME: "+str(fname))
    xl_workbook = xlrd.open_workbook(fname)

    # List sheet names, and pull a sheet by name
    sheet_names = xl_workbook.sheet_names()
    print('Sheet Names', sheet_names)

    xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])

    # Or grab the first sheet by index
    #  (sheets are zero-indexed)
    xl_sheet = xl_workbook.sheet_by_index(0)
    print ('Sheet name: %s' % xl_sheet.name)

    num_rows = xl_sheet.nrows  # Number of rows
    num_cols = xl_sheet.ncols   # Number of columns


    entrez_id = ""
    tempName = ""
    print ("NUMBER OF Rows: " , num_rows)
    print ("NUMBER OF Cols: " ,num_cols)
    # In this case, 1 is where the patient names start
    for c in range(0, num_cols):
        current = current + 1
        entrez_id = ""
        # count = 0
        for r in range(0, num_rows):
            if(r == 0):
                # Add name of patient to index zero of list
                tempName = (str((xl_sheet.cell(r, c).value)))
            else:
                try:
                    entrez_id = entrez_id + (str(int(xl_sheet.cell(r, c).value))) + ", "
                except:
                    entrez_id = entrez_id + (str((xl_sheet.cell(r, c).value))) + ", "
        print("Name: ",tempName)
        # print("IDs" , entrez_id)
        # Call topgene parser
        # print("TEMPNAME????????????????????????"+tempName)
        # print("ENTREZIDS????????????????????????"+entrez_id)
        mechanizer(tempName, entrez_id, input_type, category, pval_method, indiv_output)
        entrez_id = ""

def getFiles(path):
    arr = os.listdir(path)
    return arr
# ./malachite.py "/Users/Gershkowitz/Desktop/malachite/Phase1/LuSc-nuResults/" "ENTREZ" "['Drug','Disease','TFBS']" "Phase1/Phase1output/LuSc/" "LuSc" "/Users/Gershkowitz/Desktop/malachite-final/Phase2/Results/LuSc_Output/"

# os.system("python "+ pwd + "/Phase1/cmndline.py"  +" \""+inputFiles+"\" " +" \""+inputType+"\" "+" \""+categories+"\" "+" \""+indiv_output+"\"")

# os.system("python "+ pwd + "/Phase2/cmndPhase2.py"  +" \""+indiv_output+"\" " +" \""+categories+"\" " +" \""+name_for_output+"\" "+" \""+concat_output+"\"")

if __name__ == "__main__":
    main()
