import tkinter as tk
from tkinter import ttk
import mysql.connector as msc
from tkinter import messagebox
from Database_Structure import Database,Table,Column

dbc=msc.connect(host='localhost',user='root',passwd='root',database='spms')
db=dbc.cursor()
def run_query(query):
	print(query)
	db.execute(query)
	x=db.fetchall()
	dbc.commit()
	return x


class MainApp(tk.Tk):
	def __init__(self,*args,**kwargs):
		self.dbc=msc.connect(host='localhost',user='root',passwd='root',database='spms')
		self.db=self.dbc.cursor()
		tk.Tk.__init__(self,*args,**kwargs)
		self.state('zoomed')
		self.config(bg='black')
		container=tk.Frame(self)
		container.place(x=50,y=50)
		self.container=container
		self.drawLogin()
		self.mainloop()


	def drawLogin(self):
		LoginPage(self)

	def logger(self,tup):
		if tup[-2]=='C':
			CEODashBoard(self,tup)
		elif tup[-2]=='M':
			MGRDashBoard(self,tup)
		elif tup[-2]=='E':
			EMPDashBoard(self,tup)



class LoginPage(ttk.Frame):
	def __init__(self,parent:MainApp):
		self.parent=parent
		ttk.Frame.__init__(self,parent)
		login_frame=ttk.LabelFrame(self,text="Login Details")
		user_label=ttk.Label(login_frame,text="username:")
		pass_label=ttk.Label(login_frame,text="password:")
		user_label.grid(row=0,column=0)
		pass_label.grid(row=1,column=0)
		user_entry=ttk.Entry(login_frame)
		pass_entry=ttk.Entry(login_frame)
		user_entry.grid(row=0,column=1)
		pass_entry.grid(row=1,column=1)
		login_button=ttk.Button(login_frame,text="Login",
command=lambda u=user_entry,p=pass_entry:self.login(u.get(),p.get()))
		login_button.grid(row=2,column=1)
		login_frame.pack()
		self.pack()

	def login(self,user,passwd):
		if user=='' or passwd=='':messagebox.showinfo("No Value Provided","Please enter valid credentials")
		else:
			qr=run_query(f"select e.* from employee e,login_details l where (l.uname,l.passwd)in(('{user}','{passwd}')) and e.emp_id=l.emp_id;")
			if len(qr)==0:
				messagebox.showinfo("Login Failed","Bad username or password")
			elif len(qr)==1:
				messagebox.showinfo("Login Successful","Login Successful")
				self.destroy()
				self.parent.logger(qr[0])



class CEODashBoard(ttk.Frame):
	def __init__(self,parent:MainApp,tup):
		self.parent=parent
		self.no_mgr=0
		ttk.Frame.__init__(self,parent,width=1000,height=1000)
		(self.emp_id,self.emp_name,self.phno,self.gender,self.dob,self.dept_id,self.designation,self.status)=tup
		self.query_status=tk.StringVar()
		self.status_label=ttk.Label(self,text='query status:',textvariable=self.query_status)
		self.status_label.place(x=300,y=750)
		self.logoutButton = ttk.Button(self, text="logout", command=lambda: self.logout())
		self.generateDashBoard()

		self.place(x=0,y=0)


	def logout(self):
		self.destroy()
		self.parent.drawLogin()

	def generateDashBoard(self):
		Name_Container=ttk.Frame(self)
		ttk.Label(Name_Container,text=f"Employee ID:{self.emp_id}",anchor=tk.W,width=20).grid(row=0,column=0)
		ttk.Label(Name_Container,text=f"Name:{self.emp_name}",anchor=tk.W,width=20).grid(row=1,column=0)
		self.logoutButton.place(x=800,y=100)
		Name_Container.place(x=100,y=80)
		dashboard_tabs=ttk.Notebook(self)
		dashboard_tabs.parent=self
		dashboard_tabs.place(x=100,y=130)
		createPorject=TableForm(dashboard_tabs)
		createUser=CreateUser(dashboard_tabs)
		dashboard_tabs.add(createPorject,text="create project")
		dashboard_tabs.add(createUser,text="Add new EMployee")
		dashboard_tabs.add(showEmployee(dashboard_tabs), text="show managers")
		dashboard_tabs.add(showEmployee1(dashboard_tabs),text="working employees")
		dashboard_tabs.add(showEmployee2(dashboard_tabs),text="employees on bench")
		if self.no_mgr==1:
			self.query_status.set("Pleaase free a Manager to start a new project")
			createPorject.destroy()




