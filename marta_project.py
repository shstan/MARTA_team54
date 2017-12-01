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

                if (self.existBreeze.isdigit() == 0):
                    messagebox.showwarning("Breezecard input invalid", "Breezecard number must be 16-digit numbers. \n Your input contains something other than number.")
                    return False

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
                    self.cursor.execute("UPDATE Breezecard SET cUsername = %s WHERE cardNum = %s", (self.regusername, self.regpassword))
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
        self.listmyCards = []
        for card in myCards:
            self.listmyCards.append(card[0])

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
        self.cursor.execute("SELECT value FROM Breezecard WHERE cardNum = %s", self.listmyCards[0])
        balance = self.cursor.fetchone()[0]

        self.balanceVar = StringVar()
        self.balanceVar.set("$ " + str(balance))

        self.balanceShowLabel = Label(passengerFunctionalityWindow, textvariable=self.balanceVar)
        self.balanceShowLabel.grid(row=3, column=2, sticky=W)

        #Breezecard Dropdown Menu
        self.breezecardDropVar = StringVar(passengerFunctionalityWindow)
        self.breezecardDropVar.set(self.listmyCards[0])

        self.breezecardDropDown = OptionMenu(passengerFunctionalityWindow, self.breezecardDropVar, *self.listmyCards, command = self.displayBalance)
        self.breezecardDropDown.grid(row=2, column=2, sticky=W)

        #Manage Cards Button
        manageCardButton = Button(passengerFunctionalityWindow, text="Manage Cards", command=self.passengerManageCardButtonClicked)
        manageCardButton.grid(row=2, column=3, sticky=W+E)

        #Create View Trip History Button
        viewTripHistoryButton = Button(passengerFunctionalityWindow, text="View Trip History", command=self.passengerFunctionalityWindowViewTripHistoryButtonClicked)
        viewTripHistoryButton.grid(row=8, column=1, sticky=W)

        #Log Out Button
        logOutButton = Button(passengerFunctionalityWindow, text="Log Out", command=self.passengerFunctionalityWindowLogOutButtonClicked)
        logOutButton.grid(row=8, column=5, sticky=E)

        #======================================================Start and End Trip=================================================
        #Starts At Label
        startsAtLabel = Label(passengerFunctionalityWindow, text="Starting at: ")
        startsAtLabel.grid(row=4, column=1, sticky=W)

        #Starts At and Ends At Dropdown Menu
        self.cursor.execute("SELECT * FROM Station")
        stations = self.cursor.fetchall()
        self.liststations = []
        self.busstations = []
        self.trainstations = []
        self.dictionarystations = {}
        #index: 0-stopID, 1-name, 2-IsTrain, 3-fare, 4-closedStatus
        for station in stations:
            station_name = station[1]
            if (station[2] == 0):
                station_name = station_name + "(Bus station)"
                station_name = station_name + " - $" + "{0:.2f}".format(station[3])
                self.busstations.append(station_name)
                self.liststations.append(station_name)
            else:
                station_name = station_name + " - $" + "{0:.2f}".format(station[3])
                self.trainstations.append(station_name)
                self.liststations.append(station_name)
            self.dictionarystations[station_name] = station[0]

        self.dictionaryEndStations = {}
        for station in self.liststations:
            if "(Bus station)" in station:
                self.dictionaryEndStations[station] = self.busstations
            else:
                self.dictionaryEndStations[station] = self.trainstations

        self.startsAtDropVar = StringVar(passengerFunctionalityWindow)
        self.endsAtDropVar = StringVar(passengerFunctionalityWindow)

        self.startsAtDropVar.trace("w", self.update_options)

        self.startsAtDropDown = OptionMenu(passengerFunctionalityWindow, self.startsAtDropVar,*self.liststations)
        self.startsAtDropDown.grid(row=4, column=2, sticky=W)

        self.endsAtDropDown = OptionMenu(passengerFunctionalityWindow, self.endsAtDropVar, "")
        self.endsAtDropDown.grid(row=5, column=2, sticky=W)

        self.startsAtDropVar.set(self.liststations[0])

        #Starts At Button
        self.startAtButton = Button(passengerFunctionalityWindow, text="Start Trip", state=NORMAL, command=self.toggle_startbutton)
        self.startAtButton.grid(row=4, column=3, sticky=W+E)

        #Ending At Label
        endingAtLabel = Label(passengerFunctionalityWindow, text="Ending at: ")
        endingAtLabel.grid(row=5, column=1, sticky=W)

        #Ends At Button
        self.endsAtButton = Button(passengerFunctionalityWindow, text="End Trip", command=self.toggle_endbutton)
        self.endsAtButton.grid(row=5, column=3, sticky=W+E)

        ##MANAGE CARDS LINK
        ##END TRIP LINK
    def displayBalance(self, cardNum):
        #DisplayBalance depends on Dropdown menu
        self.cursor.execute("SELECT value FROM Breezecard WHERE cardNum = %s", cardNum)
        balance = self.cursor.fetchone()[0]
        self.balanceVar.set("$ " + str(balance))

    def update_options(self, *args):
        updatedEndList = self.dictionaryEndStations[self.startsAtDropVar.get()]
        self.endsAtDropVar.set(updatedEndList[0])

        menu = self.endsAtDropDown['menu']
        menu.delete(0, 'end')
        for updatedEnd in updatedEndList:
            menu.add_command(label=updatedEnd, command=lambda endingstation=updatedEnd: self.endsAtDropVar.set(endingstation))       

    def toggle_startbutton(self):
        #Press Start Trip
        startID = self.dictionarystations[self.startsAtDropVar.get()]
        breezecardUsed =self.breezecardDropVar.get()

        self.cursor.execute("SELECT IsTrain FROM Station WHERE (fare < (SELECT value FROM Breezecard WHERE cardNum = %s)) AND (stopID = %s)", (breezecardUsed, startID))
        constraintStation = self.cursor.fetchone()
        #Error: Buzzcard doesn't have enough balance
        if not constraintStation:
            messagebox.showwarning("Cannot start trip", "You don't have enough balance on your Breezecard.")
            return False

        #Error: Buzzcard is suspended
        self.cursor.execute("SELECT * FROM Conflict WHERE conCardNum = %s", breezecardUsed)
        constraintBuzzcard = self.cursor.fetchall()
        if constraintBuzzcard:
            messagebox.showwarning("Cannot start trip", "Your buzzcard is suspended. \n Please call/email one of our representatives.")
            return False

        #Error: passenger already is in trip
        for checker in self.listmyCards:
            self.cursor.execute("SELECT startID, endID FROM Trip WHERE bcNum = %s", checker)
            ended = self.cursor.fetchall()
            for end in ended:
                if not end[1]:
                    self.inverse_dictionary = {v: k for k, v in self.dictionarystations.items()}
                    myTripOrigin = self.inverse_dictionary[end[0]]
                    self.startsAtDropVar.set(myTripOrigin)
                    self.startsAtDropDown.config(state=DISABLED)

                    self.startAtButton.config(text="In Progress")
                    self.startAtButton.config(state=DISABLED)
                    messagebox.showwarning("Cannot start trip", "You are already in trip. Please end the trip before starting another.")
                    return False

        #Start Trip
        currentTime = datetime.now()
        currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("SELECT fare FROM Station WHERE stopID = %s", startID)
        FareStart = self.cursor.fetchone()[0]
        print(type(FareStart))
        self.startAtButton.config(text="In Progress")
        self.startAtButton.config(state=DISABLED)
        self.startsAtDropDown.config(state=DISABLED)
        self.cursor.execute("INSERT INTO Trip(bcNum, startTime, currentFare, startID, endID) VALUES(%s, %s, %s, %s, NULL)",
            (breezecardUsed, currentTime, FareStart, startID))
        self.cursor.execute("UPDATE Breezecard SET value = value - %s WHERE cardNum = %s", (FareStart, breezecardUsed))
        self.db.commit()
        messagebox.showwarning("Trip Success", "You are now in trip!")
        return True

    def toggle_endbutton(self):
        #Press End Trip
        #cards = self.listmyCards
        willendID = self.dictionarystations[self.endsAtDropVar.get()]
        #startID = self.dictionarystations[self.startsAtDropVar.get()]
        #print(cards, willendID, startID)

        self.cursor.execute("SELECT * FROM Trip WHERE (endID IS NULL) AND (bcNum IN (SELECT cardNum FROM Breezecard WHERE cUsername = %s))", self.passusername)
        notendedTrip = self.cursor.fetchall()
        if not notendedTrip:
            messagebox.showwarning("All trips ended", "You are not in trip right now.")
            return False
        else:
            self.startAtButton.config(text="Start Trip")
            self.startAtButton.config(state=NORMAL)
            self.startsAtDropDown.config(state=NORMAL)
            self.cursor.execute("UPDATE Trip SET endID = %s WHERE (endID IS NULL) AND (bcNum IN (SELECT cardNum FROM Breezecard WHERE cUsername = %s))", (willendID, self.passusername))
            self.db.commit()
            messagebox.showwarning("Trip Success", "You have arrived to your destiny. \n Thank you for using MARTA")
            return True      

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

        def on_closing():
            self.manageCardsWindow.withdraw()
            self.passengerFunctionalityWindow.withdraw()
            self.createPassengerFunctionalityWindow()
            self.buildPassengerFunctionalityWindow(self.passengerFunctionalityWindow)

        self.manageCardsWindow.protocol("WM_DELETE_WINDOW", on_closing)

    def buildManageCardsWindow(self, manageCardsWindow):
        #self.passusername - user
        #self.listmyCards - list of cards
        #Add component for manageCardWindow

        #Breezecards Title Label
        breezecardsLabel = Label(manageCardsWindow, text="Breeze Cards", font="Verdana 13 bold ")
        breezecardsLabel.grid(row=1, column=1, sticky= W+E)

        #Breezecard Adding Entry
        self.entryBreezeCard = StringVar()
        breezecardEntry = Entry(manageCardsWindow, textvariable=self.entryBreezeCard, width=20)
        breezecardEntry.grid(row=2, column=2, sticky=W)

        #Breezecard Adding Button
        addCardButton = Button(manageCardsWindow, text="Add Card", command=self.manageCardsWindowAddCardButtonClicked)
        addCardButton.grid(row=2, column=3, sticky=W)


        ManageCardTableLabel1 = Label(manageCardsWindow, text="Card #", width=20)
        ManageCardTableLabel1.grid(row=3, column=1)
        ManageCardTableLabel2 = Label(manageCardsWindow, text="Value", width=20)
        ManageCardTableLabel2.grid(row=3, column=2)
        ManageCardTableLabel3 = Label(manageCardsWindow, text="", width=20)
        ManageCardTableLabel3.grid(row=3, column=3)
        nextrow = 4 + self.showMyBreezecard()


        #Add Value to Selected Card
        self.addValueToSelectedCardLabel = Label(manageCardsWindow, text="Add Value to Selected Card: ")
        self.addValueToSelectedCardLabel.grid(row=nextrow, column=2, sticky=W+E)


        self.printcardNumVar = StringVar()
        self.printcardNumVar.set("")

        self.addValueToSelectedCardLabel2 = Label(manageCardsWindow, textvariable=self.printcardNumVar, fg="blue")
        self.addValueToSelectedCardLabel2.grid(row=nextrow, column=3, sticky=W)

        #Credit Card Label
        self.creditcardLabel = Label(manageCardsWindow, text="Credit Card #: ")
        self.creditcardLabel.grid(row=nextrow+1, column=1, sticky=W)

        #Credit card Entry
        self.entryCreditCard = StringVar()
        self.creditcardEntry = Entry(manageCardsWindow, textvariable=self.entryCreditCard, width=20)
        self.creditcardEntry.grid(row=nextrow+1, column=2, sticky=W)

        #Value Label
        self.valueLabel = Label(manageCardsWindow, text="Value: ")
        self.valueLabel.grid(row=nextrow+2, column=1, sticky=W)

        #Value Entry
        self.entryValue = StringVar()
        self.valueEntry = Entry(manageCardsWindow, textvariable=self.entryValue, width=20)
        self.valueEntry.grid(row=nextrow+2, column=2, sticky=W)

        #Add Value Button
        self.addValueButton = Button(manageCardsWindow, text="Add Value", command=self.manageCardsWindowAddValueButtonClicked)
        self.addValueButton.grid(row=nextrow+3, column=3, sticky=W+E)

    def select_tablecard(self, num):
        self.printcardNumVar.set(num)

    def remove_tablecard(self, removenum):
        self.cursor.execute("SELECT count(*) FROM Breezecard WHERE cUsername = %s", self.passusername)
        myBreezecard = self.cursor.fetchone()[0]

        if messagebox.askokcancel("Remove card", "Are you sure you want to remove this card?"):
            if (myBreezecard > 1):
                self.cursor.execute("UPDATE Breezecard SET cUsername = NULL WHERE cardNum = %s", removenum)
                self.db.commit()
                self.manageCardsWindow.withdraw()
                self.createManageCardsWindow()
                self.buildManageCardsWindow(self.manageCardsWindow)
            else:
                randomBreezenum = str(randint(0,9)) + str(randint(100000000000000,999999999999999))
                self.cursor.execute("INSERT INTO Breezecard(cardNum, value, cUsername) VALUES (%s, 0.00, %s)", (randomBreezenum, self.passusername))
                self.cursor.execute("UPDATE Breezecard SET cUsername = NULL WHERE cardNum = %s", removenum)
                self.db.commit()
                #self.manageCardsWindow.withdraw()
                #self.createManageCardsWindow()
                self.buildManageCardsWindow(self.manageCardsWindow)

        #self.passengerFunctionalityWindow.withdraw()

    def showMyBreezecard(self):
        self.cursor.execute("SELECT cardNum, value FROM Breezecard WHERE cUsername = %s", self.passusername)
        myBreezecard = self.cursor.fetchall()
        self.myBreezecardNumButton = []
        self.myremovecardNumButton = []
        for index, breeze in enumerate(myBreezecard):
            self.myBreezecardNumButton.append(breeze[0])
            self.myremovecardNumButton.append(breeze[0])
            cardNumButton = Button(self.manageCardsWindow, text=breeze[0], width=19, padx=6, pady=4, borderwidth=1, relief="solid", command=lambda num=breeze[0]: self.select_tablecard(num)).grid(row=3+index+1, column=1)
            Button(self.manageCardsWindow, text=breeze[1], width=19, padx=6, pady=4, borderwidth=1, relief="solid").grid(row=3+index+1, column=2)
            removecardNumButton = Button(self.manageCardsWindow, text="remove", width=19, padx=6, pady=4, borderwidth=1, relief="solid", command=lambda removenum=breeze[0]: self.remove_tablecard(removenum)).grid(row=3+index+1, column=3)
            self.myBreezecardNumButton.append(cardNumButton)
            self.myremovecardNumButton.append(cardNumButton)
        return len(myBreezecard)

    def manageCardsWindowAddCardButtonClicked(self):
        # Click the Add Card Button on Manage Cards Window:
        entryBreezecard = self.entryBreezeCard.get()
        #self.passusername - user

        #Error if entry is empty
        if not entryBreezecard:
            messagebox.showwarning("Breezecard input is empty", "Please enter Breezecard.")
            return False

        #Error if entry is invalid (not 16-digit)
        if (len(entryBreezecard) != 16):
            messagebox.showwarning("Breezecard input invalid", "Breezecard has to be 16-digit number")
            return False

        #Error if entry is invalid (16 digit with something other than number)
        if (entryBreezecard.isdigit() == 0):
            messagebox.showwarning("Breezecard input invalid", "Breezecard number must be 16-digit numbers. \n Your input contains something other than number.")
            return False

        #1) Breezecard doesn't exist in database -> insert into database with value 0.00
        hasBreeze = self.cursor.execute("SELECT * FROM Breezecard WHERE cardNum = %s", entryBreezecard)
        if not hasBreeze:
            self.cursor.execute("INSERT INTO Breezecard(cardNum, value, cUsername) VALUES (%s, 0.00, %s)", (entryBreezecard, self.passusername))
            self.db.commit()
            messagebox.showwarning("Add Card Success", "You have successfully added Breezecard to the system.")
            rowing = 4 + self.showMyBreezecard()
            self.addValueToSelectedCardLabel.grid(row=rowing)
            self.addValueToSelectedCardLabel2.grid(row=rowing)
            self.creditcardLabel.grid(row=rowing+1)
            self.creditcardEntry.grid(row=rowing+1)
            self.valueLabel.grid(row=rowing+2, column=1, sticky=W)
            self.valueEntry.grid(row=rowing+2, column=2, sticky=W)
            self.addValueButton.grid(row=rowing+3, column=3, sticky=W+E)
            return True

        self.cursor.execute("SELECT cUsername FROM Breezecard WHERE cardNUm = %s", entryBreezecard)
        hasUser = self.cursor.fetchone()[0]
        #2) Breezecard exist in database without user -> update to current user
        if not hasUser:
            self.cursor.execute("UPDATE Breezecard SET cUsername = %s WHERE cardNum = %s", (self.passusername, entryBreezecard))
            self.db.commit()
            messagebox.showwarning("Add Card Success", "You have successfully added Breezecard to the system.")
            rowing = 4 + self.showMyBreezecard()
            self.addValueToSelectedCardLabel.grid(row=rowing)
            self.addValueToSelectedCardLabel2.grid(row=rowing)
            self.creditcardLabel.grid(row=rowing+1)
            self.creditcardEntry.grid(row=rowing+1)
            self.valueLabel.grid(row=rowing+2, column=1, sticky=W)
            self.valueEntry.grid(row=rowing+2, column=2, sticky=W)
            self.addValueButton.grid(row=rowing+3, column=3, sticky=W+E)
            return True
        #3) Breezecard exist in database with user -> update to current user
        else:
            currentTime = datetime.now()
            currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO Conflict(conUsername, conCardNum, dateTime) VALUES (%s, %s, %s)", (self.passusername, entryBreezecard, currentTime))
            self.db.commit()
            messagebox.showwarning("Add Card Failed", "This Breezecard already has a user. \n Please contact one of our representatives.")
            return False

    def manageCardsWindowAddValueButtonClicked(self):
        # Click the Add Value Button on Manage Cards Window:
        entryCreditCard = self.entryCreditCard.get()
        entryValue = self.entryValue.get()

        #Error: entryCreditCard empty
        if not entryCreditCard:
            messagebox.showwarning("Credit Card Input Empty", "Please input your credit card information.")
            return False
        #Error: entryValue empty
        #Error: breezecard not selected
        #Error: entryCreditCard not 16 digits long
        #Error: entryCreditCard not digit
        #Error: currentValue + newValue = 1000 (value exceeded)

        #Add Value to the Card and update the page



        print("clicked")

    def passengerFunctionalityWindowViewTripHistoryButtonClicked(self):
        # Click the View Trip History Button on Passenger Functionality Window:
        pass

    def passengerFunctionalityWindowLogOutButtonClicked(self):
        # Click the Log Out Button on Passenger Functionality Window:
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