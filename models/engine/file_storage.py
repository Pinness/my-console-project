import os
import json
from json.decoder import JSONDecodeError


class FileStorage:

    __file_path = "data.json"
    __objects = {}


    def all(self):
        return self.__objects

    def new(self, obj):
        obj_class = obj.__class__.__name__
        obj_id = obj.id
        key = f"{obj_class}.{obj_id}"
        self.__objects[key] = obj.to_dict()



       # obj_key = print("{}.{}".format(obj_class, obj_id))
        #self.__object[obj_key] = obj



    #convert __object to json and store in data.json
    def save(self):
       # serialised_obj = json.dumps(self.__objects)
        with open(self.__file_path, 'w') as file_obj:
            serialised_obj = json.dump(self.__objects, file_obj)
            #file_obj.write(serialised_obj)  #write the serialized object to the file


    #convert json to python obj
    def reload(self):
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, 'r') as file_obj:
                #json_file = file.read() #reads the entire file
                try:
                    deserialised_file = json.load(file_obj)
                    self.__objects.update(deserialised_file) #update the __object attri
                except JSONDecodeError:
                    pass
