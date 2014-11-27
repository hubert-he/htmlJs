#!/usr/bin/env python
# -*- coding: utf-8 -*-
import markupbase
import re
import sys
import os
import ConfigParser
import codecs

blackList = ['VPI', 'VCI', 'DHCP', 'IPv4', 'IPv6', 'NAPT', 'ADSL', 'ATM', 'Ipv4', 'Ipv6', 'LLC', 'VC-Mux', 'PCR', 'CDVT', 'SCR', 'MBS']

##############################################################################
#   This part is all about procedure on  js processing
#   here thanks for beauty_js.js written by Einar Lielmanis.
#   Hubert_He@Realsil_Inc modified and add some new features
#############################################################################
class JSParser:
    def __init__(self):
        self.parser_pos = 0
        self.linepos = 0
        self.input = ''
        self.last_pos = 0
        self.last_type = 'TK_START_EXPR' # last token type
        self.old_type = ['', '', '','']
        self.last_text = '' # last token text
        self.old_text = ['', '', '','']
        self.last_word = ''
        self.output = ''
        self.length = 0
        self.whitespace = '\n\r\t '
        self.js_spec_keyWord = ['alert', 'prompt', 'confirm']
        self.spec_keyword_pattern = re.compile(r'\(.*[\'|\"|\t| |\n]\)')
        self.wordchar = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$'
        self.punct = ('+', '-', '*', '/', '%', '&', '++', '--', '=', '+=', '-=', '*=', '/=', '%=', '==', '===', '!=', '!==', '>', '<', '>=', '<=', '>>', '<<', '>>>', '>>>=', '>>=', '<<=', '&&', '&=', '|', '||', '!', '!!', ',', ':', '?', '^', '^=', '|=', '::')
        self.line_starters = ('continue', 'try', 'throw', 'return', 'var', 'if', 'switch', 'case', 'default', 'for', 'while', 'break', 'function')
        self.oskDefined = ('#if', '#ifdef', '<VWS_FUNCTION')
        self.backlist = ['getElementById', 'getElementByName']
        self.blackqoto = ['==', '===', '!=', '!===']
        
    def reset(self, jsString):
        self.input = jsString
        self.length = len(jsString)
    def get_file(self, filename):
        self.input = open(filename, 'r').read()
        self.length = len(self.input)
    def print_token(self,token):
        #print token
        self.output += token
    def get_next_token(self):
        if(self.parser_pos >= self.length):
            return [self.parser_pos, '', 'TK_EOF']
        curr_character = self.input[self.parser_pos]
        self.parser_pos += 1
        while(curr_character in self.whitespace):
            if(self.parser_pos >= self.length):
                return [self.parser_pos,'', 'TK_EOF']
            if curr_character == '\n':
                self.linepos = self.parser_pos
            curr_character = self.input[self.parser_pos]
            self.parser_pos += 1
        if(curr_character in self.wordchar):
            if(self.parser_pos < self.length):
                while(self.input[self.parser_pos] in self.wordchar):
                    curr_character += self.input[self.parser_pos]
                    self.parser_pos += 1
                    if(self.parser_pos == self.length):
                        break
            if(self.parser_pos != self.length and re.match(r'^[0-9]+[Ee]$', curr_character) and self.input[self.parser_pos] in "-+"):
                sign = self.input[self.parser_pos]
                self.parser_pos += 1
                tmp = self.get_next_token(parser_pos)
                curr_character += sign + tmp[0]
                return [self.parser_pos, curr_character, 'TK_WORD']
            #if curr_character == 'function':
            #    return [self.parser_pos, curr_character, 'TK_WORD_FUNCTION']
            if(curr_character == 'in'):
                return [self.parser_pos, curr_character, 'TK_OPERATOR']
            if curr_character in self.js_spec_keyWord:
                return [self.parser_pos, curr_character, 'TK_SPEC_WORD']
            return [self.parser_pos, curr_character, 'TK_WORD']
        if(curr_character == '(' or curr_character == '['):
            return [self.parser_pos, curr_character, 'TK_START_EXPR']
        
        if(curr_character == ')' or curr_character == ']'):
            return [self.parser_pos, curr_character, 'TK_END_EXPR']
        
        if(curr_character == '{'):
            return [self.parser_pos, curr_character, 'TK_START_BLOCK']
        
        if(curr_character == '}'):
            return [self.parser_pos, curr_character, 'TK_END_BLOCK']
        
        if(curr_character == ';'):
            return [self.parser_pos, curr_character, 'TK_SEMICOLON']
        # about comment
        if(curr_character == '/'):
            comment = ''
            if self.input[self.parser_pos] == '*':
                self.parser_pos += 1
                if self.parser_pos < self.length:
                    while not(self.input[self.parser_pos + 1] and self.input[self.parser_pos] == '*' and self.input[self.parser_pos + 1] == '/') and self.parser_pos < self.length:
                        comment += self.input[self.parser_pos]
                        self.parser_pos += 1
                        if self.parser_pos >= self.length:
                            break
                self.parser_pos += 2
                return [self.parser_pos, '/*' + comment + '*/', 'TK_BLOCK_COMMENT']
            if self.input[self.parser_pos] == '/':
                comment = curr_character
                while  self.input[self.parser_pos] != '\r' and self.input[self.parser_pos] != '\n':
                    comment += self.input[self.parser_pos]
                    self.parser_pos += 1
                    if self.parser_pos >= self.length:
                        break
                self.parser_pos += 1
                return [self.parser_pos, comment, 'TK_COMMENT']
        
        if(curr_character == "'" or curr_character == '"' or  # string handled 
           (curr_character == '/' and                         # regular expression handled
            ((self.last_type == 'TK_WORD' and self.last_text == 'return') or
                (self.last_type == 'TK_START_EXPR' or self.last_type == 'TK_END_BLOCK' or
                 self.last_type == 'TK_OPERATOR' or self.last_type == 'TK_EOF' or self.last_type == 'TK_SEMICOLON')))):
            sep = curr_character
            esc = False
            ret_str = '';
            if (self.parser_pos < self.length):
                while(esc or self.input[self.parser_pos] != sep):
                    ret_str += self.input[self.parser_pos]
                    if(not esc):
                        esc = (self.input[self.parser_pos] == '\\')
                    else:
                        esc = False
                    self.parser_pos += 1
                    if (self.parser_pos >= self.length):
                        break
                    
                self.parser_pos += 1
                ret_str = sep + ret_str + sep
                if(sep == '/'):
                    while (self.parser_pos < self.length and self.input[self.parser_pos] in self.wordchar):
                        ret_str += self.input[self.parser_pos]
                        self.parser_pos += 1
                    tmpcount = self.parser_pos
                    tmpstr = ''
                    while (tmpcount < self.length and self.input[tmpcount] != ';' and self.input[tmpcount] != ','):
                        if self.input[tmpcount] != '/':
                            tmpstr += self.input[tmpcount]
                        else:
                            break
                        tmpcount += 1
                    
                    if tmpcount < self.length and self.input[tmpcount] == '/':
                        self.parser_pos = tmpcount + 1
                        return [self.parser_pos, '', 'TK_UNKNOWN']
                    return [self.parser_pos, '', 'TK_UNKNOWN']
                return [self.parser_pos, ret_str, 'TK_STRING']
        if (curr_character in self.punct):
            if curr_character == '<':
                tmpCnt = self.parser_pos
                oskStr = curr_character
                while self.input[self.parser_pos] in self.whitespace:
                    self.parser_pos += 1
                    if self.parser_pos >= self.length:
                        break
                while self.input[self.parser_pos] not in self.whitespace:
                    oskStr += self.input[self.parser_pos]
                    self.parser_pos += 1
                    if self.parser_pos >= self.length:
                        break
                if oskStr in self.oskDefined:
                    while  self.input[self.parser_pos] != '\r' and self.input[self.parser_pos] != '\n':
                        oskStr += self.input[self.parser_pos]
                        self.parser_pos += 1
                        if self.parser_pos >= self.length:
                            break
                    self.parser_pos += 1
                    return [self.parser_pos, oskStr, 'TK_OSKSTRING']
                else:
                    self.parser_pos = tmpCnt
            while (self.parser_pos < self.length and ((curr_character + self.input[self.parser_pos]) in self.punct)):
                curr_character += self.input[self.parser_pos]
                self.parser_pos += 1
                if (self.parser_pos >= self.length):
                    break
            return [self.parser_pos, curr_character, 'TK_OPERATOR']
        if (curr_character == '.'):
            return [self.parser_pos, curr_character, 'TK_SPECIAL_DOT']
        if (curr_character == '#'):
            oskString = curr_character
            tempCount = self.parser_pos
            while self.input[self.parser_pos] not in self.whitespace:
                oskString += self.input[self.parser_pos]
                self.parser_pos += 1
                if self.parser_pos >= self.length:
                    break
            if oskString in self.oskDefined:
                while  self.input[self.parser_pos] != '\r' and self.input[self.parser_pos] != '\n':
                    oskString += self.input[self.parser_pos]
                    self.parser_pos += 1
                    if self.parser_pos >= self.length:
                        break
                self.parser_pos += 1
                return [self.parser_pos, oskString, 'TK_OSKSTRING']
            else:
                while  self.input[self.parser_pos] != '\r' and self.input[self.parser_pos] != '\n':
                    oskString += self.input[self.parser_pos]
                    self.parser_pos += 1
                    if self.parser_pos >= self.length:
                        break
                self.parser_pos += 1
                return [self.parser_pos, oskString, 'TK_OSKSTRING']
            
        return [self.parser_pos, curr_character, 'TK_UNKNOWN']
        
    def handleJsFunction(self):
        print "handleJsFunction"
        '''
        curr_token = self.get_next_token()
        print curr_token
        locateBrace = self.parser_pos + self.input[self.parser_pos:].find('{')
        self.parser_pos = locateBrace + 1
        function_open_brace = 1
        variable_infunction = {}
        while function_open_brace != 0 :
            curr_token = self.get_next_token()
            print curr_token
            token_pos  = curr_token[0]
            token_text = curr_token[1]
            token_type = curr_token[2]
            if token_type == 'TK_EOF':
                print "Alert: handleJsFunction Exception"
                break
            if token_text == '{':
                function_open_brace += 1
            if token_text == '}':
                function_open_brace -= 1
            if token_type == 'TK_WORD' and token_text == 'var':
                var_cur_token = self.get_next_token()
                var_flag = 1
                var_name = ''
                while var_cur_token[1] != ';':
                    if var_cur_token[2] == 'TK_WORD' and var_flag == 1:
                        var_name = var_cur_token[1]
                        var_flag = 0
                    else:
                        if var_curr_token[1] == ',':
                            var_flag = 1
                        elif var_cur_token[1] == '=':
                            variable_infunction[var_name] = self.input[var_cur_token[0]+1]
                    var_cur_token = self.get_next_token()
         
'''
"""A parser for HTML and XHTML."""

