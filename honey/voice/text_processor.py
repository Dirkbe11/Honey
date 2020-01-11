
class TextProcessor():
    def __init__(self, output_function):
        self.user_dictionary = {}
        self.command_executer = output_function

    #clears text data from users cache
    def clear_user_history(self, user):
        self.user_dictionary[user] = ""

    #appends text to user specific strings + searches for keyword HONEY
    def process_initial(self, user, text):
        print("PRE: " + text)
        
        if not user in self.user_dictionary:
            self.user_dictionary[user] = text
        else:
            self.user_dictionary[user] += text

        #find first instance of "honey"
        command_start_index = self.user_dictionary[user].find("honey")

        if command_start_index != -1:
            return True
        else:
            if len(self.user_dictionary[user]) > 30:
                self.clear_user_history(user)
            return False


    #performs the actual processing/searching for user commands
    def ProcessText(self, text, user):
        if(text.startswith("honey where is my super suit") or text.startswith("honey where is my supersuit")):
            self.ProcessCommand("EE1")
            self.clear_user_history(user)
            return

        command_start_index = text.find("honey") #find first instance of "honey"
        if command_start_index != -1:

            text = text[command_start_index:]
            if len(text) != 0:
                command_end_index = text.find("please")

                if command_end_index != -1:
                    command = text[5:command_end_index]
                    self.ProcessCommand(command)
        #             self.clear_user_history(user)
        #         elif len(text) > 30:
        #              self.clear_user_history(user)
        #     else:
        # else: 

        self.clear_user_history(user)

    def ProcessCommand(self, command):
        #clean command
        command = command.lstrip()
        print("FINAL: " + command)
        self.command_executer(command)
        
