from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

from urllib.request import Request, urlopen
from tkinter import ttk, messagebox
import pymysql
import requests
import bs4 as bs
import lxml
import numpy as np
import matplotlib.pyplot as plt

root = Tk()
root.title("Student Management System")
root.geometry('1250x700+150+50')
root.config(bg="red")
root.resizable(False, False)
s = ttk.Style()

s.configure('Wild.TButton', background='black', foreground='blue', highlightthickness='20',
            font=('Helvetica', 18, 'italic'), anchor='w')
s.configure('id.TButton', background='red', foreground='#32a88b', highlightthickness='10',
            font=('Times', 10, 'bold', 'italic'))

global isfilevalid
isfilevalid = False

def insertImage():

    global filename
    global isfilevalid
    filename = filedialog.askopenfilename(initialdir="/", title="select a file",
                                          filetype=(("jpg", "*.jpg"), ("All Files", "*.*")))
    isfilevalid = True


################# database operations ################
global cursor, con

try:
    con = pymysql.connect(host="localhost", user="root", password="abc456", db='sms')
    cursor = con.cursor()
except pymysql.Error as e:
    messagebox.showerror("insert new Entry ", "%s: " % (e.args[1]))


######################## insert data ################
def insert(list):
    con = None
    try:
        con = pymysql.connect(host="localhost", user="root", password="abc456", db='sms')

        # prepare a cursor object using cursor() method
        cursor = con.cursor()
        query = "insert into student values('%d','%s','%s','%s','%s','%s','%s','%s')"
        params = (int(list[0]), list[1], list[2], list[3], list[4], list[5], list[6], list[7])
        cursor.execute(query % params)
        con.commit()
        fetch_data()
        con.close()
    except pymysql.Error as e:
        messagebox.showerror("insert new Entry ", "%s: " % (e.args[1]))
    finally:
        if (con == None):
            con.commit()
            con.close()


############### UPDATE TABLE ##############
def update_table(list):
    con = None
    try:
        con = pymysql.connect(host="localhost", user="root", password="abc456", db='sms')
        cursor = con.cursor()
        print("conn success")
        query = "update sms set name=%s,mobile=%s,email=%s,address=%s,gender=%s,dob=%s,image=%s where rno=%s"
        params = (list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[0])
        print(list[7])
        cursor.execute(query, params)
        print("query sucess")
        con.commit()
        fetch_data()
        con.close()
    except pymysql.Error as e:
        messagebox.showerror("insert new Entry ", "%s: " % (e.args[1]))
    finally:
        if (con == None):
            con.close()


############# get image ############

def get_image(event):
    global my_img1

    cursor_row = student_table.focus()
    contents = student_table.item(cursor_row)
    row = contents['values']
    Image_frame = Frame(root, relief=GROOVE, borderwidth=4)
    Image_frame.place(x=1115, y=50, width=120, height=120)
    try:
        my_img1 = ImageTk.PhotoImage(Image.open(row[7]).resize((120,120), Image.ANTIALIAS))
        my_img = Label(Image_frame, image=my_img1)
        my_img.pack()
    except:
        messagebox.showinfo("Image not inserted","Please insert an image")


###################### delete data from table #############

def delete_data():
    con = None
    try:
        cursor_row = student_table.focus()
        contents = student_table.item(cursor_row)
        row = contents['values']
        con = pymysql.connect(host="localhost", user="root", password="abc456", db='sms')
        cursor = con.cursor()
        query = "delete from sms where rno=%s"
        params = (row[0])
        cursor.execute(query, params)
        con.commit()
        con.close()
        fetch_data()
    except IndexError:
        messagebox.showerror("Error", "Select atleast one item")
    except Exception as e:
        messagebox.showerror("Error", "%s: " % (e.args[1]))