# This file is based on sgmllib.py, but the API is slightly different.

# XXX There should be a way to distinguish between PCDATA (parsed
# character data -- the normal case), RCDATA (replaceable character
# data -- only char and entity references and end tags are special)
# and CDATA (character data -- only end tags are special).

# Regular expressions used for parsing

interesting_normal = re.compile('[&<#]')
incomplete = re.compile('&[a-zA-Z#]')

entityref = re.compile('&([a-zA-Z][-.a-zA-Z0-9]*)[^a-zA-Z0-9]')
charref = re.compile('&#(?:[0-9]+|[xX][0-9a-fA-F]+)[^0-9a-fA-F]')
#scriptTagOpen = re.compile('<script[ |a-z|A-Z|=|\"|\']*>', flags=re.IGNORECASE)
scriptTagOpen = re.compile('<script.*>', flags=re.IGNORECASE)
oskStringTag = re.compile('[ |\t]*<VWS_(FUNCTION|SCREEN).*>')
starttagopen = re.compile('<[a-zA-Z]')
piclose = re.compile('>')
commentclose = re.compile(r'--\s*>')
#hubert tagfind = re.compile('[a-zA-Z][-.a-zA-Z0-9:_]*')
tagfind = re.compile('([a-zA-Z][-.a-zA-Z0-9:_]*)(?:\s|/(?!>))*')
tagfind_tolerant = re.compile('[a-zA-Z][^\t\n\r\f />\x00]*')

