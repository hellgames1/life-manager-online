# life-manager-online
 Python (Django) and Javascript online adaptation of my life-manager project

This is my first ever attempt at a Django project.
It's a continuation of my previous largest project (life-manager) which by now I'm probably done with.
I'll try to implement everything that I did there, and get to the features that I didn't complete.

How to setup:
1. Download repository to your computer
2. Check your local IP address, on Windows open command line and type ipconfig
3. Go to /lmoproject/lifemanageronline/settings.py
4. Change ALLOWED_HOSTS to whatever your local IP is
5. Go to directory /lmoproject/ and open terminal
6. Run python manage.py makemigrations
7. Run python manage.py migrate
8. Run python manage.py runserver 192.168.0.104:8000 where you replace the IP with your local one
9. Go to http://192.168.0.104:8000/setup (again replacing it with your IP)
10. The setup procedure will begin on the terminal where you've run the server, follow the prompts
11. Done!


If you want to be able to access this remotely (from mobile network or another Wi-Fi),
set up port forwarding in your router settings with the port 8000 and your local IP.
Add your public IP in ALLOWED_HOSTS in settings.py
WARNING! This code is extremely vulnerable and hackers might be able to hack it and execute
their own code. I do not recommend using this app on your public network yet!!!