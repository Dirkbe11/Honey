
class TextProcessor():
    def __init__(self, output_function):
        self.user_dictionary = {}
        self.command_executer = output_function

    #appends text to user specific strings, then calls process on it
    def Process(self, user, text):
        print("PRE: " + text)
        print(len(text))
        if not user in self.user_dictionary:
            self.user_dictionary[user] = text
        else:
            self.user_dictionary[user] += text
        
        self.ProcessText(user)

    #performs the actual processing/searching for user commands
    def ProcessText(self, user):
        potential_command = self.user_dictionary[user] #get candidate command from dictionary by user
        print("interesting...")
        command_start_index = potential_command.find("honey") #find first instance of "honey"
        print("Potential Command: " + potential_command)
        if command_start_index != -1:
            # print("honey found!")
            self.user_dictionary[user] = self.user_dictionary[user][command_start_index:]
            
            if len(self.user_dictionary[user]) != 0:
                command_end_index = self.user_dictionary[user].find("please")

                if command_end_index != -1:
                    command = self.user_dictionary[user][5:command_end_index]
                    self.ProcessCommand(command)
                    self.user_dictionary[user] = (self.user_dictionary[user][command_end_index+6:]).lstrip()
                    
                elif len(self.user_dictionary[user]) > 30:
                    self.user_dictionary[user] = ""
                
        else: 
            self.user_dictionary[user] = ""

    def ProcessCommand(self, command):
        #clean command
        command = command.lstrip()
        print("FINAL: " + command)
        self.command_executer(command)
        