############## search data #########################
def search_data():
    con = None
    try:
        con = pymysql.connect(host="localhost", user="root", password="abc456", db='sms')
        cursor = con.cursor()
        query = "select * from sms where " + str(search_combo.get()) + " LIKE '%" + str(searchEntry.get() + "%'")
        print(query)
        cursor.execute(query)
        rows = cursor.fetchall()
        if (len(rows) == 0):
            raise Exception("Entry not found")
        if len(rows) != 0:
            print("this is executed")
            student_table.delete(*student_table.get_children())
            for row in rows:
                student_table.insert('', END, values=row)
            con.commit()
        con.close()
    except pymysql.Error as e:
        messagebox.showerror("insert new Entry ", "%s: " % (e.args[1]))
    finally:
        if (con == None):
            con.commit()
            con.close()


#################### fetch data ##############

def fetch_data():
    con = None
    try:
        con = pymysql.connect(host="localhost", user="root", password="abc456", db='sms')
        cursor = con.cursor()
        query = "select * from sms"
        cursor.execute(query)
        rows = cursor.fetchall()
        if len(rows) != 0:
            student_table.delete(*student_table.get_children())
            for row in rows:
                student_table.insert('', END, values=row)
            con.commit()
        con.close()
    except pymysql.Error as e:
        messagebox.showerror("insert new Entry ", "%s: " % (e.args[1]))
    finally:
        if (con == None):
            con.commit()
            con.close()


####################### graph ###################
def makegraph():
    try:
        con = pymysql.connect(host="localhost", user="root", password="abc456", db='sms')
        cursor = con.cursor()
        query = "select * from sms"
        cursor.execute(query)
        data = cursor.fetchall()
        marks = []
        names = []
        for m in data:
            marks.append(m[6])
        for n in data:
            names.append(n[1])
        plt.bar(names, marks, label="Marks of Students", width=0.20)
        plt.title("Marks of Students")
        plt.xlabel("Names", fontsize=10)
        plt.ylabel("Marks", fontsize=10)
        plt.legend()
        plt.grid()
        plt.show()

        print(marks)
        print(names)

        con.commit()
        con.close()
    except Exception as e:
        messagebox.showerror(e)
    finally:
        if (con == None):
            con.commit()
            con.close()


############ quote changer ##############
def qouteschanger():
    try:
        url = "https://www.success.com/17-motivational-quotes-to-inspire-you-to-be-successful/"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        web_byte = urlopen(req).read()
        soup = bs.BeautifulSoup(web_byte, 'lxml')

        for div in soup.find('h3', {'class': 'rtecenter'}):
            quote_str = div.string
            print(quote_str)

        quotes.config(text=quote_str, anchor="center")
    except Exception as e:
        messagebox.showerror("try again", "internet connection not available")


