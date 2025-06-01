# Jogo Instrumentação — Flashcards de Ondas (Manim)

Este repositório contém scripts em Python para gerar animações de flashcards de ondas utilizando a biblioteca [Manim](https://www.manim.community/). Os arquivos principais são:

- `bilhete_flashcard_1_animation.py`: Gera a animação do flashcard 1.
- `bilhete_flashcard.py`: Lógica e estilos compartilhados para os flashcards.
- `sine_wave_code.py`: Utilitário para ondas senoidais.

## Estrutura de Pastas

- `media/`: Pasta onde o Manim salva as mídias renderizadas (vídeos, imagens, SVGs, etc). Está no `.gitignore` e não é versionada.
- `manimations/`: Pode conter projetos ou scripts auxiliares.
- `__pycache__/`: Cache do Python (ignorado pelo git).

## Pré-requisitos

- Python 3.8+
- [Manim Community Edition](https://docs.manim.community/en/stable/installation.html)

Recomenda-se criar um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install manim
```

## Como Renderizar as Animações

Para renderizar um dos scripts (por exemplo, o flashcard 1):

```bash
manim bilhete_flashcard_1_animation.py FlashcardAnimation -pql
```

- `-pql`: Renderiza em qualidade baixa e abre o vídeo automaticamente.
- Para qualidade alta, use `-pqh`.

Os arquivos renderizados serão salvos na pasta `media/`.

### Renderizando Todos os Flashcards de Uma Só Vez

Se você possui vários flashcards, pode renderizar todos de uma vez com o comando abaixo (execute dentro da pasta `manimations`):

```bash
cd manimations
for i in {1..10}; do \
  FLASHCARD_NUMBER=$i uv run manim -qh ../bilhete_flashcard.py FlashcardLayout -o bilhete_flashcard_$i; \
done
```

Esse comando utiliza a variável de ambiente `FLASHCARD_NUMBER` para renderizar cada flashcard individualmente, salvando os arquivos de saída com nomes distintos.

> Obs: O comando `uv run` é utilizado para ambientes gerenciados pelo [uv](https://github.com/astral-sh/uv), mas você pode substituir por `python` ou `manim` diretamente, conforme seu ambiente.

## Dicas

- Edite os scripts para criar novos flashcards ou modificar estilos.
- O arquivo `.gitignore` já está configurado para evitar o upload de arquivos grandes e mídias renderizadas.

## Licença

Este projeto é apenas para fins educacionais. Sinta-se livre para modificar e adaptar!
