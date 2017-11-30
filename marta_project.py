from tkinter import *
from PIL import ImageTk, Image
import pymysql
from tkinter import messagebox
from tkinter import ttk, Canvas
from datetime import datetime, timedelta
import decimal
import hashlib
from hashlib import md5
from random import *

#MARTA v1.3
#By Team 54, CS4400 2017 Fall
class MARTA_Client:
    def __init__(self):
        # Invoke createLoginWindow; Invoke buildLoginWindow, Set loginWindow as mainloop
        #Connect to the database
        self.db = self.connect()
        self.cursor = self.db.cursor()

        # Login Window
        self.createLoginWindow()
        self.buildLoginWindow(self.loginWindow)

        self.loginWindow.mainloop()
        #self.newUserRegistrationWindow.mainloop()
        sys.exit()

    #=================================LOGIN WINDOW========================================
    def createLoginWindow(self):
        # Create blank Login Window
        self.loginWindow = Tk()
        self.loginWindow.title("MARTA v1.3.54.1")

        self.loginWindow.withdraw()
        self.loginWindow.update_idletasks()  # Update "requested size" from geometry manager
        x = (self.loginWindow.winfo_screenwidth() - self.loginWindow.winfo_reqwidth()) / 2
        y = (self.loginWindow.winfo_screenheight() - self.loginWindow.winfo_reqheight()) / 2
        self.loginWindow.geometry("+%d+%d" % (x, y))
        self.loginWindow.deiconify()

    def buildLoginWindow(self, loginWindow):
        # Add component for Login Window
        # Login Label
        loginLabel = Label(loginWindow, text="Login", font="Verdana 13 bold ")
        loginLabel.grid(row=1, column=3, sticky=W + E)

        # Username Label
        usernameLabel = Label(loginWindow, text="Username")
        usernameLabel.grid(row=2, column=2, sticky=W)

        # Password Label
        passwordLabel = Label(loginWindow, text="Password")
        passwordLabel.grid(row=4, column=2, sticky=W)

        #Image
        image = Image.open("MARTA-logo.jpg")
        image = image.resize((60, 60), Image.ANTIALIAS)
        buzzImage = ImageTk.PhotoImage(image)
        imageLabel = Label(loginWindow, image=buzzImage)
        imageLabel.image = buzzImage
        imageLabel.grid(row=2, column=4, rowspan=3, sticky=E)

        # Username Entry
        self.loginUsername = StringVar()
        usernameEntry = Entry(loginWindow, textvariable=self.loginUsername, width=20)
        usernameEntry.grid(row=2, column=3, sticky=W + E)

        # Password Entry
        self.loginPassword = StringVar()
        passwordEntry = Entry(loginWindow, textvariable=self.loginPassword, show='*', width=20)
        passwordEntry.grid(row=4, column=3, sticky=W + E)

        # Login Buttons
        loginButton = Button(loginWindow, text="Login", command=self.loginWindowLoginButtonClicked)
        loginButton.grid(row=6, column=3)

        # Register Button
        registerButton = Button(loginWindow, text="Register", command=self.loginWindowRegisterButtonClicked)
        registerButton.grid(row=6, column=4, sticky=E)

    #password hashing
    def computeMD5hash(self, str):
        m = hashlib.md5()
        m.update((str.encode('utf-8')))
        c = m.hexdigest()
        return c


    def loginWindowLoginButtonClicked(self):
        # Click the button on Login Window:
        # Obtain the username and password from keypress;
        self.username = self.loginUsername.get()
        self.password = self.loginPassword.get()

        #compute password hashing
        self.password = self.computeMD5hash(self.password)


        # Error message for Username input empty
        if not self.username:
            messagebox.showwarning("Username input is empty", "Please enter username.")
            return False
        # Error message for password input empty
        if not self.password:
            messagebox.showwarning("Password input is empty", "Please enter password")
            return False
        #Error message for username input doesn't exist in db
        isUsername = self.cursor.execute("SELECT * FROM User WHERE username = %s", self.username)
        if not isUsername:
            messagebox.showwarning("Username doesn't exist", "The username you entered does not exist.")
            return False
        #Error message for username and password doesn't match with db
        usernameAndPasswordMatch = self.cursor.execute(
            "SELECT * FROM User WHERE (username = %s AND password = %s)", (self.username, self.password))
        if not usernameAndPasswordMatch:
            messagebox.showwarning("Username and password don\'t match",
                                   "Sorry, the username and password you entered"
                                   + " do not match.")
            return False

        self.cursor.execute("SELECT IsAdmin FROM User WHERE (username = %s AND password = %s)", (self.username, self.password))
        isAdmin = self.cursor.fetchone()[0]
        if (isAdmin == 0):
            self.loginWindow.withdraw()
            self.createPassengerFunctionalityWindow()
            self.buildPassengerFunctionalityWindow(self.passengerFunctionalityWindow)
        else:
            self.loginWindow.withdraw()
            self.createAdminFunctionalityWindow()
            self.buildAdminFunctionalityWindow(self.adminFunctionalityWindow)
        return True

    def loginWindowRegisterButtonClicked(self):
        # Click button on Login Window:
        # Invoke createNewUserRegistrationWindow; Invoke buildNewUserRegistrationWindow;
        # Hide Login Window; Set newUserRegistrationWindow on the top

        self.createNewUserRegistrationWindow()
        self.buildNewUserRegistrationWindow(self.newUserRegistrationWindow)
        #self.loginWindow.withdraw()

    #=============New User Registration Window==============

    def createNewUserRegistrationWindow(self):
        # Create blank newUserRegistrationWindow
        self.newUserRegistrationWindow = Toplevel()
        self.newUserRegistrationWindow.title("Create a MARTA Account")

    def buildNewUserRegistrationWindow(self,newUserRegistrationWindow):
        # Add components for newUserRegistrationWindow

        # Username Label
        usernameLabel = Label(newUserRegistrationWindow, text="Username")
        usernameLabel.grid(row=2, column=2, sticky=W)

        # Email Address Label
        emailAddressLabel = Label(newUserRegistrationWindow, text="Email Address")
        emailAddressLabel.grid(row=3, column=2, sticky=W)


        # Password Label
        passwordLabel = Label(newUserRegistrationWindow, text="Password")
        passwordLabel.grid(row=4, column=2, sticky=W)

        # Confirm Password Label
        confirmPasswordLabel = Label(newUserRegistrationWindow, text="Confirm Password")
        confirmPasswordLabel.grid(row=5, column=2, sticky=W)

        # Username Entry
        self.registrationUsername = StringVar()
        regusernameEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationUsername, width=25)
        regusernameEntry.grid(row=2, column=3, padx=1)


        # Email Address Entry
        self.registrationEmailAddress = StringVar()
        regemailAddressEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationEmailAddress,width=25)
        regemailAddressEntry.grid(row=3, column=3, padx=1)

        # Password Entry
        self.registrationPassword = StringVar()
        regpasswordEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationPassword,show = '*',width=25)
        regpasswordEntry.grid(row=4, column=3, padx=1)

        # Confirm Password Entry
        self.registrationConfirmPassword = StringVar()
        regconfirmPasswordEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationConfirmPassword,show = '*',width=25)
        regconfirmPasswordEntry.grid(row=5, column=3, padx=1)

        self.var = StringVar()
        r1 = Radiobutton(newUserRegistrationWindow, text="Option 1", variable=self.var, value="exist")
        r1.grid(row=6, column=1, sticky=W)
        breezebox = Label(newUserRegistrationWindow, text="Card Number")
        breezebox.grid(row=7, column=1, sticky=E)
        self.registrationCardNum = StringVar()
        breezeboxEntry = Entry(newUserRegistrationWindow, textvariable=self.registrationCardNum, width=20)
        breezeboxEntry.grid(row=7, column=2, padx=1)

        r2 = Radiobutton(newUserRegistrationWindow, text="Option 2", variable=self.var, value="new")
        r2.grid(row=8, column=1, sticky=W)

        self.var.set("new")

        # Create Button
        newRegisterButton = Button(newUserRegistrationWindow, text="Register", command=self.newRegistrationWindowButtonClicked)
        newRegisterButton.grid(row=8, column=4, sticky=E)


    def newRegistrationWindowButtonClicked(self):
        #Clock the button on Register Window
        #Obtain username, Email Address, Password, confirm password from keypress
        self.regusername = self.registrationUsername.get()
        self.regemail = self.registrationEmailAddress.get()
        self.regpassword = self.registrationPassword.get()
        self.regconfirmpassword = self.registrationConfirmPassword.get()
        self.radiobuttonvalue = self.var.get()

        #TODO: password hashing before input in the db
        # Error message for username input empty
        if not self.regusername:
            messagebox.showwarning("Username input is empty", "Please enter registering username.")
            return False
        #Error message for email input empty
        if not self.regemail:
            messagebox.showwarning("Email input is empty", "Please enter registering email.")
            return False
        #Error message for password input empty
        if not self.regpassword:
            messagebox.showwarning("Password input is empty", "Please enter password.")
            return False

        #Error message for password not longer than 8 characters
        if (len(self.regpassword) < 8):
            messagebox.showwarning("Password input invalid", "Password has to be longer than 8 characters/numbers. \n (password is case sensitive)")
            return False

        #Error message for email not valid
        if not (re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.regemail)):
            messagebox.showwarning("Not a valid email", "Please enter valid E-mail address.")
            return False
        #Error message for username input already exist in db
        isUsername = self.cursor.execute("SELECT * FROM User WHERE username = %s", self.regusername)
        if isUsername:
            messagebox.showwarning("Username already exist", "The username you entered already exist. \n Try different username.")
            return False

        #Error message for email input already exist in db
        isEmail = self.cursor.execute("SELECT * FROM Passenger WHERE email = %s", self.regemail)
        if isEmail:
            messagebox.showwarning("Email already exist", "The email you entered already exist. \n Try different email.")
            return False

        #Error message for password not matching confirmpassword
        if (self.regpassword != self.regconfirmpassword):
            messagebox.showwarning("Password confirmation Error", "Password and Confirm password doesn't match.")
            return False
     
        #For clicking "Use my existing Breezecard"
        if (self.radiobuttonvalue == "exist"):
            self.existBreeze = self.registrationCardNum.get()
            #Error message for Breezecard input empty
            if not self.existBreeze:
                messagebox.showwarning("Exist card input is empty", "Please enter the existing Breezecard Number.")
                return False

            #Error message for Breezecard input invalid (less than 16-digit)
            if (len(self.existBreeze) != 16):
                messagebox.showwarning("Breezecard input invalid", "Breezecard number is invalid. \n Breezecard number must be 16-digit long.")
            else:
                #Error message for Breezecard input invalid (input contains other things than number)
                #Error message for Breezecard input not exist in db
                isBreezecard = self.cursor.execute("SELECT * FROM Breezecard WHERE cardNum = %s", self.existBreeze)
                if not isBreezecard:
                    messagebox.showwarning("Breezecard doesn't exist", "Breezecard you put in doesn't not exist in our system.")
                    return False

                self.cursor.execute("SELECT cUsername FROM Breezecard WHERE cardNum = %s", self.existBreeze)
                hasUser = self.cursor.fetchone()[0]
                #1) If Breezecard input doesn't have user -> put it in Breezecard table (update)
                if not hasUser:
                    self.hashpassword = self.computeMD5hash(self.regpassword)
                    self.cursor.execute("INSERT INTO User(username, password, IsAdmin) VALUES(%s, %s, FALSE)", (self.regusername, self.hashpassword))
                    self.cursor.execute("INSERT INTO Passenger(pUsername, email) VALUES(%s, %s)", (self.regusername, self.regemail))
                    self.cursor.execute("UPDATE Breezecard SET cUsername = %s", self.regusername)
                    self.db.commit()
                    messagebox.showwarning("Registration Success", "You have successfully registered to MARTA system! Please log in.")
                    self.newUserRegistrationWindow.destroy()
                    return True
                #2) If Breezecard input already have user -> put Breezecard in conflict table and assign passenger with random card
                else:
                    randomBreeze = str(randint(0,9)) + str(randint(100000000000000,999999999999999))
                    currentTime = datetime.now()
                    currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
                    self.hashpassword = self.computeMD5hash(self.regpassword)
                    self.cursor.execute("INSERT INTO User(username, password, IsAdmin) VALUES(%s, %s, FALSE)", (self.regusername, self.hashpassword))
                    self.cursor.execute("INSERT INTO Passenger(pUsername, email) VALUES(%s, %s)", (self.regusername, self.regemail))
                    self.cursor.execute("INSERT INTO Breezecard(cardNum, value, cUsername) VALUES(%s, 0.00, %s)", (randomBreeze, self.regusername))
                    self.cursor.execute("INSERT INTO Conflict(conUsername, conCardNum, dateTime) VALUES(%s, %s, %s)", (self.regusername, self.existBreeze, currentTime))

                    self.db.commit()
                    messagebox.showwarning("Registration Success", "Your account has been made but the card already has existing user. \n Please contact one of our representatives.")
                    self.newUserRegistrationWindow.destroy()
                    return True



        #For clicking "Create a New Breezecard" - make random 16-digit that doesn't exist in db
        if (self.radiobuttonvalue == "new"):
            self.newBreeze = str(randint(0,9)) + str(randint(100000000000000,999999999999999))
            self.hashpassword = self.computeMD5hash(self.regpassword)
            self.cursor.execute("INSERT INTO User(username, password, IsAdmin) VALUES(%s, %s, FALSE)", (self.regusername, self.hashpassword))
            self.cursor.execute("INSERT INTO Passenger(pUsername, email) VALUES(%s, %s)", (self.regusername, self.regemail))
            self.cursor.execute("INSERT INTO Breezecard(cardNum, value, cUsername) VALUES(%s, 0.00, %s)", (self.newBreeze, self.regusername))
            self.db.commit()
            messagebox.showwarning("Registration Sucess", "You have successfully registered to MARTA system! Please log in.")
            self.newUserRegistrationWindow.destroy()
            return True

    #=====================Passenger Functionality Window=======================
    def createPassengerFunctionalityWindow(self):
        self.passengerFunctionalityWindow = Toplevel()
        self.passengerFunctionalityWindow.title("Welcome to Marta")

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.loginWindow.destroy()

        self.passengerFunctionalityWindow.protocol("WM_DELETE_WINDOW", on_closing)

    def buildPassengerFunctionalityWindow(self, passengerFunctionalityWindow):
        self.passusername = self.loginUsername.get()
        self.cursor.execute("SELECT cardNum FROM Breezecard WHERE cUsername = %s", self.passusername)
        myCards = self.cursor.fetchall()
        listmyCards = []
        for card in myCards:
            listmyCards.append(card[0])
        print(listmyCards)

        #Welcome user label
        welcomeLabel = Label(passengerFunctionalityWindow, text= ("Welcome, " + self.passusername))
        welcomeLabel.grid(row=1, column=5, sticky=E)

        #Breezecard Label
        breezecardLabel = Label(passengerFunctionalityWindow, text="Breezecard: ")
        breezecardLabel.grid(row=2, column=1, sticky=W)

        #Balance Label
        balanceLabel = Label(passengerFunctionalityWindow, text="Balance: ")
        balanceLabel.grid(row=3, column=1, sticky=W)

        #Balance Showing Label
        self.cursor.execute("SELECT value FROM Breezecard WHERE cardNum = %s", listmyCards[0])
        balance = self.cursor.fetchone()[0]

        self.balanceVar = StringVar()
        self.balanceVar.set("$ " + str(balance))

        self.balanceShowLabel = Label(passengerFunctionalityWindow, textvariable=self.balanceVar)
        self.balanceShowLabel.grid(row=3, column=2, sticky=W)

        #Breezecard Dropdown Menu
        self.breezecardDropVar = StringVar(passengerFunctionalityWindow)
        self.breezecardDropVar.set(listmyCards[0])

        self.breezecardDropDown = OptionMenu(passengerFunctionalityWindow, self.breezecardDropVar, *listmyCards, command = self.displayBalance)
        self.breezecardDropDown.grid(row=2, column=2, sticky=W)

        #Manage Cards Button
        manageCardButton = Button(passengerFunctionalityWindow, text="Manage Cards", command=self.passengerManageCardButtonClicked)
        manageCardButton.grid(row=2, column=3, sticky=W+E)

        #Starts At Label
        startsAtLabel = Label(passengerFunctionalityWindow, text="Starting at: ")
        startsAtLabel.grid(row=4, column=1, sticky=W)

        #Starts At Dropdown Menu
        self.cursor.execute("SELECT * FROM Station")
        stations = self.cursor.fetchall()
        liststations = []
        self.dictionarystations = {}
        #index: 0-stopID, 1-name, 2-IsTrain, 3-fare, 4-closedStatus
        for station in stations:
            station_name = station[1]
            if (station[2] == 0):
                station_name = station_name + "(Bus station)"
            station_name = station_name + " - $" + "{0:.2f}".format(station[3])
            liststations.append(station_name)
            self.dictionarystations[station_name] = station[0]

        self.startsAtDropVar = StringVar(passengerFunctionalityWindow)
        self.startsAtDropVar.set(liststations[0])

        self.startsAtDropDown = OptionMenu(passengerFunctionalityWindow, self.startsAtDropVar,*liststations)
        self.startsAtDropDown.grid(row=4, column=2, sticky=W)

        #Starts At Button toggling (checking whether trip has ended)

        #Starts At Button
        self.startAtButton = Button(passengerFunctionalityWindow, text="Start Trip", command=self.toggle_startbutton)
        self.startAtButton.grid(row=4, column=3, sticky=W+E)

        #Ending At Label
        endingAtLabel = Label(passengerFunctionalityWindow, text="Ending at: ")
        endingAtLabel.grid(row=5, column=1, sticky=W)

        #Ending At Dropdown Menu
        

        #Create View Trip History Button
        viewTripHistoryButton = Button(passengerFunctionalityWindow, text="View Trip History", command=self.passengerFunctionalityWindowViewTripHistoryButtonClicked)
        viewTripHistoryButton.grid(row=8, column=1, sticky=W)

        #Log Out Button
        logOutButton = Button(passengerFunctionalityWindow, text="Log Out", command=self.passengerFunctionalityWindowLogOutButtonClicked)
        logOutButton.grid(row=8, column=5, sticky=E)

        ##MANAGE CARDS LINK
        ##END TRIP LINK
    def displayBalance(self, cardNum):
        #DisplayBalance depends on Dropdown menu
        self.cursor.execute("SELECT value FROM Breezecard WHERE cardNum = %s", cardNum)
        balance = self.cursor.fetchone()[0]
        self.balanceVar.set("$ " + str(balance))

    def toggle_startbutton(self):
        #Press Start Trip
        print(self.startsAtDropVar.get())
        startID = self.dictionarystations[self.startsAtDropVar.get()]
        print(startID)
        if self.startAtButton["text"] == "Start Trip":
            self.startAtButton["text"] = "In Progress"
        else:
            self.startAtButton["text"] = "Start Trip"

    def passengerFunctionalityWindowViewTripHistoryButtonClicked(self):
        # Click the View Trip History Button on Passenger Functionality Window:
        pass
    def passengerFunctionalityWindowLogOutButtonClicked(self):
        # Click the Log Out Button on Passenger Functionality Window:
        pass        

    ##===========================================Passenger Functionality - Manage Cards==================================================
    def passengerManageCardButtonClicked(self):
        # Click button on passnger functionality Window:
        # Invoke createNewManageCardsWindow; Invoke buildNewManageCardsWindow;

        self.createManageCardsWindow()
        self.buildManageCardsWindow(self.manageCardsWindow)
        #self.passengerFunctionalityWindow.withdraw()

    def createManageCardsWindow(self):
        self.manageCardsWindow = Toplevel()
        self.manageCardsWindow.title("Manage Cards")

    def buildManageCardsWindow(self, manageCardsWindow):
        #Add component for manageCardWindow

        #Breezecards Label
        breezecardsLabel = Label(manageCardsWindow, text="Breeze Cards")
        breezecardsLabel.grid(row=2, column=1, sticky=W)

        #Add Card Button
        addCardButton = Button(manageCardsWindow, text="Add Card", command=self.manageCardsWindowAddCardButtonClicked)
        addCardButton.grid(row=5, column=5, sticky=E)

        #Credit Card # Label
        creditcardLabel = Label(manageCardsWindow, text="Credit Cards")
        creditcardLabel.grid(row=6, column=1, sticky=W)

        #Value Label
        valueLabel = Label(manageCardsWindow, text="Value")
        valueLabel.grid(row=7, column=1, sticky=W)

        #Add Value Button
        addValueButton = Button(manageCardsWindow, text="Add Card", command=self.manageCardsWindowAddValueButtonClicked)
        addValueButton.grid(row=8, column=5, sticky=E)



    def manageCardsWindowAddCardButtonClicked(self):
        # Click the Add Card Button on Manage Cards Window:
        pass

    def manageCardsWindowAddValueButtonClicked(self):
        # Click the Add Value Button on Manage Cards Window:
        pass

    #=============Administrator Functionality Window========================
    def createAdminFunctionalityWindow(self):
        self.adminFunctionalityWindow = Toplevel()
        self.adminFunctionalityWindow.title("Administrator")

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.loginWindow.destroy()

        self.adminFunctionalityWindow.protocol("WM_DELETE_WINDOW", on_closing)

    def buildAdminFunctionalityWindow(self, adminFunctionalityWindow):
        #Add component for adminFunctionalityWindow

        #Station Management Button
        stationManagementButton = Button(adminFunctionalityWindow, text="Station Management")
        stationManagementButton.grid(row=1, column=3, sticky=W + E)

        #Suspend Cards Button
        suspendedCardButton = Button(adminFunctionalityWindow, text="Suspended Cards")
        suspendedCardButton.grid(row=3, column=3, sticky=W + E)

        #Breezecard Management Button
        breezecardManagementButton = Button(adminFunctionalityWindow, text="Breezecard Management")
        breezecardManagementButton.grid(row=5, column=3, sticky=W + E)

        #Passenger Flow Report Button
        passengerFlowReportButton = Button(adminFunctionalityWindow, text="Passenger Flow Report")
        passengerFlowReportButton.grid(row=7, column=3, sticky=W + E)


    # --------------------Database Connection-----------------
    def connect(self):
        try:
            #TODO: figure out the name of the database
            db = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                                 db='cs4400_Group_54', user='cs4400_Group_54', passwd='qUYP7usT')
            return db
        except:
            messagebox.showwarning('Error!', 'Cannot connect. Internet Connection Issue or DB not ready.')
            return False
a = MARTA_Client()
a.db.close()