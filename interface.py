import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import pytesseract
import pyttsx3
from PIL import Image
import threading
import time
import platform

class LeitorTelaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("A3 - Leitor de Tela")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        
        # Configurar Tesseract
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        
        # Estado do leitor
        self.leitor_ativo = False
        self.thread_leitura = None
        self.engine = None  # TTS engine compartilhado
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid para centralizar
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Configuração Inicial", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame para os botões - centralizado
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Botão Ligar
        self.ligar_btn = ttk.Button(button_frame, 
                                   text="Ligar Leitor de Tela",
                                   command=self.ligar_leitor,
                                   state="normal")
        self.ligar_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Botão Desligar
        self.desligar_btn = ttk.Button(button_frame, 
                                      text="Desligar Leitor de Tela",
                                      command=self.desligar_leitor,
                                      state="disabled")
        self.desligar_btn.grid(row=0, column=1)
        
        # Label de status
        self.status_label = ttk.Label(main_frame, text="Leitor desligado", 
                                     foreground="gray")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        # Label de informação
        info_label = ttk.Label(main_frame, 
                              text="O leitor captura e lê o texto da tela a cada 5 segundos",
                              font=("Arial", 9),
                              foreground="gray")
        info_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))
    
    def get_smart_region(self):
        """Calcula região inteligente evitando navbar e elementos do topo"""
        largura, altura = pyautogui.size()
        
        # Detectar altura da taskbar do Windows
        taskbar_height = 60  # Padrão
        try:
            if platform.system() == "Windows":
                import ctypes
                full_h = ctypes.windll.user32.GetSystemMetrics(1)  # SM_CYSCREEN
                work_h = ctypes.windll.user32.GetSystemMetrics(17)  # SM_CYFULLSCREEN
                taskbar_height = max(full_h - work_h, 40)
        except:
            pass
        
        # Área típica de navegador/apps (header, navbar, tabs)
        top_offset = int(altura * 0.15)  # 15% do topo (navbar, tabs, etc)
        bottom_offset = taskbar_height + 20  # taskbar + margem
        side_margin = int(largura * 0.08)  # 8% das laterais (sidebars)
        
        # Região final focada no conteúdo
        x = side_margin
        y = top_offset
        w = largura - (2 * side_margin)
        h = altura - top_offset - bottom_offset
        
        return (x, y, w, h)
    
    def inicializar_engine(self):
        """Cria um novo engine TTS completamente limpo"""
        try:
            # Criar novo engine
            engine = pyttsx3.init()
            
            # Configurar velocidade e volume (opcional)
            engine.setProperty('rate', 150)  # Velocidade da fala
            engine.setProperty('volume', 0.9)  # Volume (0.0 a 1.0)
            
            return engine
        except Exception as e:
            print(f"Erro ao inicializar engine TTS: {e}")
            return None
        
    def ligar_leitor(self):
        self.leitor_ativo = True
        self.ligar_btn.config(state="disabled")
        self.desligar_btn.config(state="normal")
        self.status_label.config(text="🔊 Leitor ligado - Monitorando tela...", 
                                foreground="green")
        
        # Limpar completamente o engine anterior
        if self.engine:
            try:
                self.engine.stop()
                del self.engine
            except:
                pass
        
        # Criar um engine completamente novo
        self.engine = self.inicializar_engine()
        
        # Verificar se já existe uma thread ativa e criar uma nova sempre
        if self.thread_leitura and self.thread_leitura.is_alive():
            # Se por algum motivo ainda há uma thread ativa, aguardar um pouco
            self.leitor_ativo = False
            time.sleep(0.1)
            self.leitor_ativo = True
        
        # Sempre criar uma nova thread
        self.thread_leitura = threading.Thread(target=self.loop_leitura)
        self.thread_leitura.daemon = True
        self.thread_leitura.start()
        
        print("Thread iniciada!")  # Debug
        
    def desligar_leitor(self):
        self.leitor_ativo = False
        
        # Parar qualquer fala em andamento
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
        
        self.ligar_btn.config(state="normal")
        self.desligar_btn.config(state="disabled")
        self.status_label.config(text="🔇 Leitor desligado", 
                                foreground="gray")
        
        print("Leitor desligado!")  # Debug
        
    def loop_leitura(self):
        print("Loop de leitura iniciado!")  # Debug
        while self.leitor_ativo:
            try:
                print("Executando leitura...")  # Debug
                self.executar_leitura()
                # Aguarda 5 segundos antes da próxima leitura
                for _ in range(50):  # 50 x 0.1s = 5s
                    if not self.leitor_ativo:
                        print("Saindo do loop - leitor desativado")  # Debug
                        break
                    time.sleep(0.1)
                    
            except Exception as e:
                print(f"Erro no loop: {e}")  # Debug
                self.root.after(0, self.mostrar_erro, str(e))
                break
        
        print("Loop de leitura finalizado!")  # Debug
                
    def executar_leitura(self):
        if not self.leitor_ativo:
            return
            
        try:
            # Usar região inteligente ao invés da região fixa
            regiao_x, regiao_y, regiao_largura, regiao_altura = self.get_smart_region()
            
            print(f"Região inteligente: x={regiao_x}, y={regiao_y}, w={regiao_largura}, h={regiao_altura}")
            
            # Captura tela
            imagem = pyautogui.screenshot(region=(regiao_x, regiao_y, regiao_largura, regiao_altura))
            imagem.save("tela_capturada.png")
            
            # OCR
            imagem = Image.open("tela_capturada.png")
            texto = pytesseract.image_to_string(imagem)
            
            print(f"Texto capturado: '{texto[:50]}...'")  # Debug
            
            # Text-to-speech apenas se há texto e o leitor ainda está ativo
            if texto.strip() and self.leitor_ativo and self.engine:
                try:
                    print("Tentando falar texto...")  # Debug
                    self.engine.say(texto)
                    self.engine.runAndWait()
                    print("Texto falado com sucesso!")  # Debug
                except Exception as e:
                    print(f"Erro TTS: {e}")
                    # Se der erro na fala, criar um engine completamente novo
                    try:
                        print("Recriando engine TTS...")
                        del self.engine
                        self.engine = self.inicializar_engine()
                        if self.engine:
                            self.engine.say(texto)
                            self.engine.runAndWait()
                            print("Texto falado após recriar engine!")
                    except Exception as e2:
                        print(f"Erro ao recriar engine: {e2}")
                
        except Exception as e:
            print(f"Erro na execução: {e}")  # Debug
            if self.leitor_ativo:
                self.root.after(0, self.mostrar_erro, str(e))
            
    def mostrar_erro(self, erro):
        self.leitor_ativo = False
        
        # Parar qualquer fala em andamento
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
                
        self.ligar_btn.config(state="normal")
        self.desligar_btn.config(state="disabled")
        self.status_label.config(text="❌ Erro - Leitor desligado", foreground="red")
        messagebox.showerror("Erro", f"Erro: {erro}")

def main():
    root = tk.Tk()
    app = LeitorTelaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()