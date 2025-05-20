import pyautogui
import pytesseract
import pyttsx3
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


x, y, largura, altura = 100, 150, 1000, 600
imagem = pyautogui.screenshot(region=(x, y, largura, altura))
imagem.save("tela.png")


imagem = Image.open("tela.png")
texto = pytesseract.image_to_string(imagem)

print("Texto capturado:")
print(texto)


if texto.strip():
    print("Texto detectado!")
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()
else:
    print("Nenhum texto detectado.")

input("Pressione Enter para sair...")