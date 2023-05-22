# Proyecto Final: Introducción al desarrollo de videojuegos con ECS
Por:
- Juan Andrés Romero Colmenares - 202013449
- Juan Felipe Castro - 
- María Paula González - 

## Introducción
En esta entrega se desarrollará un videojuego con el fin de aplicar los conceptos de arquitectura ECS (Entity Component System). Para esto se utilizará el lenguaje de programación Python y la librería Pygame.

## Configuración de Assets
Las configuraciones de los enemigos, la ventana y el nivel se encuentra en la carpeta `./assets/cfg/`. En esta carpeta se encuentran los archivos  `player.json`, `bullet.json`, `enemy_data.json`, `level_01.json`, `window.json` y `explosion.json`. Estos archivos contienen la información necesaria para la configuración del jugador, las balas, la creación de los enemigos, el nivel y la ventana y las explosiones respectivamente. Si se quiere cambiar la configuración de estos elementos, se debe modificar el archivo correspondiente.

Por otro lado, también se encuentran `starfield.json` y `interface.json` que se encargan de la configuración del campo de estrellas y la interfaz gráfica que se muestra en pantalla respectivamente.

### Habilidad especial
La habilidad especial del jugador es unna sobrecarga de la nave que le permite al jugador disparar mucho más rápido por unos segundos. Esta habilidad se puede activar con la tecla `F` y solo se puede utilizar cada 5 segundos.

# Link a Itch.io
El juego fue publicado en itch.io y se puede jugar en el siguiente link:
