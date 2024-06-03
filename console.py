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


    def strip_clean(self, args):
        """strips the argument and return a string of command
        Args:
            args: input list of args
        Return:
            returns string of argumetns
        """
        new_list = []
        new_list.append(args[0])
        try:
            my_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_list.append(((new_str.split(", "))[0]).strip('"'))
            new_list.append(my_dict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_list)


    def default(self, line):
        """retrieve all instances of a class and
        retrieve the number of instances
        """
        my_list = line.split('.')
        if len(my_list) >= 2:
            if my_list[1] == "all()":
                self.do_all(my_list[0])
            elif my_list[1] == "count()":
                self.do_count(my_list[0])
            elif my_list[1][:4] == "show":
                self.do_show(self.strip_clean(my_list))
            elif my_list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(my_list))
            elif my_list[1][:6] == "update":
                args = self.strip_clean(my_list)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, line)

if __name__ == "__main__":
    BYTECommand().cmdloop()
