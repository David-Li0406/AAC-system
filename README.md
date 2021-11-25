# AAC: A automatic article correction system with article recommendation, image recongnition and voice comment

## Startup project

### Requirement
```bash
#install npm and vue_cli, then
cd client 
npm install

#install python, create an vitual environment, then
cd server
pip install -r requirements.txt
```

### Database
```bash
#install mysql, then
mysql
>CREATE DATABASE `aacdb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

#init database
python manage.py db init
#migrate database
python manage.py db migrate
#upgrade database
python manage.py db upgrade
```

### Run
```bash
#run client
cd client
npm run dev
#run server
cd server
python run.py
```

## Module Description

### Dataset design
![avatar](/source/dataset.png)

### Login and Register
When the user registering, we use Prop in Vue to check the mailbox format at the front end. After the user input the email, we use axios to asynchronously request the back end to check duplicate mailboxes, and ensure that the verification code is valid at the back end.

![avatar](/source/login1.png)
![avatar](/source/login2.png)

When the user logging in, after the user submit his information, we use crypto.js to encrypt user's information during transmission. And we will storage the username and password if the user choose 'Remember me'

![avatar](/source/login3.png)

### Visualization

We used the radar chart in echart to show the user’s writing ability, and encapsulated the star rating component to further visualize

![avatar](/source/vis1.png)


### Access control and authentication
For access control, our general consideration is as following:
    
    The front end ensures that ordinary users do not enter the management page through page controls 

    The backend ensures that users cannot obtain management permissions by stitching URLs or simulating http access

![avatar](/source/control1.png)
![avatar](/source/control2.png)

For detailed implementation, we use Token(JWT), our implementation step are shown in the following graph:

![avatar](/source/control3.jpg)

For information storage, we use Vuex, and we also storage a backup in localStoraage to prevent user information from being lost during refresh 
