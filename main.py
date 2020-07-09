import pygame  # importuje modul pygame
import random  # importuje ten modul aby potem wygenerowac losowe miejsce dla enemy
import math  # importujemy ten modul aby obliczyc pierwiastek w funkcji kolizji
from pygame import mixer



# funkcja init() z pakietu pygame rozpoczyna program
pygame.init()
clock = pygame.time.Clock()

# Wynik
score = 0

font_url = "assets/font2.ttf"
font = pygame.font.Font(font_url, 33)
textX = 10
textY = 10
# tworzymy ekran gry za pomocą display i ustawiamy mu rozmiar w tupli
screen = pygame.display.set_mode((800, 600))  # [szerokość to x, wysokość to y]

# tworzymy tytuł/nazę gry
pygame.display.set_caption("Teenage Mutant Ninja Turtles _by:AM0k_(Lukasz Chalinski)")

# wgrywam ikonę gry

icon_url = "assets/logo.png"
icon = pygame.image.load(icon_url)  # ładujemy obraz do zmiennej
pygame.display.set_icon(icon)  # wgrywamy obraz do gry

# wgrywamy ikone i tworzymy ikonę gracza oraz jego wstępne parametry
playerImg_url = "assets/leonardo.png"
playerImg = pygame.image.load(playerImg_url)  # ładujemy obrazek do pamięci i zapisujem do zmiennej
playerX = 368  # nadajemy wspolrzedna x w jakiej bedzie mial sie pojawic ikona gracza
playerY = 500  # nadajemy wspolrzedna y w jakiej bedzie mial sie pojawic ikona gracza
speedX = 0  # ustalamy prędkość początkową gracza po osi x (poziomej)
speedY = 0
playerSpeedChange = 2

# wgrywamy ikonki i tworzymy przeciwników
enemyImg = []
enemyX = []
enemyY = []
enemy_speedX = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg_url = "assets/foot-clan.png"
    enemyImg.append(pygame.image.load(enemyImg_url))  # ładujemy obrazek do pamięci i zapisujem do listy
    enemyImg_url2 = "assets/shreder.png"
    enemyImg.append(pygame.image.load(enemyImg_url2))
    enemyX.append(random.randint(0, 736))  # nadajemy wspolrzedna x w jakiej bedzie mial sie pojawic ikona gracza
    enemyY.append(0)  # nadajemy wspolrzedna y w jakiej bedzie mial sie pojawic ikona gracza
    enemy_speedX.append(random.choice([-1, 1, -2, 2, 3, -3]))  # ustalamy prędkość początkową gracza po osi x (poziomej) i losuje czy w lewo czy w prawo

# wgrywamy ikone strzału i ją tworzymy
bulletImg_url = "assets/pizza.png"
bulletImg = pygame.image.load(bulletImg_url)
bulletX = -50
bulletY = -50
bulletYspeed = 4  # potrzebujemu tutaj tylko osi Y bo strzal bedzie sie poruszal po osi pionowej
bulletState = "ready"  # będzie przyjmować albo ready albo throw (czyli gotowa do rzutu lub rzucona)

# tworzymy funkcje koniec gry
over_font_url = "assets/font2.ttf"
over_font = pygame.font.Font(over_font_url, 80)
game_state = "play"  # stan gry play/over


def game_over():
    global game_state, num_of_enemies, enemyY
    for j in range(num_of_enemies):
        enemyY[j] = 2000
    game_state = "over"
    over_tekst = over_font.render("GAME OVER!", True, (0, 0, 0))
    screen.blit(over_tekst, (170, 220))


def new_game():
    global game_state, score, playerY, playerX
    game_state = "play"
    score = 0
    for i in range(num_of_enemies):
        gen_enemy(i)
    playerX = 368
    playerY = 500


# tworzymy obiekt playera ktory przyjmuje 2 argumenty ktore sa pozycja na ekranie
def player(x, y):
    screen.blit(playerImg, (x, y))  # blit oznacza "narysuj", jako argumenty przyjmuje adres obrazka i tuple z wspólrzednych


# tworzymy obiekt wroga
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# tworzymy obiekt strzalu pociskiem
def shot_bullet(x, y):
    global bulletState
    bulletState = "throw"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY, d):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < d:
        return True
    else:
        return False


def gen_enemy(i):
    global enemyX, enemyY, enemy_speedX
    enemyX[i] = random.randint(0, 736)
    enemyY[i] = 0
    enemy_speedX[i] = random.choice([-1, 1])


def show_score(x, y):
    score_text = font.render("W y n i k:  " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (x, y))


