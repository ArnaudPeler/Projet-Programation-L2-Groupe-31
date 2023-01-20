import mistune
def detect_tag(markdown_content:str) -> list[str]:
    first_line = markdown_content.split('\n')[0]
    if '@' in first_line:
        return first_line.split('@')[1::]
    else:
        return []

def mermaid_html(code_mermaid):
    return "<pre class='mermaid'>"+code_mermaid+"</pre>"

def reponse_html(block_reponse):
    html="<form>"
    id_reponse=0
    liste_reponse=block_reponse.split('\n')
    for reponse in liste_reponse:
        if reponse!='':
            html+="<input type='checkbox' id='"+str(id_reponse)+"'/><label for='"+str(id_reponse)+"'>"+reponse+"</label>"
            id_reponse+=1
    html+="</form>"
    return html
    
class particularBlock_renderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        if (info=="mermaid"):
            return mermaid_html(mistune.escape(code))
        elif(info=="reponses"):
            return reponse_html(mistune.escape(code))
        elif(re.match("\$\$(.)*\$\$", code)):
            return "<span class='math>'"+code+"</span>"



partiuclar_markdown=mistune.create_markdown(renderer=particularBlock_renderer())