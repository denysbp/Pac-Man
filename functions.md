# Functions

## Render

### `__init__(self, w, h, levels, data)`

Responsabilidade: preparar tudo o que o jogo precisa para funcionar.

Guarda a configuração recebida, chama `set_global_positions_sizes` para criar as variáveis base e inicia o MLX. Liga-se à base de dados, cria a tabela caso ainda não exista e carrega as pontuações guardadas. Por fim guarda a lista de níveis e chama `set_images` e `create_classes_and_classes_atributes`.

### `set_global_positions_sizes(self, w, h)`

Responsabilidade: criar as variáveis globais de posições, tamanhos e estados.

Define os valores dos bits das paredes (`N`, `E`, `S`, `W`), os offsets do mapa, a altura do HUD e o tamanho da janela. Inicializa as dimensões do labirinto, a lista dos cantos, os pontos e o contador de vitória. Cria também as flags que controlam o estado do jogo, como `start`, `victory`, `gameover`, `gamewin`, `PAUSE` e `quit`, e guarda as vidas iniciais em `initial_lives`.

### `set_images(self)`

Responsabilidade: criar a janela e carregar todas as imagens.

Abre a janela do MLX e carrega os PNG das gomas, do jogador, dos controles e dos ecrãs de vitória, game over, pausa, modos e nomes. Cria a imagem `buffer` onde o mapa é desenhado. As imagens do menu principal são carregadas para a lista `menu`.

### `get_image(self)`

Responsabilidade: devolver a imagem do menu que está selecionada.

Usa `img_index` para escolher a imagem da lista `menu`. O resto da divisão pelo tamanho da lista garante que o índice nunca sai da lista.

### `create_classes_and_classes_atributes(self)`

Responsabilidade: criar os objetos e as variáveis usadas durante o jogo.

Cria o `Player`, o dicionário `player_sheat` com os modos especiais e as velocidades do jogador e dos bots. Define o tempo do nível (`TIME`) e o `level_deadline`, e as variáveis do super pac. Cria os quatro bots e as memórias (`Memory`) do buffer e das gomas, que permitem escrever pixels diretamente. Cria também as listas de gomas e coloca a seed a `0` quando não foi indicada.

### `find_spawn_below_42(self)`

Responsabilidade: encontrar a posição inicial do jogador.

Procura as células com valor `15`, identifica a última linha onde elas aparecem e escolhe a coluna central dessa zona. O jogador é colocado na linha seguinte.

### `clear_buffer(self)`

Responsabilidade: limpar os pixels atuais do buffer.

Coloca todos os bytes da memória da imagem em zero. Isto remove o desenho anterior antes de o mapa ser desenhado novamente.

### `calcule_maze_dimetions(self, height, width)`

Responsabilidade: calcular os tamanhos do mapa a partir do labirinto.

Guarda a altura e a largura do labirinto e calcula o tamanho de cada célula (`CELL_W` e `CELL_H`) com o espaço que sobra na janela depois dos offsets e do HUD. Calcula o tamanho total do mapa e os quatro cantos, que servem para as gomas grandes e para o spawn dos bots. Junta os cantos e as gomas pequenas a `gum_position` e coloca o jogador na posição inicial.

### `start_level(self, next_level=True)`

Responsabilidade: criar e preparar um nível.

Reinicia o tempo do nível. Se todos os níveis já foram jogados, ativa `gamewin` e termina. Quando `next_level` é verdadeiro, cria um novo labirinto com o `MazeGenerator` e calcula as dimensões. Depois limpa as gomas comidas, repõe os pontos, coloca o jogador no início e prepara os quatro bots com o spawn, a posição, o labirinto e o primeiro caminho com `call_bfs`. No fim aumenta o `index` do nível.

### `cell_position(self, row, col)`

Responsabilidade: converter uma posição da matriz do labirinto em coordenadas da janela.

Recebe a linha e a coluna da célula e devolve as coordenadas `x` e `y` onde essa célula começa.

### `is_walkable(self, cell)`

Responsabilidade: verificar se uma célula pode ser percorrida.

Analisa as paredes guardadas nos bits da célula. Se existir pelo menos uma direção sem parede, a célula é considerada acessível.

### `get_wall_rects(self, row, col)`

Responsabilidade: transformar as paredes de uma célula em retângulos de colisão.

Lê as paredes da célula e cria um `Rect` para cada parede existente, com uma espessura pequena. Se a posição recebida estiver fora do mapa, devolve uma lista vazia.

### `check_colision(self, dx, dy)`

Responsabilidade: verificar se o jogador pode ocupar uma determinada posição.

Cria o retângulo que representa o jogador na posição futura, identifica as células onde os quatro cantos do jogador ficam e verifica se esse retângulo toca alguma parede. Devolve `False` quando há colisão.

### `check_colision_to_bot(self, bot, dx, dy)`

