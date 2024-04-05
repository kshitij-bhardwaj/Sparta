import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

window = customtkinter.CTk()  # create CTk window like you do with the Tk window



class Facility:
  def __init__(self, name, num_slots):
    self.name = name
    self.slots = [True] * num_slots  # Initialize slots as all available (True)

  def check_availability(self, slot_number):
    if 0 <= slot_number < len(self.slots) and self.slots[slot_number]:
      return True
    else:
      return False

  def book_slot(self, slot_number, roll_number):
    if self.check_availability(slot_number):
      self.slots[slot_number] = False  # Mark slot as booked
      return f"Slot {slot_number + 1} for {self.name} booked successfully!"
    elif ((self.name == "Gym" and slot_number <= gym_slots) or (self.name == "Squash" and slot_number <= squash_slots) or (self.name == "Badminton" and slot_number <= badminton_slots)):
      return f"Slot {slot_number + 1} for {self.name} is already booked."
    else : return "Invalid Slot Number"
  def cancel_booking(self, slot_number):
    if 0 <= slot_number < len(self.slots) and not self.slots[slot_number]:
      # Check if user trying to cancel actually booked the slot (using roll number)
      # Implement logic to verify user ownership of booking (e.g., database lookup)
      self.slots[slot_number] = True  # Mark slot as available
      return f"Slot {slot_number + 1} for {self.name} cancelled successfully."
    else:
      return f"Slot {slot_number + 1} for {self.name} is either unavailable or not booked by you"

class User:
  def __init__(self, roll_number):
    self.roll_number = roll_number
    self.booking_history = []

  def book_slot(self, facility, slot_number):
    # Call Facility.book_slot and update booking history if successful
    message = facility.book_slot(slot_number, self.roll_number)
    if message.startswith("Slot"):  # Booking successful
      self.booking_history.append((facility, slot_number))
    return message

  def view_booking_history(self):
    if not self.booking_history:
      return "No bookings found in your history."
    history_string = "Your Booking History:\n"
    for facility, slot in self.booking_history:
      history_string += f"{facility.name} - Slot {slot + 1}\n"
    return history_string
  
  def cancel_booking(self, facility_name, slot_number):
    for facility, slot in self.booking_history:
      if (facility_name.name == facility.name and slot_number == slot):
        cancel_string = facility_name.cancel_booking(slot_number)
        self.booking_history.remove((facility_name, slot_number))
      else : 
        try : cancel_string = f"Slot {slot_number + 1} for {self.name} is either unavailable or not booked by you"
        except : cancel_string = "Select the correct Facility and Slot to cancel booking"
      return cancel_string

def main(window):
  window.title("Sports Facility Management")
  window.geometry("400x400")
  # Facility objects (Modify names and number of slots)
  global gym_slots
  global squash_slots
  global badminton_slots
  gym_slots = 10
  squash_slots = 4
  badminton_slots = 6
  gym = Facility("Gym", gym_slots)
  squash_court = Facility("Squash Court", squash_slots)
  badminton_court = Facility("Badminton Court", badminton_slots)

  

  # Labels and Entry fields
  roll_number_label = customtkinter.CTkLabel(master=window, text="Roll Number:")
  roll_number_entry = customtkinter.CTkEntry(master=window)
  slot_number_label = customtkinter.CTkLabel(master=window, text="Slot Number:")
  slot_number_entry = customtkinter.CTkEntry(master=window)

  # User object (Replace with user input)
  user = User(roll_number_entry.get())  # Replace with actual roll number input
  # Function definitions for buttons (call previously defined functions)
  def book_slot():
    slot_number = int(slot_number_entry.get()) - 1  # Adjust for 0-based indexing
    message = user.book_slot(selected_facility, slot_number)
    info_text.configure(text=message)

  def check_availability():
    slot_number = int(slot_number_entry.get()) - 1  # Adjust for 0-based indexing
    available = selected_facility.check_availability(slot_number)

    if available:
      info_text.configure(text = f"Slot {slot_number + 1} for {selected_facility.name} is available.")
    else:
      info_text.configure(text = f"Slot {slot_number + 1} for {selected_facility.name} is already booked.")

  def view_history():
    history = user.view_booking_history()

    info_text.configure(text = history)

  def cancel_booking():
    slot_number = int(slot_number_entry.get()) - 1  # Adjust for 0-based indexing
    message = user.cancel_booking(selected_facility, slot_number)

    info_text.configure(text = message)

  def select_facility(facility_name):  # Function to handle facility selection
    global selected_facility  # Access global variable for selected facility
    facilities = {"Gym": gym, "Squash Court": squash_court, "Badminton Court": badminton_court, "None": None}
    selected_facility = facilities.get(facility_name)
    if(selected_facility == None) : info_text.configure(text = "No Facility was selected. Try again.")
    else : info_text.configure(text = f"Selected Facility: {selected_facility.name if selected_facility else 'None'}")

  combobox = customtkinter.CTkOptionMenu(master=window, fg_color= '#f9f9f9', text_color= '#c1c7c9',
                                       values=["Gym", "Squash Court", "Badminton Court"],
                                       command=select_facility)
  combobox.set("None")  # set initial value
  # Buttons with click events
  book_button = customtkinter.CTkButton(window, text="Book Slot", command=book_slot)
  check_button = customtkinter.CTkButton(window, text="Check Availability", command=check_availability)
  history_button = customtkinter.CTkButton(window, text="View Booking History", command=view_history)
  cancel_button = customtkinter.CTkButton(window, text="Cancel Booking", command=cancel_booking)
  # Text area for displaying information
  info_text = customtkinter.CTkLabel(window, height=10, width=300, text = "Hello There!")
  info_text.pack()
  # Layout widgets on the window
  roll_number_label.pack()
  roll_number_entry.pack()
  slot_number_label.pack()
  slot_number_entry.pack()
  #facility_selection_frame.pack()
  combobox.pack(padx=20, pady=20)
  book_button.pack(padx=20, pady=5)
  check_button.pack(padx=20, pady=5)
  history_button.pack(padx=20, pady=5)
  cancel_button.pack(padx=20, pady=5)
  window.mainloop()

if __name__ == "__main__":
  main(window)

