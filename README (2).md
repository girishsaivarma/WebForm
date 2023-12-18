# WebForm

# Group Mates:
Girish Sai Varma Penumathsa   (gpenumat@stevens.edu)
Praneeth Movva                (pmovva1@stevens.edu)
Charan Sai Chintha            (cchintha@stevens.edu)

# GitRepo:
https://github.com/girishsaivarma/WebForm

# HoursWorked:
We spent around 30 - 33 hours working on this project.

# Description On How the code was tested:
First we have installed all the necessary softwares and Installed Flask. We have used postman to test all my testcases after writing the code and starting the Flask server. we made sure that the generated key was unique and is not conflicted with other keys. 

# Any Known Bugs:
There are no known bugs. All the programs are working fine.

# An example of difficult issue:
Trying to get the test cases to work properly and security was a challenge. Authenticating user and for deleting or editing posts it was difficult to make sure tht everything was fine. Even the time based range queries took a lot of time as we encountered deadlock and had to resolve everything and fixed it.

# List of 5 Extensions done:
1. Users and user keys
2. User profiles
3. Date- and time-based range queries
4. Fulltext search
5. File upload

# Summary
* Consider the base_url: http://127.0.0.1:5000/

1) For Users and user keys:
* Create a post for user using /register (in Post method)

```
{
    "username": "{{user_1}}"
}
```

2) For User Profiles:
* to get the user use /user/{{user_id1}}     (in GET method)

```
{
    "id": 1,
    "name": null,
    "username": "testuser1"
}
```

3) Date and Time:
* Use /post?start_time={{x}}&end_time={{y}}  (in GET Method)
* Use the above thing with the time range to get the desired users between that time

4) Fulltext Search:
* In this extension, we simply filter out the text based on the input string.
* use /posts/search (in GET Method)

5) File Upload:
* This is helpful to encode any binary data sent in JSON 
* We have also added optional decode and store the file, or just store the base64 string
* /post   (GET Method)

# To test
* First run our setup.sh file and install all the necessary dependencies 
* Then start the server using run.sh and starting testing the code in Postman.

Thank you

