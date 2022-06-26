'''
2022 © MaoHuPi
canvas.py v1.0.0
'''
import os
import pygame

textFont = './font.ttf'
class getContext2d:
    def __init__(self, canvas, lineWidth = 10, fillStyle = (255, 255, 255), strokeStyle = (0, 0, 0), font = '10px '+textFont):
        self.canvas = canvas
        self.lineWidth = lineWidth
        self.fillStyle = fillStyle
        self.strokeStyle = strokeStyle
        self.nowXY = [0, 0]
        self.font = font
        self.polygon_data = []
    def fillRect(self, x, y, w, h):
        pygame.draw.rect(self.canvas, self.fillStyle, [x, y, w, h], 0)
    def strokeRect(self, x, y, w, h):
        pygame.draw.rect(self.canvas, self.strokeStyle, [x, y, w, h], int(self.lineWidth))
    def fillText(self, t, x, y, againstX = 'left', againstY = 'top', fontType = 'sys'):
        font = self.font.split()
        flag = len(font) == 3
        b = font[0] == 'bg' if flag else False
        s = int(font[1].replace('px', '')) if flag else int(font[0].replace('px', ''))
        f = font[2] if flag else font[1]
        font = pygame.font.SysFont(f, s) if fontType != 'file' else pygame.font.Font(f, s)
        size = {'w':0, 'h':0}
        size['w'], size['h'] = font.size(t)
        addX = size['w'] if againstX == 'right' else size['w']/2 if againstX == 'center' else 0
        addY = size['h'] if againstY == 'bottom' else size['h']/2 if againstY == 'center' else 0
        if b:
            self.canvas.blit(font.render(t, True, self.fillStyle, self.strokeStyle), (int(x-addX), int(y-addY)))
        else:
            self.canvas.blit(font.render(t, True, self.fillStyle), (int(x-addX), int(y-addY)))
    def drawImage(self, i, xy, wh = False, a = False):
        if wh:
            i = pygame.transform.scale(i, (int(wh[0]), int(wh[1])))
        if a:
            i.set_alpha(a)
        self.canvas.blit(i, (int(xy[0]), int(xy[1])))
    def fillBox(self, x, y, w, h, r):
        pygame.draw.rect(self.canvas, self.fillStyle, [x+r, y, w-2*r, h], 0)
        pygame.draw.rect(self.canvas, self.fillStyle, [x, y+r, w, h-2*r], 0)
        pygame.draw.circle(self.canvas, self.fillStyle, (x+r, y+r), r, 0)
        pygame.draw.circle(self.canvas, self.fillStyle, (x+r, y+h-r), r, 0)
        pygame.draw.circle(self.canvas, self.fillStyle, (x+w-r, y+r), r, 0)
        pygame.draw.circle(self.canvas, self.fillStyle, (x+w-r, y+h-r), r, 0)
    def strokeBox(self, x, y, w, h, r):
        lw = self.lineWidth
        pygame.draw.line(self.canvas, self.strokeStyle, (x+r+lw, y), (x+w-2*r+lw, y), int(self.lineWidth))
        pygame.draw.line(self.canvas, self.strokeStyle, (x+w, y+r+lw), (x+w, y+h-2*r+lw), int(self.lineWidth))
        pygame.draw.line(self.canvas, self.strokeStyle, (x+w-2*r+lw, y+h), (x+r+lw, y+h), int(self.lineWidth))
        pygame.draw.line(self.canvas, self.strokeStyle, (x, y+h-2*r+lw), (x, y+r+lw), int(self.lineWidth))
    def moveTo(self, x = 'old', y = 'old'):
        x = x if x != 'old' else self.nowXY[0]
        y = y if y != 'old' else self.nowXY[1]
        self.nowXY = [x, y]
        self.polygon_data.append({'x':x, 'y':y, 'draw':False})
    def lineTo(self, x, y, drawLine = False):
        x = x if x != 'old' else self.nowXY[0]
        y = y if y != 'old' else self.nowXY[1]
        if drawLine:
            pygame.draw.line(self.canvas, self.strokeStyle, (self.nowXY[0], self.nowXY[1]), (x, y), int(self.lineWidth))
        self.nowXY = [x, y]
        self.polygon_data.append({'x':x, 'y':y, 'draw':True})
    def stroke(self):
        if len(self.polygon_data) > 1:
            for i in range(0, len(self.polygon_data)-1):
                if self.polygon_data[i+1]['draw']:
                    pygame.draw.line(self.canvas, self.strokeStyle, (self.polygon_data[i]['x'], self.polygon_data[i]['y']), (self.polygon_data[i+1]['x'], self.polygon_data[i+1]['y']), int(self.lineWidth))
    def fill(self):
        if len(self.polygon_data) > 1:
            polygons = []
            for i in range(0, len(self.polygon_data)):
                polygons.append([self.polygon_data[i]['x'], self.polygon_data[i]['y']])
            pygame.draw.polygon(self.canvas, self.fillStyle, polygons)
    def beginPath(self):
        self.polygon_data = []
    def closePath(self):
        self.polygon_data.append({'x':self.polygon_data[0]['x'], 'y':self.polygon_data[0]['y'], 'draw':True})

class canvas:
    def __init__(self, width = 0, height = 0, bgc = (0, 0, 0), title = '', icon = '', initNow = True):
        self.this = False
        self.width = width
        self.height = height
        self.bgc = bgc
        self.running = False
        self.title = title
        self.getContex2d = False
        self.alpha = pygame.Surface((width, height), pygame.SRCALPHA)
        self.alpha_getContex2 = False
        self.icon = icon
        if initNow:
            self.init()
    def init(self):
        self.this = pygame.display.set_mode((int(self.width), int(self.height)), pygame.RESIZABLE)
        if type(self.icon) == type('') and os.path.exists(self.icon):
            self.icon = pygame.image.load(self.icon)
            pygame.display.set_icon(self.icon)
        pygame.display.set_caption(self.title)
        self.getContex2d = getContext2d(canvas = self.this)
        self.alpha_getContex2d = getContext2d(canvas = self.alpha)
    def draw_Background(self):
        self.this.fill(self.bgc)
    def getContext(self, type:str):
        type = type.lower()
        if type == '2d':
            return(self.getContex2d)
        else:
            if type == 'webgl' or type == 'gl':
                print('不支援 webGL！')
            return(False)
