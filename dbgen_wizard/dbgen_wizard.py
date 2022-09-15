import pygame
pygame.init()

screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Database Generation Wizard")
font = pygame.font.Font(None, 32)
font_large = pygame.font.Font(None, 64)
font_small = pygame.font.Font(None, 16)
input_box = pygame.Rect(120, 100, 440, 32)
active = 0
text=""
text2=""
typeselected = 1
decimalselected = 0
behaviourselected=0
frame = 0
running = True
editing = 1
arr = []
blinker1=""
blinker2=""
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 500)
type1show = []
type2show = []
type3show = []
type4show = []
description = ["+ and - button increase and decrease by 1",
               "+ and - button decrease/increase by entered amount",
               "press on the field and edit the value directly",
               "just a checkbox, can either be checked or unchecked"]
for i in range(20):
    type1show.append(pygame.image.load(f'type1_{i}.png'))
    type2show.append(pygame.image.load(f'type2_{i}.png'))
    type3show.append(pygame.image.load(f'type3_{i}.png'))
    type4show.append(pygame.image.load(f'type4_{i}.png'))
    arr.append([text, typeselected, decimalselected, behaviourselected, text2])

arr.append([text, typeselected, decimalselected, behaviourselected, text2])
def finish():
    global running
    finalarr = []
    for item in arr:
        if item[0] != "" and item[4] != "":
            finalarr.append(item)

    exitstring=""
    for index, item in enumerate(finalarr):
        typ = -1
        keep = "error"
        done = "error"
        if item[1]==1:
            typ = 1
        elif item[1]==2 and item[2]==0:
            typ = 2
        elif item[1]==2 and item[2]==1:
            typ = 3
        elif item[1]==2 and item[2]==2:
            typ = 4
        elif item[1]==3 and item[2]==0:
            typ = 5
        elif item[1]==3 and item[2]==1:
            typ = 6
        elif item[1]==3 and item[2]==2:
            typ = 7
        elif item[1]==4:
            typ = 8
        if item[3] == 0:
            keep = "no"
        elif item[3] == 1:
            keep = "yes"
        if index == len(finalarr)-1:
            done = "yes"
        else:
            done = "no"
        exitstring+=f"{item[0]}\n{typ}\n{keep}\n{item[4]}\n{done}\n"
        f = open("COPYTHIS.txt", "w")
        towrite = exitstring
        f.write(towrite)
        f.close()
        import webbrowser
        webbrowser.open("COPYTHIS.txt")
        running = False

