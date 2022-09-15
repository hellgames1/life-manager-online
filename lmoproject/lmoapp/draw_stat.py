from lmoapp.models import Day, UserSettings
from PIL import Image, ImageDraw, ImageFont, ImageOps
from math import floor, ceil
from django.http import HttpResponse
def image_stat(request):
    if request.method=="GET" and "trackval" in request.GET and "f" in request.GET and "t" in request.GET:
        object_pointer = list(Day.objects.filter(id__gte=int(request.GET['f']),id__lte=int(request.GET['t'])))
        settingspointer = UserSettings.objects.all()[0].__dict__
        text = settingspointer["val"+request.GET['trackval']+"name"]
        data = []
        titles = []
        months_verbose = ["error","January","February","March","April","May","June","July","August","September","October","November","December"]
        for obj in object_pointer:
            date = obj.descr[:2]
            month_verbose = months_verbose[int(obj.descr[2:4])]
            titles.append(f"{date} {month_verbose}")
            data.append(obj.__dict__["int"+request.GET['trackval']])

        print(len(data))
        spacing = int(980/len(data))
        width = int(980/len(data)/2)
        height = 780/max(data)
        offset = int(100+width/2)
        print(width)
        lines = list(range(0,ceil(max(data))+1))
        while len(lines)>44:
            lines = lines[0::2]

        img = Image.new('RGB', (1080, 1080), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('calibri.ttf', 72)
        font_small = ImageFont.truetype('calibri.ttf', 24)
        font_extrasmall = ImageFont.truetype('calibri.ttf', 16)

        if len(data)>44:
            usefont = font_extrasmall
        else:
            usefont = font_small


        draw.text((540-font.getlength(text)/2, 10), text,fill="black", font=font)
        for i in lines:
            draw.line((50, 880 - i * height, 1080,880 - i * height) , fill=(127, 127, 127), width=1)
            draw.text((40-font_small.getlength(str(i)), 870 - i * height), str(i),fill=(127, 127, 127), font=font_small)
        for i in range(len(data)):
            draw.line((offset+spacing*i, 880, offset+spacing*i, 880-data[i]*height), fill=(68, 114, 196), width=width)
            txt = Image.new('RGB', usefont.getsize(titles[i]),(255,255,255))
            d = ImageDraw.Draw(txt)
            d.text((0, 0), titles[i], font=usefont, fill="black")
            w = txt.rotate(90, expand=1)
            img.paste(w, (offset-8+spacing*i, 900))
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response
    else:
        return HttpResponse("invalid request")