import re
import pdb
import sys

open_tag_expr = re.compile('<[\w]+[\s\w=["]*[\w\-]*["]*]*>')
open_tag_name_expr = re.compile('<[\w]+[\s\w=\w*["]*]*/>')
close_tag_expr = re.compile('</[\w]+>')

def read_tag_type(tag_str):
     i = 0
     n = len(tag_str)
     tag_type = ''
     while (i<n):
         if (tag_str[i]==' ' or tag_str[i]=='>'):
             break
         else:
            if (tag_str[i]!='<'):
                tag_type = tag_type + tag_str[i]
         i = i + 1
     return tag_type

def process_comment(str_w,pos,n):
     i = pos
     while (i<n):
         if (str_w[i]=='>' and str_w[i-1]=='-' and str_w[i-2]=='-'):
             break
         i = i+1
     return i

def process_table(str_w,pos,n):
    i = pos
    nbraces = 1
    while (i<n):
        if (i<(n-1) and str_w[i] == '{' and str_w[i+1] == '|'):
            nbraces = nbraces + 1
            i = i+1
        else:
            if (i<(n-1) and str_w[i] == '|' and str_w[i+1] == '}'):
                nbraces = nbraces - 1
                i = i+1
        if (nbraces == 0):
            break
        i = i+1
    return i

def process_braces(str_w,pos,n):
    i = pos
    nbraces = 1
    while (i<n):
        if (i<(n-1) and str_w[i] == '{' and str_w[i+1] == '{'):
            nbraces = nbraces + 1
            i = i+1
        else:
            if (i<(n-1) and str_w[i] == '}' and str_w[i+1] == '}'):
                nbraces = nbraces - 1
                i = i+1
        if (nbraces == 0):
            break
        i = i+1
    return i

def process_title(str_w,pos,n):
    i = pos
    title_str = ''
    while (i<n):
        
        if (i<n-1 and str_w[i]=='=' and str_w[i+1]=='='):
            i = i+1
            break
        title_str += str_w[i]
        i = i + 1
    return i,title_str


def process_tag(str_w,pos,n,open_tag):
    i = pos
    content_tag = ''
    queue_tag = []
    while (i<n):
        if (str_w[i] ==  '<'):
            close_tag = read_tag(str_w,i,n)
            if (close_tag_expr.match(close_tag)):
                #print("-> ",close_tag.encode('utf-8'))

                tag_type_str = ''
                close_tag_type = read_tag_type(close_tag)
                while (queue_tag != []):
                      tag_type_str = queue_tag.pop()
                      if (close_tag_type!=tag_type_str):
                           print("Warning:",tag_type_str.encode('utf-8')," not closed. ")
                      else:
                           break
 
                i = i + len(close_tag) - 1
                #se a tag fechou nao preciso do conteudo
                content_tag = ''
                break
            elif (close_tag.startswith('<!--')):
                i = process_comment(str_w,i,n)
            elif (open_tag_name_expr.match(close_tag)):
                #there is types of tags that dont close
                #because reference to an existing tag 
                #the iterator must go up to the end of close tag
                i = i + len(close_tag) - 1 
            else:
                if (open_tag_expr.match(close_tag)):
                    i = i + len(close_tag)
                    #print(">> ",close_tag.encode('utf-8'))
                    #<br> tag is not closed, therefore I just ignore it
                    if (close_tag != '<br>'):
                         queue_tag.append(read_tag_type(close_tag))
                else:
                    print("Warning: ",open_tag.encode('utf-8')," ",close_tag.encode('utf-8'))
        if (i<n):
             content_tag += str_w[i]
        i = i+1
    return i,content_tag

def read_tag(str_w,pos,n):
    i = pos
    tag_type = ''
    while (i<n and str_w[i]!='>'):
        tag_type += str_w[i]
        if (i<(n-2) and str_w[i+1]=='!' and str_w[i+2]=='-'):
             tag_type = '<!--'
             return tag_type
        i = i + 1
    if (i<n):
       tag_type += str_w[i]
    return tag_type

def process_wiki_str(str_w):
    new_str_w = ''
    i = 0
    n = len(str_w)
    while (i<n):

        #removing titles
        if (i<n-1 and str_w[i]=='=' and str_w[i+1] == '='):
             i = i+2
             i,title_str = process_title(str_w,i,n)
             if ("References" in title_str):
                  break
             elif ("Further reading" in title_str):
                  break
             elif ("External links" in title_str):
                  break
             elif ("See also" in title_str):
                  break
                
             
        #removing link to concepts/pages...
        if ( i<n-1  and str_w[i] == '[' and str_w[i+1]=='['):
             link_phrase = ''
             i = i+2
             while(i<n-1 and (str_w[i]!=']' or str_w[i+1]!=']')):
                if (str_w[i]=='|'):
                    link_phrase = ''
                else:
                    link_phrase +=str_w[i]
                i = i+1
             new_str_w += ' ' + link_phrase
             #pular na fita o caracter ]
             i = i+2

        if (i>=n):
            break

        #removing comments tags: <!-- ... -->
        #removing reference tags... <ref> ... </ref>
        tag_string = ''
        if (str_w[i] == '<' ):
             open_tag = read_tag(str_w,i,n)
             if (open_tag_expr.match(open_tag)):
                 i = i+len(open_tag)
                 if (open_tag!='<br>'):
                     i,tag_string = process_tag(str_w,i,n,open_tag)
                 tag_string = ''
             elif (open_tag_name_expr.match(open_tag)):
                 #there is types of tags that dont close
                 #because they reference to an existing tag 
                 i = i + len(open_tag) - 1
             elif (open_tag.startswith('<!--')):
                 i = process_comment(str_w,i,n)
             else:
                 new_str_w += tag_string
            
        if (i>=n):
            break
        if ( i<n-1  and str_w[i] == '{'):
             #removing braces
             if ( str_w[i+1] == '{'):
                   i = process_braces(str_w,i+2,n)
             elif ( str_w[i+1]=='|'):
                  #removing tables
                   i = process_table(str_w,i+2,n)
          
        if (i>=n):
            break
        #removing another caracthers
        if ('a' <= str_w[i] and str_w[i]<='z'):
             new_str_w +=str_w[i]
        elif ('A' <= str_w[i] and str_w[i]<='Z'):
             new_str_w +=str_w[i]
        elif ('0' <= str_w[i] and str_w[i]<='9'):
             new_str_w +=str_w[i]
        elif (str_w[i] == '\''):
             if (i<n-1 and str_w[i+1]!='\''):
                new_str_w +=str_w[i]
             else:
                i = i+1
        elif (str_w[i] == '-'):
             new_str_w +=str_w[i]
        elif (str_w[i] == ','):
             new_str_w +=str_w[i]
        elif (str_w[i] == '.'):
             new_str_w +=str_w[i]
        elif (str_w[i] == ' '):
             new_str_w +=str_w[i]
        i = i+1
    return new_str_w