class TableForm(ttk.LabelFrame):
	def __init__(self,parent):
		ttk.LabelFrame.__init__(self,parent,text='create project',width=1000,height=280)
		self.place(x=0,y=0)
		self.parent=parent
		y=0
		qr=run_query("desc project")
		fields={}
		mgr_ids=run_query(f"select emp_id from employee where designation='M' and status='Y';")
		if len(mgr_ids)==0:
			self.parent.parent.no_mgr=1;return
		for i in qr:
			print(i)
			fields[i[0]]=''
			ttk.Label(self,text=i[0],width=20,anchor=tk.W).place(x=0,y=y)
			y+=20
		depts=run_query(f"select dept_id from department;")


		y=0
		for i in qr:
			if i[3]=='MUL':
				fields[i[0]]=ttk.Combobox(self,width=17,values=list(i[0]for i in mgr_ids))
				fields[i[0]].place(x=125,y=y)
			else:
				fields[i[0]]=ttk.Entry(self,width=20)
				fields[i[0]].place(x=125,y=y)
			y+=20
		y+=1
		self.dept_dict={}
		ttk.Label(self,text='dept_id',width=20,anchor=tk.W).place(x=0,y=y)
		ttk.Label(self,text='Available',width=20,anchor=tk.W).place(x=125,y=y)
		ttk.Label(self,text='Required',width=20,anchor=tk.W).place(x=250,y=y)
		y+=20
		for i in depts:
			ttk.Label(self,text=i[0],width=20,anchor=tk.W).place(x=0,y=y)
			count_of_emp=run_query(f"select count(*) from employee where dept_id={i[0]} and status='Y';")[0][0]
			ttk.Label(self,text=count_of_emp).place(x=125,y=y)
			self.dept_dict[i]=(count_of_emp,ttk.Entry(self,width=20))
			self.dept_dict[i][1].place(x=250,y=y)
			y+=20
		self.fields=fields
		createButton=ttk.Button(self,text='Create',command=lambda : self.create())
		createButton.place(x=0,y=y)
		print(self.fields.values())


	def create(self):
		for i in self.dept_dict:
			a=self.dept_dict[i]
			if a[0]<int(a[1].get()):
				self.parent.parent.query_status.set(f"Only {a[0]} employees available in dept {i[0]} but required {a[1].get()}")
				return None
		t=tuple(i.get() for i in self.fields.values())
		run_query(f"insert into project values ({t[0]},'{t[1]}','{'-'.join(t[2].split('-')[::-1])}','{'-'.join(t[3].split('-')[::-1])}',{t[4]});")
		emp_count=0
		for i in self.dept_dict:
			for j in run_query(f"select emp_id from employee where dept_id={i[0]} limit {self.dept_dict[i][1].get()};"):
				emp_count+=1
				run_query(f"insert into currently_works values ({t[0]},{j[0]});")
		self.parent.parent.query_status.set(f"project {t[1]} successfully created and {emp_count} employees are assigned.")