# dźwięk tła
music_url = "sounds/music.mp3"
mixer.music.load(music_url)
mixer.music.play(-1)  # puszczamy mp3 nieskonczona ilosc razy w loopie
mixer.music.set_volume(0.1)

# tworzymy pętle aby program działał nieprzerwanie
running = True  # można rozumieć jako "gra działa/jest uruchomiona"
throw_sound_url = "sounds/throw.wav"
death_sound_url2 = "sounds/death2.wav"  # smierc wroga
death_sound_url = "sounds/death.wav"
while running:  # dopóki gra jest uruchomiona
    screen.fill((232, 244, 208))  # nadajemy kolor dla tła

    for event in pygame.event.get():  # dla każdego wydarzenia które przyjmuje pygame
        if event.type == pygame.QUIT:  # jeśli to wydarzenie to naciśnięcie "x"
            running = False  # gra zosanie przerwana - okno zamknięte
        if game_state == "play":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if bulletState == "ready":
                        throw_sound = mixer.Sound(throw_sound_url)
                        throw_sound.play()
                        bulletY = playerY
                        bulletX = playerX
                        shot_bullet(bulletX, bulletY)
        if game_state == "over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    new_game()

    # ruch postaci z klawiatury
    keys = pygame.key.get_pressed()  # wszystkie klawisze  ktore są nacisniete w tym momencie
    speedX = 0
    speedY = 0
    if game_state == "play":
        if keys[pygame.K_LEFT]:  # jeśli strzałka w lewo jest wciśnięta to w lewo
            speedX = -playerSpeedChange
        elif keys[pygame.K_RIGHT]:
            speedX = playerSpeedChange

        if keys[pygame.K_UP]:  # jeśli strzałka w prawo jest wciśnięta to w prawo
            speedY = -playerSpeedChange
        elif keys[pygame.K_DOWN]:
            speedY = playerSpeedChange

    playerX += speedX  # tutaj inicjujemy poziomy ruch (po osi x)
    playerY += speedY  # tutaj inicjujemy ruch pionowy (po osi y)

    # 1tutaj nie pozwalamy przemieszczać się postaci za krawędź planszy w poziomie
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # tutaj nie pozwalamy przemieszczać się postaci za krawędź planszy w pionie
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # ruch przeciwnika
    # tutaj nie pozwalamy przemieszczać się wroga za krawędź planszy w poziomie
    # enemyY nie potrzebuje bo wrog przesuwa sie tylko w lewo i prawo
    for i in range(num_of_enemies):
        if enemyY[i] > 536:  # jeśli przeciwnik dojdzie na doł planszy koniec gry
            game_over()
            break

        if enemyX[i] <= 0:
            enemy_speedX[i] *= -1  # zmieniamy kierunek wroga po dotknięciu krawędzi
            enemyY[i] += 34
        elif enemyX[i] >= 736:
            enemy_speedX[i] *= -1
            enemyY[i] += 32

        # sprawdzamy kolizje naboju z wrogiem
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY, 25)

        if collision:
            death_sound = mixer.Sound(death_sound_url2)
            death_sound.set_volume(0.16)
            death_sound.play()

            bulletState = "ready"
            bulletY = -50
            score += 1
            gen_enemy(i)

        # sprawdzamy kolizje playera z wrogiem
        player_collision = is_collision(enemyX[i], enemyY[i], playerX, playerY, 50)
        if player_collision:

            death_sound = mixer.Sound(death_sound_url)
            death_sound.play()
            game_over()

        # inicjujemy wroga
        enemy(enemyX[i], enemyY[i], i)

        # inicjujemy ruch wroga (będzie się zwiększać albo zmenijszać)
        enemyX[i] += enemy_speedX[i]

    # inicjujemy funkcje player
    player(playerX, playerY)

    if bulletY <= -32:
        bulletY = -50
        bulletState = "ready"

    # inicjujemy ruch naboju po naciśnięciu spacji
    if bulletState == "throw":
        shot_bullet(bulletX, bulletY)
        bulletY -= bulletYspeed

    # Pokazujemy wynik
    show_score(textX, textY)

    pygame.display.update()  # ekran zostaje "odświeżony co 1 klatkę"
    clock.tick(240)
# datas=[("assets/font2.ttf", "assets/"), ("assets/logo.png", "assets/"), ("assets/leonardo.png", "assets/"), ("assets/foot-clan.png", "assets/"), ("assets/shreder.png", "assets/"), ("assets/pizza.png", "assets/"), ("assets/font.ttf", "assets/"), ("sounds/music.mp3", "sounds/"), ("sounds/throw.wav", "sounds/"), ("sounds/death2.wav", "sounds/"), ("sounds/death.wav", "sounds/")],
