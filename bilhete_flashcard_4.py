from manim import *
import numpy as np

# Configure for a static 16:9 image
config.frame_height = 9
config.frame_width = 16
config.pixel_height = 1080
config.pixel_width = 1920
config.output_file = "bilhete_flashcard_4"
config.disable_caching = True

class FlashcardLayout(Scene):
    """
    Generates flashcard 4/4 with code 134253
    """
    def construct(self):
        # Configurar fundo branco
        self.camera.background_color = WHITE
        
        # 1. Title - mudado para Bilhete 4/4
        title = Text("Bilhete 4/4", font_size=48, color=BLACK)
        title.to_edge(UL, buff=0.5)

        # 2. Define card dimensions
        axes_width = config.frame_width * 0.85
        axes_height = config.frame_height * 0.5

        # 3. Create Axes object with grid - removendo números
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=axes_width,
            y_length=axes_height,
            axis_config={
                "include_numbers": False,  # Removido os números
                "include_tip": False,
                "stroke_color": GREY_A,
                "stroke_width": 1,
                "color": GREY_A,
            },
            tips=False,
        )

        # Posicionar eixos e centralizar
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

        # Diferentes estilos de linha
        line_styles = [
            {"stroke_width": 2},
            {"stroke_width": 2},
            {"stroke_width": 2},
            {"stroke_width": 3},
            {"stroke_width": 2},
            {"stroke_width": 1.5}
        ]

        # Define dash patterns
        dash_patterns = [
            None,
            [0.2, 0.2],
            [0.1, 0.1],
            None,
            [0.3, 0.2, 0.05, 0.2],
            None
        ]

        # Define a frequência base para cada número no código 
        base_freqs = {
            1: 1.5,
            2: 3.6,
            3: 5.0,
            4: 2.0,
            5: 6.0,
            6: 3.0
        }
        
        # CÓDIGO ESPECÍFICO: 134253 - mapeando frequências na ordem correta
        code = [1, 3, 4, 2, 5, 3]
        frequencies = [base_freqs[digit] for digit in code]

        # Função para gerar uma transição suave entre frequências usando sigmoid
        def smooth_transition(x, freq1, freq2, transition_point, width=0.1):
            """Cria uma transição suave entre freq1 e freq2 usando uma função sigmoid"""
            sigmoid = 1 / (1 + np.exp(-(x - transition_point) / width))
            return freq1 * (1 - sigmoid) + freq2 * sigmoid
        
        # Função que retorna a frequência instantânea em qualquer ponto x
        def frequency_at_x(x):
            """Retorna a frequência em qualquer ponto x, com transições suaves"""
            segment = int(x)
            if segment >= 6:
                return frequencies[5]
            elif segment < 0:
                return frequencies[0]
            
            # Dentro de um segmento
            if segment == 5:  # Último segmento
                return frequencies[5]
            
            # Transição suave entre segmentos
            transition_width = 0.05  # Largura da zona de transição
            if x % 1 > 1 - transition_width:  # Próximo à transição
                return smooth_transition(
                    x,
                    frequencies[segment],
                    frequencies[segment+1],
                    segment + 1 - transition_width/2,
                    transition_width
                )
            
            return frequencies[segment]  # No meio do segmento
        
        # Calcular a fase integrando a frequência
        def phase_at_x(x, step=0.01):
            """Calcula a fase em x integrando numericamente a frequência"""
            points = np.arange(0, x+step, step)
            phases = [0]  # Fase inicial
            
            for i in range(1, len(points)):
                # Integração numérica simples (método do trapézio)
                dx = points[i] - points[i-1]
                f1 = frequency_at_x(points[i-1]) * PI
                f2 = frequency_at_x(points[i]) * PI
                phases.append(phases[-1] + (f1 + f2) / 2 * dx)
                
            return phases[-1]
        
        # Função para calcular o valor da onda em qualquer ponto x
        def fm_wave(x):
            """Calcula o valor da onda modulada em frequência em um ponto x"""
            return np.sin(phase_at_x(x))
        
        # Plota a onda FM completa
        fm_plot = axes.plot(
            fm_wave,
            x_range=[0, 6, 0.01],
            color=BLACK,
            stroke_width=2
        )
        
        # Aplicar estilos diferentes para cada segmento da onda
        segment_plots = VGroup()
        for i in range(6):
            segment_plot = axes.plot(
                fm_wave,
                x_range=[i, i+1, 0.01],
                color=BLACK,
                **line_styles[i]
            )
            
            # Aplicar o padrão tracejado se necessário
            if dash_patterns[i] is not None:
                segment_plot.set_dash_pattern(dash_patterns[i])
                
            segment_plots.add(segment_plot)

        # Cheat sheet simplificado em uma única linha
        cheat_sheet_entries = VGroup()
        
        for i in range(6):
            # Criar entrada do cheat sheet
            entry = VGroup()
            
            # Retângulo para cada entrada - aumentado ligeiramente
            bg = Rectangle(
                width=2.2,
                height=1.4,  # Aumentado para acomodar a frequência
                stroke_color=BLACK,
                stroke_width=1,
                fill_opacity=0
            )
            
            # Número no canto superior esquerdo - ajustado para evitar sobreposição
            number = Text(f"{i+1}", font_size=20, color=BLACK)
            number.move_to(bg.get_corner(UL) + RIGHT * 0.3 + DOWN * 0.3)
            
            # Adicionar indicador de frequência abaixo da onda
            freq_text = Text(f"{frequencies[i]:.1f}π Hz", font_size=14, color=BLACK)
            freq_text.move_to(bg.get_bottom() + UP * 0.2)
            
            # Mini onda dentro do retângulo - reposicionada abaixo do número
            mini_wave = VMobject()
            t = np.linspace(0, 1, 100)
            wave_points = []
            
            # Ajustar a posição vertical para ficar entre o número e o texto de frequência
            wave_y_center = bg.get_center()[1] + 0.1  # Ligeiramente acima do centro
            
            for ti in t:
                x = bg.get_left()[0] + 0.2 + ti * 1.8
                y = wave_y_center + 0.3 * np.sin(frequencies[i] * PI * ti * 3)
                wave_points.append([x, y, 0])
            
            mini_wave.set_points_as_corners(wave_points)
            mini_wave.set_stroke(width=line_styles[i]["stroke_width"], color=BLACK)
            
            # Aplicar padrão tracejado na amostra de onda
            if dash_patterns[i] is not None:
                mini_wave.set_dash_pattern(dash_patterns[i])
            
            # Adicionar elementos
            entry.add(bg, number, mini_wave, freq_text)
            
            # Posicionar na linha horizontal - espaçamento aumentado
            entry.shift(RIGHT * (i * 2.6 - 6.5))  # Maior espaçamento horizontal
            entry.shift(DOWN * 3.5)
            
            cheat_sheet_entries.add(entry)
        
        # Adicionar elementos à cena
        self.add(title)
        self.add(axes)
        self.add(x_lines, y_lines)
        self.add(segment_plots)  # Substituir sine_segments por segment_plots
        self.add(cheat_sheet_entries)
        
        # Borda do cartão
        frame_rect = Rectangle(
            width=config.frame_width * 0.98,
            height=config.frame_height * 0.98,
            stroke_color=BLACK,
            stroke_width=0.5
        )
        self.add(frame_rect)