class CreateUser(ttk.Labelframe):
	def __init__(self,parent):
		ttk.LabelFrame.__init__(self,parent,width=350,height=350)
		self.parent=parent
		self.place(x=0,y=0)
		self.createForm()
	def createForm(self):
		fields=run_query(f"desc employee;")
		depts=list(i[0] for i in run_query(f"select * from department;"))
		gender=list(i[0] for i in run_query(f"select distinct(gender) from employee;"))
		designation=list(i[0] for i in run_query(f"select distinct(designation) from employee order by designation asc;"))[1:]
		status=list(i[0] for i in run_query(f"select distinct(status) from employee;"))
		col_dict={'gender':gender,'designation':designation,'status':status,'dept_id':depts}
		self.field_dict={}
		y=0
		for i in fields:
			if i[3]=='MUL' or i[0]in('gender','dept_id','designation','status'):
				ttk.Label(self,text=i[0],width=20,anchor=tk.W).place(x=0,y=y)
				self.field_dict[i[0]]=ttk.Combobox(self, width=17, values=col_dict[i[0]])
				self.field_dict[i[0]].place(x=125, y=y)
				y+=20
			else:
				ttk.Label(self,text=i[0],width=20,anchor=tk.W).place(x=0,y=y)
				e1=ttk.Entry(self,width=20)
				e1.place(x=125,y=y)
				self.field_dict[i[0]]=e1
				y+=20
		insertButton=ttk.Button(self,text="Create",command=lambda:self.insertEmployee())
		insertButton.place(x=0,y=y)


	def insertEmployee(self):
		t=tuple(i.get() for i in self.field_dict.values())
		if self.errorDetection(t):return
		desig={'M':'manager','E':'employee'}
		print(f"abc:{t}")
		print(f"insert into employee values ({t[0]},'{t[1]}','{t[2]}','{t[3]}','{t[4]}',{t[5]},'{t[6]}','{t[7]}');")
		run_query(f"insert into employee values ({t[0]},'{t[1]}','{t[2]}','{t[3]}','{t[4]}',{t[5]},'{t[6]}','{t[7]}');")
		run_query(f"insert into login_details values({t[0]},'{desig[t[6]]+str(t[0])}'),'{desig[t[6]]+str(t[0])}'")
		self.parent.parent.query_status.set("Employee created successfully.")



	def errorDetection(self,t:tuple):
		if any(i=='' for i in t):
			self.parent.parent.query_status.set("PLease Enter the values of all Columns.")
			return 1
		else:
			return 0


class showEmployee(ttk.LabelFrame):
	def __init__(self,parent):
		self.parent=parent
		ttk.LabelFrame.__init__(self,parent,text='',width=500,height=350)
		self.place(x=0,y=0)
		self.place_forget()
		self.createEditForm()


	def createEditForm(self):
		y=0
		x=0
		ttk.Label(self,text="Managers").place(x=0,y=0)
		y+=20
		managers=run_query(f"select e.emp_id,e.emp_name,d.dept_name,p.proj_id from employee e,department d, project p where e.designation='M' and p.mgr_id=e.emp_id and d.dept_id=e.dept_id ;")
		managers+=run_query(f"select e.emp_id,e.emp_name,d.dept_name from employee e,department d where status='Y' and d.dept_id=e.dept_id and e.designation='M';")
		ttk.Label(self,text="emp_id",width=15).place(x=x,y=y);x+=90
		ttk.Label(self, text="emp_name", width=15).place(x=x, y=y);x+=90
		ttk.Label(self, text="dept_name", width=15).place(x=x, y=y);x+=90
		ttk.Label(self,text="proj_id",width=15).place(x=x,y=y)
		y+=20
		for i in managers:
			x=0
			for j in i:
				ttk.Label(self,text=j,width=15).place(x=x,y=y);x+=90
			y+=20



class showEmployee1(ttk.LabelFrame):
	def __init__(self,parent):
		self.parent=parent
		ttk.LabelFrame.__init__(self,parent,text='',width=500,height=500)
		self.place(x=0,y=0)
		self.place_forget()
		self.createEditForm()


	def createEditForm(self):
		x = 0
		y=0
		ttk.Label(self, text="Employees on project").place(x=0, y=y);
		y += 20
		employee = run_query(
			f"select c.emp_id,e.emp_name,p.proj_name from employee e, currently_works c,project p where c.emp_id=e.emp_id and p.proj_id=c.proj_id;")
		ttk.Label(self, text="emp_id", width=15).place(x=x, y=y);
		x += 90
		ttk.Label(self, text="emp_name", width=15).place(x=x, y=y);
		x += 90
		ttk.Label(self, text="proj_name", width=15).place(x=x, y=y);
		x += 90
		y += 20
		for i in employee:
			x = 0
			for j in i:
				ttk.Label(self, text=j, width=15).place(x=x, y=y);
				x += 90
			y += 20



