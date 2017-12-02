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
                    self.cursor.execute("INSERT INTO Breezecard(cardNum, value, cUsername) VALUES(%s, 0.00, %s)", (self.existBreeze, self.regusername))
                    self.db.commit()
                    messagebox.showwarning("Registration Success", "You have successfully registered to MARTA system! Please log in.")
                    self.newUserRegistrationWindow.destroy()
                    return True
                #2) If Breezecard input already have user -> delete from Breezecard table and put in Conflict table (suspend)
                else:
                    currentTime = datetime.now()
                    currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
                    self.hashpassword = self.computeMD5hash(self.regpassword)
                    self.cursor.execute("INSERT INTO User(username, password, IsAdmin) VALUES(%s, %s, FALSE)", (self.regusername, self.hashpassword))
                    self.cursor.execute("INSERT INTO Passenger(pUsername, email) VALUES(%s, %s)", (self.regusername, self.regemail))
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
        #Add components for passengerFunctionalityWindow

        #temporary label
        passengerLabel = Label(passengerFunctionalityWindow, text = "passenger")
        passengerLabel.grid(row=2, column=2, sticky=W)

    #=============Administrator Functionality Window========================
    def createAdminFunctionalityWindow(self):
        self.adminFunctionalityWindow = Toplevel()
        self.adminFunctionalityWindow.title("Administrator")

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.loginWindow.destroy()

        self.adminFunctionalityWindow.protocol("WM_DELETE_WINDOW", on_closing)

    # def buildAdminFunctionalityWindow(self, adminFunctionalityWindow):
    #     #Add component for adminFunctionalityWindow

    #     #Station Management Button
    #     stationManagementButton = Button(adminFunctionalityWindow, text="Station Management", command = self.stationManagementButtonClicked)
    #     stationManagementButton.grid(row=1, column=3, sticky=W + E)

    #     #Suspend Cards Button
    #     suspendedCardButton = Button(adminFunctionalityWindow, text="Suspended Cards")
    #     suspendedCardButton.grid(row=3, column=3, sticky=W + E)

    #     #Breezecard Management Button
    #     breezecardManagementButton = Button(adminFunctionalityWindow, text="Breezecard Management")
    #     breezecardManagementButton.grid(row=5, column=3, sticky=W + E)

    #     #Passenger Flow Report Button
    #     passengerFlowReportButton = Button(adminFunctionalityWindow, text="Passenger Flow Report")
    #     passengerFlowReportButton.grid(row=7, column=3, sticky=W + E)



        #---------------------------- ver 3.0 -------------------------------------
    def buildAdminFunctionalityWindow(self, adminFunctionalityWindow):
        #Add component for adminFunctionalityWindow

        #Station Management Button
        stationManagementButton = Button(adminFunctionalityWindow, text="Station Management",command=self.adminFunctionalityWindowStationManagementButtonClicked)
        stationManagementButton.grid(row=1, column=3, sticky=W + E)

        #Suspend Cards Button
        suspendedCardButton = Button(adminFunctionalityWindow, text="Suspended Cards")
        suspendedCardButton.grid(row=3, column=3, sticky=W + E)

        #Breezecard Management Button
        breezecardManagementButton = Button(adminFunctionalityWindow, text="Breezecard Management",command = self.adminFunctionalityWindowBreezecardManagementButtonClicked)
        breezecardManagementButton.grid(row=5, column=3, sticky=W + E)

        #Passenger Flow Report Button
        passengerFlowReportButton = Button(adminFunctionalityWindow, text="Passenger Flow Report")

        #Log Out Button        passengerFlowReportButton.grid(row=7, column=3, sticky=W + E)

        logOutAdminButton = Button(adminFunctionalityWindow, text="Log Out") #,command=self.adminFunctionalityWindowLogOutButtonClicked)
        logOutAdminButton.grid(row=9, column=3, sticky=W + E)
    #===============Administrator Functionality - Station Management=========================
    def adminFunctionalityWindowStationManagementButtonClicked(self):
        # Click the Station Management Button on Admin Functionality Window:
        self.createStationManagementWindow()
        self.buildStationManagementWindow(self.stationManagementWindow)

    #Station Management Window
    def createStationManagementWindow(self):
        self.stationManagementWindow = Toplevel()
        self.stationManagementWindow.title("Station Listing")


    # def selectElement(self,event2):
    #     curElement = self.stationListingTree.focus()
    #     print(list(self.stationListingTree.item(curElement)['values'])


    def buildStationManagementWindow(self, stationManagementWindow):
        #Add component for stationManagementWindow
        departureLabel = Label(stationManagementWindow, text = "Station Listing", font = "verdana 20 bold")
        departureLabel.grid(row=1, column=2, sticky= W+E, padx=100,pady=20)


        self.stationListingTree = ttk.Treeview(stationManagementWindow, column=("1", "2", "3", "4"))
        self.stationListingTree['show'] = "headings"
        self.stationListingTree.column("1", width = 150, anchor = "center")
        self.stationListingTree.column("2", width = 150, anchor = "center")
        self.stationListingTree.column("3", width = 150, anchor = "center")
        self.stationListingTree.column("4", width = 150, anchor = "center")

        self.stationListingTree.heading("1", text = "Station Name")
        self.stationListingTree.heading("2", text = "Stop ID")
        self.stationListingTree.heading("3", text = "Fare")
        self.stationListingTree.heading("4", text = "Status")



        self.cursor.execute("SELECT name, stopID, fare, ClosedStatus FROM Station")

        self.selectstationTuple = self.cursor.fetchall()
        self.stationNameList = []
        self.stopIDList = []
        self.fareList = []
        self.statusList = []
        self.statusListEdited = []
        for i in self.selectstationTuple:
            self.stationNameList.append(i[0])
            self.stopIDList.append(i[1])
            self.fareList.append(i[2])
            self.statusList.append(i[3])

        for i in range(len(self.statusList)):
            if self.statusList[i] == 0:
                self.statusListEdited.append("Closed");
            elif self.statusList[i] == 1:
                self.statusListEdited.append("Open");


        # Insert data into the treeview
        for i in range(len(self.selectstationTuple)):
            self.stationListingTree.insert('',i,values=(self.stationNameList[i],self.stopIDList[i],self.fareList[i],self.statusListEdited[i]))
        self.stationListingTree.grid(row=2,column=1, columnspan=4, padx=20, pady=20)




        #Create Create New Station Button
        createNewStationButton = Button(stationManagementWindow, text="Create New Station",command = self.stationManagementWindowCreateNewStationButtonClicked)
        createNewStationButton.grid(row=4, column=1, sticky=W)

        #Create View Station Button
        viewStationButton = Button(stationManagementWindow, text="View Station",command = self.stationManagementWindowViewStationButtonClicked)
        viewStationButton.grid(row=4, column=4, sticky=E)


    def stationManagementWindowCreateNewStationButtonClicked(self):
        # Click the Create New Station Button on Station Management Window:
        self.createCreateNewStationWindow()
        self.buildCreateNewStationWindow(self.createNewStationWindow)

        #self.loginWindow.withdraw()

    #=============New User Registration Window==============
    def createCreateNewStationWindow(self):
        self.createNewStationWindow = Toplevel()
        self.createNewStationWindow.title("Create New Station")


        #---------------------------------------------------------
    def buildCreateNewStationWindow(self, createNewStationWindow):
        #Add component for Create New Station Window
        top_title = Label(createNewStationWindow, text = "Create Station", font = "verdana 10 bold")
        top_title.grid(column=2, sticky= W+E, padx = (0, 95))
        #Station Name Label
        stationNameLabel = Label(createNewStationWindow, text="Station Name")
        stationNameLabel.grid(row=1, column=1, sticky=W, pady=(10,5))

        #StopID Label
        stopIDLabel = Label(createNewStationWindow, text="Stop ID")
        stopIDLabel.grid(row=3, column=1, sticky=W, pady = 5)

        #Entry Fare Label
        entryFareLabel = Label(createNewStationWindow, text="Entry Fare")
        entryFareLabel.grid(row=5, column=1, sticky=W,pady = 5)

        #Station Type Label
        stationTypeLabel = Label(createNewStationWindow, text="Station Type")
        stationTypeLabel.grid(row=7, column=1, sticky=W,pady = 5)

        # nearestIntersection = Label(createNewStationWindow, text="Nearest Intersection")
        # nearestIntersection.grid(row=7, column=2, sticky=W)

        self.typeSelected = StringVar()
        self.typeSelected.set("bus")
        r1 = Radiobutton(createNewStationWindow, text="Bus Station", variable=self.typeSelected, value="bus")
        r1.grid(row=6, column=2, sticky=W)
        self.registerNearInt = StringVar()
        nearSEctionEntry = Entry(createNewStationWindow, textvariable=self.registerNearInt, width=20)
        nearSEctionEntry.grid(row=7, column=2, sticky=W)
        r2 = Radiobutton(createNewStationWindow, text="Train Station", variable=self.typeSelected, value="train")
        r2.grid(row=8, column=2, sticky=W)


        #Description of Open Station Label
        # descriptionOpenStationLabel = Label(createNewStationWindow,text="When checked, passengers can enter at this station.")
        # descriptionOpenStationLabel.grid(row=11,column=1, sticky = W)
        self.var1 = IntVar()
        self.var1.set(1)
        c1 = Checkbutton(createNewStationWindow, text="Open Station", variable=self.var1, onvalue=1, offvalue=0).grid(row=9, column=1, sticky=W)

         # Username Entry
        self.registrationStationName = StringVar()
        stationNameEntry = Entry(createNewStationWindow, textvariable=self.registrationStationName, width=25)
        stationNameEntry.grid(row=1, column=2, sticky = W,pady=(10,5))

        # Email Address Entry
        self.registrationStopID = StringVar()
        stopIDEntry = Entry(createNewStationWindow, textvariable=self.registrationStopID,width=25)
        stopIDEntry.grid(row=3, column=2, sticky= W , pady = 5)

        # Password Entry
        self.registrationFare = StringVar()
        self.registrationFare.set("$")
        fareEntry = Entry(createNewStationWindow, textvariable=self.registrationFare,width=25)
        fareEntry.grid(row=5, column=2, sticky =W, pady = 5)




        #Create Create Station Button
        createStationButton = Button(createNewStationWindow, text="Create Station", command=self.createNewStationWindowCreateStationButtonClicked)
        createStationButton.grid(row=12, column=2, padx=(100,0), sticky=E)


    def createNewStationWindowCreateStationButtonClicked(self):
        # Click the Create Station Button on Create New Station Window:
        def isfloat(value):
            try:
                float(value)
                return True
            except ValueError:
                return False
        #Clock the button on create new station Window
        self.regStationName = self.registrationStationName.get()
        self.regStopID = self.registrationStopID.get()
        self.regFare = self.registrationFare.get()
        if self.regFare[0] == '$':
            self.regFare = self.regFare[1:]
        self.regNearInt = self.registerNearInt.get()
        self.regType = self.typeSelected.get()
        self.checkboxVar = self.var1.get()
        print (self.checkboxVar)

        # Error message for station input empty
        if not self.regStationName:
            messagebox.showwarning("Station Name input is empty", "Please enter registering station name.")
            return False
        #Error message for stop id input empty
        if not self.regStopID:
            messagebox.showwarning("Stop ID input is empty", "Please enter registering Stop ID.")
            return False
        #Error message for fare input empty
        if not self.regFare:
            messagebox.showwarning("Station Fare input is empty", "Please enter valid station fare.")
            return False
        # Error message that input is not float value
        if not isfloat(self.regFare):
              messagebox.showwarning("Station Fare input is empty", "Please enter valid station fare.")
              return False
        else:
            isFare = (float(self.regFare) <= 50 and float(self.regFare) >= 0)

        # print (isFare)
        # Error message that input is not bween 0.00 and 50.00
        if not isFare:
            messagebox.showwarning("Fare input is not correct","Fare to enter must be between $0.00 and $50.00 \nPlease enter valid station fare.")
            return False


        if self.regType == "bus":
            if not self.regNearInt:
               messagebox.showwarning("Nearest Intersection input is empty", "Please enter valid input.")
               return False

        #Error message for username input already exist in db
        isStation = self.cursor.execute("SELECT * FROM Station WHERE name = %s", self.regStationName)
        if isStation:
            messagebox.showwarning("Station Name already exist", "The station name you entered already exist. \n Try different station.")
            return False

        #Error message for email input already exist in db
        isStopID = self.cursor.execute("SELECT * FROM Station WHERE stopID = %s", self.regStopID)
        if isStopID:
            messagebox.showwarning("stopID already exist", "The stopID you entered already exist. \n Try different stopID.")
            return False

        if (self.regType == "bus"):
            self.cursor.execute("INSERT INTO Station(stopID, name, IsTrain, fare, ClosedStatus) VALUES(%s, %s, False, %s, %s)", (self.regStopID, self.regStationName, self.regFare, self.checkboxVar))
            self.cursor.execute("INSERT INTO Bus(busID, nearestIntersection) VALUES(%s,%s)", (self.regStopID, self.regNearInt))
            messagebox.showwarning("Registration Success", "bus station has successfully registered to database.")
            self.createNewStationWindow.destroy()
            self.db.commit()
            self.buildStationManagementWindow(self.stationManagementWindow)
            return True
        elif (self.regType == "train"):
            self.cursor.execute("INSERT INTO Station(stopID, name, IsTrain, fare, ClosedStatus) VALUES(%s, %s, True, %s, %s)", (self.regStopID, self.regStationName, self.regFare, self.checkboxVar))
            messagebox.showwarning("Registration Success", "train station has successfully registered to database.")
            self.createNewStationWindow.destroy()
            self.db.commit()
            self.buildStationManagementWindow(self.stationManagementWindow)
            return True

    #------------------------- view station -------------------------------

    def stationManagementWindowViewStationButtonClicked(self):
        # Click the View Station Button on Station Management Window:
        curItem = self.stationListingTree.selection()
        if not self.stationListingTree.selection():
            messagebox.showwarning("Nothing Selected", "Please select an entry in the table!")
            return False
        self.createViewStationWindow(curItem)
        self.buildViewStationWindow(self.viewStationWindow, curItem)

    #Create View Station Window
    def createViewStationWindow(self, curItem):
        selectedStation = self.stationListingTree.item(curItem)['values'][0]
        self.viewStationWindow = Toplevel()
        self.viewStationWindow.title("Station Detail - %s" % selectedStation)#####STRING OF STATION NAME

    def buildViewStationWindow(self, viewStationWindow, curItem):
        #Add component for View Station Window
        #Station Detail Name Label
        def change_case(event=None):
            self.updateFareClicked(self.selectedFare)

        def red_text(event=None):
            updatefareLabel.config(fg="red")

        def black_text(event=None):
            updatefareLabel.config(fg="blue")



        self.selectedStation = self.stationListingTree.item(curItem)['values'][0]
        self.selectedStopID = self.stationListingTree.item(curItem)['values'][1]
        self.selectedFare = self.stationListingTree.item(curItem)['values'][2]
        self.selectedStatus = self.stationListingTree.item(curItem)['values'][3]
        if self.selectedStatus == "Open":
            statusBin = 1;
        elif self.selectedStatus == "Closed":
            statusBin = 0;
        print ("selected status: " + str(self.selectedStatus))

        stationDetailNameLabel = Label(viewStationWindow,text=self.selectedStation, font = "Verdana 12 bold") #####STRING OF STATION NAME
        stationDetailNameLabel.grid(row=2,column=1,sticky=W) #####STRING OF STATION NAME


        #Station Detail StopID Label
        stationDetailStopIDLabel = Label(viewStationWindow,text="Stop %s" % self.selectedStopID, fg = "red", font = "Verdana 8 bold") #####STRING OF STATION STOP ID
        stationDetailStopIDLabel.grid(row=2,column=10,sticky=E) #####STRING OF STATION STOP ID

        #Fare Label
        fareLabel = Label(viewStationWindow,text="Fare")
        fareLabel.grid(row=3,column=1,sticky=W)

        self.newFare = StringVar()
        self.newFare.set("$%s" % self.selectedFare)
        fareEntry2 = Entry(viewStationWindow, textvariable=self.newFare, width=30)
        fareEntry2.grid(row=3, column=2, sticky =W, pady = 5)

        updatefareLabel = Label(viewStationWindow, text="Update Fare", fg= "blue", font = "time 8 underline")
        updatefareLabel.bind("<Button-1>",change_case)
        updatefareLabel.bind("<Enter>",red_text)
        updatefareLabel.bind("<Leave>",black_text)

        updatefareLabel.grid(row=3,column=3, sticky=W)


        #Nearest Intersection in Station Detail Label
        nearestIntersectionStationDetailLabel = Label(viewStationWindow, text="Nearest\n  Intersection")
        nearestIntersectionStationDetailLabel.grid(row=5,column=1,sticky=W)

        ###INSERT MESSAGE "Not available for train stations" If Train CODE
        self.isTrainType();
        if (self.selectedType == 1):
            descriptionLabel = Label(viewStationWindow, text="Not available for train stations", font = "Verdana 7 bold")
            descriptionLabel.grid(row=5,column=2,sticky=W, padx=(0,150))
        elif (self.selectedType == 0):
            self.newNearIntSect = StringVar()
            self.cursor.execute("SELECT nearestIntersection FROM Bus WHERE busID = %s", self.selectedStopID)
            self.selectedIntSect = self.cursor.fetchone()
            self.selectedIntSect = self.selectedIntSect[0]
            self.newNearIntSect.set(self.selectedIntSect)
            print (self.selectedIntSect)
            stopIDEntry = Entry(viewStationWindow, textvariable=self.newNearIntSect,width=30)
            stopIDEntry.grid(row=5, column=2, sticky= W , padx=(0,150))






        #Open Station in Station Detail Label
        self.var2 = IntVar()
        self.var2.set(statusBin)
        c1 = Checkbutton(viewStationWindow, text="Open Station", variable=self.var2, onvalue=1, offvalue=0).grid(row=9, column=1, sticky=W)


        #Description of Open Station in Station Detail Label
        descriptionOpenStationStationDetailLabel = Label(viewStationWindow,text="When checked, passengers can enter at this station.")
        descriptionOpenStationStationDetailLabel.grid(row=10,column=1,sticky=W)

    # def change_case(event=None):
    #     def isfloat(value):
    #         try:
    #             float(value)
    #             return True
    #         except ValueError:
    #             return False
    #     print ("in def")
    #     inputFare = self.newFare.get()
    #     if inputFare[0] == '$':
    #         inputFare = inputFare[1:]
    #     if not inputFare:
    #         messagebox.showwarning("Station Fare input is empty", "Please enter valid station fare.")
    #         return False
    #     if not isfloat(self.inputFare):
    #         messagebox.showwarning("Station Fare input is empty", "Please enter valid station fare.")
    #     else:
    #         isFare = (float(self.inputFare) <= 50 and float(self.inputFare) >= 0)
    #     # Error message that input is not bween 0.00 and 50.00
    #     if not isFare:
    #         messagebox.showwarning("Fare input is not correct","Fare to enter must be between $0.00 and $50.00 \nPlease enter valid station fare.")
    #         return False
    def isTrainType(self):
        self.cursor.execute("SELECT IsTrain FROM Station WHERE stopID = %s", self.selectedStopID)
        self.selectedType = self.cursor.fetchone()
        self.selectedType =self.selectedType[0]
        print ("%s station is :" % self.selectedStation + str(self.selectedType))

        return True

    def updateFareClicked(self, selectedFare):
        def isfloat(value):
            try:
                float(value)
                return True
            except ValueError:
                return False
        print (self.newFare.get())
        inputFare = self.newFare.get()
        oldFare = self.selectedFare
        print (oldFare)

        if not inputFare:
            messagebox.showwarning("Station Fare input is empty", "Please enter valid station fare.")
            return False
        if inputFare[0] == '$':
            inputFare = inputFare[1:]
        if not isfloat(inputFare):
            messagebox.showwarning("Input is not float value", "Please enter valid fare value.")
            return False
        else:
            isFare = (float(inputFare) <= 50 and float(inputFare) >= 0)
        # Error message that input is not bween 0.00 and 50.00
        if float(oldFare) == float(inputFare):
            messagebox.showwarning("Nothing Has Changed", "Nothing has changed.\nPlease enter desire fare.")
            return False

        self.cursor.execute("UPDATE Station SET fare = %s WHERE StopID = %s",  (inputFare, self.selectedStopID))
        self.db.commit()
        messagebox.showwarning("Change Successfully", "Fare information has been updated for %s" % self.selectedStation)
        return True

    def adminFunctionalityWindowBreezecardManagementButtonClicked(self):
        self.createBreezecardMangementWindow()
        self.buildcreateBreezecardMangementWindow(self,createNewStationWindow)

    def createBreezecardMangementWindow(self):
        self.stationManagementWindow = Toplevel()
        self.stationManagementWindow.title("Breeze Card Management")


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