#hubert attrfind = re.compile(
#    r'\s*([a-zA-Z_][-.:a-zA-Z_0-9]*)(\s*=\s*'
#    r'(\'[^\']*\'|"[^"]*"|[-a-zA-Z0-9./,:;+*%?!&$\(\)_#=~@]*))?')
attrfind = re.compile(
    r'((?<=[\'"\s/])[^\s/>][^\s/=>]*)(\s*=+\s*'
    r'(\'[^\']*\'|"[^"]*"|(?![\'"])[^>\s]*))?(?:\s|/(?!>))*')
#hubert
'''
locatestarttagend = re.compile(r"""
  <[a-zA-Z][-.a-zA-Z0-9:_]*          # tag name
  (?:\s+                             # whitespace before attribute name
    (?:[a-zA-Z_][-.:a-zA-Z0-9_]*     # attribute name
      (?:\s*=\s*                     # value indicator
        (?:'[^']*'                   # LITA-enclosed value
          |\"[^\"]*\"                # LIT-enclosed value
          |[^'\">\s]+                # bare value
         )
       )?
     )
   )*
  \s*                                # trailing whitespace
""", re.VERBOSE)
'''
locatestarttagend = re.compile(r"""
  <[a-zA-Z][-.a-zA-Z0-9:_]*          # tag name
  (?:[\s/]*                          # optional whitespace before attribute name
    (?:(?<=['"\s/])[^\s/>][^\s/=>]*  # attribute name
      (?:\s*=+\s*                    # value indicator
        (?:'[^']*'                   # LITA-enclosed value
          |"[^"]*"                   # LIT-enclosed value
          |(?!['"])[^>\s]*           # bare value
         )
       )?(?:\s|/(?!>))*
     )*
   )?
  \s*                                # trailing whitespace
""", re.VERBOSE)
endendtag = re.compile('>')
endtagfind = re.compile('</\s*([a-zA-Z][-.a-zA-Z0-9:_]*)\s*>')


class HTMLParseError(Exception):
    """Exception raised for all parse errors."""

    def __init__(self, msg, position=(None, None)):
        assert msg
        self.msg = msg
        self.lineno = position[0]
        self.offset = position[1]
        

    def __str__(self):
        result = self.msg
        if self.lineno is not None:
            result = result + ", at line %d" % self.lineno
        if self.offset is not None:
            result = result + ", column %d" % (self.offset + 1)
        return result


class HTMLParser(markupbase.ParserBase):
    """Find tags and other markup and call handler functions.

    Usage:
        p = HTMLParser()
        p.feed(data)
        ...
        p.close()

    Start tags are handled by calling self.handle_starttag() or
    self.handle_startendtag(); end tags by self.handle_endtag().  The
    data between tags is passed from the parser to the derived class
    by calling self.handle_data() with the data as argument (the data
    may be split up in arbitrary chunks).  Entity references are
    passed by calling self.handle_entityref() with the entity
    reference as the argument.  Numeric character references are
    passed to self.handle_charref() with the string containing the
    reference as the argument.
    """

    CDATA_CONTENT_ELEMENTS = ("script", "style")


    def __init__(self):
        """Initialize and reset this instance."""
        self.reset()
        self.vwsInput = 0
        
    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        self.lineflag = 0
        self.rawdata = ''
        self.linepos = 0
        self.lasttag = '???'
        self.cdata_elem = None
        self.interesting = interesting_normal
        self.keyword = {}
        markupbase.ParserBase.reset(self)
    def getStartText(self):
        return self.__starttag_text
    def feed(self, data):
        r"""Feed data to the parser.

        Call this as often as you want, with as little or as much text
        as you want (may include '\n').
        """
        self.rawdata = self.rawdata + data
        self.goahead(0)

    def close(self):
        """Handle any buffered data."""
        self.goahead(1)

    def error(self, message):
        raise HTMLParseError(message, self.getpos())

    __starttag_text = None

    def get_starttag_text(self):
        """Return full source of start tag: '<...>'."""
        return self.__starttag_text

#hubert   def set_cdata_mode(self):
#        self.interesting = interesting_cdata

#    def clear_cdata_mode(self):
#        self.interesting = interesting_normal
    def set_cdata_mode(self, elem):
        self.cdata_elem = elem.lower()
        self.interesting = re.compile(r'</\s*%s\s*>' % self.cdata_elem, re.I)

    def clear_cdata_mode(self):
        self.interesting = interesting_normal
        self.cdata_elem = None
    # Internal -- handle data as far as reasonable.  May leave state
    # and data to be processed by a subsequent call.  If 'end' is
    # true, force handling all data as if followed by EOF marker.
    def goahead(self, end):
        rawdata = self.rawdata
        i = 0
        n = len(rawdata)
        while i < n:
            if len(self.keyword) != 0:
                match = self.interesting.search(rawdata, i) # < or &
            else:
                match = re.compile('[&<#]').search(rawdata, i)
            if match:
                j = match.start()
