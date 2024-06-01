#!/usr/bin/python3

import cmd
from models.base_model import BaseModel
from models.engine.file_storage  import FileStorage
from models import storage
from models.user import User


class MyConsole (cmd.Cmd):
    classes = {"BaseModel" : BaseModel, "User": User}


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
        # Split the argument to extract class name and additional attributes
        class_name, *attributes  = arg.split()

        # Check if class name is missing

        if not class_name:
            print("** class name missing **")
            return


        # Check if class exists in registered classes
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return


        # Initialize an empty dictionary to store additional attributes
        kwargs = {}

        # Parse additional attributes if provided
        for attr in attributes:
            # Split each attribute into key-value pair
            key, value = attr.split('=')
            # Store the key-value pair in the kwargs dictionary
            kwargs[key] = value


        # Create a new instance of the specified class with the additional attributes
        new_instance = self.classes[class_name](**kwargs)


        # Add the new instance to storage and save
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
            for key, obj in storage.all().items():

                if class_name in key:
                    filtered_instance[key] = obj

            if not filtered_instance:
                print("** class doesn't exist **")

            else:
                for key, obj in filtered_instance.items():
                    print(obj)

        else:

            for key, obj in storage.all().items():
                print(obj)



    def do_update(self, args):
       
        # Split the arguments# 
        args = args.split()


        # Check if the class name is missing
        if len(args) < 1:
            print("** class name missing **")
            return


        class_name = args[0]

        # Validate the class name
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        # Check if the instance ID is missing
        if len(args) < 2:
            print("** instance id missing **")
            return


        instance_id = args[1]
        instance_key = f"{class_name}.{instance_id}"
        instance_dict = storage.all().get(instance_key)




        # Check if the instance exists
        if not instance_dict:
            print("** no instance found **")
            return

        # Check if the attribute name is missing


        instance = self.classes[class_name](**instance_dict)

        # Check if the attribute name is missing
        if len(args) < 3:
            print("** attribute name missing **")
            return


        attribute_name = args[2]

        # Check if the attribute value is missing
        if len(args) < 4:
            print("** value missing **")
            return


        # Extract the attribute value, ensuring it is correctly quoted
        attribute_value = " ".join(args[3:]).strip('"')


        # Update the attribute value
        setattr(instance, attribute_name, attribute_value)

        # Save the changes to the storage
        storage.new(instance)  # Update the storage with the new instance
        instance.save()
        print(instance)





if __name__ == '__main__':
    MyConsole().cmdloop()
