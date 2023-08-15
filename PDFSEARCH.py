import sys
import os
import pytesseract
import fitz
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTextBrowser

# Classe que define a aplicação de busca em PDF
class AplicacaoBuscaPDF(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicializa a interface do usuário
        self.inicializar_interface()

    def inicializar_interface(self):
        # Configuração da janela principal
        self.setWindowTitle("Busca em PDF")
        self.setGeometry(100, 100, 600, 400)

        # Layout vertical para os widgets
        self.layout = QVBoxLayout()

        # Caixa de texto para inserção de texto de busca
        self.caixa_texto = QLineEdit(self)
        self.layout.addWidget(self.caixa_texto)

        # Botão para navegar e selecionar um arquivo PDF
        self.botao_navegar = QPushButton("Procurar um PDF", self)
        self.botao_navegar.clicked.connect(self.selecionar_pdf)
        self.layout.addWidget(self.botao_navegar)

        # Botão para iniciar a busca
        self.botao_buscar = QPushButton("Buscar", self)
        self.botao_buscar.clicked.connect(self.realizar_busca)
        self.layout.addWidget(self.botao_buscar)

        # Área de exibição de resultados
        self.exibicao_resultados = QTextBrowser(self)
        self.layout.addWidget(self.exibicao_resultados)

        # Configuração do widget central
        widget_central = QWidget(self)
        widget_central.setLayout(self.layout)
        self.setCentralWidget(widget_central)

        # Caminho do arquivo PDF selecionado
        self.caminho_arquivo_pdf = None
        self.doc = None

    def selecionar_pdf(self):
        opcoes = QFileDialog.Options()
        opcoes |= QFileDialog.ReadOnly

        # Diálogo para selecionar um arquivo PDF
        caminho_arquivo, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo PDF", "", "Arquivos PDF (*.pdf)", options=opcoes)

        if caminho_arquivo:
            self.caminho_arquivo_pdf = caminho_arquivo
            self.doc = fitz.open(self.caminho_arquivo_pdf)

    def realizar_busca(self):
        if not self.doc:
            return

        texto_a_buscar = self.caixa_texto.text()

        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\SEU_USUARIO\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

        resultados = []
        for num_pagina in range(self.doc.page_count):
            pagina = self.doc.load_page(num_pagina)
            imagem = pagina.get_pixmap()

            pil_imagem = Image.frombytes("RGB", [imagem.width, imagem.height], imagem.samples)

            # Utiliza o pytesseract diretamente no PDF
            texto_pagina = pytesseract.image_to_string(pil_imagem, lang='por')

            if texto_a_buscar.lower() in texto_pagina.lower():
                resultados.append(num_pagina + 1)

        if resultados:
            self.exibicao_resultados.clear()
            self.exibicao_resultados.append("Encontrado nas páginas: " + ", ".join(map(str, resultados)))
        else:
            self.exibicao_resultados.clear()
            self.exibicao_resultados.append("Texto não encontrado no PDF")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = AplicacaoBuscaPDF()
    janela.show()
    sys.exit(app.exec_())