#                if match.group() == '\n' and self.lineflag == 0:
#                    self.linepos = j
#                    self.lineflag = 1
            else:
                if self.cdata_elem:
                    break
                j = n
            if i < j:
                #print rawdata[i:j]
                self.handle_data(rawdata[i:j],i,j)
            i = self.updatepos(i, j)
            if i == n: break
            startswith = rawdata.startswith
            if startswith('<', i):
                if oskStringTag.match(rawdata, i):
                    k=self.parse_oskString(i)
                elif scriptTagOpen.match(rawdata, i):
                    k = self.parse_scripttag(i)
                elif starttagopen.match(rawdata, i): # < + letter
                    k = self.parse_starttag(i)
                elif startswith("</", i):
                    k = self.parse_endtag(i)
                elif startswith("<!--", i):
                    k = self.parse_comment(i)
                elif startswith("<?", i):
                    k = self.parse_pi(i)
                elif startswith("<!", i):
                    k = self.parse_declaration(i)
                elif (i + 1) < n:
                    self.handle_data("<",0,0)
                    k = i + 1
                else:
                    break
                if k < 0:
                    print "FOUND UnCoupled Tag"
                    if not end:
                        break
                    k = rawdata.find('>', i + 1)
                    if k < 0:
                        k = rawdata.find('<', i + 1)
                        if k < 0:
                            k = i + 1
                    else:
                        k += 1
                    #print rawdata[i:k]
                    self.handle_data(rawdata[i:k],i,k)
                    #self.error("EOF in middle of construct")
                    #break
                i = self.updatepos(i, k)
            elif startswith("&#", i):
                match = charref.match(rawdata, i)
                if match:
                    name = match.group()[2:-1]
                    self.handle_charref(name)
                    k = match.end()
                    if not startswith(';', k-1):
                        k = k - 1
                    i = self.updatepos(i, k)
                    continue
                else:
                    break
            elif startswith('&', i):
                match = entityref.match(rawdata, i)
                if match:
                    name = match.group(1)
                    self.handle_entityref(name)
                    k = match.end()
                    if not startswith(';', k-1):
                        k = k - 1
                    i = self.updatepos(i, k)
                    continue
                match = incomplete.match(rawdata, i)
                if match:
                    # match.group() will contain at least 2 chars
                    if end and match.group() == rawdata[i:]:
                        self.error("EOF in middle of entity or char ref")
                    # incomplete
                    break
                elif (i + 1) < n:
                    # not the end of the buffer, and can't be confused
                    # with some other construct
                    #self.handle_data("&")
                    i = self.updatepos(i, i + 1)
                else:
                    break
            elif startswith('#', i):
                
                match = re.compile('(#if.*)|(#endif.*)|(#else.*)|()$').match(rawdata, i)
                #match = re.compile(r'#[i|e][a-z|A-Z|!|\(|\)]*\n').match(rawdata, i)
                if match:
                    #print rawdata[i:match.end()]
                    self.handle_oskString(rawdata[i:match.end()])
                    i = self.updatepos(i, match.end())
                    
                    continue
                else:
                    #print "no"
                    self.handle_oskString(rawdata[i])
                    i += 1
            else:
                assert 0, "interesting.search() lied"
        # end while
        #hubert if end and i < n:
        if end and i < n and not self.cdata_elem:
            self.handle_data(rawdata[i:n],i,n)
            i = self.updatepos(i, n)
        self.rawdata = rawdata[i:]

    # Internal -- parse processing instr, return end or -1 if not terminated
    def parse_pi(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i+2] == '<?', 'unexpected call to parse_pi()'
        match = piclose.search(rawdata, i+2) # >
        if not match:
            return -1
        j = match.start()
        self.handle_pi(rawdata[i+2: j])
        j = match.end()
        return j
    #Internal -- forcus on the osk special string,that is #ifdef, <VWS_XXX > .etc
    def parse_oskString(self, i):
        match = re.compile(oskStringTag).search(self.rawdata, i)
        if not match:    return -1
        j = match.end()
        self.handle_oskString(self.rawdata[i:j])
        return j
        
    #Internal -- forcuse on the processing about <script> xxx </script>
    def parse_scripttag(self, i):
        self.__starttag_text = None
        endpos = self.check_for_whole_start_tag(i)
        if endpos < 0:
            return endpos
        rawdata = self.rawdata
        match = re.compile("</script[\t ]*>", flags=re.IGNORECASE).search(rawdata, endpos) 
        if not match:
            return -1
        j = match.end()
        self.handle_script(rawdata[endpos:match.start()], endpos)
        return j
        
    # Internal -- handle starttag, return end or -1 if not terminated
    def parse_starttag(self, i):
        self.__starttag_text = None
        endpos = self.check_for_whole_start_tag(i)
        if endpos < 0:
            return endpos
        rawdata = self.rawdata
        self.__starttag_text = rawdata[i:endpos]
        #print self.__starttag_text
        # Now parse the data between i+1 and j into a tag and attrs
        #attrs = []
        attrs = {}
        match = tagfind.match(rawdata, i+1)
        assert match, 'unexpected call to parse_starttag()'
        k = match.end()
        #hubert self.lasttag = tag = rawdata[i+1:k].lower()
        self.lasttag = tag = match.group(1).lower()