##################### FORM ####################
def loadform(check, decide):
    def submit(decide):
        checkrollno = rollEntry.get()
        checkname = nameEntry.get()
        checkmobile = mobEntry.get()
        checkmarks = marksEntry.get()
        print(checkrollno + checkmarks + checkname + checkmobile)
        str = ""
        valid = False

        try:
            if not (checkrollno.isnumeric()):
                valid = True
                raise Exception("Enter Only Numbers in Roll No\n")
            if int(checkrollno) <= 0:
                valid = True
                raise Exception("Enter Only positive Numbers in Roll No\n")

            namecheck = checkname.strip()
            data = namecheck.replace(' ', '')
            if not (data.isalpha()):
                valid = True
                raise Exception('Enter only Alphabets in Name Field\n')

            if not (checkmobile.isnumeric()):
                valid = True
                raise Exception("Enter Only Numbers in Contact No\n")

            if not (len(checkmobile) == 10):
                valid = True
                raise Exception("Enter valid contact\n")

            if (not (checkmarks.isnumeric())):
                valid = True
                raise Exception("Enter valid marks\n")

            if (int(checkmarks) < 0 or int(checkmarks) > 100):
                valid = True
                raise Exception("Enter valid marks\n")

            print(str)
        except Exception as e:
            messagebox.showerror("try again", e)

        if (not (valid)):
            if (decide == "adds"):
                if(isfilevalid):
                    list = [rollEntry.get(), nameEntry.get(), mobEntry.get(),
                            emailEntry.get(), addressEntry.get('1.0', END), combo_gender.get(), marksEntry.get(),
                            filename]

                else:
                    list = [rollEntry.get(), nameEntry.get(), mobEntry.get(),
                            emailEntry.get(), addressEntry.get('1.0', END), combo_gender.get(), marksEntry.get(),
                            "C:\demo\bird.jpg"]
                insert(list)
                check.destroy()

            else:
                if(isfilevalid):
                    list = [rollEntry.get(), nameEntry.get(), mobEntry.get(), emailEntry.get(),
                        addressEntry.get('1.0', END), combo_gender.get(), marksEntry.get(), filename]
                else:
                    list = [rollEntry.get(), nameEntry.get(), mobEntry.get(), emailEntry.get(),
                            addressEntry.get('1.0', END), combo_gender.get(), marksEntry.get(),"C:\demo\demo\image.jpg"]


                print(list)
                update_table(list)
                print("update")
                check.destroy()

    ################## labels for dataentry ###############

    rno = Label(check, text=" Enter Roll No :", font=('Times', 20, 'bold'), relief=GROOVE, anchor="w")
    rno.place(x=10, y=20)

    name = Label(check, text=" Enter Name :", font=('Times', 20, 'bold'), anchor="w")
    name.place(x=10, y=80)

    mob = Label(check, text=" Enter Mobile :", font=('Times', 20, 'bold'), anchor="w")
    mob.place(x=10, y=140)

    email = Label(check, text=" Enter Email :", font=('Times', 20, 'bold'), anchor="w")
    email.place(x=10, y=200)

    address = Label(check, text=" Enter Address :", font=('Times', 20, 'bold'), anchor="w")
    address.place(x=10, y=260)

    gen = Label(check, text=" Enter Gender :", font=('Times', 20, 'bold'), anchor="w")
    gen.place(x=10, y=340)

    marks = Label(check, text=" Enter Marks :", font=('Times', 20, 'bold'), anchor="w")
    marks.place(x=10, y=400)

    ######### ENTRY WIDGET #####################

    rollEntry = Entry(check, font=('roman', 15, 'bold'), bd=5)
    rollEntry.place(x=220, y=20)

    nameEntry = Entry(check, font=('roman', 15, 'bold'), bd=5)
    nameEntry.place(x=220, y=80)

    mobEntry = Entry(check, font=('roman', 15, 'bold'), bd=5)
    mobEntry.place(x=220, y=140)

    emailEntry = Entry(check, font=('roman', 15, 'bold'), bd=5)
    emailEntry.place(x=220, y=200)

    addressEntry = Text(check, width=25, height=3, borderwidth=3)
    addressEntry.place(x=220, y=260, height=60)

    combo_gender = ttk.Combobox(check, text="Gender", font=('roman', 15, 'bold'), state='readonly')
    combo_gender['values'] = ("male", "female", "other")
    combo_gender.place(x=220, y=340)

    marksEntry = Entry(check, font=('roman', 15, 'bold'), bd=5)
    marksEntry.place(x=220, y=400)

    ############## image button ###########
    save_Image = Button(check, text="Insert Image", width=10, command=insertImage)
    save_Image.place(x=170, y=450)

    ############## submit button ############
    submits = ttk.Button(check, text="Submit", style='Wild.TButton', width=10, command=lambda: submit(decide))
    submits.place(x=150, y=500)

    check.mainloop()


####################### data Entry functions ############

def add():
    addframe = Toplevel(master=root)
    addframe.title(" add data entry")
    addframe.geometry("500x600+200+150")
    addframe.resizable(False, False)
    addframe.grab_set()
    loadform(addframe, "adds")


def delete():
    print("delete")
    delete_data()


def update():
    updtframe = Toplevel(master=root)
    updtframe.title("update entry")
    updtframe.geometry("500x600+200+150")
    updtframe.resizable(False, False)
    updtframe.grab_set()
    loadform(updtframe, "updates")


def graph():
    makegraph()


def exit():
    res = messagebox.askyesnocancel('Notification', 'Do you Want to exit ?')
    if (res == True):
        root.destroy()


def search():
    print("search")
    search_data()


