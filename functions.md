# Functions

## Render

### `__init__(self, w, h)`

Responsabilidade: preparar tudo o que o jogo precisa para funcionar.

Cria a janela e a imagem principal do MLX, prepara a memória do buffer, carrega as imagens das gomas e do jogador e inicializa as variáveis usadas pelo mapa, movimento e desenho.

### `find_spawn_below_42(self)`

Responsabilidade: encontrar a posição inicial do jogador.

Procura as células com valor `15`, identifica a última linha onde elas aparecem e escolhe a coluna central dessa zona. O jogador é colocado na linha seguinte.

### `clear_buffer(self)`

Responsabilidade: limpar os pixels atuais do buffer.

Coloca todos os bytes da memória da imagem em zero. Isto remove o desenho anterior antes de o mapa ser desenhado novamente.

### `start_level(self, width, height, seed)`

Responsabilidade: criar e preparar um nível.

Cria o labirinto, calcula o tamanho de cada célula, calcula o tamanho total do mapa, guarda a posição das gomas e calcula os cantos da área do mapa.

### `cell_position(self, row, col)`

Responsabilidade: converter uma posição da matriz do labirinto em coordenadas da janela.

Recebe a linha e a coluna da célula e devolve as coordenadas `x` e `y` onde essa célula começa.

### `is_walkable(self, cell)`

Responsabilidade: verificar se uma célula pode ser percorrida.

Analisa as paredes guardadas nos bits da célula. Se existir pelo menos uma direção sem parede, a célula é considerada acessível.

### `get_wall_rects(self, row, col)`

Responsabilidade: transformar as paredes de uma célula em retângulos de colisão.

Lê as paredes da célula e cria um `Rect` para cada parede existente. Se a posição recebida estiver fora do mapa, devolve uma lista vazia.

### `check_colision(self, dx, dy, position)`

Responsabilidade: verificar se o jogador pode ocupar uma determinada posição.

Cria o retângulo que representa o jogador na posição futura, identifica as células onde os quatro cantos do jogador ficam e verifica se esse retângulo toca alguma parede.

### `blip(self)`

Responsabilidade: colocar o buffer do mapa na janela.

Envia a imagem `buffer` para a janela do MLX.

### `close(self, param)`

Responsabilidade: terminar o programa corretamente.

Destrói a janela do MLX e pede ao loop principal para terminar.

### `key_press(self, keycode, param)`

Responsabilidade: encaminhar uma tecla recebida para o sistema de controles.

Recebe o código da tecla através do MLX e chama `controls` para decidir o que fazer.

### `frames(self, x, y)`

Responsabilidade: atualizar o que aparece na janela.

Limpa a janela, reconstrói o buffer quando existe uma alteração no mapa, coloca o buffer na janela e desenha o jogador por cima.

### `controls(self, key, param)`

Responsabilidade: tratar os comandos do jogador.

Verifica as teclas usadas para subir, descer, esquerda e direita. Também trata a tecla de saída. Quando uma direção é escolhida, atualiza a imagem do jogador e redesenha a cena.

### `draw_board(self)`

Responsabilidade: desenhar o mapa no buffer.

Percorre todas as células do labirinto, desenha as paredes e coloca as gomas nas células acessíveis. As gomas que já estão em `heated` não são desenhadas novamente.

### `render_loop(self, param)`

Responsabilidade: executar a atualização principal do jogo.

Chama `move` para atualizar a posição do jogador e depois atualiza a imagem apresentada na janela.

### `reload_board(self, *arg)`

Responsabilidade: atualizar o mapa depois de uma alteração relacionada com gomas.

Percorre os objetos recebidos, verifica se alguma goma foi atingida e marca o mapa para ser redesenhado.

Esta função pertence a uma abordagem anterior de atualização do mapa e atualmente não é usada no `run`.

### `move(self, param)`

Responsabilidade: atualizar a posição do jogador.

Verifica a direção atual, calcula a próxima posição, verifica colisões com paredes e limites do mapa e altera a posição quando o movimento é permitido.

Depois verifica se o jogador atingiu uma goma. Quando uma goma é comida, a sua posição é adicionada a `heated` e o mapa é marcado para ser reconstruído.

Por fim, atualiza a imagem do jogador e a imagem apresentada na janela.

### `run(self)`

Responsabilidade: iniciar e executar o jogo.

Cria o nível, encontra a posição inicial do jogador, desenha o mapa, registra os eventos do teclado e inicia o loop principal do MLX.