class showEmployee2(ttk.LabelFrame):
	def __init__(self,parent):
		self.parent=parent
		ttk.LabelFrame.__init__(self,parent,text='',width=500,height=350)
		self.place(x=0,y=0)
		self.place_forget()
		self.createEditForm()


	def createEditForm(self):
		x = 0
		y=0
		x = 0
		ttk.Label(self, text="Employees on bench").place(x=0, y=y);
		y += 20
		employee = run_query(f"select emp_id,emp_name from employee where status='Y';")
		ttk.Label(self, text="emp_id", width=15).place(x=x, y=y);
		x += 90
		ttk.Label(self, text="emp_name", width=15).place(x=x, y=y)
		y += 20
		for i in employee:
			x = 0
			for j in i:
				ttk.Label(self, text=j, width=15).place(x=x, y=y);
				x += 90
			y += 20


class DeleteEmployeee(ttk.LabelFrame):
	def __init__(self,parent):
		self.parent=parent
		ttk.LabelFrame.__init__(self,parent,text='',wdith=400,height=500)
		self.grid(row=0,column=0)
		self.v1=tk.StringVar()
		ttk.OptionMenu(self,v1,'select',*list('managers','employees')).grid(row=0,column=0)
		ttk.Button(self,text="show",command=lambda:self.show())
		self.frame=ttk.Frame(self)

	def show(self):
		d={'managers':'M','employees':'E'}
		self.frame.destroy()
		self.frame=ttk.Frame(self)
		self.frame.grid(row=0,column=0)
		ttk.Label(self.frame,text='----').grid(row=0,column=0)
		t=run_query(f"desc {d[self.v1.get()]}")
		c=1
		self.check_dict={}
		for i in t:
			ttk.Label(self.frame,text=i[0],wdiht=15).grid(row=0,column=c);c+=1
		qrt=run_query(f"select * from {d[self.v1.get()]}")
		v1=
		for i in qrt:


class MGRDashBoard(ttk.Frame):
	def __init__(self,parent:MainApp,tup):
		self.parent=parent
		ttk.Frame.__init__(self,parent,width=1000,height=1000)
		(self.emp_id,self.emp_name,self.phno,self.gender,self.dob,self.dept_id,self.designation,self.status)=tup
		self.projects=[int(i[0])for i in run_query(f"select proj_id from project where mgr_id={self.emp_id};")]
		self.emp_list=[]
		self.emp_dict = {}
		for i in self.projects:
			for j in run_query(f"select e.emp_id,e.emp_name from currently_works c,employee e where c.emp_id=e.emp_id and c.proj_id={i}"):
				self.emp_list+=[j[0]]
				self.emp_dict[j[1]]=j[0]

		self.proj_dict={i[1]:int(i[0])for i in run_query(f"select proj_id,proj_name from project where mgr_id={self.emp_id};")}
		self.query_status=tk.StringVar()
		self.status_label=ttk.Label(self,text='query status:',textvariable=self.query_status)
		self.status_label.place(x=300,y=750)
		self.logoutButton = ttk.Button(self, text="logout", command=lambda: self.logout())
		self.generateDashBoard()
		self.place(x=0,y=0)



	def logout(self):
		self.destroy()
		self.parent.drawLogin()

	def generateDashBoard(self):
		Name_Container=ttk.Frame(self)
		ttk.Label(Name_Container,text=f"Employee ID:{self.emp_id}",anchor=tk.W,width=20).grid(row=0,column=0)
		ttk.Label(Name_Container,text=f"Name:{self.emp_name}",anchor=tk.W,width=20).grid(row=1,column=0)
		Name_Container.place(x=100,y=80)
		self.logoutButton.place(x=800, y=100)
		dashboard_tabs=ttk.Notebook(self)

		dashboard_tabs.parent=self
		dashboard_tabs.place(x=100,y=130)
		dashboard_tabs.add(assignTask(dashboard_tabs),text="assign tasks")
		dashboard_tabs.add(PendingTasks(dashboard_tabs),text='pending tasks')
		dashboard_tabs.add(editPasswd(dashboard_tabs), text="change Password")
		dashboard_tabs.add(editProfile(dashboard_tabs), text="view/edit profile")



