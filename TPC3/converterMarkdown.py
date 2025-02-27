import re

def converterHeader(linha):
    match = re.match(r'^(#{1,6})\s*(.*)$', linha)
    if match:
        return f"<h{len(match.group(1))}>{match.group(2)}</h{len(match.group(1))}>"
    return linha

def converterItalico(linha):
    match = re.match(r'^\*(.*)\*$', linha)
    if match:
        return f"<i>{match.group(1)}</i>"
    return linha

def converterBold(linha):
    match = re.match(r'^\*\*(.*)\*\*$', linha)
    if match:
        return f"<b>{match.group(1)}</b>"
    return linha

def converterLink(linha):
    match = re.match(r'^(.*)\[([^\]]+)\]\(([^\)]+)\)$', linha)
    if match:
        antes, texto, link = match.groups()
        return f'{antes}<a href="{link}">{texto}</a>'
    return linha

def converterImagem(linha):
    match = re.match(r'!\[([^\]]+)\]\(([^\)]+)\)$', linha)
    if match:
        texto, link = match.groups()
        return f'Como se vê na imagem seguinte: <img src="{link}" alt="{texto}">'
    return linha

def converterListaOrdenada(linha):
    def list_replacer(match):
        items = match.group('items').strip().split("\n")
        items_html = "\n".join(f"<li>{item[3:]}</li>" for item in items)
        return f"<ol>\n{items_html}\n</ol>"

    linha = re.sub(r'(?P<items>(?:^\d+\..*\n?)+)', list_replacer, linha, flags=re.MULTILINE)

    return linha

def main():
    linha_markdown = "###### Exemplo de Cabeçalho"
    output_header = converterHeader(linha_markdown)

    linha_markdownItalico = "*Exemplo de texto em itálico*"
    output_italico = converterItalico(linha_markdownItalico)

    linha_markdownBold = "**Exemplo de texto em negrito**"
    output_bold = converterBold(linha_markdownBold)

    linha_markdownLink = "Como pode ser consultado em [página da UC](http://www.uc.pt)"
    output_link = converterLink(linha_markdownLink)

    linha_markdownImagem = "![imagem dum coelho](http://www.coellho.com)"
    output_imagem = converterImagem(linha_markdownImagem)

    listaNumerada = """1. Primeiro item
2. Segundo item
3. Terceiro item"""
    output_numerada = converterListaOrdenada(listaNumerada)

    with open("output.txt", "w") as output:
        output.write("Resultados:\n\n")
        output.write("Conversão de Header:\n")
        output.write(f"Input: {linha_markdown}\nOutput: {output_header}\n")
        output.write("-----------------------------\n\n")
        output.write("Conversão de Itálico:\n")
        output.write(f"Input: {linha_markdownItalico}\nOutput: {output_italico}\n")
        output.write("-----------------------------\n\n")
        output.write("Conversão de Bold:\n")
        output.write(f"Input: {linha_markdownBold}\nOutput: {output_bold}\n")
        output.write("-----------------------------\n\n")
        output.write("Conversão de Link:\n")
        output.write(f"Input: {linha_markdownLink}\nOutput: {output_link}\n")
        output.write("-----------------------------\n\n")
        output.write("Conversão de Imagem:\n")
        output.write(f"Input: {linha_markdownImagem}\nOutput: {output_imagem}\n")
        output.write("-----------------------------\n\n")
        output.write("Conversão de Lista:\n")
        output.write(f"Input: {listaNumerada}\n\nOutput: {output_numerada}\n")

if __name__ == "__main__":
    main()