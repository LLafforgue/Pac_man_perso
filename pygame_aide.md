
## gestion ecran et fond:

### Le principe du double buffer:

### fonctions de base :
 pygame.Surface

    pygame object for representing images
    Surface((width, height), flags=0, depth=0, masks=None) -> Surface
    Surface((width, height), flags=0, Surface) -> Surface
	Ce qui s'y passe n'est pas approprement visible a l'ecran !

pygame.display

	Est une fenetre de surface speciale. Elle herite de pygame.Surface.
	Cette fenetre est visible apres le `flip()`.
	Elle peut recevoir un blit.


## Creer du texte:

```python
	import pygame
	pygame.init()
	pygame.font.init()  # souvent inclus dans pygame.init()

	# Police système (par nom) (une option parmi d'autre)
	font = pygame.font.SysFont("Times New Roman", 32)
	# autre : font = pygame.font.Font("ma_police.ttf", 32)

	# render(texte, antialiasing, couleur, couleur_fond=None)
	surface_texte = font.render("Bonjour !", True, (255, 255, 255))

	# Dans la boucle while:
	# Coller la surface sur l'écran aux coordonnées (100, 50)
	ecran.blit(surface_texte, (100, 50))
```

Pour acceder a l'ensemble des fonts disponibles :
```python
	polices_dispo = pygame.font.get_fonts()
	print(polices_dispo)  # liste de strings : ['arial', 'verdana', 'courier', ...]
```

## Assets:

Pour simplement afficher et transformer un asset.

```python
	# Charger l'image depuis un fichier
	image = pygame.image.load("mon_sprite.png")

	# Optionnel mais recommandé : optimise le format pour l'affichage
	image = image.convert()        # image sans transparence
	image = image.convert_alpha()  # image avec transparence (PNG)

	# Redimensionner
	image = pygame.transform.scale(image, (64, 64))

	# Rotation (en degrés)
	image_tournee = pygame.transform.rotate(image, 45)

	# Miroir horizontal
	image_miroir = pygame.transform.flip(image, True, False)

	# Dans la boucle while:
	# Afficher à la position (x, y)
	ecran.blit(image, (100, 200))

```

Pour les animer :
La technique classique : toutes les frames d'une animation sont dans une seule image (spritesheet).

__[ [frame0][frame1][frame2][frame3] ]  ← spritesheet.png__

On découpe la bonne frame à afficher selon le temps :
```python

def get_frame(sheet, index):
    # Découpe un rectangle dans la spritesheet
    rect = pygame.Rect(index * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT)
    frame = pygame.Surface((FRAME_WIDTH, FRAME_HEIGHT), pygame.SRCALPHA)
    frame.blit(sheet, (0, 0), rect)
    return frame

# Pré-charger toutes les frames
frames = [get_frame(spritesheet, i) for i in range(NB_FRAMES)]

```
Penser a utiliser `pygame.time.Clock.tick(60)` comme delta time `dt` pour que l'animation tourne a la meme vitesse quelque soit la puissance de la machine.

```python
# Dans la boucle:
    # Avancer l'animation selon le temps réel
    temps_ecoule += dt
    if temps_ecoule >= VITESSE_ANIM:
        frame_index = (frame_index + 1) % len(frames)  # boucle
        temps_ecoule = 0

    ecran.fill((30, 30, 30))
    ecran.blit(frames[frame_index], (168, 118))  # centré ~
    pygame.display.flip()

```

## Lexique:

- L'antialiasing (lissage) :
L'antialiasing atténue l'effet 'escalier' inerant aux pixels en coloriant les pixels de bordure avec des teintes intermédiaires (semi-transparentes), pour que l'œil perçoive une courbe lisse.