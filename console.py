#!/usr/bin/python3
'''
    Implementing the console for the ByteChat project.
'''

import cmd
import shlex
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models import storage
from models.user import User

class BYTECommand(cmd.Cmd):
    """
    Custom console class
    """

    prompt = '(BYTECHAT) '
    valid_classes = {'BaseModel', 'User'}

    method_mapping = {
        'all': 'do_all',
        'count': 'do_count',
        'show': 'do_show'
    }

    def do_quit(self, line):
        """Quit command to exit the program """
        return True

    def do_EOF(self, line):
        """Quits command interpreter with ctrl+d"""
        print("")
        return True

    def emptyline(self):
        """Do nothing on empty input"""
        pass

    def do_create(self, arg):
        """
        create a new instance of BaseModel and save it to the Json file.
        Usage: show <class_name> <id>
        """

        command = shlex.split(arg)

        if len(command) == 0:
            print("** class name missing **")
        elif command[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            class_name = command[0]
            new_instance = eval(f"{class_name}()")
            storage.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Show the string representation of an instance.
        Usage: show <class_name> <id>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
            return
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        elif len(commands) < 2:
            print("** instance id missing **")
            return
        else:
            objects = storage.all()

            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                print(objects[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Delete an instance based on the class name and id.
        Usage: destroy <class_name> <id>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        print the string representation of all instances or a specific class
        usage: all[class_name]
        """
        objects = storage.all()

        commands = shlex.split(arg)

        if len(commands) == 0:
            for key, value in objects.items():
                print(str(value))
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            for key, value in objects.items():
                if key.split('.')[0] == commands[0]:
                    print(str(value))

    def do_update(self, arg):
        """
        Update an instance by adding or updating an attribute.
        Usage: update <class_name> <id> <attribute_name> "<attribute_value>"
        """
        commands = arg.split()
        
        
        if len(commands) == 0:
            print("** class name missing **")
            return
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) == 1:
            print("** instance id missing **")
            return
        elif len(commands) == 2:
            print("** attribute name missing **")
            return
        elif len(commands) == 3:
            print("** value missing **")
            return
        else:

            class_name = commands[0]
            instance_id = commands[1]
            attribute_name = commands[2]
            attribute_value = ' '.join(commands[3:])

            objects = storage.all()
            key = "{}.{}".format(class_name, instance_id)

            if key not in objects:
                print("** no instance found **")
                return

            obj = objects[key]

            try:
                setattr(obj, attribute_name, attribute_value)
                obj.save()
            except Exception as e:
                pass

    def do_all(self, arg):
        """
        print the string representation of all instances or a specific class
        usage: all[class_name]
        """
        objects = storage.all()

        commands = shlex.split(arg)

        if len(commands) == 0:
            for key, value in objects.items():
                print(str(value))
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            for key, value in objects.items():
                if key.split('.')[0] == commands[0]:
                    print(str(value))
    

    def do_count(self, arg):
        """
        Counts and retrieves the number of instances of a class
        Usage: <class name>.count()
        """
        objects = storage.all()
        command = shlex.split(arg)

        if not command:
            print("** class name missing **")
            return

        class_name = command[0]

        if class_name not in self.valid_classes:
            print("** invalid class name **")
            return

        count = 0

        for obj in objects.values():
            if obj.__class__.__name__ == class_name:
                count += 1

        print(count)


    def default(self, line):
        """
        Called on an input line when the command prefix is not recognized.
        """
        parts = line.split('.')  # Split the line by '.' instead of ','

        if len(parts) == 2:
            class_name = parts[0].strip()
            method_name = parts[1].rstrip('()').strip()  # Remove parentheses from method name

            if class_name not in self.valid_classes:
                print("** Class doesn't exist. **")
                return

            if method_name in self.method_mapping:
                method_func = getattr(self, self.method_mapping[method_name])
                method_func(class_name)
                return

        print("** Command not recognized. **")

if __name__ == "__main__":
    BYTECommand().cmdloop()