class assignTask(ttk.LabelFrame):
	def __init__(self,parent):
		ttk.LabelFrame.__init__(self,parent)
		self.parent=parent
		self.frame=ttk.Frame(self,width=300,height=300)
		self.frame.grid(row=0,column=0)
		self.place(x=0,y=0)
		self.createForm()
		self.stack=[]

	def createForm(self):
		self.pi = tk.IntVar()
		self.ei = tk.IntVar()
		self.ts = tk.StringVar()
		self.tasks={i[1]:i[0] for i in run_query("select * from task;")}

		self.y=0
		ttk.Label(self.frame,text='select project:').place(x=0,y=self.y)
		self.y+=20
		ttk.OptionMenu(self.frame,self.pi,'select',*self.parent.parent.projects).place(x=0,y=self.y)
		self.y += 20
		ttk.Button(self.frame,text="select",command=lambda:self.selectProject()).place(x=0,y=self.y)
		self.y+=20
	def selectProject(self):
		while len(self.stack)>0:self.stack.pop().destroy();self.y-=20
		proj_id=self.pi.get()
		self.stack+=[ttk.Label(self.frame,text="select employee:")]
		self.stack[-1].place(x=0,y=self.y)
		self.y+=20
		emps=[int(i[0]) for i in run_query(f"select emp_id from currently_works where proj_id={proj_id};")]
		self.stack+=[ttk.OptionMenu(self.frame,self.ei,'select',*emps)]
		self.stack[-1].place(x=0,y=self.y)
		self.y+=20
		self.stack+=[ttk.Button(self.frame, text="select", command=lambda:self.selectEmployee(proj_id))]
		self.stack[-1].place(x=0, y=self.y)
		self.y += 20

	def selectEmployee(self,proj_id):
		while len(self.stack) > 3: self.stack.pop().destroy();self.y-=20
		emp_id=self.ei.get()
		self.stack+=[ttk.Label(self.frame,text="select task:")]
		self.stack[-1].place(x=0,y=self.y)
		self.y+=20
		tasks=[i[0] for i in run_query(f"select task_desc from task where task_id not in (select task_id from emp_tasks where emp_id={emp_id} and proj_id={proj_id});")]
		self.stack+=[ttk.OptionMenu(self.frame,self.ts,'select',*tasks)]
		self.stack[-1].place(x=0,y=self.y)
		self.y+=20
		self.stack+=[ttk.Button(self.frame, text="assign",command=lambda:self.assignTask(proj_id,emp_id))]
		self.stack[-1].place(x=0, y=self.y)
		self.y += 20
	def assignTask(self,proj_id,emp_id):
		print(proj_id,emp_id,self.ts.get(),self.tasks[self.ts.get()])
		self.parent.parent.query_status.set(f"Task assigned to emp {run_query(f'select emp_name from employee where emp_id={emp_id}')[0][0]}")
		run_query(f"insert into emp_tasks values({proj_id},{emp_id},{self.tasks[self.ts.get()]})")
		self.frame.destroy()
		self.frame = ttk.Frame(self, width=300, height=300)
		self.frame.grid(row=0, column=0)
		self.stack=[]
		self.y=0
		self.createForm()


