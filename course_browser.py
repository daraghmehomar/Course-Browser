import random
import tkinter as tk
from tkinter import ttk
#omar daraghmeh 1200162
LOC=list() #LIST OF COURSES  
LOL=list() #LIST OF LABS
mapC=[("MW 08:30-09:45"),("MW 10:00-11:15"),("MW 11:25-12:40"),("MW 12:50-02:05"),("MW 02:15-03:30"),
      ("TR 08:30-09:45"),("TR 10:00-11:15"),("TR 11:25-12:40"),("TR 12:50-02:05"),("TR 02:15-03:30"),
      ("SW 08:30-09:45"),("SW 10:00-11:15"),("SW 11:25-12:40"),("SW 12:50-02:05"),("SW 02:15-03:30"),
      ("SM 08:30-09:45"),("SM 10:00-11:15"),("SM 11:25-12:40"),("SM 12:50-02:05"),("SM 02:15-03:30")]

mapL=[("M 08:00-11:10"),("M 11:25-02:05"),("M 02:15-04:55"),
      ("T 08:00-11:10"),("T 11:25-02:05"),("T 02:15-04:55"),
      ("W 08:00-11:10"),("W 11:25-02:05"),("W 02:15-04:55"),
      ("R 08:00-11:10"),("R 11:25-02:05"),("R 02:15-04:55"),
      ("S 08:00-11:10"),("S 11:25-02:05"),("S 02:15-04:55"),]


class courses: #class to make objects of the courses
  def __init__(self,code,sec,Cname,Dname):
    self.code = code  
    self.sec=sec
    self.doctor = Dname
    self.CourseName = Cname


class labs:#class to make objects of the labs
  def __init__(self,code,sec,Lname,Dname):
    self.code = code
    self.doctor = Dname
    self.sec=sec
    self.LabName = Lname

def generate_chromosome(length, n):
    while(True):
        chromosome = [random.randint(0,length-1) for _ in range(n)]  # initialize the list with length 
        if(checkForDoctors(chromosome,length)):
            break
    return chromosome

def checkForDoctors(chromosome,length):
    flag=True
    lst=[{} for _ in range(length)]
    for i in range(len(chromosome)):
        if(int(length)==20):
            if LOC[i].doctor not in lst[chromosome[i]]:
                lst[chromosome[i]][LOC[i].doctor]=1
            else:
                lst[chromosome[i]][LOC[i].doctor]+=1 
        else:
            if LOL[i].doctor not in lst[chromosome[i]]:
                lst[chromosome[i]][LOL[i].doctor]=1
            else:
                lst[chromosome[i]][LOL[i].doctor]+=1            
    for doctors in lst:
        for doctor in doctors:
            if int(doctors[doctor])>1:
                flag = False
                break
    return flag                

def fitness(chromosome,length):
    lst =[0 for _ in range(length)]
    for i in range(len(chromosome)):
        lst[chromosome[i]]+=1
    return 10-(max(lst)-min(lst))

def selection(pop, fitnesses):
    # Select a chromosome from the population with probability proportional to its fitness
    idx = random.choices(range(len(pop)), weights=fitnesses, k=1)[0]
    return pop[idx]

def crossover(chromosome1, chromosome2,length):
    # Select a random crossover point and combine the two chromosomes
    while(True):
        idx = random.randint(1, len(chromosome1)-1)
        chromosome=chromosome1[:idx] + chromosome2[idx:]
        if(checkForDoctors(chromosome,length)):
            break
    return chromosome

def genetic_algorithm(pop_size, length,n, n_generations):
    # Initialize the population with random chromosomes
    population = [generate_chromosome(length,n) for _ in range(pop_size)]
    
    # Evaluate the fitness of each chromosome
    fitnesses = [fitness(chrom,length) for chrom in population]

    for _ in range(n_generations):
        # Select the parents for crossover
        parent1 = selection(population, fitnesses)
        parent2 = selection(population, fitnesses)
        
        # Generate the offspring by crossover and mutation
        offspring = crossover(parent1, parent2,length)
        
        
        # Replace the least fit chromosome in the population with the offspring
        idx = fitnesses.index(min(fitnesses))
        population[idx] = offspring
        fitnesses[idx] = fitness(offspring,length)
    
    # Return the fittest chromosome
    return max(zip(population, fitnesses), key=lambda x: x[1])[0]


fname = "courses.txt"
try:
    fchand = open(fname)
except:
    print('File cannot be opened:', fname)
    exit()
fname = "labs.txt"
try:
    flhand = open(fname)
except:
    print('File cannot be opened:', fname)
    exit()

 