################ DATA FRAME ############
data_frame = Frame(root, bg='cyan', relief=GROOVE, borderwidth=4)
data_frame.place(x=10, y=180, width=400, height=500)

####################### buttons for data entry ########
add = ttk.Button(data_frame, text="1. Add Student", style='Wild.TButton', width=20, command=add)
add.pack(side=TOP, expand=True)

delete = ttk.Button(data_frame, text="2. Delete Student", style='Wild.TButton', width=20, command=delete)
delete.pack(side=TOP, expand=True)

update = ttk.Button(data_frame, text="3. Update Student", style='Wild.TButton', width=20, command=update)
update.pack(side=TOP, expand=True)

show_all = ttk.Button(data_frame, text="4. Show All ", style='Wild.TButton', width=20, command=fetch_data)
show_all.pack(side=TOP, expand=True)

graph = ttk.Button(data_frame, text="5. Graph", style='Wild.TButton', width=20, command=graph)
graph.pack(side=TOP, expand=True)

exit = ttk.Button(data_frame, text="6.  Exit", style='Wild.TButton', width=20, command=exit)
exit.pack(side=TOP, expand=True)

############## image frame #######


################ content FRAME ############
content_frame = Frame(root, bg='cyan', relief=GROOVE, borderwidth=4)
content_frame.place(x=420, y=180, width=815, height=500)
###################### Image Frame #########################


###########serach opt ###################
search_label = Label(root, text="Search By", bg='cyan', font=("times", 15, 'italic'))
search_label.place(x=450, y=190)

search_combo = ttk.Combobox(root, state='readonly')
search_combo['values'] = ("rno", "name")
search_combo.place(x=550, y=193)

searchEntry = Entry(root, font=('', 10, 'italic'), bd=2)
searchEntry.place(x=700, y=193)

search_btn = ttk.Button(root, text="Search", command=search)
search_btn.place(x=850, y=190)

########## table frame ###############
table_frame = Frame(root, bg='blue', relief=GROOVE, borderwidth=4)
table_frame.place(x=425, y=250, width=805, height=425)

scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
scroll_y = Scrollbar(table_frame, orient=VERTICAL)
student_table = ttk.Treeview(table_frame, columns=("roll", "Name", "Contact", "Email", "Address", "Gender", "Marks"),
                             xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_x.pack(side=BOTTOM, fill=X)
scroll_x.config(command=student_table.xview)
scroll_y.config(command=student_table.yview)
student_table.heading("roll", text="Roll No")
student_table.heading("Name", text="Name")
student_table.heading("Contact", text="Contact")
student_table.heading("Email", text="Email")
student_table.heading("Address", text="Address")
student_table.heading("Gender", text="Gender")
student_table.heading("Marks", text="Marks")
student_table['show'] = 'headings'
student_table.pack(fill=BOTH, expand=1)
student_table.bind("ButtonRelease-3", delete_data)
fetch_data()
student_table.bind("<ButtonRelease-1>", get_image)

################ title ###################
t = " Student Management System "
Title = Label(root, text=t, borderwidth=6, bg='red', font=('chiller', 25))
Title.place(x=400, y=110)

############# quotes ###############

quotes = Label(root, text="hi", borderwidth=6, bg='red', font=('chiller', 25))
quotes.place(x=300, y=10)
qouteschanger()

############### weather ############
strs = ""
try:
    apiaddress = "http://api.openweathermap.org/data/2.5/weather?q=mumbai&units=metric&appid=5ec14d035276f3fe60e483f6dabbf65a"
    json_data = requests.get(apiaddress).json()
    formatted_data = json_data['main']
    strs += "Temperature :  " + str(formatted_data['temp']) + u"\N{DEGREE SIGN}" + "C" + "\n"
    strs += "Feels_like :  " + str(formatted_data['feels_like']) + u"\N{DEGREE SIGN}" + "C"
except Exception as e:
    messagebox.showerror("try again", "internet connection not available")

weather = Label(root, text=strs, borderwidth=6, bg='cyan', font=('chiller', 10), width=20)
weather.place(x=10, y=10)

root.mainloop()