class PendingTasks(ttk.LabelFrame):
	def __init__(self,parent:ttk.Notebook):
		self.parent=parent
		ttk.LabelFrame.__init__(self,parent)
		self.frame=ttk.Frame(self,width=400,height=300)
		self.frame.grid(row=0,column=0)
		self.place(x=0,y=0)
		self.proj_filter=tk.StringVar()
		self.emp_filter=tk.StringVar()
		self.filers=[ttk.OptionMenu(self.frame,self.proj_filter,'select project',*['select project']+list(i for i in self.parent.parent.proj_dict)),
		             ttk.OptionMenu(self.frame,self.emp_filter,'select employee',*['select employee']+list(i for i in self.parent.parent.emp_dict))]
		self.filers[0].place(x=0,y=0)
		self.filers[1].place(x=110,y=0)
		self.y_increment=20
		filterButton=ttk.Button(self.frame,text='filter',width=20,command=lambda:self.filter()).place(x=230,y=0)
		self.y=0
		self.y+=30
		ttk.Label(self.frame,text="project").place(x=0,y=self.y)
		ttk.Label(self.frame,text="employee").place(x=90,y=self.y)
		ttk.Label(self.frame, text="task").place(x=180, y=self.y)
		self.table_container=ttk.Frame(self.frame,width=400,height=300)
		self.y+=self.y_increment
		self.table_container.place(x=0,y=self.y)

	def filter(self):
		self.table_container.destroy()
		self.table_container=ttk.Frame(self.frame,width=400,height=300)
		self.table_container.place(x=0,y=self.y)
		#print(self.proj_filter.get(),self.em)
		qr=[]
		if self.proj_filter.get()=="select project":
			if self.emp_filter.get()=="select employee":
				qr=run_query(f"select e.* from emp_tasks e,project p where e.proj_id=p.proj_id and p.mgr_id={self.parent.parent.emp_id};")
				y=0
				for i in qr:
					ttk.Label(self.table_container,text=i[0]).place(x=0,y=y)
					ttk.Label(self.table_container, text=i[1]).place(x=90,y=y)
					ttk.Label(self.table_container, text=i[2]).place(x=180,y=y)
					y+=self.y_increment
			else:
				print(self.parent.parent.emp_dict[self.emp_filter.get()])
				qr = run_query(
					f"select e.* from emp_tasks e,project p where e.proj_id=p.proj_id and p.mgr_id={self.parent.parent.emp_id} and e.emp_id={self.parent.parent.emp_dict[self.emp_filter.get()]};")
				y = 0
				for i in qr:
					ttk.Label(self.table_container, text=i[0]).place(x=0, y=y)
					ttk.Label(self.table_container, text=i[1]).place(x=90, y=y)
					ttk.Label(self.table_container, text=i[2]).place(x=180, y=y)
					y += self.y_increment
		else:
			if self.emp_filter.get()=="select employee":
				qr=run_query(f"select e.* from emp_tasks e,project p where e.proj_id={self.parent.parent.proj_dict[self.proj_filter.get()]} and p.mgr_id={self.parent.parent.emp_id};")
				y=0
				for i in qr:
					ttk.Label(self.table_container,text=i[0]).place(x=0,y=y)
					ttk.Label(self.table_container, text=i[1]).place(x=90,y=y)
					ttk.Label(self.table_container, text=i[2]).place(x=180,y=y)
					y+=self.y_increment
			else:
				print(self.parent.parent.emp_dict[self.emp_filter.get()])
				qr = run_query(
					f"select e.* from emp_tasks e where e.proj_id={self.parent.parent.proj_dict[self.proj_filter.get()]} and e.emp_id={self.parent.parent.emp_dict[self.emp_filter.get()]};")

				y = 0
				for i in qr:
					ttk.Label(self.table_container, text=i[0]).place(x=0, y=y)
					ttk.Label(self.table_container, text=i[1]).place(x=90, y=y)
					ttk.Label(self.table_container, text=i[2]).place(x=180, y=y)
					y += self.y_increment
		if len(qr) == 0:
			self.parent.parent.query_status.set("Query Completed. Fetched Null Set.")
		else:
			self.parent.parent.query_status.set("Query Completed.")



