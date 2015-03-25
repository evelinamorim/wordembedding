import re
import pdb
import sys

open_tag_expr = re.compile('<[\w]+[\s\w=["]*\w*["]*]*>')
open_tag_name_expr = re.compile('<[\w]+[\s\w=\w*["]*]*/>')
close_tag_expr = re.compile('</[\w]+>')

def process_comment(str_w,pos,n):
     i = pos
     while (i<n):
         if (str_w[i]=='>' and str_w[i-1]=='-' and str_w[i-2]=='-'):
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
    while (i<pos):
        if (i<n-1 and str_w[i]=='=' and str_w[i+1]=='='):
            i = i+1
            break
        i = i + 1
    return i

def process_tag(str_w,pos,n,open_tag):
    i = pos
    content_tag = ''
    while (i<n):
        if (str_w[i] ==  '<'):
            close_tag = read_tag(str_w,i,n)
            if (close_tag_expr.match(close_tag)):
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
                    i,content_tag = process_tag(str_w,i,n,close_tag)
                else:
                    print("Warning: ",open_tag," ",close_tag)
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
             i = process_title(str_w,i,n)
             
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
        #removing braces
        if ( i<n-1  and str_w[i] == '{' and str_w[i+1]=='{'):
             i = process_braces(str_w,i+2,n)
          
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