Responsabilidade: verificar se um bot pode ocupar uma determinada posição.

Faz o mesmo que `check_colision`, mas usa o tamanho da imagem do bot recebido em vez do tamanho do jogador.

### `blip(self)`

Responsabilidade: colocar o buffer do mapa na janela.

Envia a imagem `buffer` para a janela do MLX.

### `close(self, param)`

Responsabilidade: terminar o programa corretamente.

Marca `quit` para o ciclo do `run` parar, reativa o autorepeat do teclado, destrói a janela do MLX e pede ao loop principal para terminar.

### `key_press(self, keycode, param)`

Responsabilidade: encaminhar uma tecla recebida para o sistema de controles.

Recebe o código da tecla através do MLX. Se o jogo estiver num ecrã final (vitória do nível, game over ou fim do jogo), ignora a tecla. Caso contrário chama `controls`.

### `frames(self, x, y)`

Responsabilidade: atualizar o que aparece na janela.

Se o jogo acabou, mostra o ecrã de game over ou de vitória final. Caso contrário limpa a janela, reconstrói o buffer quando existe uma alteração no mapa, coloca o buffer na janela, desenha o HUD, o jogador e os bots por cima. Também verifica se todas as gomas foram comidas para ativar a vitória do nível e faz a pausa de 3 segundos quando o jogador perde uma vida.

### `controls(self, key, param)`

Responsabilidade: tratar os comandos do jogador.

A tecla `ESC` fecha o jogo e o espaço liga ou desliga a pausa. Fora da pausa trata as teclas de 1 a 6, que alteram a velocidade, a invencibilidade, as vidas, o nível, o congelamento dos bots e a intangibilidade, e a tecla `m`, que mostra os modos. Trata ainda as teclas de direção (setas e WASD), que atualizam a imagem do jogador e redesenham a cena.

### `put_img(self, cell, x, y)`

Responsabilidade: desenhar uma célula no buffer.

Desenha no buffer as linhas das paredes que a célula tem. Se a célula for acessível e a goma ainda não tiver sido comida, coloca também a goma pequena no centro da célula.

### `draw_board(self)`

Responsabilidade: desenhar o mapa no buffer.

Percorre todas as células do labirinto e chama `put_img` para cada uma. Depois desenha as gomas grandes nos cantos. As gomas que já foram comidas não são desenhadas novamente.

### `end_screen(self)`

Responsabilidade: tratar o fim do jogo.

No primeiro frame guarda a pontuação na base de dados, define quando o ecrã termina (3 segundos depois) e mostra o game over ou a vitória. Quando esse tempo passa, chama `back_to_menu`.

### `back_to_menu(self)`

Responsabilidade: voltar ao menu principal.

Repõe o jogo com `reset_game`, ativa `start`, limpa a janela e pede ao loop atual para terminar, para o `run` mostrar o menu outra vez.

### `reset_game(self)`

Responsabilidade: repor o estado do jogo para uma nova partida.

Desativa as flags de fim de jogo, vitória e pausa, volta ao primeiro nível e repõe as vidas e a velocidade do jogador. Desliga o super pac e os modos especiais, limpa as listas de gomas e revive os bots. Repõe também os dados do menu, como o nome, a opção selecionada e os submenus, e volta a ler as pontuações da base de dados.

### `render_loop(self, param)`

Responsabilidade: executar a atualização principal do jogo.

Corre em cada frame. Se o jogo estiver no menu não faz nada. Se acabou, chama `end_screen`. Durante a vitória de um nível conta o tempo de espera e, no fim, começa o nível seguinte. Em pausa mostra a imagem de pausa. Nos outros casos chama `move` e `frames`.

### `level_win(self)`

Responsabilidade: mostrar a mensagem de vitória do nível.

Coloca a imagem de vitória centrada na horizontal, a meio da janela.

### `game_win(self)`

Responsabilidade: mostrar o ecrã de vitória final.

Limpa a janela e coloca a imagem de vitória do jogo centrada.

### `game_over(self)`

Responsabilidade: mostrar o ecrã de game over.

Limpa a janela e coloca a imagem de game over centrada.

### `pause(self)`

Responsabilidade: mostrar a imagem de pausa.

Coloca a imagem de pausa no centro da janela.

### `is_near_player(self, bot, player, distance)`

Responsabilidade: verificar se um bot está perto do jogador.

Calcula a diferença de posições nos dois eixos e compara o quadrado da distância com o quadrado do valor recebido. Assim evita usar a raiz quadrada.

### `check_bot_player_collision(self, bot, invencible=False)`

Responsabilidade: verificar se um bot está a tocar no jogador.

Se o jogador estiver invencível devolve `False`. Caso contrário cria o retângulo do jogador e o retângulo de impacto do bot, centrado na imagem do bot, e verifica se os dois se cruzam.

