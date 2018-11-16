# heart_rate_sentinel_server
This server will allow the client to post heart rate information for a new
or existing patient. It will also allow the client to get the status of the
patient (whether the patient has tachycardia or not), all of the patient
heart rate readings and the average heart rate of the patient. This information
is stored in a Mongo database. 


**TO RUN:**
The server should be running on the virtual machine under the hostname:
vcm-7293.vm.duke.edu. In order to POST to the server, run post_patient.py.
To check the GET function of the server, type in the website (http://vcm-7293.vm.duke.edu:5008) and appropriate 
extensions.


**TEST FUNCTIONS:**
Test functions have been written for functions which either do not depend
on the use of the database or uses a GET or POST function. This leads
to poor coverage. 


**FUTURE IMPROVEMENTS:**
Creating a separate file for my functions that the server calls upon so
my server code isn't over 300 lines. Also, as it was discussed in class,
some of the calculations could be move from the GET to POST (or vice versa)
to make the code more computationally efficient.
