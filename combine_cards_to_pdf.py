import os
from PIL import Image
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas

# Configurações
IMAGES_DIR = "manimations/media/images/bilhete_flashcard/"  # caminho corrigido
OUTPUT_PDF = "bilhetes_flashcards.pdf"
IMAGES_PER_PAGE = 4

# Tamanho da página (A4 paisagem)
PAGE_WIDTH, PAGE_HEIGHT = landscape(A4)

# Tamanho e posições dos cartões (2x2)
CARD_WIDTH = PAGE_WIDTH / 2
CARD_HEIGHT = PAGE_HEIGHT / 2
POSITIONS = [
    (0, PAGE_HEIGHT / 2),
    (CARD_WIDTH, PAGE_HEIGHT / 2),
    (0, 0),
    (CARD_WIDTH, 0),
]

def get_image_files(directory):
    # Ordena numericamente pelo número final antes da extensão
    def extract_number(filename):
        import re
        # Busca o número antes da extensão (ex: bilhete_flashcard_10.png -> 10)
        match = re.search(r'_(\d+)\.[a-zA-Z]+$', filename)
        return int(match.group(1)) if match else float('inf')
    files = [
        f for f in os.listdir(directory)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    files = list(set(files))  # Remove duplicatas, se houver
    files.sort(key=extract_number)
    return [os.path.join(directory, f) for f in files]

def main():
    image_files = get_image_files(IMAGES_DIR)
    if not image_files:
        print("Nenhuma imagem encontrada.")
        return

    c = canvas.Canvas(OUTPUT_PDF, pagesize=landscape(A4))

    for i in range(0, len(image_files), IMAGES_PER_PAGE):
        batch = image_files[i:i+IMAGES_PER_PAGE]
        for idx, img_path in enumerate(batch):
            img = Image.open(img_path)
            # Garante que a imagem está em PNG temporário (ReportLab lida melhor com PNG)
            if img_path.lower().endswith('.png'):
                temp_path = img_path
            else:
                temp_path = f"_temp_{idx}.png"
                img.save(temp_path)
            x, y = POSITIONS[idx]
            # O ReportLab redimensiona a imagem para caber no espaço do cartão
            c.drawImage(temp_path, x, y, width=CARD_WIDTH, height=CARD_HEIGHT, preserveAspectRatio=True, anchor='c')
            if not img_path.lower().endswith('.png'):
                os.remove(temp_path)
        c.showPage()
    c.save()
    print(f"PDF gerado: {OUTPUT_PDF}")

if __name__ == "__main__":
    main()
