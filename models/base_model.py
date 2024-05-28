
from datetime import datetime
from uuid import uuid4
from models import storage


class BaseModel:

    def __init__(self, *args, **kwargs):
        self.id = str(uuid4()) #generate unique id for each instance
        self.created_at = self.updated_at = datetime.now()

        if not kwargs:#check if its a new instance and store it
            storage.new(self)


        if kwargs:
            #Remove the '__class__' key if present, None if not present
            kwargs.pop('__class__', None)

            obj_value = None

            for key, value in kwargs.items():
                if key in ['created_at', 'updated_at']:
                    #Convert the string value to a datetime object
                    obj_value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")

                setattr(self, key, obj_value)

        #else:
          #  self["id] = str(uuid4())
            #self.created_at = self.updated_at = datetime.now()



    def __str__(self):
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)


    def save(self):
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        instance_dict = self.__dict__.copy()
        instance_dict['class'] = self.__class__.__name__
        instance_dict['created_at'] = self.created_at.isoformat()
        instance_dict['updated_at'] = self.updated_at.isoformat()
        return instance_dict
