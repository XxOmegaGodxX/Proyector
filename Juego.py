import random

import pygame
import pgzrun
from pgzero.actor import Actor
from pgzero.constants import mouse
from pgzero.keyboard import keyboard
from pgzero.screen import Screen

WIDTH = 600
HEIGHT = 450

TITLE = "Viaje al espacio"
FPS = 30

# Objetos y varaibles
ship = Actor("ship1", (300, 400))
space = Actor("space")
enemies = []
planets = [Actor("plan1", (random.randint(0, 600), -100)), Actor("plan2", (random.randint(0, 600), -100)), Actor("plan3", (random.randint(0, 600), -100))]
meteors = []
bullets = []
mode = 'menu'
type1 = Actor("ship1", (100, 200))
type2 = Actor("ship2", (300, 200))
type3 = Actor("ship3", (500, 200))
count = 0

def fill():
    # Elaborando la lista de enemigos
    for i in range(5):
        x = random.randint(0, 600)
        y = random.randint(-450, -50)
        enemy = Actor("enemy", (x, y))
        enemy.speed = random.randint(2, 8)
        enemies.append(enemy)
        
    # Elaborando la lista de meteoritos
    for i in range(5):
        x = random.randint(0, 600)
        y = random.randint(-450, -50)
        meteor = Actor("meteor", (x, y))
        meteor.speed = random.randint(2, 10)
        meteors.append(meteor)
fill()


def get_screen():
    return Screen(pygame.display.get_surface())


# Elaboración
def draw():
    screen = get_screen()

    # Pantalla del menú de inicio
    if mode == 'menu':
        space.draw()
        screen.draw.text('Choose the ship', center=(300, 100), color="white", fontsize=36)
        type1.draw()
        type2.draw()
        type3.draw()
    # Modo de juego
    if mode == 'game':
        space.draw()
        planets[0].draw()
        # Atraer a los meteoritos
        for i in range(len(meteors)):
            meteors[i].draw()
        ship.draw()
        # Atraer a los enemigos
        for i in range(len(enemies)):
            enemies[i].draw()
        # Dibujo de proyectiles hacia arriba
        for i in range(len(bullets)):
            bullets[i].draw()
        screen.draw.text(str(count), (10, 10), color="white")
    # Ventana de finalización del juego
    elif mode == 'end':
        space.draw()
        screen.draw.text("GAME OVER!", center=(300, 200), color="white", fontsize=36)
        screen.draw.text(str(count), center=(300, 250), color="white", fontsize=64)

# Controles
def on_mouse_move(pos):
    ship.pos = pos

# Añadiendo nuevos enemigos a la lista
def new_enemy():
    x = random.randint(0, 400)
    y = -50
    enemy = Actor("enemy", (x, y))
    enemy.speed = random.randint(2, 8)
    enemies.append(enemy)

# Movimiento del enemigo
def enemy_ship():
    for i in range(len(enemies)):
        if enemies[i].y < 650:
            enemies[i].y = enemies[i].y + enemies[i].speed
        else:
            enemies.pop(i)
            new_enemy()

# Movimiento del planeta
def planet():
    if planets[0].y < 550:
            planets[0].y = planets[0].y + 1
    else:
        planets[0].y = -100
        planets[0].x = random.randint(0, 600)
        first = planets.pop(0)
        planets.append(first)

# Movimiento del meteorito
def meteorites():
    for i in range(len(meteors)):
        if meteors[i].y < 450:
            meteors[i].y = meteors[i].y + meteors[i].speed
        else:
            meteors[i].x = random.randint(0, 600)
            meteors[i].y = -20
            meteors[i].speed = random.randint(2, 10)

# Colisiones
def collisions():
    global mode
    global count
    for i in range(len(enemies)):
        if ship.colliderect(enemies[i]):
            mode = 'end'
        # Projectile collisions
        for j in range(len(bullets)):
            if bullets[j].colliderect(enemies[i]):
                count = count + 1
                enemies.pop(i)
                bullets.pop(j)
                new_enemy()
                break

def update(dt):
    global count, mode, enemies, planets, meteors, bullets
    if mode == 'game':
        enemy_ship()
        collisions()
        planet()
        meteorites()
        # Movimiento del proyectil
        for i in range(len(bullets)):
            if bullets[i].y < 0:
                bullets.pop(i)
                break
            else:
                bullets[i].y -= 10
    elif mode == 'end' and keyboard.space:
        mode = 'menu'
        count = 0
        enemies = []
        planets = [Actor("plan1", (random.randint(0, 600), -100)), Actor("plan2", (random.randint(0, 600), -100)), Actor("plan3", (random.randint(0, 600), -100))]
        meteors = []
        bullets = []
        fill()
        
def on_mouse_down(button, pos):
    global mode, ship
    if mode == 'menu' and type1.collidepoint(pos):
        ship.image = "ship1"
        mode = 'game'
    elif mode == 'menu' and type2.collidepoint(pos):
        ship.image = "ship2"
        mode = 'game'
    elif mode == 'menu' and type3.collidepoint(pos):
        ship.image = "ship3"
        mode = 'game'
    # Disparos   
    elif mode == 'game' and button == mouse.LEFT:
        bullet = Actor("missiles")
        bullet.pos = ship.pos
        bullets.append(bullet)
pgzrun.go()