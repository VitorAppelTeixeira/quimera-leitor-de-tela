# A3-LeitorDeTela

#  OCR Reader com Voz (Python)

Este é um script em Python que **captura a tela**, **extrai o texto visível** usando OCR (Reconhecimento Óptico de Caracteres) e **lê o texto em voz alta** usando uma engine de voz.

---

##  Funcionalidades

- Captura automaticamente uma screenshot da tela inteira.
- Usa o Tesseract OCR para extrair qualquer texto visível.
- Converte o texto em fala com `pyttsx3`.
- Ideal para testes simples de leitura de tela com Python.

---

## Requisitos

Antes de rodar o script, você precisa ter:

- **Python 3.x**
- **Tesseract OCR instalado**
- As bibliotecas Python:
  - `pyautogui`
  - `pytesseract`
  - `pyttsx3`
  - `Pillow`

---

##  Instalação

1. **Instale o Tesseract**  
   Baixe e instale a versão para Windows:  
   https://github.com/UB-Mannheim/tesseract/wiki

   Durante a instalação, copie o caminho (geralmente:  
   `C:\Program Files\Tesseract-OCR\tesseract.exe`).

2. **Instale as bibliotecas no terminal**:

```bash
pip install pyautogui pytesseract pyttsx3 pillow

#Como usar
#Abra o conteúdo que deseja capturar (como uma página da web).

#Execute o script.

#O programa irá:
#Tirar um print da tela.
#Detectar o texto na imagem.
#Exibir e falar o conteúdo em voz alta.


# Melhorias futuras (sugestões)
# Permitir capturar apenas uma área específica da tela.

# Adicionar delay antes da captura.

# Suporte a múltiplos idiomas.

# Interface gráfica (GUI).