#attrfind = re.compile(
#    r'((?<=[\'"\s/])[^\s/>][^\s/=>]*)(\s*=+\s*'
#    r'(\'[^\']*\'|"[^"]*"|(?![\'"])[^>\s]*))?(?:\s|/(?!>))*')
        tmpEnd = 0
        while k < endpos:
            if tmpEnd == 0:
                m = attrfind.match(rawdata, k) 
            else:
                m = attrfind.match(rawdata, k+1) # set k+1 to replace k, because <div <VWS_FUNC....
            if not m:
                break
            attrname, rest, attrvalue = m.group(1, 2, 3)
            tmpStart = m.start()
            
            if attrname == '<VWS_SCREEN' or attrname == '<VWS_FUNCTION':
                tmpEnd = rawdata[tmpStart:].find('>')
                attrvalue = rawdata[tmpStart: tmpStart + tmpEnd + 1]
                k = tmpStart + tmpEnd + 1
                endpos = k + rawdata[k:].find('>') + 1
                #print '%d, %d, %s, %s' %(m.start(), tmpEnd, attrname, attrvalue)
            elif attrvalue == '<VWS_SCREEN' or attrvalue == '<VWS_FUNCTION':
                tmpEnd = rawdata[tmpStart:].find('>')
                attrvalue = rawdata[tmpStart: tmpStart + tmpEnd + 1]
                k = tmpStart + tmpEnd + 1
            else:
                if not rest:
                    attrvalue = None
                    k = m.end()
                elif attrvalue[:1] == '\'' == attrvalue[-1:] or \
                    attrvalue[:1] == '"' == attrvalue[-1:]:
                    attrvalue = attrvalue[1:-1]
                    k = m.end()
                if attrvalue:
                    attrvalue = self.unescape(attrvalue)
                    k = m.end()
            #attrs.append((attrname.lower(), attrvalue))
            attrs[attrname.lower()] = attrvalue
            
        if tmpEnd != 0:
            self.vwsInput = 1
            endpos = k + rawdata[k:].find('>') + 1
        end = rawdata[k:endpos].strip()
        if end not in (">", "/>"):
            lineno, offset = self.getpos()
            if "\n" in self.__starttag_text:
                lineno = lineno + self.__starttag_text.count("\n")
                offset = len(self.__starttag_text) \
                         - self.__starttag_text.rfind("\n")
            else:
                offset = offset + len(self.__starttag_text)
                self.handle_data(rawdata[i:endpos],i,endpos)
                return endpos
            #hubert self.error("junk characters in start tag: %r"
            #           % (rawdata[k:endpos][:20],))
        if end.endswith('/>'):
            # XHTML-style empty tag: <span attr="value" />
            #print "$end"
            self.handle_startendtag(tag, attrs)
        else:
            self.handle_starttag(tag, attrs,i)
            if tag in self.CDATA_CONTENT_ELEMENTS:
                self.set_cdata_mode(tag)#hubert
        return endpos

    # Internal -- check to see if we have a complete starttag; return end
    # or -1 if incomplete.
    def check_for_whole_start_tag(self, i):
        rawdata = self.rawdata
        m = locatestarttagend.match(rawdata, i)
        if m:
            j = m.end()
            next = rawdata[j:j+1]
            if next == ">":
                return j + 1
            if next == "/":
                if rawdata.startswith("/>", j):
                    return j + 2
                if rawdata.startswith("/", j):
                    # buffer boundary
                    return -1
                # else bogus input
                self.updatepos(i, j + 1)
                self.error("malformed empty start tag")
            if next == "":
                # end of input
                return -1
            if next in ("abcdefghijklmnopqrstuvwxyz=/"
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
                # end of input in or before attribute value, or we have the
                # '/' from a '/>' ending
                return -1
            if j > i:
                return j
            else:
                return i + 1
            #self.updatepos(i, j)
            #hubert self.error("malformed start tag")
        raise AssertionError("we should not get here!")

    # Internal -- parse endtag, return end or -1 if incomplete
    def parse_endtag(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i+2] == "</", "unexpected call to parse_endtag"
        match = endendtag.search(rawdata, i+1) # >
        if not match:
            return -1
        j = match.end()
        if len(self.keyword) != 0:
            self.__starttag_text = rawdata[i:j]
        gtpos = match.end()
        match = endtagfind.match(rawdata, i) # </ + tag + >
        
        if not match:
            if self.cdata_elem is not None:
                self.handle_data(rawdata[i:gtpos],i, gtpos)
                return gtpos
            # find the name: w3.org/TR/html5/tokenization.html#tag-name-state
            namematch = tagfind_tolerant.match(rawdata, i+2)
            if not namematch:
                # w3.org/TR/html5/tokenization.html#end-tag-open-state
                if rawdata[i:i+3] == '</>':
                    return i+3
                else:
                    return self.parse_bogus_comment(i)
            tagname = namematch.group().lower()
            # consume and ignore other stuff between the name and the >
            # Note: this is not 100% correct, since we might have things like
            # </tag attr=">">, but looking for > after tha name should cover
            # most of the cases and is much simpler
            gtpos = rawdata.find('>', namematch.end())
            self.handle_endtag(tagname)
            return gtpos+1
            #hubert self.error("bad end tag: %r" % (rawdata[i:j],))
        elem = match.group(1).lower() # script or style
        if self.cdata_elem is not None:
            if elem != self.cdata_elem:
                #self.handle_data(rawdata[i:gtpos])
                return gtpos
        #tag = match.group(1)
        #self.handle_endtag(tag.lower())
        self.handle_endtag(elem)
        self.clear_cdata_mode()
        return gtpos

    # Overridable -- finish processing of start+end tag: <tag.../>
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs, 0)
        #self.handle_endtag(tag)
    def handle_script(self, scriptStr):
        pass
    # Overridable -- handle start tag
    def handle_starttag(self, tag, attrs):
        pass
    def handle_otherString(self, spos, epos):
        pass
    # Overridable -- handle end tag
    def handle_endtag(self, tag):
        pass
    def handle_oskString(self, data):
        pass
    # Overridable -- handle character reference
    def handle_charref(self, name):
        pass

    # Overridable -- handle entity reference
    def handle_entityref(self, name):
        pass

    # Overridable -- handle data
    def handle_data(self, data,s,e):
        pass

    # Overridable -- handle comment
    def handle_comment(self, data):
        pass

    # Overridable -- handle declaration
    def handle_decl(self, decl):
        pass

    # Overridable -- handle processing instruction
    def handle_pi(self, data):
        pass

    def unknown_decl(self, data):
        pass
        #self.error("unknown declaration: %r" % (data,))

    # Internal -- helper to remove special character quoting
    entitydefs = None
    def unescape(self, s):
        if '&' not in s:
            return s
        def replaceEntities(s):
            s = s.groups()[0]
            try:
                if s[0] == "#":
                    s = s[1:]
                    if s[0] in ['x','X']:
                        c = int(s[1:], 16)
                    else:
                        c = int(s)
                    return unichr(c)
            except ValueError:
                return '&#'+s+';'
            else:
                # Cannot use name2codepoint directly, because HTMLParser supports apos,
                # which is not part of HTML 4
                import htmlentitydefs
                if HTMLParser.entitydefs is None:
                    entitydefs = HTMLParser.entitydefs = {'apos':u"'"}
                    for k, v in htmlentitydefs.name2codepoint.iteritems():
                        entitydefs[k] = unichr(v)
                try:
                    return self.entitydefs[s]
                except KeyError:
                    return '&'+s+';'

        return re.sub(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));", replaceEntities, s)
  