class EMPDashBoard(ttk.Frame):
	def __init__(self,parent,tup:tuple):
		self.parent=parent
		ttk.Frame.__init__(self, parent, width=1000, height=1000)
		(self.emp_id,self.emp_name,self.phno,self.gender,self.dob,self.dept_id,self.designation,self.status)=tup
		self.projects = [int(i[0]) for i in run_query(f"select distinct(c.proj_id),p.proj_name from currently_works c,project p where c.emp_id={self.emp_id} and p.proj_id=c.proj_id;")]
		self.emp_list = []
		self.emp_dict = {}
		for i in self.projects:
			for j in run_query(
					f"select e.emp_id,e.emp_name from currently_works c,employee e where c.emp_id=e.emp_id and c.proj_id={i}"):
				self.emp_list += [j[0]]
				self.emp_dict[j[1]] = j[0]

		self.proj_dict = {i[1]: int(i[0]) for i in
		                  run_query(f"select distinct(c.proj_id),p.proj_name from currently_works c,project p where c.emp_id={self.emp_id} and p.proj_id=c.proj_id;")}

		self.query_status = tk.StringVar()
		self.status_label = ttk.Label(self, text='query status:', textvariable=self.query_status)
		self.status_label.place(x=300, y=750)
		self.logoutButton = ttk.Button(self, text="logout", command=lambda: self.logout())
		self.generateDashBoard()
		self.place(x=0, y=0)

	def logout(self):
		self.destroy()
		self.parent.drawLogin()

	def generateDashBoard(self):
		Name_Container = ttk.Frame(self)
		ttk.Label(Name_Container, text=f"Employee ID:{self.emp_id}", anchor=tk.W, width=20).grid(row=0, column=0)
		ttk.Label(Name_Container, text=f"Name:{self.emp_name}", anchor=tk.W, width=20).grid(row=1, column=0)
		Name_Container.place(x=100, y=80)
		self.logoutButton.place(x=800, y=100)
		dashboard_tabs = ttk.Notebook(self)

		dashboard_tabs.parent = self
		dashboard_tabs.place(x=100, y=130)
		dashboard_tabs.add(Tasks(dashboard_tabs), text="tasks")
		dashboard_tabs.add(pastProjects(dashboard_tabs),text="Past Projects")
		dashboard_tabs.add(editPasswd(dashboard_tabs),text="change Password")
		dashboard_tabs.add(editProfile(dashboard_tabs),text="view/edit profile")


class Tasks(ttk.LabelFrame):
	def __init__(self,parent):
		self.parent=parent
		ttk.LabelFrame.__init__(self,parent,width=400,height=400)
		self.place(x=0,y=0)
		self.frame=ttk.Frame(self,width=300,height=300)
		self.y_increment = 20
		self.y = 0
		self.proj_filter=tk.StringVar()
		self.proj_menu=ttk.OptionMenu(self,self.proj_filter,'select project',*['select project']+list(i for i in self.parent.parent.proj_dict))
		self.proj_menu.place(x=0,y=0)
		self.filter_button=ttk.Button(self,text="filter",command=lambda:self.filter())
		self.filter_button.place(x=180,y=0)
		self.y+=30
		ttk.Label(self,text="select",width=10).place(x=0,y=self.y)
		ttk.Label(self,text="project",width=20).place(x=90,y=self.y)
		ttk.Label(self,text="task",width=20).place(x=180,y=self.y)
		self.y+=self.y_increment
		self.frame_y=30
		self.frame.place(x=0,y=self.frame_y)
		self.y=30
		self.filter()


	def filter(self):
		self.delete_check={}
		qr=[]

		if self.proj_filter.get()=="select project":
			qr = run_query(f"select proj_id,task_id from emp_tasks where emp_id={self.parent.parent.emp_id};")
		else:
			qr = run_query(
				f"select proj_id,task_id from emp_tasks where emp_id={self.parent.parent.emp_id} and proj_id={self.parent.parent.proj_dict[self.proj_filter.get()]}")

		if len(qr) == 0: self.parent.parent.query_status.set("query copleted .No pending tasks.");return
		for i in qr:
			print(i)
			v1=tk.IntVar()
			checkBox=ttk.Checkbutton(self.frame,text="",variable=v1)
			checkBox.place(x=0,y=self.y)
			self.delete_check[checkBox]=[v1,[]]
			x=0
			x+=90
			for j in i:
				self.delete_check[checkBox][1]+=[j]
				ttk.Label(self.frame,text=j,width=20).place(x=x,y=self.y)
				x+=90
			self.y += self.y_increment

		self.completeButton=ttk.Button(self.frame,text="Complete",command=lambda:self.complete())
		self.completeButton.place(x=0,y=self.y)

	def complete(self):
		query=f"delete from emp_tasks where emp_id={self.parent.parent.emp_id} and (proj_id,task_id) in ("
		for i in self.delete_check:
			if self.delete_check[i][0].get()==1:
				query+=f"({str(self.delete_check[i][1])[1:-1]}),"
		query=query[:-1]+");"
		print(query)
		run_query(query)
		self.parent.parent.query_status.set('tasks completed')
		self.frame.destroy()
		self.frame=ttk.Frame(self,width=300,height=300)
		self.frame.place(x=0,y=self.frame_y)
		self.y = self.frame_y
		self.filter()

