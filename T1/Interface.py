
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
*  Trabalho 1: BUSCA HEURÍSTICA E BUSCA LOCAL
*  INF1771 - INTELIGÊNCIA ARTIFICIAL
* 
*  Autores: Luiz Arthur Meira - 1512570
*
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from asyncio.windows_events import NULL
from colour import Color
import pygame

pygame.init()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* PARAMETROS GLOBAIS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

PLANO = (225, 198, 153)
ROCHOSO = (155, 103, 60)
AGUA = (0, 0, 255)
MONTANHOSO = (150, 150, 150)
FLORESTA = (0, 128, 0)
PONTOS = (255, 0, 0)
BUSCA = (214, 0, 110)
CAMINHO = (40, 40, 40)

TERRENOS = {
  ".": PLANO,
  "R": ROCHOSO,
  "F": FLORESTA,
  "A": AGUA,
  "M": MONTANHOSO
}

PERSONAGENS = ['Aang','Zukko','Toph','Katara','Sokka','Appa','Momo']

BORDER_BOTTOM = 260

font = pygame.font.SysFont(pygame.font.get_fonts()[2], 18)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* INTERFACE
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Interface:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h+BORDER_BOTTOM
        self.blockW = w/300
        self.blockH = h/82
        self.display= pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('TRABALHO 1 – BUSCA HEURÍSTICA E BUSCA LOCAL')
        self.clock = pygame.time.Clock()
    
    def add_map(self, map):
        self.map = map
    
    def add_percorreu(self, percorreu):
        self.percorreu = percorreu
    
    def add_andou(self, path):
        self.andou = path

    def add_steps(self, steps):
        self.steps = steps
    
    def update(self,percorreu, path, step, custos):
        self.add_percorreu(percorreu)
        self.add_andou(path)
        self._update_ui(step, custos)
        self.clock.tick(100)
    
    def _update_ui(self, step, custos):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self.display.fill(AGUA)

        image = pygame.image.load(r'background.png')
        self.display.blit(image, (0, 574))
        
        
        
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.percorreu[i][j] != 0:
                    pygame.draw.rect(self.display, BUSCA, pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
                else:
                    terrain = self.map[i][j]
                    if terrain in ['.', 'R', 'F', 'A', 'M']:
                        pygame.draw.rect(self.display, TERRENOS[terrain], pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
                    else:
                        pygame.draw.rect(self.display, PONTOS, pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
        for ponto in self.andou:
            pygame.draw.rect(self.display, CAMINHO, pygame.Rect(ponto[1]*self.blockW, ponto[0]*self.blockH, self.blockW, self.blockH))
        s = ""
        for i in range(31):
            if i != 0 and i%4 == 0:
                s += "\n"
            if i < len(custos):
                custo = custos[i]
                s += "Etapa "+ str(i+1).zfill(2)+": "+ str(int(custo)).zfill(3)+"  "
            else:
                s += "Etapa "+ str(i+1).zfill(2)+": 0  "
        s = s.split("\n")
        linhas = []
        for linha in s:
            linhas.append(font.render(linha, True, (0,0,0)))
        for i in range(len(linhas)):
            self.display.blit(linhas[i], [490, 600+ i*30])
        pygame.display.flip()
    
    def finish(self, path):
        self.add_andou(path)
        count = 0
        for etapa in self.andou:
            count += len(etapa)
        self.add_steps(count)
        self.update_finish()
        self.clock.tick(100)
    
    def update_finish(self, participants = NULL, custos = 0, dificuldade = 0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
       
        self.display.fill((255,255,255))

        image = pygame.image.load(r'background.png')
        self.display.blit(image, (0, 574))

        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                terrain = self.map[i][j]
                if terrain in ['.', 'R', 'F', 'A', 'M']:
                    pygame.draw.rect(self.display, TERRENOS[terrain], pygame.Rect(j*self.blockW, i*self.blockH, self.blockW, self.blockH))
        count = 0
        for etapa in self.andou:
            for ponto in etapa:
                pygame.draw.rect(self.display, PONTOS, pygame.Rect(ponto[1]*self.blockW, ponto[0]*self.blockH, self.blockW, self.blockH))
                count += 1
        if (participants != NULL):
            custo = 0
            s = ""
            for i in range(len(custos)):
                custo += custos[i]
            for i in range(7):
                s += PERSONAGENS[i]
                s += ": "
                for j, val in enumerate(participants[i]):
                    if val == 1:
                        s += str(j+1) + "  "
                s += "\n"
            s = s.split("\n")
            linhas = []
            for linha in s:
                linhas.append(font.render(linha, True, (0,0,0)))
            for i in range(len(linhas)):
                self.display.blit(linhas[i], [490, 600+i*30])
            self.display.blit(font.render("Total: {:}, {:.6f}".format(int(custo), dificuldade), True, (0,0,0)), [490, 810])
        pygame.display.flip()
