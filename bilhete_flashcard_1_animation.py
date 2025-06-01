from manim import *
import numpy as np

# Configure for 16:9 video
config.frame_height = 9
config.frame_width = 16
config.pixel_height = 1080
config.pixel_width = 1920
config.output_file = "bilhete_flashcard_1_animation"
config.disable_caching = True

class FlashcardAnimation(Scene):
    """
    Generates animation of flashcard 1/4 with code 152314
    """
    def construct(self):
        # Configurar fundo branco
        self.camera.background_color = WHITE
        
        # 1. Title
        title = Text("Bilhete 1/4", font_size=48, color=BLACK)
        title.to_edge(UL, buff=0.5)

        # 2. Define card dimensions
        axes_width = config.frame_width * 0.85
        axes_height = config.frame_height * 0.5

        # 3. Create Axes object with grid
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
        
        # Borda do cartão
        frame_rect = Rectangle(
            width=config.frame_width * 0.98,
            height=config.frame_height * 0.98,
            stroke_color=BLACK,
            stroke_width=0.5
        )

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
        
        # CÓDIGO ESPECÍFICO: 152314 - mapeando frequências na ordem correta
        code = [1, 5, 2, 3, 1, 4]
        frequencies = [base_freqs[digit] for digit in code]
        
        # Função para gerar uma transição suave entre frequências usando sigmoid
        def smooth_transition(x, freq1, freq2, transition_point, width=0.1):
            sigmoid = 1 / (1 + np.exp(-(x - transition_point) / width))
            return freq1 * (1 - sigmoid) + freq2 * sigmoid
        
        # Função que retorna a frequência instantânea em qualquer ponto x
        def frequency_at_x(x):
            segment = int(x)
            if segment >= 6:
                return frequencies[5]
            elif segment < 0:
                return frequencies[0]
            
            if segment == 5:  # Último segmento
                return frequencies[5]
            
            # Transição suave entre segmentos
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
        
        # Calcular a fase integrando a frequência
        def phase_at_x(x, step=0.01):
            points = np.arange(0, x+step, step)
            phases = [0]
            
            for i in range(1, len(points)):
                dx = points[i] - points[i-1]
                f1 = frequency_at_x(points[i-1]) * PI
                f2 = frequency_at_x(points[i]) * PI
                phases.append(phases[-1] + (f1 + f2) / 2 * dx)
                
            return phases[-1]
        
        # Função para calcular o valor da onda em qualquer ponto x
        def fm_wave(x):
            return np.sin(phase_at_x(x))
        
        # Frequências do cheat sheet (não mudam entre os flashcards)
        cheat_freqs = [1.5, 3.6, 5.0, 2.0, 6.0, 3.0]  # Correspondem a 1,2,3,4,5,6
        
        # Cheat sheet em uma única linha com animação
        cheat_sheet_entries = VGroup()
        mini_waves = VGroup()  # Guardar referências para as mini ondas para animar depois
        
        for i in range(6):
            entry = VGroup()
            
            # Retângulo ampliado para maior espaço
            bg = Rectangle(
                width=2.2,
                height=1.6,  # Aumentado para mais separação
                stroke_color=BLACK,
                stroke_width=1,
                fill_opacity=0
            )
            
            # Número movido mais para cima
            number = Text(f"{i+1}", font_size=20, color=BLACK)
            number.move_to(bg.get_top() + DOWN * 0.3)  # Movido para mais perto do topo
            
            # Indicador de frequência
            freq_text = Text(f"{cheat_freqs[i]:.1f}π Hz", font_size=14, color=BLACK)
            freq_text.move_to(bg.get_bottom() + UP * 0.2)
            
            # Mini onda centralizada com mais espaço
            mini_wave = VMobject()
            t = np.linspace(0, 1, 100)
            wave_points = []
            
            wave_y_center = bg.get_center()[1]  # Centralizado
            
            for ti in t:
                x = bg.get_left()[0] + 0.2 + ti * 1.8
                y = wave_y_center + 0.3 * np.sin(cheat_freqs[i] * PI * ti * 3)
                wave_points.append([x, y, 0])
            
            mini_wave.set_points_as_corners(wave_points)
            mini_wave.set_stroke(width=line_styles[i]["stroke_width"], color=BLACK)
            
            if dash_patterns[i] is not None:
                mini_wave.set_dash_pattern(dash_patterns[i])
            
            entry.add(bg, number, freq_text, mini_wave)
            
            entry.shift(RIGHT * (i * 2.6 - 6.5))
            entry.shift(DOWN * 3.5)
            
            # Guardar a mini onda para animação separada
            mini_waves.add(mini_wave)
            cheat_sheet_entries.add(entry)
        
        # Função para criar animações cíclicas para as mini ondas usando ValueTracker
        def create_wave_animation(wave_mob, freq):
            # Criar uma função de animação cíclica baseada na frequência
            def wave_updater(mob):
                t = self.renderer.time * 2  # Usando o tempo interno do renderer
                wave_points = []
                
                original_points = mob.get_points_defining_boundary()
                x_min = min(p[0] for p in original_points)
                x_max = max(p[0] for p in original_points)
                y_center = mob.get_center()[1]
                
                # Recalcular os pontos da onda com fase variando com o tempo
                points = np.linspace(0, 1, 100)
                for p in points:
                    x = x_min + p * (x_max - x_min)
                    # A fase adicional depende do tempo
                    y = y_center + 0.3 * np.sin(freq * PI * p * 3 + t * freq)
                    wave_points.append([x, y, 0])
                
                mob.set_points_as_corners(wave_points)
            
            return wave_updater
        
        # INÍCIO DA ANIMAÇÃO
        
        # 1. Mostrar título, eixos, grid, e cheat sheet de imediato
        self.add(title, axes, x_lines, y_lines, frame_rect, cheat_sheet_entries)
        
        # 2. Aplicar os updaters às mini ondas para que elas fiquem animando constantemente
        for i, wave in enumerate(mini_waves):
            wave.add_updater(create_wave_animation(wave, cheat_freqs[i]))
        
        # 3. Criar os segmentos da onda principal
        segment_plots = []
        for i in range(6):
            segment_plot = axes.plot(
                fm_wave,
                x_range=[i, i+1, 0.01],
                color=BLACK,
                **line_styles[i]
            )
            
            if dash_patterns[i] is not None:
                segment_plot.set_dash_pattern(dash_patterns[i])
                
            segment_plots.append(segment_plot)
        
        # 4. Desenhar cada segmento da onda principal em sequência para parecer contínuo
        # Total de 5 segundos para desenhar todos os segmentos
        segment_time = 5/6  # Tempo para cada segmento
        for i, segment in enumerate(segment_plots):
            self.play(
                Create(segment),
                run_time=segment_time,
                rate_func=linear  # Taxa linear para velocidade constante
            )
        
        # 5. Manter a visualização por mais 5 segundos depois que a onda estiver completa
        self.wait(5)
        
        # 6. Remover os updaters ao finalizar
        for wave in mini_waves:
            wave.clear_updaters()