class pastProjects(ttk.LabelFrame):
	def __init__(self,parent):
		self.parent=parent
		ttk.LabelFrame.__init__(self,parent,text="",width=500,height=400)
		self.grid(row=0,column=0)
		desc_proj=run_query("desc project;")
		x=0
		for i in desc_proj:
			ttk.Label(self,text=i[0],width=20).place(x=x,y=0)
			x+=90
		y=0
		y+=20
		proj_details=run_query(f"select p.* from project p,history h where h.proj_id=p.proj_id and h.emp_id={self.parent.parent.emp_id};")
		for i in proj_details:
			x=0
			for j in i:
				ttk.Label(self,text=j,width=20).place(x=x,y=y)
				x+=90
			y+=20


class editPasswd(ttk.LabelFrame):
	def __init__(self,parent):
		ttk.LabelFrame.__init__(self,parent)
		self.grid(row=0,column=0)
		self.parent=parent
		ttk.Label(self,text="Enter new passed:").grid(row=0,column=0)
		self.pd=ttk.Entry(self,width=20).grid(row=0,column=1)
		cb=ttk.Button(self,text='change',command=lambda:self.change()).grid(row=1,column=1)
	def change(self):
		np=self.pd.get()
		if len(np)>=8:
			run_query(f"update table login_details set passwd={np} where emp_id={self.parent.parent.emp_id};")
			self.parent.parent.query_status.set("Password changed")
		else:
			self.parent.parent.query_status.set("Enter atelast 8 characters")



class editProfile(ttk.LabelFrame):
	def __init__(self,parent):
		ttk.LabelFrame.__init__(self,parent)
		self.parent=parent
		desc_emp=run_query("desc employee")
		self.desc_emp=desc_emp[1:5]
		ttk.Label(self,text="EMPLOYEE DETAILS")
		self.frame=ttk.Frame(self)
		self.frame.grid(row=0,column=0)
		self.grid(row=0,column=0)
		self.draw()


	def draw(self):
		self.frame.destroy()
		self.frame = ttk.Frame(self)
		self.frame.grid(row=1, column=0)
		r=0
		for i in self.desc_emp:
			ttk.Label(self.frame,text=i[0] +":",width=10).grid(row=r,column=0)
			r+=1
		ttk.Button(self.frame, text="edit profile", command=lambda: self.edit()).grid(row=r, column=1)
		r=0
		for j in run_query(f"select emp_name,phno,gender,dob from employee where emp_id={self.parent.parent.emp_id};"):
			for i in j:
				ttk.Label(self.frame,text=i,width=20).grid(row=r,column=1)
				r+=1
	def edit(self):
		self.frame.destroy()
		self.frame=ttk.Frame(self)
		self.frame.grid(row=1,column=0)
		r=0
		for i in self.desc_emp:
			ttk.Label(self.frame,text=i[0] +":",width=20).grid(row=r,column=0)
			r+=1
		l={}
		r=0
		for i in self.desc_emp:
			l[i[0]]=ttk.Entry(self.frame,width=20)
			l[i[0]].grid(row=r,column=1)
			r+=1
		self.l=l
		ttk.Button(self.frame,text="Done",command=lambda:self.done()).grid(row=r,column=1)

	def done(self):
		query=f"update employee set"
		for i in self.l:
			a=''
			if self.l[i].get()!='':
				a=i+"="+self.l[i].get()+' and'
			query+=a
		query=query[:-4]
		query+=f"where emp_id={self.parent.parent.emp_id};"
		try:
			run_query(query)
		except:
			self.parent.parent.query_status.set("error please chack given values")
		self.draw()

MainApp()

