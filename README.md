# Linkedin_booster

The code aims to help people mass connect with a specific target based on some criteria (e.g: data scientist or recrutiers in a specific region). 

The code is not very user friendly for now.

## Setup

1- You need to set up selenium for Chrome. https://selenium-python.readthedocs.io/installation.html. You need the chrome version no matter which browser you use on a daily basis.

2- Change the link to the research one you're interested in (e.g: Search for Recruiter - people on linkedin, and select some criteria like 1st & 2nd connections -you can't connect with 3rd+ so this is an important [and necessary] criterion to add, if you want an english profile, etc...-. At the end of it add &page={page} to be able to go over the pages.
You'll find an example at the beginning of the script :).

3- In order to connect to the linkedin account, I'm going through cookies. For that, when you use the script for the first time, it will only go to the linkedin login page. Just add time.sleep(1000) before line 23 for example, then login into your linkedin account and leave the script + remove the time.sleep. The next time, the webdriver will directly use the cookies. Don't worry, selenium doesn't use your "real" cookies, only the ones generated *in* the webdriver.

4- On line 55, you need to put your own path to the cookies. I left mine as an example so that you know where to look.

5- On line 101, you can customize your own message to send. The message is being read only when the connection request is accepted. Please note that there's a character limit of 300. I suggest aiming for 285 as some first names can be long.