class MyParser(HTMLParser):
    def __init__(self, outf='', offsetf=''):
        HTMLParser.__init__(self)
        self.keyWordList = {'':[]}
        self.output=outf
        self.offsethtm = offsetf
        self.langPos = 0
        self.totalLang = 0
        self.sepdelim = '@#$'
        self.count = 0
        #print outf
        self.tmpfile = open(outf.name + ".offset", "wb");
    def writeToFile(self, content):
        self.tmpfile.write(content)
    def writeToKeyWordList(self, what):
        
        linend = self.linepos + self.rawdata[self.linepos+1:].find('\n')
        self.keyWordList[what] = [self.rawdata[self.linepos+1:linend].strip(), '']
        
        #print "--%s" %(self.rawdata[self.linepos+1:linend].strip())
        #self.keyWordList.append([self.rawdata[self.linepos+1:linend], what])
    def handle_endtag(self,tag):
        if len(self.keyword) != 0:
            #print "xx%s" %(self.get_starttag_text())
            self.output.write(self.getStartText())
    def handle_otherString(self, spos, epos):
        self.output.write(self.rawdata[spos:epos])
    def handle_oskString(self, data):
        if len(self.keyword) != 0:
            self.output.write(data)
    def handle_decl(self, decl):
        """head"""
        HTMLParser.handle_decl(self, decl)
     #   print decl
    def handle_script(self, scriptStr, pos=1):
        js = JSParser()
        js.reset(scriptStr)
        if len(self.keyword) != 0 and pos != 0:
            self.output.write("<script>\n")
       
        while True:
            curr_token = js.get_next_token()
            #print curr_token
            token_pos  = curr_token[0]
            token_text = curr_token[1]
            token_type = curr_token[2]
            if(token_type == 'TK_EOF'):
                if len(self.keyword) != 0:
                    self.output.write(scriptStr[js.last_pos:token_pos])
                break
            if(token_type == 'TK_WORD_FUNCTION'):
                if len(self.keyword) == 0:
                    js.handleJsFunction()
                #print js.input[js.parser_pos:]
            elif(token_type == 'TK_SPEC_WORD'):
                match = js.spec_keyword_pattern.match(js.input[js.parser_pos:]) #re.compile(r'\(.*\)[ |\t|\n]*')
                if len(self.keyword) != 0:
                    #print match.group()
                    #print "not finished"
                    #print token_text
                    if match:
                        js.parser_pos += match.end()                    
                        if match.group() in self.keyword:
                            #self.offsethtm.write(match.group() + "@#$" + self.keyword[match.group()][self.langPos].encode('utf-8') + '\n')
                            #self.offsethtm.write(match.group() + "@#$" + self.keyword[match.group()][self.langPos] + '\n')
                            self.offsethtm.write(match.group())
                            langPos = 0
                            while langPos < self.totalLang:
                                self.offsethtm.write("@#$" + self.keyword[match.group()][langPos])
                                langPos += 1
                            self.offsethtm.write('\n')
                            self.output.write(scriptStr[js.last_pos:token_pos] + "@#$"+ str(self.count) + "@#$")
                    token_pos = js.parser_pos
                    self.count += 1
                else:
                    #self.keyWordList[token_text] = token_text
                    if match:
                        js.parser_pos += match.end()
                        self.tmpfile.write(match.group() + '\n')
                        token_pos = js.parser_pos
            elif(token_type == 'TK_STRING'):
                if re.match(r"[\'|\"][0-9|\t| ]*[\'|\"]", token_text):
                    if len(self.keyword) != 0:
                        self.output.write(token_text)
                else:
                    if len(self.keyword) != 0:
                        if token_text in self.keyword:
                            #print token_text
                            if len(self.keyword[token_text]) != 0 and self.keyword[token_text] != u'':
                                if self.keyword[token_text] == u'':
                                    print self.keyword[token_text]
                                #print type(self.keyword[token_text][0])
                                #print js.last_pos
                                #print scriptStr[js.last_pos:token_pos]
                                if len(self.keyword[token_text]) >= self.langPos+1:
                                    #self.output.write(self.keyword[token_text][self.langPos].encode('utf-8'))
                                    self.output.write("@#$"+ str(self.count) + "@#$")
                                    self.count += 1
                                    #print str(pos + js.last_pos) + '@#$' + str(len(token_text)) + '@#$' + self.keyword[token_text][self.langPos].encode('utf-8')
                                    #self.offsethtm.write(str(pos + js.last_pos) + '@#$' + str(len(token_text)) + '@#$' + self.keyword[token_text][self.langPos].encode('utf-8') + '\n')
                                    #self.offsethtm.write(token_text + "@#$" + self.keyword[token_text][self.langPos].encode('utf-8') + '\n')
                                    self.offsethtm.write(token_text)
                                    langPos = 0
                                    while langPos < self.totalLang:
                                        self.offsethtm.write("@#$" + self.keyword[token_text][langPos])
                                        langPos += 1
                                    self.offsethtm.write('\n')
                                        
                            else:
                                self.output.write(token_text)
                                #print token_text
                                #print self.keyword[token_text]
                        else:
                            self.output.write(scriptStr[js.last_pos:token_pos])
                    else:
                        linend = js.linepos + scriptStr[js.linepos+1:].find('\n')
                        
                        #print js.old_text
                        #print js.old_text[3]
                        if (js.last_text == '(' and js.old_text[0] in js.backlist) or (js.last_text in js.blackqoto) \
                        or (js.last_text == '=' and js.old_text[0] == 'display' and js.old_text[1] == '.' and js.old_text[2] == 'style'):
                            #print js.old_text
                            pass
                        else:
                            self.keyWordList[token_text] = [scriptStr[js.linepos:linend].strip(), '']
                            #self.tmpfile.write(scriptStr[js.linepos:linend].strip() + '\n')
                            self.tmpfile.write(token_text + '\n')
            else:
                if len(self.keyword) != 0:
                    self.output.write(scriptStr[js.last_pos:token_pos])
            i = 3
            while i > 0:
                js.old_type[i] = js.old_type[i-1]
                js.old_text[i] = js.old_text[i-1]
                i -= 1
            js.old_type[0] = js.last_type
            js.old_text[0] = js.last_text
            js.last_type = token_type
            js.last_text = token_text
            js.last_pos = token_pos
        if len(self.keyword) != 0 and pos != 0:
            self.output.write("</script>\n")    
    def handle_inputTag(self, attrs, pos):
        print attrs
        if 'type' in attrs:
            if attrs['type'].lower() == 'button' or attrs['type'].lower() == 'reset' or attrs['type'].lower() == 'submit':
                #print "+attrs:%s" %(attrs['value'])
                if len(self.keyword) != 0:
                    if attrs['value'] in self.keyword:
                        #print self.getStartText().replace(attrs['value'], self.keyword[attrs['value']][0])
                        if len(self.keyword[attrs['value']]) >= self.langPos+1:
                            if len(self.keyword[attrs['value']][self.langPos]) != 0 and self.keyword[attrs['value']][self.langPos] != u'':
                                #self.offsethtm.write(str(pos + self.getStartText().index(attrs['value'])) + '@#$' + str(len(attrs['value'])) + '@#$' + self.keyword[attrs['value']][self.langPos].encode('utf-8') + '\n')
                                #print str(pos + self.getStartText().index(attrs['value'])) + '@#$' + str(len(attrs['value'])) + '@#$' + self.keyword[attrs['value']][self.langPos].encode('utf-8')
                                #self.output.write(self.getStartText().replace(attrs['value'], self.keyword[attrs['value']][self.langPos].encode('utf-8')))
                                #self.output.write(self.keyword[attrs['value']][self.langPos].encode('utf-8'))
                                #self.offsethtm.write(attrs['value'] + '@#$' + self.keyword[attrs['value']][self.langPos].encode('utf-8') + '\n')
                                #self.offsethtm.write(attrs['value'] + '@#$' + self.keyword[attrs['value']][self.langPos] + '\n')
                                self.offsethtm.write(attrs['value'])
                                langPos = 0
                                while langPos < self.totalLang:
                                    self.offsethtm.write("@#$" + self.keyword[attrs['value']][langPos])
                                    langPos += 1
                                self.offsethtm.write('\n')
                                #self.output.write("@#$"+ str(self.count) + "@#$")
                                #self.output.write(self.getStartText().replace(attrs['value'], "@#$"+ str(self.count) + "@#$"))
                                self.output.write("<input ")
                                flag_close = 0
                                for item in attrs:
                                    if item == 'value':
                                        self.output.write(item + "=" + "\"@#$"+ str(self.count) + "@#$\" ")
                                    elif item == '<vws_screen' or item == '<vws_function':
                                        #print item
                                        flag_close = 1
                                        self.output.write('\n'  + attrs[item] + '\n')
                                    else:
                                        self.output.write(item + '=' + '"' + attrs[item] + '" ')
                                self.count += 1
                                if flag_close == 0:
                                    self.output.write(">")
                        else:
                            self.output.write(self.getStartText())
                            if self.vwsInput == 1:
                                self.output.write("\n>")
                                self.vwsInput = 0
                    else:
                        self.output.write(self.getStartText())
                        if self.vwsInput == 1:
                            self.output.write("\n>")
                            self.vwsInput = 0
                else:
                    self.tmpfile.write(attrs['value'].strip() + '\n')
                    self.writeToKeyWordList(attrs['value'].strip())
                    
            elif attrs['type'].lower() == 'text' and 'value' in attrs:
                if attrs['value'] == '' or re.match(r"[0-9]*", attrs['value']):
                    if len(self.keyword) != 0:
                        #print self.getStartText()
                        self.output.write(self.getStartText())
                        if self.vwsInput == 1:
                            self.output.write("\n>")
                            self.vwsInput = 0
                else:
                    if len(self.keyword) != 0:
                        if attrs['value'] in self.keyword:
                            if len(self.keyword[attrs['value']]) >= self.langPos+1:
                                if len(self.keyword[attrs['value']][self.langPos]) != 0 and self.keyword[attrs['value']][self.langPos] != u'':
                            #print self.getStartText().replace(attrs['value'], self.keyword[attrs['value']][0])
                                    #print str(pos + self.getStartText().index(attrs['value'])) + '@#$' + str(len(attrs['value'])) + '@#$' + self.keyword[attrs['value']][self.langPos].encode('utf-8')
                                    #self.offsethtm.write(str(pos + self.getStartText().index(attrs['value'])) + '@#$' + str(len(attrs['value'])) + '@#$' + self.keyword[attrs['value']][self.langPos].encode('utf-8') + '\n')
                                    #self.offsethtm.write(str(pos + self.getStartText().index(attrs['value'])) + '@#$' + str(len(attrs['value'])) + '@#$' + self.keyword[attrs['value']][self.langPos] + '\n')
                                    self.offsethtm.write(attrs['value'])
                                    langPos = 0
                                    while langPos < self.totalLang:
                                        self.offsethtm.write("@#$" + self.keyword[attrs['value']][langPos])
                                        langPos += 1
                                    self.offsethtm.write('\n')
                                    #self.output.write(self.getStartText().replace(attrs['value'], self.keyword[attrs['value']][self.langPos].encode('utf-8')))
                                    self.output.write(self.getStartText().replace(attrs['value'], self.keyword[attrs['value']][self.langPos]))
                                    
                        self.output.write(self.getStartText())
                        if self.vwsInput == 1:
                            self.output.write("\n>")
                            self.vwsInput = 0
                    else:
                        self.writeToKeyWordList(attrs['value'].strip())
                        self.tmpfile.write(attrs['value'].strip() + '\n')
                    #print "+attrs %s" %(attrs['value'])
            else:
                if len(self.keyword) != 0:
                    print self.getStartText()
                    print self.vwsInput
                    self.output.write(self.getStartText())
                    if self.vwsInput == 1:
                        self.output.write("\n>")
                        self.vwsInput = 0
        else:
            if len(self.keyword) != 0:
                self.output.write(self.getStartText())
                if self.vwsInput == 1:
                    self.output.write("\n>")
                    self.vwsInput = 0
    def handle_starttag(self, tag, attrs, pos):
        """start_tag"""
        
        if tag.lower() == 'input':
            self.handle_inputTag(attrs, pos)
        else:
            #print "++%s" %(tag)
            if len(self.keyword) != 0:
                self.output.write(self.get_starttag_text())
        if not HTMLParser.get_starttag_text(self).endswith("/>"):
            pass
        
    def handle_data(self, data,s,e):
        """content"""
        HTMLParser.handle_data(self, data,s,e)
        #print "+%s" %(data)
        if re.match(r'^(\n|\r|\t| )*$',data) or re.match(r'^[\d|\.|-]*$' ,data):
            if len(self.keyword) != 0:
                self.output.write(data)
        elif self.lasttag == "style":
            if len(self.keyword) != 0:
                self.output.write(data)
        else:
            
            tmpData = ' '.join(re.split(r'\s+', data)).strip()
            #tmpData = data.replace("\n", "").strip()
            print tmpData
            if tmpData in blackList:
                if len(self.keyword) != 0:
                    self.output.write(data)
                #print tmpData
            elif len(tmpData) > 1:
                if len(self.keyword) != 0:
                    if tmpData in self.keyword:
                        #print tmpData
                        #if len(self.keyword[tmpData]) != 0 and len(self.keyword[tmpData][self.langPos]) != 0:
                            if len(self.keyword[tmpData]) >= self.langPos+1:
                                #print type(self.keyword[tmpData][0])
                                if len(self.keyword[tmpData][self.langPos]) != 0 and self.keyword[tmpData][self.langPos] != '':
                                    #self.output.write(self.keyword[tmpData][self.langPos].encode('utf-8'))
                                    self.output.write("@#$"+ str(self.count) + "@#$")
                                    self.count += 1
                                    #self.offsethtm.write(str(s)+'@#$'+str(e-s) + '@#$' + self.keyword[tmpData][self.langPos].encode('utf-8') + '\n')
                                    #self.offsethtm.write(tmpData + '@#$' + self.keyword[tmpData][self.langPos].encode('utf-8') + '\n')
                                    #self.offsethtm.write(tmpData + '@#$' + self.keyword[tmpData][self.langPos] + '\n')
                                    self.offsethtm.write(tmpData)
                                    langPos = 0
                                    while langPos < self.totalLang:
                                        self.offsethtm.write("@#$" + self.keyword[tmpData][langPos])
                                        langPos += 1
                                    self.offsethtm.write('\n')
                                    #print str(s)+'@#$'+str(e-s) + '@#$' + self.keyword[tmpData][self.langPos].encode('utf-8')
                            else:
                                self.output.write(data)
                    else:
                        self.output.write(data)
                else:
                    self.tmpfile.write(' '.join(re.split(r'\s+', tmpData)) + '\n')
                    self.writeToKeyWordList(' '.join(re.split(r'\s+', tmpData)))
                    #self.writeToKeyWordList(' '.join(re.split(r'\s+', tmpData)).decode('utf8', 'ignore'))
                #print "+data:%s" %(tmpData)
            else:
                if len(self.keyword) != 0:
                    self.output.write(data)

    def handle_startendtag(self, tag, attrs):
        """self-closure"""
        HTMLParser.handle_startendtag(self, tag, attrs)
        #print "++%s" %(HTMLParser.get_starttag_text(self))
         
    def handle_comment(self, data):
        """comment"""
        HTMLParser.handle_comment(self, data)
        if len(self.keyword) != 0:
            self.output.write('<!--' + data + '-->')
    def close(self):
        HTMLParser.close(self)
        print "parser over"        