### `move_bots(self)`

Responsabilidade: atualizar o comportamento e a posição de todos os bots.

Primeiro verifica se o super pac terminou e, nesse caso, repõe as imagens dos bots. Depois percorre cada bot. Um bot morto volta a viver quando o seu tempo acaba e, enquanto estiver morto, é ignorado. Durante o super pac o bot foge do jogador e, se for tocado, é morto, dá pontos e calcula o caminho de volta ao spawn. Fora do super pac, se tocar no jogador, este perde uma vida ou o jogo acaba. Quando o caminho atual termina, o bot escolhe um novo: persegue o jogador se estiver perto ou vai para um ponto aleatório. No fim move o bot um passo se não houver parede, atualizando `pixel` e `i`, ou avança para a direção seguinte quando há colisão.

### `gums(self)`

Responsabilidade: verificar se o jogador comeu alguma goma.

Verifica a goma pequena atingida e testa a colisão com as gomas grandes dos cantos. Quando uma goma pequena é comida, guarda-a em `heated_small`, soma os pontos e marca o mapa para ser redesenhado. Quando é uma goma grande, guarda-a em `heated_big`, ajusta os pontos, ativa o super pac com o seu tempo limite e muda a imagem dos bots que estão vivos.

### `try_move_step(self, dx_dir, dy_dir, step, intangibility)`

Responsabilidade: mover o jogador um passo.

Aplica o passo na direção recebida e verifica os limites do mapa. Se o modo intangível não estiver ativo, verifica também as paredes. Quando há colisão desfaz o passo e devolve `False`. Se o movimento é possível devolve `True`.

### `move(self, param)`

Responsabilidade: atualizar a posição do jogador e do resto do jogo.

Divide o movimento em passos pequenos (no máximo 4 pixels) e para no primeiro que colide. Depois chama `gums`, atualiza a imagem do jogador, move os bots quando não estão congelados e redesenha a cena.

### `draw_information(self)`

Responsabilidade: desenhar o HUD.

Mostra os pontos e o tempo que falta para acabar o nível, e ativa o game over quando o tempo chega a zero. Mostra a imagem dos modos quando ela está ativa e as vidas: até 3 vidas desenha um ícone por vida e acima disso escreve o número.

### `mouse_handler(self, mouse_code, x, y, param)`

Responsabilidade: tratar eventos do rato.

Neste momento não faz nada, o jogo não usa o rato.

### `new_game(self)`

Responsabilidade: desenhar o ecrã de novo jogo.

Se o nome já foi confirmado mostra a imagem que pede para carregar em `Enter`. Caso contrário mostra a imagem para escrever o nome e o nome que está a ser escrito.

### `high_scores(self)`

Responsabilidade: desenhar a lista de pontuações.

Percorre as pontuações guardadas e escreve cada uma no formato `nome - score`, uma linha por cada resultado.

### `show_controls(self)`

Responsabilidade: mostrar a imagem dos controles.

Coloca a imagem dos controles centrada na horizontal.

### `redraw_start_screen(self)`

Responsabilidade: atualizar o ecrã do menu.

Limpa a janela e chama `start_screen` para desenhar o menu de novo.

### `start_game(self, keycode, param)`

Responsabilidade: tratar as teclas do menu.

`ESC` volta do submenu para o menu principal ou fecha o jogo. No ecrã de novo jogo trata as letras, o `Backspace` e o `Enter` que confirma o nome. No menu principal, as setas mudam a opção e o `Enter` abre a opção escolhida. Quando o nome já está confirmado, o espaço inicia o jogo e termina o loop do menu. No fim redesenha o ecrã.

### `set_name_player(self, keycode)`

Responsabilidade: adicionar uma letra ao nome do jogador.

Converte o código da tecla com o dicionário `keyboard`, limita o tamanho do nome e alterna o `capslock` quando é essa a tecla. Só aceita letras e espaços, em maiúsculas ou minúsculas conforme o `capslock`.

### `start_screen(self)`

Responsabilidade: desenhar o menu.

Se algum submenu está ativo (novo jogo, pontuações ou controles), desenha esse ecrã. Caso contrário coloca a imagem da opção selecionada do menu principal, centrada.

### `game_menu(self)`

Responsabilidade: executar o menu principal.

Desenha o menu, regista o evento do teclado para `start_game` e inicia o loop do MLX. O loop só termina quando o jogador começa o jogo ou fecha a janela.

### `run(self)`

Responsabilidade: iniciar e executar o jogo.

Desativa o autorepeat do teclado e entra num ciclo que só acaba quando o jogador fecha o jogo. Em cada volta mostra o menu, cria o primeiro nível, limpa o buffer, desenha o mapa, regista os eventos do teclado e o loop de atualização e inicia o loop do MLX. Quando a partida acaba, o loop termina e o ciclo mostra o menu outra vez.