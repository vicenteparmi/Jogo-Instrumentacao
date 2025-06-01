"""
# Como gerar os flashcards

Este script utiliza o Manim para gerar imagens dos flashcards de FM. Siga as instruções abaixo para renderizar todos os cartões de uma vez:

## Pré-requisitos
- Python 3.8+
- Manim instalado (recomenda-se usar o ambiente virtual com `uv`)
- Dependências do projeto instaladas

## Comando para renderizar um flashcard específico

Execute o comando abaixo dentro da pasta `manimations`:

    cd /Users/vicenteparmi/Documents/Developer/Jogo-Instrumentacao/manimations
    FLASHCARD_NUMBER=5 uv run manim -p -qh ../bilhete_flashcard.py FlashcardLayout

Altere o número de 1 a 10 para gerar o flashcard desejado.

## Renderizando todos os flashcards automaticamente

Você pode gerar todos os flashcards de 1 a 10 com o seguinte comando shell:

    cd /Users/vicenteparmi/Documents/Developer/Jogo-Instrumentacao/manimations
    for i in {1..10}; do \
      FLASHCARD_NUMBER=$i uv run manim -qh ../bilhete_flashcard.py FlashcardLayout -o bilhete_flashcard_$i; \
    done

Os arquivos serão salvos na pasta de mídia padrão do Manim.

"""

from manim import *
import numpy as np
import os

# Configure para imagem estática 16:9 (ex: 1080p)
config.frame_height = 9
config.frame_width = 16
config.pixel_height = 1080
config.pixel_width = 1920
config.disable_caching = True

# Dicionário com os dados de cada flashcard
FLASHCARDS = {
    1: {"code": [1, 5, 2, 3, 1, 4], "answer": "413251"},
    2: {"code": [6, 1, 3, 4, 1, 6], "answer": "614316"},
    3: {"code": [4, 3, 2, 5, 6, 1], "answer": "165234"},
    4: {"code": [1, 3, 4, 2, 5, 3], "answer": "352431"},
    5: {"code": [2, 6, 5, 4, 3, 1], "answer": "134562"},
    6: {"code": [5, 2, 6, 1, 3, 4], "answer": "431625"},
    7: {"code": [3, 4, 5, 6, 1, 2], "answer": "216543"},
    8: {"code": [6, 5, 4, 1, 2, 3], "answer": "321456"},
    9: {"code": [2, 1, 3, 6, 4, 5], "answer": "546312"},
    10: {"code": [5, 4, 1, 3, 6, 2], "answer": "263145"},
}

