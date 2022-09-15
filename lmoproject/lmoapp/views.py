from django.shortcuts import render, redirect
from lmoapp.models import Day, UserSettings
from datetime import datetime
from django.http import HttpResponse
from lmoapp.credentials import default_username, default_password

# Create your views here.
def login_check(request):
    return "username" in request.session and "password" in request.session and request.session["username"] == default_username and request.session["password"]==default_password

def check(request):
    if login_check(request):
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
    else:
        return redirect("/login")

def change(request):
    if login_check(request):
        if request.method == 'GET' and 'day' in request.GET and 'var' in request.GET and 'val' in request.GET and 'y' in request.GET:
            day = request.GET['day']
            var = request.GET['var']
            val = request.GET['val']
            y = request.GET['y']
            now = datetime.now()
            currentday = now.strftime("%d%m%Y")
            keep = UserSettings.objects.all()[0].__dict__["val"+var+"keep"]
            daypointer = Day.objects.filter(descr=day)
            if var == "notez":
                exec(f"daypointer.update(notes='{val}')")
            else:
                exec(f"daypointer.update(int{var}={val})")
            #print(Day.objects.filter(id__gt=2))
            print(f"Changed value of variable #{var} to \"{val}\" for day {day}")
            if keep == 1:
                exec(f"Day.objects.filter(id__gt=daypointer[0].id).update(int{var}={val})")
                print("Also updated all days after that!")
            if day != currentday:
                return redirect("/?v="+day+"&y="+y)
            else:
                return redirect("/?y="+y)
        else:
            return HttpResponse("Invalid request!")
    else:
        return redirect("/login")

def mainview(request):
    if login_check(request):
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
                value = daypointer["int"+str(i)]
                typpe = settingspointer["val"+str(i)+"type"]
                if typpe == 1 or typpe == 2 or typpe == 5 or typpe == 8:
                    value = f"{value:.0f}"
                elif typpe == 3 or typpe == 6:
                    value = f"{value:.1f}"
                elif typpe == 4 or typpe == 7:
                    value = f"{value:.2f}"
                if typpe == 3 or typpe == 4:
                    typpe = 2
                elif typpe == 6 or typpe == 7:
                    typpe = 3
                elif typpe == 8:
                    typpe = 4
                ivalue = int(float(value))
                options.append({"order": str(i), "name": settingspointer["val"+str(i)+"name"], "type"+str(typpe): "yes", "val": value, "valminus": ivalue-1, "valplus": ivalue+1, "valinverted": 1-ivalue})
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
    else:
        return redirect("/login")

def calendar(request):
    if login_check(request):
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
                        if typpe == 1 or typpe == 2 or typpe == 5 or typpe == 8:
                            value = f"{value:.0f}"
                        elif typpe == 3 or typpe == 6:
                            value = f"{value:.1f}"
                        elif typpe == 4 or typpe == 7:
                            value = f"{value:.2f}"
                        if typpe == 8 and value == "0":
                            value = "no"
                        elif typpe == 8 and value == "1":
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
    else:
        return redirect("/login")
def login(request):
    if request.method == 'POST' and 'username' in request.POST and 'password' in request.POST:
        request.session["username"] = request.POST["username"]
        request.session["password"] = request.POST["password"]
        return redirect("/")
    else:
        return render(request,'login.html')