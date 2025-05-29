# Importa módulos essenciais do Python e bibliotecas externas
import sys  # Para acessar argumentos e funções do sistema operacional
import os   # Para trabalhar com caminhos e arquivos do sistema

# Importa classes e widgets do PyQt5 usados para criar a interface gráfica
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox, QSizePolicy, QScrollArea, QDialog
)
from PyQt5.QtGui import QPixmap, QImage  # Para manipular imagens exibidas na interface
from PyQt5.QtCore import Qt              # Fornece constantes como alinhamentos e modos de janela

from rembg import remove  # Importa a função 'remove' do pacote rembg, que tira o fundo das imagens


# Define uma classe para a janela de visualização ampliada da imagem
class JanelaImagemAmpliada(QDialog):
    def __init__(self, pixmap, titulo):
        super().__init__()  # Inicializa a classe base QDialog
        self.setWindowTitle(titulo)  # Define o título da janela
        self.setWindowModality(Qt.ApplicationModal)  # Torna a janela modal (bloqueia a principal até fechar)
        self.resize(900, 700)  # Define o tamanho da janela
        self.setStyleSheet("background-color: #114b5f;")  # Define a cor de fundo da janela

        layout = QVBoxLayout(self)  # Layout vertical principal da janela

        scroll = QScrollArea(self)  # Adiciona uma área de rolagem para suportar imagens grandes
        scroll.setWidgetResizable(True)  # Permite que o conteúdo se ajuste ao tamanho da área
        scroll.setStyleSheet("background-color: #E3FCF9; border: none;")  # Estilo da área de rolagem
        layout.addWidget(scroll)  # Adiciona o scroll ao layout principal

        conteudo = QWidget()  # Widget interno que vai conter a imagem
        scroll.setWidget(conteudo)  # Define esse widget como o conteúdo do scroll

        imagem_layout = QVBoxLayout(conteudo)  # Layout vertical dentro do conteúdo
        imagem_layout.setAlignment(Qt.AlignCenter)  # Centraliza a imagem

        label = QLabel()  # Rótulo para exibir a imagem
        label.setPixmap(pixmap)  # Define o pixmap passado como argumento
        label.setAlignment(Qt.AlignCenter)  # Centraliza a imagem no rótulo
        imagem_layout.addWidget(label)  # Adiciona o rótulo ao layout


