import pyautogui
import pytesseract
from PIL import Image
import pyttsx3

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Pega resolução da tela
largura, altura = pyautogui.size()

# Define região central (tipo 60% da tela)
regiao_x = int(largura * 0.2)
regiao_y = int(altura * 0.2)
regiao_largura = int(largura * 0.6)
regiao_altura = int(altura * 0.6)

# Captura só o centro da tela
imagem = pyautogui.screenshot(region=(regiao_x, regiao_y, regiao_largura, regiao_altura))
imagem.save("tela_central.png")

# OCR
imagem = Image.open("tela_central.png")
texto = pytesseract.image_to_string(imagem)

# Mostra texto e fala
print("Texto capturado:")
print(texto)

if texto.strip() == "":
    print("⚠️ Nenhum texto detectado.")
else:
    print("✅ Texto detectado!")

engine = pyttsx3.init()
engine.say(texto)
engine.runAndWait()

input("Pressione Enter para sair...")