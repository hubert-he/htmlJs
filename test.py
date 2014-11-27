#!/usr/bin/env python

import string, os, sys, re
from xlwt import Workbook, XFStyle, Borders, Pattern, Font, easyxf

  	
result_file = "xls.txt"
languageMap = {"en":"English", \
               "fr":"French", \
               "it":"Italian", \
               "sp":"Spanish", \
               "ge":"German", \
               "hu":"Hungarian", \
               "po":"Polish", \
               "cz":"Czech", \
               "ch":"Chinese", \
               "tw":"Traditional Chinese" \
               }

def printStr(cnt):
    if cnt < 0:
        return "000"
    elif cnt < 10:
        return "00"+str(cnt)
    elif cnt < 100:
        return "0"+str(cnt)
    elif cnt < 1000:
        return str(cnt)
    else:
        return str(cnt)

if __name__ == "__main__":
    try:
        dir = sys.argv[1]
        files = os.listdir(dir)
        language_list = ['en', 'sp']
    except:
        print "ARGV:"
        sys.exit()
    try:
        keyword_xls = Workbook(encoding='utf-8')
        keyword_sheet = keyword_xls.add_sheet('content')
    except :
        print "error on worksheet creating"
        sys.exit()
    p = re.compile('(.*)\.offset$')
    row = 0
    col = 0
    titleStyle = easyxf(
        'pattern: pattern solid, fore_colour pale_blue;'
        'borders: left thin, right thin, top thin, bottom thin;'
        'font: bold True, height 220;'
        )
    rowstyle = easyxf(
        'pattern: pattern solid, fore_colour yellow;'
        'borders: left thin, right thin, top thin, bottom thin;'
        )
    cellStyle = easyxf(
        'alignment: horizontal left, indent 0, vertical top, wrap True;'
        'protection:cell_locked True;'
	'font: height 220;'
        )
    colStyle = easyxf(
        'protection:cell_locked False;'
    )
    col_width = 256*30
    col_width_field = 256*40
    language_col = len(language_list)
       # keyword_sheet.write(row,col,"", rowstyle)
#   print header of xls
    keyword_sheet.write(row,0,"local language htm", titleStyle)
    keyword_sheet.col(0).width = col_width
    keyword_sheet.row(row).set_style(titleStyle)
    i = 1
    for entry in language_list:
        keyword_sheet.write(row,i,languageMap[entry], titleStyle)
        i += 1
    row += 1
    
    for fname in files:
        web_name = p.match(fname)
	keyword = {}
        if web_name:
            keyword_sheet.row(row).set_style(rowstyle)
            keyword_sheet.write(row,col,"", rowstyle)
            
            row += 1
            keyword_sheet.row(row).set_style(rowstyle)
            keyword_sheet.write(row,col,web_name.group(1), rowstyle)
            row += 1
            fhandler = open(dir + os.sep + fname, 'rb')
            lines = fhandler.readlines()
	    for lt in lines:
		lt = lt.strip()
		keyword[lt] = lt
	    #print keyword
            count = 0
            for line in lines:
                line = line.strip()
		if line not in keyword:
		    continue
		if isinstance(line, unicode) == False:
		    try:
			line2 = line.encode('utf-8')
		    except:
			print line
			print web_name.group(1)
			continue
                keyword_sheet.write(row,col,web_name.group(1) + '_' + printStr(count), cellStyle)
                keyword_sheet.col(col).width = col_width
                keyword_sheet.write(row,col+1,line2, cellStyle)
                keyword_sheet.col(col+1).width = col_width_field
                i = col + 2
                while i <= language_col:
                    keyword_sheet.write(row,i,'', colStyle)
                    i += 1
                row += 1
                count += 1
		del keyword[line]
 #   keyword_sheet.write(0,1,'test')
 #   keyword_sheet.protect = True
  #  keyword_sheet.scen_protect = True
   # keyword_sheet.wnd_protect = True
 #   keyword_sheet.obj_protect = True
   # keyword_sheet.password = "adsl0413"
    keyword_xls.save('xx.xls')
    

        