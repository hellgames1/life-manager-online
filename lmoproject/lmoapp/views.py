from django.shortcuts import render, redirect
from lmoapp.models import Day, UserSettings
from datetime import datetime
from django.http import HttpResponse

# Create your views here.
def check(request):
    if request.method == 'GET' and 'd' in request.GET:
        d = request.GET['d']
        response = datetime.now().strftime("%H:%M:%S")
        if d!="c":
            response += "@"
            daypointer = Day.objects.filter(descr=d)[0].__dict__
            settingspointer = UserSettings.objects.all()[0].__dict__
            for i in range(1, 21):
                if settingspointer["val" + str(i) + "name"] != "":
                    response += str(daypointer["int"+str(i)])+"."
                else:
                    break
            response += daypointer["notes"]
        return HttpResponse(response)
    else:
        return HttpResponse("wtf")

def change(request):
    if request.method == 'GET' and 'day' in request.GET and 'var' in request.GET and 'val' in request.GET and 'y' in request.GET:
        day = request.GET['day']
        var = request.GET['var']
        val = request.GET['val']
        y = request.GET['y']
        now = datetime.now()
        currentday = now.strftime("%d%m%Y")
        if var == "notez":
            exec(f"Day.objects.filter(descr=day).update(notes='{val}')")
        else:
            exec(f"Day.objects.filter(descr=day).update(int{var}={val})")
        print(f"Changed value of variable #{var} to \"{val}\" for day {day}")
        if day != currentday:
            return redirect("/?v="+day+"&y="+y)
        else:
            return redirect("/?y="+y)
    else:
        return HttpResponse("Invalid request!")

def mainview(request):
    context = {}
    if request.method == 'GET' and 'v' in request.GET:
        currentday = request.GET['v']
        context["nottoday"]="yes"
    else:
        now = datetime.now()
        currentday = now.strftime("%d%m%Y")
    months_verbose = ["error","January","February","March","April","May","June","July","August","September","October","November","December"]
    date = int(currentday[:2])
    month = int(currentday[2:4])
    month_verbose = months_verbose[month]
    daypointer = Day.objects.filter(descr=currentday)[0].__dict__
    settingspointer = UserSettings.objects.all()[0].__dict__
    options=[]
    response = ""
    for i in range(1,21):
        if settingspointer["val"+str(i)+"name"] != "":
            options.append({"order": str(i), "name": settingspointer["val"+str(i)+"name"], "type"+str(settingspointer["val"+str(i)+"type"]): "yes", "val": daypointer["int"+str(i)], "valminus": daypointer["int"+str(i)]-1, "valplus": daypointer["int"+str(i)]+1, "valinverted": 1-daypointer["int"+str(i)]})
            response += str(daypointer["int" + str(i)]) + "."
        else:
            break
    response += daypointer["notes"]
    if daypointer["notes"]=="":
        context["note"]="<no notes>"
    else:
        context["note"]=daypointer["notes"]
    context["noteact"]=daypointer["notes"]
    context["now"] = str(date) + " " + month_verbose
    context["descr"] = currentday
    context["options"] = options
    context["jscheck"] = response
    if 'y' in request.GET:
        context["scrollto"]=request.GET['y']
    return render(request, 'view.html', context)

def calendar(request):
    now = datetime.now()
    nowstr = now.strftime("%d%m%Y")
    context = {}
    if request.method == 'GET' and 'calday' in request.GET:
        selected=request.GET['calday']
        context["nottoday"] = "yes"
    else:
        selected=nowstr
    months_verbose = ["error","January","February","March","April","May","June","July","August","September","October","November","December"]
    days=[]
    settingspointer = UserSettings.objects.all()[0].__dict__
    for day in list(Day.objects.all()):
        date = int(day.descr[:2])
        month = int(day.descr[2:4])
        month_verbose = months_verbose[month]
        notes = day.notes
        #year = int(day.descr[4:8])
        days.append({"descr": day.descr, "date": date, "month_verbose": month_verbose})
        if day.descr == nowstr:
            days[len(days)-1]["today"]="yes"
        if day.descr == selected:
            context["now"] = str(date) + " " + month_verbose
            days[len(days)-1]["selected"]="yes"
            if notes=="":
                context["notes"]="<no notes>"
            else:
                context["notes"]=notes
            listvars=""
            for i in range(1, 21):
                if settingspointer["val" + str(i) + "name"] != "":
                    name = settingspointer["val" + str(i) + "name"]
                    typpe = settingspointer["val" + str(i) + "type"]
                    value = day.__dict__["int" + str(i)]
                    if typpe == 4 and value == 0:
                        value = "no"
                    elif typpe == 4 and value == 1:
                        value = "yes"
                    if i % 2 != 0:
                        listvars += f"<tr><td>{name}: {value}</td>"
                    else:
                        listvars += f"<td>{name}: {value}</td></tr>"

                else:
                    break
            if listvars[-5:] == "</td>":
                listvars += "</tr>"
            context["listvars"] = listvars
        if notes != "":
            days[len(days)-1]["note"]="yes"
    if request.method == 'GET' and 'y' in request.GET:
        context["scrollto"]=request.GET['y']
    context["days"]=days
    context["descr"]=selected

    return render(request, 'calendar.html', context)