if __name__ == "__main__":
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
    except:
        print "Usage: autoTrans e/d xxx.htm"
        print "e: key_info map that should be translated"
        print "d: reading the translated key_info map, then generalize new language html"
        sys.exit()
    if cmp(arg1, "e") == 0:
        try:
            print sys.argv[2]
            srcHtm = open(sys.argv[2], 'r')
            srcHtmContent = srcHtm.read()
            if srcHtmContent[:3] == codecs.BOM_UTF8:
                srcHtmContent = srcHtmContent[3:]
            htmH = MyParser(srcHtm)
            if sys.argv[2].split('.')[-1] == 'js':
                htmH.handle_script(srcHtmContent)
            else:
                htmH.feed(srcHtmContent)
        except IOError, e:
            print e
            sys.exit()
    elif cmp(arg1, "d") == 0:
        arg2=sys.argv[2]
        arg3=sys.argv[3]
        try:
            configf = ConfigParser.ConfigParser()
            configf.read("htmTool.config")
            #keywdName = configf.get("global", "keywdpath") + arg3 + '.keyword'
            keywdName = configf.get("global", "keywdpath") + arg3 + '.offset'
            srcHtmName = configf.get("global", "srchtmpath") + arg3
            print srcHtmName
            Lang_list = configf.get("global", "multilang").split(',')
            
            mask = configf.get("global", "maskDir")
            if not os.path.exists(arg2):
                os.makedirs(arg2)  
            srcHtm = open(srcHtmName, 'r')
            newhtm = open(arg2 + '/' + arg3, "wb")
            #print "keywd = %s, srcHtm = %s newhtm = %s" %(keywdName, srcHtmName, newhtm.name())
            if arg3.split('.')[-1] != 'js' and arg3.split('.')[-1] != 'htm' and arg3.split('.')[-1] != 'html':
                newhtm.write(srcHtm.read())
                newhtm.close()
                sys.exit(0)
            if os.path.isfile(keywdName):
                keywdf = open(keywdName, 'r')
                offsethtm = open(arg2 + '/' + arg3 + '.offset', "wb")
            else:
                newhtm.write(srcHtm.read())
                newhtm.close()
                sys.exit(0)
            ## real generate new htmls              
            
        except IOError, e:
            print e
            sys.exit()