class FlashcardLayout(Scene):
    """
    Gera o flashcard selecionado via FLASHCARD_NUMBER (1-10)
    """
    def construct(self):
        # Seleciona o número do flashcard
        number = int(os.environ.get("FLASHCARD_NUMBER", 1))
        data = FLASHCARDS[number]
        code = data["code"]
        answer = data["answer"]
        # Define nome de arquivo único para cada flashcard
        config.output_file = f"bilhete_flashcard_{number}"
        config.media_dir = "media/bilhete_flashcard"
        config.save_last_frame = True
        config.preview = False  # Não abrir após renderizar

        # Fundo branco
        self.camera.background_color = WHITE

        # 1. Título: só o número
        title = Text(str(number), font_size=48, color=BLACK)
        title.to_edge(UL, buff=0.5)

        # 2. Dimensões do cartão
        axes_width = config.frame_width * 0.85
        axes_height = config.frame_height * 0.5

        # 3. Eixos com grid
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=axes_width,
            y_length=axes_height,
            axis_config={
                "include_numbers": False,
                "include_tip": False,
                "stroke_color": GREY_A,
                "stroke_width": 1,
                "color": GREY_A,
            },
            tips=False,
        )
        axes.next_to(title, DOWN, buff=0.8)
        axes.center()
        axes.to_edge(UP, buff=1.2)

        # Grid mais visível
        x_lines = VGroup(*[
            Line(
                axes.c2p(i, -1.5),
                axes.c2p(i, 1.5),
                stroke_width=0.5,
                stroke_color=GREY_C,
                stroke_opacity=1
            )
            for i in np.arange(0, 6.1, 1)
        ])
        y_lines = VGroup(*[
            Line(
                axes.c2p(0, i),
                axes.c2p(6, i),
                stroke_width=0.5,
                stroke_color=GREY_C,
                stroke_opacity=1
            )
            for i in np.arange(-1.5, 1.6, 0.5)
        ])

        # Estilos visuais das ondas para cada tipo de frequência
        # Tipo 1 (8.0 Hz) - linha sólida
        # Tipo 2 (6.0 Hz) - pontos pequenos
        # Tipo 3 (4.6 Hz) - traços médios
        # Tipo 4 (4.0 Hz) - linha sólida
        # Tipo 5 (3.0 Hz) - padrão complexo (traço-ponto-traço)
        # Tipo 6 (2.5 Hz) - linha sólida
        line_styles = [
            {"stroke_width": 2},      # Tipo 1: linha sólida
            {"stroke_width": 2},      # Tipo 2: pontos pequenos
            {"stroke_width": 2},      # Tipo 3: traços médios
            {"stroke_width": 2},      # Tipo 4: linha sólida
            {"stroke_width": 2},      # Tipo 5: padrão complexo
            {"stroke_width": 2}       # Tipo 6: linha sólida
        ]
        dash_patterns = [
            None,                     # Tipo 1: linha contínua
            [0.1, 0.1],              # Tipo 2: pontos pequenos
            [0.2, 0.2],              # Tipo 3: traços médios
            None,                     # Tipo 4: linha contínua
            [0.3, 0.2, 0.05, 0.2],   # Tipo 5: traço-ponto-traço
            None                      # Tipo 6: linha contínua
        ]

        # Frequências base para cada tipo de onda (em Hz)
        # Organizadas por frequência decrescente para melhor visualização
        base_freqs = {
            1: 8.0,   # Frequência mais alta
            2: 6.0,   
            3: 4.6,   
            4: 4.0,   
            5: 3.0,   
            6: 2.5    # Frequência mais baixa
        }
        frequencies = [base_freqs[d] for d in code]

        # Função para transição suave
        def smooth_transition(x, freq1, freq2, transition_point, width=0.1):
            sigmoid = 1 / (1 + np.exp(-(x - transition_point) / width))
            return freq1 * (1 - sigmoid) + freq2 * sigmoid

        # Frequência instantânea
        def frequency_at_x(x):
            segment = int(x)
            if segment >= 6:
                return frequencies[5]
            elif segment < 0:
                return frequencies[0]
            if segment == 5:
                return frequencies[5]
            transition_width = 0.05
            if x % 1 > 1 - transition_width:
                return smooth_transition(
                    x,
                    frequencies[segment],
                    frequencies[segment+1],
                    segment + 1 - transition_width/2,
                    transition_width
                )
            return frequencies[segment]

        # Fase integrando frequência
        def phase_at_x(x, step=0.01):
            points = np.arange(0, x+step, step)
            phases = [0]
            for i in range(1, len(points)):
                dx = points[i] - points[i-1]
                f1 = frequency_at_x(points[i-1]) * PI
                f2 = frequency_at_x(points[i]) * PI
                phases.append(phases[-1] + (f1 + f2) / 2 * dx)
            return phases[-1]

        # Valor da onda
        def fm_wave(x):
            return np.sin(phase_at_x(x))

        # Segmentos da onda
        segment_plots = VGroup()
        for i in range(6): # i é o índice do segmento 0-5
            # Determina o estilo para este segmento com base no tipo de onda em 'code'
            wave_type_in_segment = code[i]  # 'code' contém os tipos de onda (1-6)
            # Os estilos são 0-indexados, os tipos de onda são 1-indexados
            style_index_for_segment = wave_type_in_segment - 1 

            segment_plot = axes.plot(
                fm_wave,
                x_range=[i, i+1, 0.01],
                color=BLACK,
                **line_styles[style_index_for_segment] # Usa o estilo para o TIPO de onda no segmento
            )
            if dash_patterns[style_index_for_segment] is not None: # Usa o estilo para o TIPO de onda no segmento
                segment_plot.set_dash_pattern(dash_patterns[style_index_for_segment])
            segment_plots.add(segment_plot)

        # --- Início das Modificações para a Cheat Sheet ---

        # Calcula a largura de um segmento do gráfico principal (cada tipo de onda)
        one_segment_screen_width = axes_width / 6.0
        
        # Ordem dos tipos de onda exibidos na cheat sheet (1 a 6)
        cheat_sheet_wave_types_ordered = [1, 2, 3, 4, 5, 6]

        # Espaço interno lateral para a mini-onda dentro da caixa
        wave_internal_padding = 0.05
        # Largura disponível para desenhar a mini-onda
        drawable_mini_wave_width = one_segment_screen_width - (2 * wave_internal_padding)
        # Largura total da caixa de cada tipo de onda
        new_bg_width = one_segment_screen_width 

        # Grupo que irá conter todas as caixas da cheat sheet
        cheat_sheet_entries = VGroup()
        
        # Espaçamento horizontal entre as caixas
        gap_between_items = 0.2
        # Largura total ocupada pelas caixas e espaços, para centralizar
        total_width_of_all_items_and_gaps = (6 * new_bg_width) + (5 * gap_between_items)
        # Posição X inicial do centro da primeira caixa
        start_x_position = -total_width_of_all_items_and_gaps / 2.0 + new_bg_width / 2.0
        current_x_position = start_x_position

        # Cria cada entrada da cheat sheet (caixa, número, mini-onda, frequência)
        for cheat_wave_type in cheat_sheet_wave_types_ordered:
            entry = VGroup()
            style_index_for_cheat_item = cheat_wave_type - 1

            # Caixa de fundo
            bg = Rectangle(
                width=new_bg_width, 
                height=1.6, 
                stroke_color=BLACK,
                stroke_width=1,
                fill_opacity=0
            )
            bg.move_to(RIGHT * current_x_position + DOWN * 3.5)

            # Número do tipo de onda
            number = Text(f"{cheat_wave_type}", font_size=20, color=BLACK)
            number.move_to(bg.get_top() + DOWN * 0.3)

            # Valor da frequência base
            current_mini_freq_val = base_freqs[cheat_wave_type] 
            freq_text = Text(f"{current_mini_freq_val:.1f} Hz", font_size=14, color=BLACK)
            freq_text.move_to(bg.get_bottom() + UP * 0.2)
            
            # Geração da mini-onda
            mini_wave = VMobject()
            t_local_mini = np.linspace(0, 1, 100)
            y_vals_mini = [np.sin(x_l * current_mini_freq_val * PI) for x_l in t_local_mini]

            wave_y_center_mini = bg.get_center()[1]
            x_center_bg = bg.get_center()[0] 
            # Calcula os limites X para centralizar a mini-onda
            x0_mini = x_center_bg - (drawable_mini_wave_width / 2)
            x1_mini = x_center_bg + (drawable_mini_wave_width / 2)
            
            wave_points_mini = []
            y_min_val_mini = -1 
            y_max_val_mini = 1  

            # Calcula os pontos da mini-onda normalizada para a caixa
            for idx_mini, x_local_val_mini in enumerate(t_local_mini):
                x_screen = x0_mini + (x1_mini - x0_mini) * x_local_val_mini
                current_y_val_mini = y_vals_mini[idx_mini]
                y_norm_factor_mini = (current_y_val_mini - y_min_val_mini) / (y_max_val_mini - y_min_val_mini)
                y_screen = wave_y_center_mini + (y_norm_factor_mini - 0.5) * (bg.height * 0.4) 
                wave_points_mini.append([x_screen, y_screen, 0])
            
            if wave_points_mini:
                mini_wave.set_points_as_corners(wave_points_mini)
            
            # Aplica estilo visual da onda
            mini_wave.set_stroke(width=line_styles[style_index_for_cheat_item]["stroke_width"], color=BLACK)
            if dash_patterns[style_index_for_cheat_item] is not None:
                mini_wave.set_dash_pattern(dash_patterns[style_index_for_cheat_item])
            
            # Adiciona todos os elementos à entrada
            entry.add(bg, number, mini_wave, freq_text)
            cheat_sheet_entries.add(entry)

            # Atualiza a posição X para a próxima caixa
            current_x_position += new_bg_width + gap_between_items
            
        # --- Fim das Modificações para a Cheat Sheet ---

        # Adicionar elementos à cena
        self.add(title)
        self.add(axes)
        self.add(x_lines, y_lines)
        self.add(segment_plots)
        self.add(cheat_sheet_entries)

        # Resposta pequena, canto superior direito
        # Exibe a sequência de códigos diretamente da onda (code) ao invés do valor pré-definido
        answer_str = "".join(map(str, code))
        answer_text = Text(answer_str, font_size=24, color=GREY_D)
        answer_text.scale(0.5)
        answer_text.to_edge(UR, buff=0.25)
        self.add(answer_text)

        # Borda do cartão
        frame_rect = Rectangle(
            width=config.frame_width * 0.98,
            height=config.frame_height * 0.98,
            stroke_color=BLACK,
            stroke_width=0.5
        )
        self.add(frame_rect)
