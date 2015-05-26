#####What is Log Injection ?
----------------------------------------
Log injection problems are a subset of injection problem, in which invalid entries taken from user input are inserted in logs or audit trails, allowing an attacker to mislead administrators or cover traces of attack. Log injection can also sometimes be used to attack log monitoring systems indirectly by injecting data that monitoring systems will misinterpret. 

source : https://www.owasp.org/index.php/Log_injection


#####How does this work?
----------------------------------------

![Screen Shot 2015 05 26 At 6.17.31 PM](static/img/Screen%20Shot%202015-05-26%20at%206.17.31%20PM.png)

We are not looking for user confidentials. Indeed, we are looking for other solution that let us out of the jail. Most common implementation for this IP ban is countdown via javascripts. However since javascripts is intended for client-side, cracking down js has taken root. Next level is validation using log file.

In this scenario, our Log file is important for:
1. Trace back user details
2. Validate time-left estimation and banned IP.

After by pass this evaluation, brutal force is possible and site is determined as vulnerable for dos.

#####What do I need to run the source code ?
---------------------------------------
1. Install pip
2. git clone https://github.com/LalaNguyen/log-injection.git
3. pip install -r requirements.txt
4. python server.py then connect to 127.0.0.1:5000

Have Fun !
