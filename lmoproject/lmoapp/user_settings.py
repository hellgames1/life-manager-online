from lmoapp.models import Day, UserSettings
from datetime import datetime
from django.http import HttpResponse
def br():
    print("####################################################################################")
    print("####################################################################################")
def do_user_settings(request):
    if len(Day.objects.all()) > 0:
        if input("You currently have a database set up! This will DELETE your current database! Are you sure? (yes/no) ")=="yes":
            for instance in Day.objects.all():
                instance.delete()
            for instance in UserSettings.objects.all():
                instance.delete()
            print("Deleted all entries! Now open /setup again to create a new database!")
        return HttpResponse("Done!")
    else:
        value_names=[]
        value_types=[]
        value_keeps=[]
        value_defaults=[]
        count = 0
        while True:
            br()
            print(f"Value #{count+1}:")
            value_name=input("Choose name for this value: ")
            br()
            print("Value types can be\n1) Number (+ and - button change value by 1)\n2) Number (+ and - button change value by entered amount)\n3) Number (absolute value is editable)\n4) Box (checked/unchecked)")
            value_type=int(input(f"Choose type for \"{value_name}\": "))
            br()
            print("Do you want floating value?\nno) the value is reset to default for each day\nyes) the value from the end of the day is carried over to the next day")
            tempkeep = input()
            if tempkeep == "yes":
                value_keep=1
            else:
                value_keep=0
            br()
            print(f"What should be the default value for \"{value_name}\"?")
            if value_type == 4:
                print("1 is checked and 0 is unchecked")
            value_default=int(input())
            count += 1
            value_names.append(value_name)
            value_types.append(value_type)
            value_keeps.append(value_keep)
            value_defaults.append(value_default)
            br()
            if count == 20:
                print("All possible 20 values to track are completed! Continuing setup...")
                br()
                break
            else:
                if input(f"You have {20-count} remaining empty spaces! Are you finished adding values? (yes/no) ")=="yes":
                    print("Continuing setup...")
                    br()
                    break
        usersettings = UserSettings()
        for i in range(1,len(value_names)+1):
            exec('usersettings.val'+str(i)+'name = "'+str(value_names[i-1])+'"')
            exec('usersettings.val'+str(i)+'type = '+str(value_types[i-1]))
            exec('usersettings.val'+str(i)+'keep = '+str(value_keeps[i-1]))
            exec('usersettings.val'+str(i)+'default = '+str(value_defaults[i-1]))
        usersettings.save()
        now = datetime.now()
        nowstr = now.strftime("%d%m%Y")
        print("You will now have to enter the beginning date. The first date should be on a monday so if it's not, it will be changed to the last monday before it.\nThe earliest date possible is 3rd of January 2022")
        progress = [3,1,2022]
        weekday = 1
        date = int(input("First enter the day (1-31) "))
        month = int(input("Now enter the month (1-12) "))
        year = int(input("Now enter the year (2022-9999) "))
        lastmonday = [-1,-1,-1]
        while progress != [date,month,year]:
            cdate = progress[0]
            cmonth = progress[1]
            cyear = progress[2]
            cdate += 1
            if weekday < 7:
                weekday += 1
            else:
                weekday = 1
            if (cmonth == 1 or cmonth==3 or cmonth==5 or cmonth==7 or cmonth==8 or cmonth==10) and cdate == 32:
                cmonth +=1
                cdate = 1
            elif cmonth == 12 and cdate == 32:
                cmonth = 1
                cdate = 1
                cyear += 1
            elif (cmonth == 4 or cmonth==6 or cmonth==9 or cmonth==11) and cdate == 31:
                cmonth +=1
                cdate = 1
            elif cmonth == 2 and ((cyear % 4 == 0 and cdate == 30) or (cyear % 4 != 0 and cdate==29)):
                cmonth +=1
                cdate = 1
            progress = [cdate,cmonth,cyear]
            if weekday == 1:
                lastmonday = progress
        if weekday==1:
            print(f"{date:02d}.{month:02d}.{year} is a monday! This will be the first day of the database.")
        else:
            weekdays = ["","","tuesday","wednesday","thursday","friday","saturday","sunday"]
            print(f"{date:02d}.{month:02d}.{year} is a {weekdays[weekday]}! Reverting back {weekday-1} days to ",end="")
            date = lastmonday[0]
            month = lastmonday[1]
            year = lastmonday[2]
            print(f"{date:02d}.{month:02d}.{year}! This will be the first day of the database.")
        howmany = int(input("The database should be how many days long? (recommended 1500) "))
        print("Generating database")
        progress = [date, month, year]
        for jkl in range(howmany):
            cdate = progress[0]
            cmonth = progress[1]
            cyear = progress[2]
            day = Day()
            day.descr = f"{cdate:02d}{cmonth:02d}{cyear}"
            for i in range(1,len(value_names)+1):
                exec('day.int'+str(i)+' = '+str(value_defaults[i-1]))
            day.save()
            cdate += 1
            if (cmonth == 1 or cmonth == 3 or cmonth == 5 or cmonth == 7 or cmonth == 8 or cmonth == 10) and cdate == 32:
                cmonth += 1
                cdate = 1
            elif cmonth == 12 and cdate == 32:
                cmonth = 1
                cdate = 1
                cyear += 1
            elif (cmonth == 4 or cmonth == 6 or cmonth == 9 or cmonth == 11) and cdate == 31:
                cmonth += 1
                cdate = 1
            elif cmonth == 2 and ((cyear % 4 == 0 and cdate == 30) or (cyear % 4 != 0 and cdate == 29)):
                cmonth += 1
                cdate = 1
            progress = [cdate, cmonth, cyear]
        print(f"Generated {howmany} days beginning on {date:02d}.{month:02d}.{year} and ending on ",end="")
        date = progress[0]
        month = progress[1]
        year = progress[2]
        print(f"{date:02d}.{month:02d}.{year}")
        return HttpResponse("Done!")


"""
woke up at
3
no
13
no
brushed my teeth
1
no
0
no
kilometers run
2
no
0
no
worked out
4
no
0
no
minutes meditation
2
no
0
no
money spent
2
no
0
no
took a shower
4
no
0
no
NNN
4
no
0
no
kilograms
3
yes
80
yes
14
9
2022
500



"""