# Define a janela principal da aplicação
class RemovedorDeFundo(QWidget):
    def __init__(self):
        super().__init__()  # Inicializa a classe base QWidget
        self.setWindowTitle("ImageClear - Removedor de Fundo")  # Título da janela

        # Define cores usadas na interface
        cor_fundo = "#114b5f"
        cor_botao = "#1A946F"
        cor_hover = "#88D398"
        cor_painel = "#E3FCF9"
        cor_texto = "#ffffff"

        # Aplica o estilo visual (CSS) aos componentes da interface
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {cor_fundo};
                color: {cor_texto};
                font-family: 'Segoe UI';
                font-size: 15px;
            }}
            QLabel#Titulo {{
                font-size: 28px;
                font-weight: bold;
                color: {cor_painel};
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
            QPushButton {{
                background-color: {cor_botao};
                color: white;
                border-radius: 10px;
                padding: 12px;
                font-weight: 600;
                font-size: 15px;
                min-width: 220px;
                min-height: 42px;
            }}
            QPushButton:hover {{
                background-color: {cor_hover};
                color: #114b5f;
            }}
            QLabel {{
                padding: 0px;
                background-color: {cor_painel};
                color: #000000;
                border-radius: 0px;
            }}
            QLabel#Status {{
                color: #dddddd;
                font-size: 16px;
                font-style: italic;
                qproperty-alignment: 'AlignCenter';
                min-width: 220px;
                background-color: transparent;
            }}
            QLabel.Legenda {{
                background-color: {cor_botao};
                color: white;
                border-radius: 10px;
                font-weight: 500;
                font-size: 14px;
                padding: 6px 0px;
                min-width: 280px;
                max-width: 280px;
                qproperty-alignment: 'AlignCenter';
                margin-top: 0px;
            }}
        """)

        # Variáveis para guardar o caminho da imagem original e bytes da imagem sem fundo
        self.caminho_imagem = None
        self.imagem_sem_fundo_bytes = None

        layout_principal = QVBoxLayout()  # Layout vertical principal
        self.setLayout(layout_principal)  # Aplica esse layout ao widget principal

        # Cria e configura o rótulo com os nomes dos criadores no canto superior esquerdo
        criadores_label = QLabel("Criadores:\nEuderlenia Albino dos Santos\nKaio Robson dos Santos Silva\nMaykon Viera Barbosa")
        criadores_label.setStyleSheet("color: #E3FCF9; font-size: 11px; background-color: transparent;")
        criadores_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout_principal.addWidget(criadores_label, alignment=Qt.AlignLeft)

        # Título centralizado do aplicativo
        self.label_titulo = QLabel("Removedor de Fundo de Imagem - ImageClear")
        self.label_titulo.setObjectName("Titulo")
        self.label_titulo.setAlignment(Qt.AlignCenter)

        # Layout horizontal com botões principais
        botoes_topo_layout = QHBoxLayout()
        self.botao_selecionar = QPushButton("Selecionar Imagem")
        self.botao_remover = QPushButton("Remover Fundo")

        # Garante que os botões cresçam horizontalmente conforme o espaço
        for botao in [self.botao_selecionar, self.botao_remover]:
            botao.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Adiciona os botões ao layout com espaçamento e centralização
        botoes_topo_layout.addStretch()
        botoes_topo_layout.addWidget(self.botao_selecionar)
        botoes_topo_layout.addSpacing(40)
        botoes_topo_layout.addWidget(self.botao_remover)
        botoes_topo_layout.addStretch()

        # Conecta os botões às respectivas funções
        self.botao_selecionar.clicked.connect(self.selecionar_imagem)
        self.botao_remover.clicked.connect(self.remover_fundo)

        # Adiciona o título e os botões ao layout principal com espaçamentos
        layout_principal.addSpacing(10)
        layout_principal.addWidget(self.label_titulo)
        layout_principal.addSpacing(15)
        layout_principal.addLayout(botoes_topo_layout)
        layout_principal.addSpacing(40)

        # Layout para exibir as imagens (original e sem fundo) lado a lado
        imagens_layout = QHBoxLayout()
        imagens_layout.setSpacing(60)
        imagens_layout.setAlignment(Qt.AlignCenter)

        # Tamanho padrão para exibição das imagens
        largura_quadrado = 280
        altura_quadrado = 280

        # Coluna para a imagem original
        coluna_original = QVBoxLayout()
        coluna_original.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        coluna_original.setContentsMargins(0, 0, 0, 0)
        coluna_original.setSpacing(0)

        self.label_imagem_original = QLabel()
        self.label_imagem_original.setFixedSize(largura_quadrado, altura_quadrado)
        self.label_imagem_original.setAlignment(Qt.AlignCenter)
        self.label_imagem_original.setStyleSheet(f"background-color: {cor_painel}; border: 1px solid #ccc;")
        self.label_imagem_original.mousePressEvent = self.abrir_imagem_original  # Ao clicar, exibe em outra janela

        self.legenda_original = QLabel("Imagem Original")
        self.legenda_original.setObjectName("Legenda")
        self.legenda_original.setProperty("class", "Legenda")
        self.legenda_original.setAlignment(Qt.AlignCenter)
        self.legenda_original.setFixedWidth(largura_quadrado)
        self.legenda_original.setContentsMargins(0, 0, 0, 0)

        coluna_original.addWidget(self.label_imagem_original)
        coluna_original.addSpacing(20)
        coluna_original.addWidget(self.legenda_original)

        # Coluna para a imagem sem fundo
        coluna_sem_fundo = QVBoxLayout()
        coluna_sem_fundo.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        coluna_sem_fundo.setContentsMargins(0, 0, 0, 0)
        coluna_sem_fundo.setSpacing(0)

        self.label_imagem_sem_fundo = QLabel()
        self.label_imagem_sem_fundo.setFixedSize(largura_quadrado, altura_quadrado)
        self.label_imagem_sem_fundo.setAlignment(Qt.AlignCenter)
        self.label_imagem_sem_fundo.setStyleSheet(f"background-color: {cor_painel}; border: 1px solid #ccc;")
        self.label_imagem_sem_fundo.mousePressEvent = self.abrir_imagem_sem_fundo  # Ao clicar, exibe em outra janela

        self.legenda_sem_fundo = QLabel("Imagem sem Fundo")
        self.legenda_sem_fundo.setObjectName("Legenda")
        self.legenda_sem_fundo.setProperty("class", "Legenda")
        self.legenda_sem_fundo.setAlignment(Qt.AlignCenter)
        self.legenda_sem_fundo.setFixedWidth(largura_quadrado)
        self.legenda_sem_fundo.setContentsMargins(0, 0, 0, 0)

        coluna_sem_fundo.addWidget(self.label_imagem_sem_fundo)
        coluna_sem_fundo.addSpacing(20)
        coluna_sem_fundo.addWidget(self.legenda_sem_fundo)

        # Status exibido entre as imagens
        self.label_status = QLabel("Nenhuma imagem selecionada.")
        self.label_status.setObjectName("Status")
        self.label_status.setAlignment(Qt.AlignCenter)
        self.label_status.setFixedWidth(220)
        self.label_status.setStyleSheet("background-color: transparent;")

        status_vlayout = QVBoxLayout()
        status_vlayout.addStretch()
        status_vlayout.addWidget(self.label_status)
        status_vlayout.addStretch()

        # Adiciona as três colunas ao layout horizontal de imagens
        imagens_layout.addLayout(coluna_original)
        imagens_layout.addLayout(status_vlayout)
        imagens_layout.addLayout(coluna_sem_fundo)

        layout_principal.addLayout(imagens_layout)

        # Botão para salvar a imagem sem fundo (inicialmente oculto)
        self.botao_salvar = QPushButton("Salvar Imagem")
        self.botao_salvar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.botao_salvar.clicked.connect(self.salvar_imagem)
        self.botao_salvar.setVisible(False)

        salvar_layout = QHBoxLayout()
        salvar_layout.addStretch()
        salvar_layout.addWidget(self.botao_salvar)
        salvar_layout.addStretch()

        layout_principal.addSpacing(30)
        layout_principal.addLayout(salvar_layout)
        layout_principal.addStretch()

    # Abre a imagem original em uma nova janela ao ser clicada
    def abrir_imagem_original(self, event):
        if self.label_imagem_original.pixmap():
            self.abrir_em_janela_ampliada(self.label_imagem_original.pixmap(), "Imagem Original")

    # Abre a imagem sem fundo em uma nova janela ao ser clicada
    def abrir_imagem_sem_fundo(self, event):
        if self.label_imagem_sem_fundo.pixmap():
            self.abrir_em_janela_ampliada(self.label_imagem_sem_fundo.pixmap(), "Imagem sem Fundo")

    # Função que cria e exibe uma nova janela com a imagem ampliada
    def abrir_em_janela_ampliada(self, pixmap, titulo):
        janela = JanelaImagemAmpliada(pixmap, titulo)
        janela.exec_()

    # Função que permite ao usuário escolher uma imagem do computador
    def selecionar_imagem(self):
        caminho, _ = QFileDialog.getOpenFileName(
            self, "Escolher imagem", "", "Imagens (*.png *.jpg *.jpeg *.webp)"
        )
        if caminho:
            self.caminho_imagem = caminho
            pixmap = QPixmap(caminho).scaled(
                self.label_imagem_original.width(), self.label_imagem_original.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.label_imagem_original.setPixmap(pixmap)
            self.label_status.setText("Imagem selecionada.")
            self.label_imagem_sem_fundo.clear()
            self.botao_salvar.setVisible(False)
            self.imagem_sem_fundo_bytes = None

    # Função que remove o fundo da imagem usando a biblioteca rembg
    def remover_fundo(self):
        if not self.caminho_imagem:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem selecionada.")
            return

        self.label_status.setText("Imagem sendo gerada...")
        QApplication.processEvents()

        try:
            with open(self.caminho_imagem, 'rb') as f:
                imagem_original = f.read()

            imagem_sem_fundo = remove(imagem_original)
            self.imagem_sem_fundo_bytes = imagem_sem_fundo

            imagem = QImage.fromData(imagem_sem_fundo)
            pixmap = QPixmap.fromImage(imagem).scaled(
                self.label_imagem_sem_fundo.width(), self.label_imagem_sem_fundo.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.label_imagem_sem_fundo.setPixmap(pixmap)

            self.label_status.setText("Imagem gerada com sucesso!")
            self.botao_salvar.setVisible(True)

        except Exception as e:
            self.label_status.setText("Erro ao gerar imagem.")
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro:\n{str(e)}")

    # Função para salvar a imagem sem fundo em um local escolhido pelo usuário
    def salvar_imagem(self):
        if not self.imagem_sem_fundo_bytes:
            QMessageBox.warning(self, "Salvar Imagem", "Nenhuma imagem para salvar. Gere a imagem primeiro.")
            return

        nome_base = "imagem"
        if self.caminho_imagem:
            nome_arquivo = os.path.basename(self.caminho_imagem)
            nome_base = os.path.splitext(nome_arquivo)[0]

        sugestao_nome = f"{nome_base}_editado.png"

        caminho, _ = QFileDialog.getSaveFileName(
            self, "Salvar imagem", sugestao_nome, "PNG (*.png)"
        )
        if caminho:
            try:
                with open(caminho, 'wb') as f:
                    f.write(self.imagem_sem_fundo_bytes)
                self.label_status.setText("Imagem salva com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro ao salvar", f"Erro ao salvar imagem:\n{str(e)}")


# Ponto de entrada da aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Cria a aplicação Qt
    janela = RemovedorDeFundo()   # Cria uma instância da janela principal
    janela.showMaximized()        # Exibe a janela em tela cheia
    sys.exit(app.exec_())         # Executa o loop principal do Qt até o usuário fechar
