import tkinter as tk
import tkinter.font as font
from tkinter import messagebox # Para las ventanas de ganar/perder

tablero = [
    [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]
]

soluciones = [] 

# --- LÓGICA DE BACKTRACKING (Tus funciones originales) ---
def marcar(x,y):
    for i in range(x+1,8):
        if tablero[i][y] == 0: tablero[i][y]=x+1
    xt,yt = x, y
    while(True):
        xt+=1; yt+=1
        if(xt>7 or yt>7): break
        if tablero[xt][yt] == 0: tablero[xt][yt]= x+1
    xt,yt = x, y
    while(True):
        xt+=1; yt-=1
        if(xt>7 or yt<0): break
        if tablero[xt][yt] == 0: tablero[xt][yt]= x+1

def desmarcar_uno(x,y):
    for i in range(x+1,8):
        if tablero[i][y] == x+1: tablero[i][y]=0
    xt,yt = x, y
    while(True):
        xt+=1; yt+=1
        if(xt>7 or yt>7): break
        if tablero[xt][yt] == x+1: tablero[xt][yt]= 0
    xt,yt = x, y
    while(True):
        xt+=1; yt-=1
        if(xt>7 or yt<0): break
        if tablero[xt][yt] == x+1: tablero[xt][yt]= 0

def guardar_solucion():
    s = ""
    for r in range(8):
        fila_str = ""
        for c in range(8):
            if tablero[r][c] == r + 1:
                fila_str += "♕"
            else:
                if (r + c) % 2 == 0:
                    fila_str += "◻"
                else:
                    fila_str += "■"
        s += fila_str + "\n"
    soluciones.append(s)

def solucion(fila):
    if fila == 8:
        guardar_solucion()
        return
    for i in range(8):
        if tablero[fila][i] == 0:
            tablero[fila][i] = fila+1
            marcar(fila,i)
            solucion(fila+1)
            desmarcar_uno(fila,i)
            tablero[fila][i] = 0

solucion(0) # Generar soluciones al inicio

# --- CONFIGURACIÓN PRINCIPAL DE LA VENTANA ---
ventana = tk.Tk()
ventana.title("Problema de las 8 Reinas")
ventana.geometry("500x650")
ventana.configure(bg="#2b2b2b")

fuente_tablero = font.Font(family="Courier", size=32)
fuente_botones = font.Font(family="Helvetica", size=12, weight="bold")
fuente_juego = font.Font(family="Courier", size=18, weight="bold")

# Creamos dos contenedores (Frames) para cambiar entre ventanas
frame_explorador = tk.Frame(ventana, bg="#2b2b2b")
frame_juego = tk.Frame(ventana, bg="#2b2b2b")

# ==========================================================
# ================= LÓGICA DEL MINIJUEGO ===================
# ==========================================================

tiempo_restante = 90
timer_id = None
reinas_colocadas = [] # Guardará las posiciones (fila, columna)
botones_tablero_juego = [[None]*8 for _ in range(8)]

def iniciar_juego():
    # Ocultar explorador y mostrar juego
    frame_explorador.pack_forget()
    frame_juego.pack(fill="both", expand=True)
    reiniciar_juego()

def salir_juego():
    global timer_id
    if timer_id:
        ventana.after_cancel(timer_id)
    # Ocultar juego y mostrar explorador
    frame_juego.pack_forget()
    frame_explorador.pack(fill="both", expand=True)

def reiniciar_juego():
    global tiempo_restante, reinas_colocadas, timer_id
    if timer_id:
        ventana.after_cancel(timer_id)
    
    tiempo_restante = 90
    reinas_colocadas.clear()
    
    # Limpiar el tablero visualmente
    for r in range(8):
        for c in range(8):
            color = "white" if (r + c) % 2 == 0 else "gray"
            botones_tablero_juego[r][c].config(text="", bg=color, state="normal")
            
    actualizar_timer()

def actualizar_timer():
    global tiempo_restante, timer_id
    if tiempo_restante <= 0:
        lbl_tiempo.config(text="¡Tiempo agotado!")
        bloquear_tablero()
        messagebox.showinfo("Fin del juego", "¡Se acabó el tiempo! No lograste colocar las 8 reinas.")
        return
    
    mins = tiempo_restante // 60
    segs = tiempo_restante % 60
    lbl_tiempo.config(text=f"Tiempo: {mins}:{segs:02d}")
    tiempo_restante -= 1
    timer_id = ventana.after(1000, actualizar_timer)

def bloquear_tablero():
    for r in range(8):
        for c in range(8):
            botones_tablero_juego[r][c].config(state="disabled")

def es_movimiento_valido(fila, col):
    # Revisa si la casilla interactúa (choca) con alguna reina ya puesta
    for r, c in reinas_colocadas:
        # Misma fila, misma columna, o misma diagonal
        if r == fila or c == col or abs(r - fila) == abs(c - col):
            return False
    return True

