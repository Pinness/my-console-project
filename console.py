#!/usr/bin/python3

import cmd
from models.base_model import BaseModel
from models.engine.file_storage  import FileStorage
from models import storage


class MyConsole (cmd.Cmd):
    classes = {"BaseModel" : BaseModel}




    def __init__(self):
        super().__init__()
        self.prompt = 'Piness >>> '
        #self.storage = storage


    def cmdloop(self):
        return super().cmdloop()


    #prompt = 'Piness >>>  '   #display prompt
    #def do_quit(self, arg):

    def do_quit(self, arg):
        return True

    def do_EOF(self, arg):
        """ Exits the program"""
        print()
        return True # exit program wshen user trigger EOF


    def do_help(self, arg):
        if arg == 'quit':
            print('Quit command to exit the program')

        elif arg == '':
            print('''Welcome to MyConsole!\n\nDocumented commands (type help <topic>):
            ========================================')
                    'Available commands:\n    help - Provide assistance\n    quit - Exit the program\n    EOF - Exit the program''')


        else:
             cmd.Cmd.do_help(self, arg)


    def emptyline(self):
        """ Enters a new line """

        pass #do nothing when an empty line is entered


    #handle wrong commands
    def default(self, arg):
        print(f"Unknown Command: {arg}")



    def do_create(self, arg):
        """ Creates a new instance and prints the ID"""
        class_name = arg.strip()

        if not class_name:
            print("** class name missing **")
            return

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return


        new_instance = self.classes[class_name]()

        storage.new(new_instance)
        storage.save()


        #print the id of the created instance
        print(new_instance.id)

    def do_show(self, arg):
        #retrieve classname and id from arg
        arg = arg.split(" ")

        #check if class name is given
        if len(arg) < 1:
            print("** class name missing")
            return

        #check if instance ID is missing
        if len(arg) < 2:
            print("** instance id missing **")
            return


        #Assign class name and instance ID from the arguments
        class_name = arg[0]
        instance_id = arg[1]


        #chevck if classname exist
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return


        #Form the instance key and retrieve instance dictionary from storage
        instance_key = f"{class_name}.{instance_id}"
        instance_dict = storage.all().get(instance_key)


        # check if the instance exists
        if not instance_dict:
            print("** no instane found **")
            return

        #print the instance dict
        print(instance_dict)




    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""

        # Parse command arguments
        arg = arg.split(" ")

        if len(arg) < 1:
            print("** class name missing **")
            return


        #assign class name
        class_name = arg[0]

        #check if class exist
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        #check if instance id is provided
        if len(arg) < 2:
            print("** instance id missing **")
            return

        instance_id = arg[1]


        #form instance key to retrieve instance dict from storage
        instance_key = f"{class_name}.{instance_id}"
        instance_dict = storage.all().get(instance_key)

        #destroy instance  dict from storage
        del storage.all()[instance_key]

        #save changes to storage file
        storage.save()



    def do_all(self, class_name = None):
        if class_name:
            filtered_instance = {}
            for key, obj in self.__objects.items():
                if class_name in key:
                    fltered_instance[key] = obj
            return filtered_instance
        else:
            return self.__objects






if __name__ == '__main__':
    MyConsole().cmdloop()
