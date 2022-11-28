import cv2 as cv
import pytesseract as ocr
import os
import sys
from PIL import Image
import numpy as np

# folder = r"D:\OCR\imagens\1"


def transcrever(folder, name):

    with open(fr'D:\OCR\imagens\txt\{name}.txt', 'w', encoding='utf-8') as wf1:

        for img in os.listdir(folder):

            foto1 = f"{folder}\{img}"

            # tipando a leitura para os canais de ordem RGB
            imagem = Image.open(foto1).convert('RGB')

            # convertendo em um array editável de numpy[x, y, CANALS]
            npimagem = np.asarray(imagem).astype(np.uint8)

            # diminuição dos ruidos antes da binarização
            npimagem[:, :, 0] = 0  # zerando o canal R (RED)

            npimagem[:, :, 2] = 0  # zerando o canal B (BLUE)

            # atribuição em escala de cinza
            im = cv.cvtColor(npimagem, cv.COLOR_RGB2GRAY)

            # aplicação da truncagem binária para a intensidade
            # pixels de intensidade de cor abaixo de 127 serão convertidos para 0 (PRETO)
            # pixels de intensidade de cor acima de 127 serão convertidos para 255 (BRANCO)
            # A atrubição do THRESH_OTSU incrementa uma análise inteligente dos nivels de truncagem
            ret, thresh = cv.threshold(
                im, 127, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

            # reconvertendo o retorno do threshold em um objeto do tipo PIL.Image
            binimagem = Image.fromarray(thresh)

            # foto = cv.imread(binimagem)

            resultado = ocr.image_to_string(binimagem, lang='por')

            wf1.write(f"-----{img}-----\n")

            wf1.write(resultado + '\n\n')

    return "finished"


if __name__ == "__main__":
    folder = sys.argv[1]
    name = sys.argv[2]

    transcrever(folder, name)
