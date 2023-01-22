import mistune
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

def detect_tag(markdown_content:str) -> list[str]:
    """

    :param makrdown_content: Le contenu d'une note markdown
    :return: La liste des tags/étiquettes de la note
    """
    first_line = markdown_content.split('\n')[0]
    if '@' in first_line:
        return first_line.split('@')[1::]

def mermaid_html(code_mermaid):
    return "<pre class='mermaid'>"+code_mermaid+"</pre>"

def reponse_html(block_reponse):
    html="<form>"
    id_reponse=0
    liste_reponse=block_reponse.split('\n')
    for reponse in liste_reponse:
        if reponse!='':
            if reponse[0]=='+':
                text_reponse=reponse.split('+ ')[1] 
                html+="<input type='checkbox' name='trueAnswer_"+str(id_reponse)+"' id='"+str(id_reponse)+"'/><label for='"+str(id_reponse)+"'>"+text_reponse+"</label>"
            else:
                html+="<input type='checkbox' id='"+str(id_reponse)+"'/><label for='"+str(id_reponse)+"'>"+reponse+"</label>"
            id_reponse+=1
    html+="</form>"
    return html

def mise_en_forme_code(info, code):
    lexer = get_lexer_by_name(info, stripall=True)
    formatter = html.HtmlFormatter()
    return highlight(code, lexer, formatter)
    
class particularBlock_renderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        if (info=="mermaid"):
            return mermaid_html(mistune.escape(code))
        elif(info=="reponses"):
            return reponse_html(mistune.escape(code))
        elif (info=="code"):
            return mise_en_forme_code('shell', code)
        elif(info):
            return mise_en_forme_code(info, code)
        else:
            return mistune.html(code)

def sans_tag(markdown):
    text_sansTag=markdown
    if text_sansTag!='':
        if text_sansTag[0]=='@':
            text_sansTag=re.sub("(@(.)*)*\n", "", text_sansTag,count=1)
    return text_sansTag
    #previousSibling
   #{% extends 'base.html' %} 


particular_markdown=mistune.create_markdown(renderer=particularBlock_renderer())