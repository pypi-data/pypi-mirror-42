import mock
class TypeNotRegisteredException(Exception): #pragma no cover
    def __init__(self, type):
        super(TypeNotRegisteredException, self).__init__("The type {} is not registered".format(str(type)))

class InstanceRecord:
    def __init__(self, instance, is_singleton = False):
        self.instance = instance
        self.is_singleton = is_singleton


_di_map = {}
_initialized = False
 #eg module.Type.VersionPinHandler: InstanceRecord(lambda: module.Type(get_instance_of(module2.Type2), get_instance_of(module3.Type3))),
def init(di_map):
    global _di_map
    global _initialized
    _di_map = di_map
    _initialized = True


def get_instance_of(object_type, name=None): #pragma: no cover
    if not _initialized:
        raise Exception("DI bootstrap has not been initialized yet.")

    key = (object_type, name) if name is not None else object_type
    if key not in _di_map:
        raise TypeNotRegisteredException(object_type)

    instance_record = None
    instance = _di_map[key]

    if isinstance(instance, InstanceRecord):
        instance_record = instance
        instance = instance_record.instance

    # Mock are callable and it is usually not the expected behavior here
    if callable(instance) and not isinstance(instance, mock.Mock):
        return_value = instance()
        if instance_record is not None and instance_record.is_singleton:
            instance_record.instance = return_value
        return return_value

    return instance