#        except:
#            print "language??"
#            print "e.g. autoTrans d ch xxx.htm"
#            sys.exit()
        htmH = MyParser(newhtm, offsethtm)
        htmH.totalLang = len(Lang_list)
        print "+:%d\n" %(htmH.totalLang)
        detectUtfBOM = keywdf.read(3)
        if detectUtfBOM[:3] != codecs.BOM_UTF8:
            keywdf.seek(0)
            print "without BOM"
            #keywdf.seek(3) # utf-8 specified[BOM field]
        for line in keywdf:
            #print line
            #l = unicode(line.replace('\n',''), 'utf8').split(htmH.sepdelim)
            l = line.replace('\n','').split(htmH.sepdelim)
            i = 1
            while i < len(l):
                l[i] = l[i].strip()
                if htmH.keyword.has_key(l[0]):
                    htmH.keyword[l[0]].append(l[i])
                else:
                    if l[i] != '':
                        htmH.keyword[l[0]] = [l[i]]
                i += 1 
        if len(htmH.keyword) == 0:
            newhtm.write(srcHtm.read())
        else:
            if arg3.split('.')[-1] == 'js':
                htmH.handle_script(srcHtm.read(), 0)
            else:
                htmH.feed(srcHtm.read())
        keywdf.close()
        srcHtm.close()
    else:
        print "Usage: autoTrans e/d xxx.htm"
        print "e: key_info map that should be translated"
        print "d: reading the translated key_info map, then generalize new language html"
        
