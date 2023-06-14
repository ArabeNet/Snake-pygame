import pygame
import sys


pygame.init()

# Definir la pantalla
screen = pygame.display.set_mode((800, 600))

# Un reloj para mantener nocion del tiempo que se ocupara mas abajo en el bucle
clock = pygame.time.Clock()

#Aqui se genera la serpiente
snake = [pygame.Rect(400, 300, 20, 20)]
color = (255, 255, 255)

#La comida
comida = pygame.Rect(200, 200, 20, 20)
comida_color = (255, 0, 0)

# La direccion inicial y velocidad de la serpiente
direction = "right"
speed = 20

# Puntajesss
puntaje = 0
font = pygame.font.SysFont("Arial", 32)

# Leer el record .txt y en caso de no tenerlo crear uno
with open("record.txt", "r") as file:
    try:
        record = int(file.read())
    except ValueError:
        record = 0

# las listas de rectángulos que representen los muros y un color para ellos
muros = [pygame.Rect(0, 0, 800, 20), pygame.Rect(0, 580, 800, 20), pygame.Rect(0, 0, 20, 600), pygame.Rect(780, 0, 20, 600)]
muro_color = (128, 128, 128)

# Crear más rectángulos que representen los obstáculos y agregarlos a la lista de los muros
obstáculos = [pygame.Rect(100, 100, 100, 20), pygame.Rect(300, 200, 20, 100), pygame.Rect(500, 300, 100, 20), pygame.Rect(700, 400, 20, 100)]
muros.extend(obstáculos)

# Cambiar el color de los obstáculos para que se diferencien de los bordes de la pantalla
obstáculo_color = (255, 255, 0)

# Crear un bucle de juego
while True:
    # Limitar el bucle a 10 fotogramas por segundo
    clock.tick(10)

    # Aca con el bucle
    for event in pygame.event.get():
        # Si el usuario cierra la ventana, se podra salir del bucle
        if event.type == pygame.QUIT:
            sys.exit()
        #Los eventos de cambio de direccion con las teclas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "down":
                direction = "up"
            if event.key == pygame.K_DOWN and direction != "up":
                direction = "down"
            if event.key == pygame.K_LEFT and direction != "right":
                direction = "left"
            if event.key == pygame.K_RIGHT and direction != "left":
                direction = "right"


    # La velocidad y dirreciones de las serpiente
    # Se añadira un rectangulo en la cabeza 
    cabeza = snake[0].copy()
    if direction == "up":
        cabeza.y -= speed
    if direction == "down":
        cabeza.y += speed
    if direction == "left":
        cabeza.x -= speed
    if direction == "right":
        cabeza.x += speed

    # El primer rectangulo de su cabeza
    snake.insert(0, cabeza)

    # Tercero, eliminar el ultimo rectangulo de la lista de la serpiente, a menos que haya comido la comida
    if cabeza.colliderect(comida):
        # Si la cabeza de la serpiente colisiona con la comida, se aumenta la cabeza y la comida va para otro lugar random de la pantalla
        puntaje += 1
        comida.x = (pygame.time.get_ticks() // speed) % (800 - speed)
        comida.y = (pygame.time.get_ticks() // speed * 2) % (600 - speed)
    else:
        # Si no colisiona con la comida, se elimina el ultimo rectangulo de la cabeza
        snake.pop()

    # Verificaciones extras para comprobar que no hizo la moricion
    if cabeza.x < 0 or cabeza.x >= 800 or cabeza.y < 0 or cabeza.y >= 600 or cabeza in snake[1:] or any(cabeza.colliderect(muro) for muro in muros):
        # Si alguna de estas condiciones se cumple, significa que el juego ha terminado y se debe mostrar un mensaje y salir del bucle
        print("Fin del juego. Tu puntaje es: " + str(puntaje))
        # Apartado para comparar los records si es mayor que el anterior en el .txt
        if puntaje > record:
            with open("record.txt", "w") as file:
                file.write(str(puntaje))
        break


    # Rellenar la pantalla de negro para el fondo
    screen.fill((0, 0, 0))

    # En esta parte se dibuja a la serpiente
    for rect in snake:
        pygame.draw.rect(screen, color, rect)

    # En esta parte se dibuja la comida
    pygame.draw.rect(screen, comida_color, comida)

    # En esta parte se dibujan los muros
    for muro in muros[:4]:
        pygame.draw.rect(screen, muro_color, muro)

    # En esta parte se dibujan los obstaculos en el mapa
    for obstáculo in muros[4:]:
        pygame.draw.rect(screen, obstáculo_color, obstáculo)

    # En esta parte se dibuja el puntaje y el record en la pantalla con un color blanco

    texto = font.render("Puntaje: " + str(puntaje), True, (255, 255, 255))
    screen.blit(texto, (10, 10))
    texto = font.render("Récord: " + str(record), True, (255, 255, 255))
    screen.blit(texto, (10, 50))

    # Actualizar la pantalla
    pygame.display.flip()