for line in fchand:
    
    words = line.split(",")
    for n in range(4,len(words)) :
        sec=words[n].split("-")
        for c in sec[1]:
            if c.isnumeric(): 
                temp=courses(words[0],c,words[1],sec[0])
                LOC.append(temp)
LOC.sort(key=lambda x: (x.code, x.sec))

for line in flhand:  
    words = line.split(",")
    for n in range(3,len(words)) :
        sec=words[n].split("-")
        for c in sec[1]:
            if c.isnumeric(): 
                temp=labs(words[0],c,words[1],sec[0])
                LOL.append(temp)
LOL.sort(key=lambda x: (x.code, x.sec))

resultC=genetic_algorithm(100,20, len(LOC),5000)

resultL=genetic_algorithm(100,15, len(LOL),5000)

lst={}
for i in range(len(resultC)):
    if LOC[i].code not in lst:
        lst[LOC[i].code]=[f"%1s   %s  %10s"%(LOC[i].sec, mapC[resultC[i]] ,LOC[i].doctor)]
    else :
        lst[LOC[i].code].append(f"%1s   %s  %10s"%(LOC[i].sec,mapC[resultC[i]] ,LOC[i].doctor) )
for i in range(len(resultL)):
    if LOL[i].code not in lst:
        lst[LOL[i].code]=[f"%1s   %s  %10s"%(LOL[i].sec,mapL[resultL[i]] ,LOL[i].doctor) ]
    else :
        lst[LOL[i].code].append(f"%1s   %s  %10s"%(LOL[i].sec,mapL[resultL[i]] ,LOL[i].doctor) )

for course in lst:
    print(course+":")
    for sec in lst[course]:
        print("\t"+sec)
print(fitness(resultC,20),fitness(resultL,15))    
# Create the main window
window = tk.Tk()
window.title("Course Browser")

# Get the width and height of the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the size of the window to the same as the screen
window.geometry(f"{screen_width}x{screen_height}")

# Create a frame to hold the label, search bar and button
search_frame = tk.Frame(window)
search_frame.pack()

# Create a label to display the text
label = ttk.Label(search_frame, text="Course Browser", font=("Arial", 32))
label.pack()

# Create an input bar for searching
search_bar = ttk.Entry(search_frame, font=("Arial", 16))
search_bar.insert(0, "Enter the code")
search_bar.config(show="")

# Define a function to delete the placeholder text
def on_search_bar_click(event):
    search_bar.delete(0, tk.END)
    search_bar.config(show="")

# Bind the click event to the function
search_bar.bind("<Button-1>", on_search_bar_click)
search_bar.pack()
# Define a function to be called when the button is clicked
def on_button_click(event):
    # Get the text from the search bar
    search_text = search_bar.get()

    # Create a pop-up window
    pop_up = tk.Toplevel()
    pop_up.title("Course")

    # Set the size and position of the pop-up window
    pop_up_width = 700
    pop_up_height = 500
    pop_up_x = screen_width // 2 - pop_up_width // 2
    pop_up_y = screen_height // 2 - pop_up_height // 2
    pop_up.geometry(f"{pop_up_width}x{pop_up_height}+{pop_up_x}+{pop_up_y}")

    # Create a label to display the text
    label = tk.Label(pop_up, text=f"You searched for: {search_text}", font=("Arial", 16))
    label.pack()
    courseName=""
    for item in LOC:
        if (item.code==search_text):
            courseName=item.CourseName
    for item in LOL:
        if item.code==search_text:
            courseName=item.LabName
    label2 = tk.Label(pop_up, text=f" {courseName}", font=("Arial", 16))
    label2.pack()        
    # Create a Listbox widget to display the data
    data_listbox = tk.Listbox(pop_up, font=("Arial", 16),width=35)
    data_listbox.pack()

    if search_text not in lst:
        data_listbox.insert(tk.END, "the code was not found!")
    else:
    # Insert the data into the Listbox
        for item in lst[search_text]:
            data_listbox.insert(tk.END, item)

# Create a button to initiate the search
search_button = tk.Button(search_frame, text="Search", font=("Arial", 16))
# Bind the button click event to the function
search_button.bind("<Button-1>", on_button_click)
search_button.pack()

data_listbox1 = tk.Listbox(window, font=("Arial", 16),width=100,height=50)
data_listbox1.pack()
for course in lst:
        courseName=""
        for item in LOC:
            if (item.code==course):
                courseName=item.CourseName
        for item in LOL:
            if item.code==course:
                courseName=item.LabName
        data_listbox1.insert(tk.END, course+":"+" "+courseName)
        for sec in lst[course]:
            data_listbox1.insert(tk.END, "    "+sec)
        data_listbox1.insert(tk.END, "")

# Run the main loop
window.mainloop()