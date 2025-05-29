![KAIO](https://github.com/user-attachments/assets/e34d6ad4-3e01-458a-84e5-0259ee7e097d)


https://github.com/user-attachments/assets/69d6e018-a4e7-47ac-ab10-33069baa8f17

# 🖼️ Removedor de Fundo de Imagens

Este projeto é uma ferramenta simples para remover o fundo de imagens automaticamente, utilizando inteligência artificial. Ideal para gerar imagens com fundo transparente de forma rápida e precisa.

## 🚀 Funcionalidades

- Remoção automática do fundo de imagens (`.jpg`, `.png`, etc.)
- Suporte a múltiplos formatos de imagem
- Interface gráfica com PyQt5 (opcional)
- Geração de imagens com fundo transparente (`.png`)

## 🧠 Tecnologias Usadas

- [Python 3.11](https://www.python.org/)
- [rembg](https://github.com/danielgatis/rembg) – Remoção de fundo com IA
- [onnxruntime](https://onnxruntime.ai/) – Execução dos modelos IA
- [PyQt5](https://pypi.org/project/PyQt5/) – Interface gráfica (se aplicável)

## 📦 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio

## (Opcional) Crie um ambiente virtual:

python -m venv venv
venv\Scripts\activate

## Instale as dependências:
pip install -r requirements.txt

## ▶️ Como Usar
## Modo script (linha de comando):

python app.py caminho/para/imagem.jpg

