from canvas import *
import color

cvs = canvas(width = 500, height = 500, title = 'test')
ctx = cvs.getContext('2d')
cvs.running = True
while cvs.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cvs.running = False
    ctx.fillStyle = color.white
    ctx.strokeStyle = color.dot_color['red']
    ctx.lineWidth = 10
    ctx.moveTo(50, 50)
    ctx.lineTo(50, 450)
    ctx.lineTo(350, 450)
    ctx.closePath()
    ctx.fill()
    ctx.stroke()
    pygame.display.update()
    pygame.time.Clock().tick(1000)