while running:
    if frame < 19:
        frame += 1
    else:
        frame = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = 1
            elif pygame.Rect(210,390,40,40).collidepoint(event.pos):
                if typeselected != 4:
                    active = 2
                else:
                    text2 = str(1-int(text2))
            else:
                active = 0
                blinker1 = ""
                blinker2 = ""

            if pygame.Rect(200,540,100,40).collidepoint(event.pos):
                arr[editing-1] = [text,typeselected,decimalselected,behaviourselected,text2]
            elif pygame.Rect(425,540,100,40).collidepoint(event.pos):
                finish()
            for i in range(20):
                if pygame.Rect(600, i*30, 200, 30).collidepoint(event.pos):
                    editing = i+1
                    text = arr[i][0]
                    text2 = arr[i][4]
                    typeselected = arr[i][1]
                    decimalselected = arr[i][2]
                    behaviourselected = arr[i][3]
                if arr[i][0]=="" or arr[i][4]=="":
                    break

            if pygame.Rect(110,160,100,40).collidepoint(event.pos):
                typeselected = 1
                decimalselected = 0
                frame = 0
                text2 = ""
            elif pygame.Rect(230,160,100,40).collidepoint(event.pos):
                typeselected = 2
                frame = 0
                text2 = ""
            elif pygame.Rect(110,220,100,40).collidepoint(event.pos):
                typeselected = 3
                frame = 0
                text2 = ""
            elif pygame.Rect(230,220,100,40).collidepoint(event.pos):
                typeselected = 4
                decimalselected = 0
                text2 = "0"
                frame = 0
            elif pygame.Rect(160,450,100,40).collidepoint(event.pos):
                behaviourselected=0
            elif pygame.Rect(270,450,100,40).collidepoint(event.pos):
                behaviourselected=1
            if typeselected == 2 or typeselected == 3:
                if pygame.Rect(210,330,100,40).collidepoint(event.pos):
                    decimalselected = 0
                elif pygame.Rect(330,330,100,40).collidepoint(event.pos):
                    decimalselected = 1
                elif pygame.Rect(450,330,100,40).collidepoint(event.pos):
                    decimalselected = 2
        if event.type == pygame.USEREVENT:
            if blinker1=="|":
                blinker1=""
            elif active==1:
                blinker1="|"
            if blinker2=="|":
                blinker2=""
            elif active==2:
                blinker2="|"
        if event.type == pygame.KEYDOWN:
            if active==1:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key != pygame.K_RETURN:
                    text += event.unicode
            elif active==2:
                if event.key == pygame.K_BACKSPACE:
                    text2 = text2[:-1]
                elif event.key != pygame.K_RETURN:
                    text2 += event.unicode
    screen.fill((255, 255, 255))

    title_surface = font_large.render(f"Value #{editing}", True, (0,0,0))
    screen.blit(title_surface, (220,20))

    screen.blit(font.render("Name:", True, (0,0,0)), (input_box.x - 75, input_box.y + 5))
    txt_surface = font.render(text+blinker1, True, (0,0,0))
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, (0,0,0), input_box, 2)

    screen.blit(font.render("Type:", True, (0,0,0)), (20,200))
    if typeselected == 1:
        pygame.draw.rect(screen, (255,0,0), (110,160,100,40), 2)
    else:
        pygame.draw.rect(screen, (0,0,0), (110,160,100,40), 2)
    screen.blit(font.render("1", True, (0,0,0)), (150,170))
    if typeselected == 2:
        pygame.draw.rect(screen, (255,0,0), (230,160,100,40), 2)
    else:
        pygame.draw.rect(screen, (0,0,0), (230,160,100,40), 2)
    screen.blit(font.render("2", True, (0,0,0)), (270,170))
    if typeselected == 3:
        pygame.draw.rect(screen, (255,0,0), (110,220,100,40), 2)
    else:
        pygame.draw.rect(screen, (0,0,0), (110,220,100,40), 2)
    screen.blit(font.render("3", True, (0,0,0)), (150,230))
    if typeselected == 4:
        pygame.draw.rect(screen, (255,0,0), (230,220,100,40), 2)
    else:
        pygame.draw.rect(screen, (0,0,0), (230,220,100,40), 2)
    screen.blit(font.render("4", True, (0,0,0)), (270,230))

    pygame.draw.rect(screen, (0,0,0), (348,148,234,124), 2)
    if typeselected==1:
        screen.blit(type1show[frame],(350,150))
    elif typeselected==2:
        screen.blit(type2show[frame],(350,150))
    elif typeselected==3:
        screen.blit(type3show[frame],(350,150))
    elif typeselected==4:
        screen.blit(type4show[frame],(350,150))
    screen.blit(font.render(description[typeselected-1], True, (0,0,0)), (20,280))

    screen.blit(font.render("Decimal places:", True, (0,0,0)), (20,340))
    if decimalselected == 0:
        pygame.draw.rect(screen, (255,0,0), (210,330,100,40), 2)
    else:
        pygame.draw.rect(screen, (0,0,0), (210,330,100,40), 2)
    screen.blit(font.render("0", True, (0,0,0)), (250,340))
    if typeselected == 2 or typeselected == 3:
        if decimalselected == 1:
            pygame.draw.rect(screen, (255,0,0), (330,330,100,40), 2)
        else:
            pygame.draw.rect(screen, (0,0,0), (330,330,100,40), 2)
        screen.blit(font.render("0.1", True, (0,0,0)), (365,340))
        if decimalselected == 2:
            pygame.draw.rect(screen, (255,0,0), (450,330,100,40), 2)
        else:
            pygame.draw.rect(screen, (0,0,0), (450,330,100,40), 2)
        screen.blit(font.render("0.01", True, (0,0,0)), (480,340))


    screen.blit(font.render("Default value:", True, (0,0,0)), (20,400))
    pygame.draw.rect(screen, (0,0,0), (210,390,40,40), 2)
    txt_surface = font.render(text2+blinker2, True, (0,0,0))
    screen.blit(txt_surface, (215, 400))

    screen.blit(font.render("Behaviour:", True, (0,0,0)), (20,460))
    if behaviourselected==0:
        pygame.draw.rect(screen, (255,0,0), (160,450,100,40), 2)
    else:
        pygame.draw.rect(screen, (0,0,0), (160,450,100,40), 2)
    screen.blit(font_small.render("Start every day", True, (0, 0, 0)), (170, 458))
    screen.blit(font_small.render("at default value", True, (0, 0, 0)), (170, 468))
    if behaviourselected==1:
        pygame.draw.rect(screen, (255,0,0), (270,450,100,40), 2)
    else:
        pygame.draw.rect(screen, (0,0,0), (270,450,100,40), 2)
    screen.blit(font_small.render("Maintain value", True, (0, 0, 0)), (280, 458))
    screen.blit(font_small.render("from previous day", True, (0, 0, 0)), (272, 468))


    pygame.draw.rect(screen, (0,0,0), (200,540,100,40), 2)
    if arr[editing-1] != [text, typeselected, decimalselected, behaviourselected, text2]:
        screen.blit(font.render("Save*", True, (255,0,0)), (225,550))
    else:
        screen.blit(font.render("Save", True, (0,0,0)), (225,550))
    pygame.draw.rect(screen, (0,0,0), (425,540,100,40), 2)
    screen.blit(font.render("Finish", True, (0,0,0)), (450,550))


    for i in range(20):
        if i+1 == editing:
            pygame.draw.rect(screen, (255, 0, 0), (600, i*30, 200, 30), 2)
        else:
            pygame.draw.rect(screen, (0, 0, 0), (600, i*30, 200, 30), 2)
        if arr[i][0]=="" or arr[i][4]=="":
            screen.blit(font_small.render(f"{i+1}. <undefined>", True, (0, 0, 0)), (605, i*30+8))
            break
        else:
            screen.blit(font_small.render(f"{i+1}. {arr[i][0]}", True, (0, 0, 0)), (605, i*30+8))
    pygame.display.flip()
    clock.tick(7)

pygame.quit()