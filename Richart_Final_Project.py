import Tkinter as tk
import csv

class User:
    def __init__(self, username="user1", user_logged=False):
        self.setUsername(username)
        self.setUserLogged(user_logged)

    def setUsername(self, username):
        self.__username=username
    def getUsername(self):
        return self.__username
    
    user = property(fget=getUsername, fset=setUsername)
    
    def setUserLogged(self, user_logged):
        self.__user_logged=user_logged
    def getUserLogged(self):
        return self.__user_logged

    logged = property(fget=getUserLogged, fset=setUserLogged)
        
class Interface:
    def __init__(self, status="Home"):
        self.status = status

class Router:
    def __init__(self, master, nUser):
        self.master = master
        self.nUser = nUser
        if self.nUser.logged == False:
            self.app = Login_Frame(self.master, self.nUser)
        else:
            self.nInterface = Interface()
            self.app = Home_Frame(self.master, self.nUser, self.nInterface)
        
class Login_Frame:
    def __init__(self, master, nUser):
        self.master = master
        self.nUser = nUser
        self.login_frame = tk.Frame(self.master)
        self.login_frame.place(width=200, relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Label(self.login_frame, text="Username").pack(padx=10, pady=5)
        self.username = tk.Entry(self.login_frame)
        self.username.pack(padx=5,pady=5)
        self.username.insert(0, "user1")
        tk.Label(self.login_frame, text="Password").pack(padx=5, pady=5)
        self.password = tk.Entry(self.login_frame)
        self.password.pack(padx=5, pady=5)
        self.password.insert(0, "password")
        self.btnLog = tk.Button(self.login_frame, text="Login", command=lambda: self.logIn(nUser, self.login_frame, self.master))
        self.btnLog.pack(padx=5, pady=5)
        self.lblOutput = tk.Label(self.login_frame, text="")
        self.lblOutput.pack(padx=5, pady=5)

    def logIn(self, nUser, login_frame, master):
        self.nUser = nUser
        self.login_frame = login_frame
        self.master = master
        roles = ['user1', 'password']
        login_errors = ""
        u = self.username.get().lower()
        p = self.password.get().lower()

        if u == roles[0]:
            if p == roles[1]:
                self.nUser.logged = True
                self.nUser.user = u
            else:
                self.lblOutput["text"] = "The password is Wrong"
        else:
            self.lblOutput["text"] = "The username is Wrong"

        if nUser.logged == True:
            self.login_frame.destroy()
            self.nRouter = Router(master, nUser)
      
class Home_Frame:
    def __init__(self, master, nUser, nInterface, patient=[]):
        self.patient=patient
        self.master=master
        self.nInterface=nInterface
        self.nUser = nUser
        self.tab_bar=tk.Frame(self.master, background="white")
        self.tab_bar.place(x=0, y=0, height=100, width=1000)
       
        
        if nInterface.status == "Home":
            tk.Label(self.tab_bar, bg="white", text=nUser.user).place(relx=0.25, rely=0.5, anchor=tk.CENTER)
            tk.Label(self.tab_bar, bg="white", text=nInterface.status).place(relx=0.35, rely=0.5, anchor=tk.CENTER)
            self.btnNewPatient=tk.Button(self.tab_bar, bg="white", text="Patient Entry", command=lambda: self.patientEntry(self.master, self.nUser, self.nInterface, self.tab_bar, self.display_frame))
            self.btnNewPatient.place(relx=0.45, rely=0.5, anchor=tk.CENTER)
            self.btnCompleted=tk.Button(self.tab_bar, bg="white",text="Completed Vaccinations", command=lambda: self.completed(self.master, self.nUser, self.nInterface, self.tab_bar, self.display_frame))
            self.btnCompleted.place(relx=0.60, rely=0.5, anchor=tk.CENTER)
            self.btnLogout=tk.Button(self.tab_bar, bg="white",text="Logout", command=lambda: self.logOut(self.master, self.tab_bar,self.display_frame, self.nUser))
            self.btnLogout.place(relx=0.7225, rely=0.5, anchor=tk.CENTER)
        else:
            tk.Label(self.tab_bar, bg="white", text=nUser.user).place(relx=0.35, rely=0.5, anchor=tk.CENTER)
            tk.Label(self.tab_bar, bg="white", text=nInterface.status).place(relx=0.45, rely=0.5, anchor=tk.CENTER)
            self.btnHome=tk.Button(self.tab_bar, bg="white",text="Home", command=lambda: self.backHome(self.master, self.nUser, self.nInterface, self.tab_bar, self.display_frame))
            self.btnHome.place(relx=0.55, rely=0.5, anchor=tk.CENTER)
            self.btnLogout=tk.Button(self.tab_bar, bg="white",text="Logout", command=lambda: self.logOut(self.master, self.tab_bar,self.display_frame, self.nUser))
            self.btnLogout.place(relx=0.65, rely=0.5, anchor=tk.CENTER)
        
        self.display_frame=tk.Frame(self.master, background="grey")
        self.display_frame.place(x=0, y=200, height=600, width=1000)

        if self.nInterface.status=="Home":
            self.lb1 = tk.Listbox(self.display_frame, height=25, width=70, borderwidth=0)
            with open("PatientDatabase.csv", "rb") as f:
                r = csv.reader(f)
                z = 0
                x=0
                for row in r:
                    if not row:
                        tk.Label(self.display_frame, text="No Patients in Database").pack()
                    else:
                        if z == 0:
                            pass
                        if row[6] != '0':
                            pass
                        else:
                            x+=1
                            result = row[0] + " " + row[1] + "                     " + row[2] + "                        Ready for Vaccination"
                            self.lb1.insert(x, result)
                        z+=1

            self.lb1.pack()
            self.btnVerifyPatient=tk.Button(self.display_frame, text="VerifyPatient", command=lambda: self.verifyPatient(self.master, self.nUser, self.nInterface, self.tab_bar, self.display_frame, self.patient))
            self.btnVerifyPatient.pack()
            
        elif self.nInterface.status=="Patient Entry":
            
            tk.Label(self.display_frame, text="First Name").pack()
            self.fName = tk.Entry(self.display_frame)
            self.fName.pack(pady=5)
            tk.Label(self.display_frame, text="Last Name").pack()
            self.lName = tk.Entry(self.display_frame)
            self.lName.pack(pady=5)
            tk.Label(self.display_frame, text="DOB(mm/dd/yyyy)").pack()
            self.dob = tk.Entry(self.display_frame)
            self.dob.pack(pady=5)
            tk.Label(self.display_frame, text="Sex(M/F)").pack()
            self.sex = tk.Entry(self.display_frame)
            self.sex.pack(pady=5)
            tk.Label(self.display_frame, text="City").pack()
            self.city = tk.Entry(self.display_frame)
            self.city.pack(pady=5)
            tk.Label(self.display_frame, text="State").pack()
            self.state = tk.Entry(self.display_frame)
            self.state.pack(pady=5)
            tk.Label(self.display_frame, text="Vaccine").pack()
            self.vacTup = ('Zostavax', 'Fluvirin', 'Pneumovax', 'TDap', 'Varivax', 'Menomune')
            self.vaccine = tk.Spinbox(self.display_frame, values=self.vacTup)
            self.vaccine.pack(pady=5)
            self.btnEntrySubmit = tk.Button(self.display_frame, text="Process", command=lambda: self.processPatient(self.master, self.nUser, self.nInterface, self.tab_bar, self.display_frame))
            self.btnEntrySubmit.pack()
            
        elif self.nInterface.status=="Verify Patient":
            pt_info =[]
            with open('PatientDatabase.csv', 'rb') as f:
                r = csv.reader(f)
                for row in r:
                    if row[0] == patient[0] and row[1] == patient[1] and row[2]==patient[2]:
                        pt_info = row

            tk.Label(self.display_frame, text="Firstname:\t" +pt_info[0]).pack(pady=5)
            tk.Label(self.display_frame, text="Lastname: \t" + pt_info[1]).pack(pady=5)
            tk.Label(self.display_frame, text="DOB:      \t" + pt_info[2]).pack(pady=5)
            tk.Label(self.display_frame, text="Sex:      \t" +pt_info[3]).pack(pady=5)
            tk.Label(self.display_frame, text="City:     \t" +pt_info[4]).pack(pady=5)
            tk.Label(self.display_frame, text="State:    \t" +pt_info[5]).pack(pady=5)
            tk.Label(self.display_frame, text="Vaccine:  \t" +pt_info[7]).pack(pady=5)
            tk.Label(self.display_frame, text="Location(Left/Right Arm)").pack(pady=5)
            self.loc = tk.Entry(self.display_frame)
            self.loc.pack(pady=5)
            tk.Label(self.display_frame, text="Date of Administration").pack()
            self.date=tk.Entry(self.display_frame)
            self.date.pack(pady=5)
            tk.Label(self.display_frame, text="Administered By").pack()
            self.admin =tk.Entry(self.display_frame)
            self.admin.pack(pady=5)
            tk.Label(self.display_frame, text="Profession(NP/MD/RPH/PA/BSN").pack()
            self.title =tk.Entry(self.display_frame)
            self.title.pack(pady=5)

            self.btnVerifyData = tk.Button(self.display_frame, text="Complete Vaccination", command=lambda: self.verifyData(self.master, self.nUser, self.nInterface, self.tab_bar, self.display_frame, pt_info))
            self.btnVerifyData.pack(pady=10)

        elif self.nInterface.status=="Completed Vaccinations":
             
            self.lb1 = tk.Listbox(self.display_frame,borderwidth=0, height=25, width=70)
            with open("PatientDatabase.csv", "rb") as f:
                r = csv.reader(f)
                x=1
                for row in r:
                    if row[6] == '1':
                        result = row[0] + " " + row[1] + "              " + row[2] + "                   Completed" + " " + row[9]
                        self.lb1.insert(x, result)
                    x+=1
            self.lb1.pack() 
                     

    def logOut(self, master,tab_bar, display_frame, nUser):
        self.nUser = nUser
        self.nUser.logged = False       
        self.master = master
        self.tab_bar = tab_bar
        self.tab_bar.destroy()
        self.display_frame.destroy()
        self.nRouter = Router(self.master, self.nUser)

    def patientEntry(self, master, nUser, nInterface, tab_bar, display_frame):
        self.nUser = nUser
        self.master = master
        self.tab_bar = tab_bar
        self.display_frame = display_frame
        self.nInterface = nInterface
        self.nInterface.status = "Patient Entry"
        self.tab_bar.destroy()
        self.display_frame.destroy()
        self.home = Home_Frame(self.master, self.nUser, self.nInterface)

    def verifyPatient(self, master, nUser, nInterface, tab_bar, display_frame,patient):
        self.nUser = nUser
        self.master = master
        self.tab_bar = tab_bar
        self.display_frame = display_frame
        self.nInterface = nInterface
        self.nInterface.status = "Verify Patient"
        self.patient = patient
        if not self.lb1.curselection():
            pass
        else:
            self.patient=self.lb1.get(self.lb1.curselection()).split()
            self.tab_bar.destroy()
            self.display_frame.destroy()
            self.ndisplay = Home_Frame(self.master, self.nUser, self.nInterface, self.patient)

    def completed(self, master, nUser, nInterface, tab_bar, display_frame):
        self.nUser = nUser
        self.master = master
        self.tab_bar = tab_bar
        self.display_frame = display_frame
        self.nInterface = nInterface
        self.nInterface.status = "Completed Vaccinations"
        self.tab_bar.destroy()
        self.display_frame.destroy()
        self.ndisplay = Home_Frame(self.master, self.nUser, self.nInterface)

    def backHome(self, master, nUser, nInterface, tab_bar, display_frame):
        self.nUser = nUser
        self.master = master
        self.tab_bar = tab_bar
        self.display_frame = display_frame
        self.nInterface = nInterface
        self.nInterface.status = "Home"
        self.tab_bar.destroy()
        self.display_frame.destroy()
        self.ndisplay = Home_Frame(self.master, self.nUser, self.nInterface)

    def processPatient(self, master, nUser, nInterface, tab_bar, display_frame):
        nPatient = [[self.fName.get(), self.lName.get(), self.dob.get(), self.sex.get(), self.city.get(), self.state.get(),'0', self.vaccine.get(), '', '', '', '']]
        with open('PatientDatabase.csv', 'ab') as f:
            w = csv.writer(f)
            w.writerows(nPatient)
        self.nUser = nUser
        self.master = master
        self.tab_bar = tab_bar
        self.display_frame = display_frame
        self.nInterface = nInterface
        self.backHome(self.master, self.nUser, self.nInterface, self.tab_bar, self.display_frame)

    def verifyData(self, master, nUser, nInterface, tab_bar, display_frame, pt_info):
        temp =[]
        self.pt_info=pt_info
        update_entry=[[self.pt_info[0], self.pt_info[1], self.pt_info[2], self.pt_info[3], self.pt_info[4], self.pt_info[5], '1', self.pt_info[7], self.loc.get(), self.date.get(), self.admin.get(), self.title.get()]]
        with open('PatientDatabase.csv', 'rb') as f:
            r= csv.reader(f)
            for row in r:
                if row[0] != pt_info[0] and row[1] != pt_info[1] and row[2] != pt_info[2]:
                    temp.append(row)
                    
        with open('PatientDatabase.csv', 'wb') as f:
            w = csv.writer(f)
            w.writerows(temp)
    
        with open('PatientDatabase.csv', 'ab') as f:
            w = csv.writer(f)
            w.writerows(update_entry)

        self.nUser = nUser
        self.master = master
        self.tab_bar = tab_bar
        self.display_frame = display_frame
        self.nInterface = nInterface
        self.backHome(self.master, self.nUser, self.nInterface, self.tab_bar, self.display_frame)



class MyApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.bg_frame = tk.Frame(root, height=700, width=1000, background='grey')
        self.menubar = tk.Menu(self.bg_frame)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Close", command=root.destroy)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        root.config(menu=self.menubar)
        self.nUser = User()
        self.nRouter = Router(self.bg_frame, self.nUser)   
        self.bg_frame.pack()

if __name__ == "__main__":
    root = tk.Tk()
    MyApp(root).pack()
    root.mainloop()
        
