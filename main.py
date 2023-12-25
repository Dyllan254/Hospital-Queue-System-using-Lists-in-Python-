import tkinter as tk
from tkinter import messagebox


class HospitalQueue:
    def __init__(self, root):
        self.root = root  # Initialize the HospitalPQ with a tkinter root window
        self.root.title("Priority Queue Visualization")  # set the title of the window

        self.priority_queue = []  # Initialize an empty list to represent the priority queue
        self.max_size = 10  # Maximum number of patients in the priority queue

        self.create_widgets()  # call the method to create the widgets of the GUI

    def create_widgets(self):
        # Waiting Room diagram
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        # Draw the waiting room outline
        self.draw_waiting_room()

        # Frame for priority queue operations on the right side of the window
        operations_frame = tk.Frame(self.root)
        operations_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Entry for patient name
        tk.Label(operations_frame, text="Patient Name").grid(row=0, column=0, pady=5)
        self.name_entry = tk.Entry(operations_frame)
        self.name_entry.grid(row=0, column=1, pady=5)

        # Entry for patient age
        tk.Label(operations_frame, text="Patient Age").grid(row=1, column=0, pady=5)
        self.age_entry = tk.Entry(operations_frame)
        self.age_entry.grid(row=1, column=1, pady=5)

        # buttons for the operations
        tk.Button(operations_frame, text="Enqueue Patient", command=self.add_patient, bg='beige').grid(
            row=2, column=0, columnspan=2, pady=10)
        tk.Button(operations_frame, text="Dequeue Patient", command=self.remove_patient, bg='beige').grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(operations_frame, text="Update Priority", command=self.update_priority,
                  bg='beige').grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(operations_frame, text="Is Empty", command=self.is_empty, bg='beige').grid(row=7,column=0,columnspan=2,pady=5)
        tk.Button(operations_frame, text="Queue Length", command=self.queue_length, bg='beige').grid(
            row=8, column=0, columnspan=2, pady=5)

    def draw_waiting_room(self):
        # Draw the waiting room outline
        self.canvas.create_line(50, 50, 750, 50, width=2)  # Top line
        self.canvas.create_line(50, 50, 50, 550, width=2)  # Left line
        self.canvas.create_line(50, 550, 750, 550, width=2)  # Bottom line
        self.canvas.create_line(750, 50, 750, 550, width=2)  # Right line

        # Waiting Room text centered at the top of the waiting room outline
        waiting_room_text_x = (50 + 750) // 2
        waiting_room_text_y = 50 // 2
        self.canvas.create_text(waiting_room_text_x, waiting_room_text_y, text="Waiting Room", font=('calibri', 18, 'bold'),
                                fill='black')

    def add_patient(self):
        if len(self.priority_queue) >= self.max_size:  # check if Priority Queue has reached its maximum
            self.show_error(
                f"Full! No more patients can be added({self.max_size}).")  # if limit is reached
            return

        # retrieve patient name and age from the input fields
        name = self.name_entry.get()
        age = self.age_entry.get()

        # check if both name and age are provided
        if name and age:
            try:
                age = int(age)  # convert the age to an integer
                patient_id = len(self.priority_queue)  # generate unique id for each patient using Priority Queue length
                # Append the patient information to the priority queue as a tuple (age, name, patient_id)
                self.priority_queue.append((age, name, patient_id))
                # Arrange the patients in ascending order in accordance with their age
                self.priority_queue.sort(key=lambda x: x[0])

                # Visualize the patients in the hospital
                self.visualize_patients()

            except ValueError:
                self.show_error("Error! Please enter a valid integer.")  # if age is not valid int

        else:
            self.show_error("Please enter both name and age.")  # if both the name and age are not provided
    def remove_patient(self):
        # Retrieve patient name and age from the entry fields
        name = self.name_entry.get()
        age = self.age_entry.get()

        # check if both name and age are provided
        if name and age:
            try:
                age = int(age)  # convert the age to an integer

                # Find the patient in the priority queue
                for patient in self.priority_queue:
                    if patient[1] == name and patient[0] == age:
                        # retrieve patient id for visual removal
                        patient_id = patient[2]
                        self.priority_queue.remove(patient)  # remove patient from the PQ

                        # Remove the visual representation of the patient from the hospital
                        self.canvas.delete(f"patient_{patient_id}")

                        # Adjust the space between patients and visualize them
                        self.visualize_patients()
                        # show info message w the patient info
                        message = f"Dequeued Patient: {name} ({age} )"
                        self.show_info(message)
                        return

                # if patient is not in the PQ
                self.show_error("Patient not found in the priority queue.")

            except ValueError:
                # if age is not an integer
                self.show_error("Invalid age. Please enter a valid integer.")

        else:
            # if both age and name are not provided
            self.show_error("Please enter both name and age.")

    def update_priority(self):
        # Retrieve patient name and age from the input fields
        name = self.name_entry.get()
        age = self.age_entry.get()

        if name and age:  # Check if both name and age are provided
            try:
                age = int(age)  # Convert the age to an integer

                # Find the patient in the priority queue
                for i, patient in enumerate(self.priority_queue):
                    if patient[1] == name and patient[0] == age:
                        # Open a new window to get the updated key from the user
                        update_window = tk.Toplevel(self.root)
                        update_window.title("Update Priority")

                        # Create an entry field for the user to enter the new key
                        tk.Label(update_window, text="Enter A New Key:").grid(row=0, column=0, pady=5)
                        new_age_entry = tk.Entry(update_window)
                        new_age_entry.grid(row=0, column=1, pady=5)

                        # Create a button to confirm the update
                        tk.Button(update_window, text="Update",
                                  command=lambda i=i: self.update_priority_confirm(i, new_age_entry.get(),
                                                                                   update_window),
                                  bg='beige').grid(row=1, column=0, columnspan=2, pady=10)

                        return

                self.show_error("Patient is not found in the priority queue.")

            except ValueError:
                self.show_error("Error! Please enter a valid integer.")

        else:
            self.show_error("Please enter both name and age.")

    def update_priority_confirm(self, index, new_age, update_window):
        try:
            new_age = int(new_age)  # convert new key to int
            old_patient = self.priority_queue[index]  # retrieve info about the old patient
            new_patient = (new_age, old_patient[1], old_patient[2])  # create a tuple with new updated key

            # Update the key (age) of the patient
            self.priority_queue[index] = new_patient

            # Arrange the patients in ascending order based on the updated key
            self.priority_queue.sort(key=lambda x: x[0])

            # Visualize the patient in the hospital
            self.visualize_patients()

            # display message about the update
            message = f"Updated Priority for Patient: {old_patient[1]} (New key: {new_age})"
            self.show_info(message)

            update_window.destroy()  # close update window

        except ValueError:
            self.show_error("Invalid age. Please enter a valid integer.")  # error if age is not valid number

    def visualize_patients(self):
        # Clear previous patient visualizations
        self.canvas.delete("all")

        # Draw waiting_room
        self.draw_waiting_room()

        # Adjust the space between patients and visualize them
        for i, (age, name, patient_id) in enumerate(self.priority_queue):
            x = 700 - (i + 1) * 50
            y = 300

            # Stickman representing the patients
            # Head
            head = self.canvas.create_oval(x - 10, y - 25, x + 10, y + 5, fill='black', tags=f"patient_{patient_id}")

            # Body
            body = self.canvas.create_line(x, y + 5, x, y + 30, fill='black', tags=f"patient_{patient_id}")

            # Left Arm
            left_arm = self.canvas.create_line(x, y + 10, x - 10, y + 30, fill='black', tags=f"patient_{patient_id}")

            # Right Arm
            right_arm = self.canvas.create_line(x, y + 10, x + 10, y + 30, fill='black', tags=f"patient_{patient_id}")

            # Left Leg
            left_leg = self.canvas.create_line(x, y + 30, x - 5, y + 60, fill='black', tags=f"patient_{patient_id}")

            # Right Leg
            right_leg = self.canvas.create_line(x, y + 30, x + 5, y + 60, fill='black', tags=f"patient_{patient_id}")

            # Text above the stickman
            text_above = self.canvas.create_text(x, y - 35, text=f"{age}", font=('calibri', 10), anchor='center',
                                                 tags=f"patient_{patient_id}")
            # Text below the stickman
            text_below = self.canvas.create_text(x, y + 75, text=f"{name}", font=('calibri', 10), anchor='center',
                                                 tags=f"patient_{patient_id}")

    # check if Priority Queue is empty
    def is_empty(self):
        if not self.priority_queue:
            self.show_info("Queue is Empty.")
        else:
            self.show_info("Queue is not Empty.")
    # length of Priority Queue
    def queue_length(self):
        message = f"Queue Length: {len(self.priority_queue)}"
        self.show_info(message)

    # Display an information message box with the provided message
    def show_info(self, message):
        messagebox.showinfo("Information", message)

    # Display an error message box with the provided message
    def show_error(self, message):
        messagebox.showerror("Error", message)


if __name__ == "__main__":
    root = tk.Tk()  # create tkinter root window
    app = HospitalQueue(root)
    root.mainloop()  # starts the event loop to run the GUI