SETUP 

* First thing first, locust is needed to run the test files!
* pip install locust
* Navigate to the t2-project in terminal : cd t2-project
* Inside t2-project folder please pull this stress test repository :
  * git clone https://github.com/mertrasna/StressTests.git
* After cloning the StressTests file, please move to the folder with cd
* Now, you can find 2 different .py files. 
  *  locust.py is the stress test without Thread running, 
  *  locustThread.py is the stress test with Thread running
* Now, please run the python script you want on terminal : locust -f locust.py
* After running script, please navigate to http://localhost:8089/ 
* Please setup locust with these parameters : 
  * Number of users : 10000
  * Ramp up : 200
  * host : http://localhost:8080
* This will set a limit of maximum 10000 users, and the spawn rate of 200 users per second!