def click_casilla(r, c):
    # Si ya hay una reina ahí, la quitamos (por si el jugador se arrepiente)
    if (r, c) in reinas_colocadas:
        reinas_colocadas.remove((r, c))
        botones_tablero_juego[r][c].config(text="")
        return

    # Si intentamos poner una y choca con otra
    if not es_movimiento_valido(r, c):
        btn = botones_tablero_juego[r][c]
        color_original = btn.cget("bg")
        btn.config(bg="red") # Parpadea en rojo
        ventana.after(400, lambda: btn.config(bg=color_original)) # Regresa a su color a los 400ms
        return

    # Si es válido y no nos hemos pasado de 8 reinas
    if len(reinas_colocadas) < 8:
        reinas_colocadas.append((r, c))
        # Puedes cambiar el color de la reina aquí con fg=
        botones_tablero_juego[r][c].config(text="♕", fg="black")

        # Si colocó las 8 ganamos
        if len(reinas_colocadas) == 8:
            if timer_id:
                ventana.after_cancel(timer_id)
            lbl_tiempo.config(text="¡Victoria!")
            bloquear_tablero()
            messagebox.showinfo("¡Felicidades!", "¡Lograste colocar las 8 reinas a tiempo!")

# ==========================================================
# ============== INTERFAZ: MODO EXPLORADOR =================
# ==========================================================
indice_actual = 0

def actualizar_pantalla():
    lbl_tablero.config(text=soluciones[indice_actual])
    lbl_contador.config(text=f"Solución {indice_actual + 1} de {len(soluciones)}")

def siguiente():
    global indice_actual
    if indice_actual < len(soluciones) - 1:
        indice_actual += 1; actualizar_pantalla()

def anterior():
    global indice_actual
    if indice_actual > 0:
        indice_actual -= 1; actualizar_pantalla()

lbl_contador = tk.Label(frame_explorador, text="", font=fuente_botones, bg="#2b2b2b", fg="white")
lbl_contador.pack(pady=10)

lbl_tablero = tk.Label(frame_explorador, text="", font=fuente_tablero, bg="#2b2b2b", fg="#4bcffa", justify="center")
lbl_tablero.pack(pady=10)

frame_botones_exp = tk.Frame(frame_explorador, bg="#2b2b2b")
frame_botones_exp.pack(pady=10)

btn_anterior = tk.Button(frame_botones_exp, text="< Anterior", font=fuente_botones, command=anterior, fg="blue", width=10)
btn_anterior.grid(row=0, column=0, padx=10)

btn_siguiente = tk.Button(frame_botones_exp, text="Siguiente >", font=fuente_botones, command=siguiente, fg="blue", width=10)
btn_siguiente.grid(row=0, column=1, padx=10)

# ¡NUEVO BOTÓN PARA JUGAR!
btn_jugar = tk.Button(frame_explorador, text="¡Jugar Mini-juego!", font=fuente_botones, command=iniciar_juego, fg="red", width=20)
btn_jugar.pack(pady=20)

actualizar_pantalla()
frame_explorador.pack(fill="both", expand=True) # Mostrar explorador al iniciar

# ==========================================================
# ================= INTERFAZ: MODO JUEGO ===================
# ==========================================================
lbl_titulo_juego = tk.Label(frame_juego, text="Coloca las 8 Reinas", font=fuente_botones, bg="#2b2b2b", fg="white")
lbl_titulo_juego.pack(pady=10)

lbl_tiempo = tk.Label(frame_juego, text="Tiempo: 1:30", font=fuente_botones, bg="#2b2b2b", fg="yellow")
lbl_tiempo.pack(pady=5)

# Frame central para guardar los 64 botones como un tablero
frame_grilla = tk.Frame(frame_juego, bg="black", bd=2)
frame_grilla.pack(pady=10)

# Crear la matriz de botones 8x8
for r in range(8):
    for c in range(8):
        color = "white" if (r + c) % 2 == 0 else "gray"
        # Usamos lambda fila=r, col=c para que cada botón recuerde sus coordenadas
        btn = tk.Button(frame_grilla, text="", font=fuente_juego, width=3, height=1, bg=color,
                        command=lambda fila=r, col=c: click_casilla(fila, col))
        btn.grid(row=r, column=c)
        botones_tablero_juego[r][c] = btn

frame_botones_juego = tk.Frame(frame_juego, bg="#2b2b2b")
frame_botones_juego.pack(pady=15)

btn_volver = tk.Button(frame_botones_juego, text="< Volver", font=fuente_botones, command=salir_juego, fg="blue", width=10)
btn_volver.grid(row=0, column=0, padx=10)

btn_reiniciar = tk.Button(frame_botones_juego, text="Reintentar", font=fuente_botones, command=reiniciar_juego, fg="green", width=10)
btn_reiniciar.grid(row=0, column=1, padx=10)

ventana.mainloop()