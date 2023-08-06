import importlib
import inspect
import os

from sb_dev_tools.SnoodlebootError import SnoodlebootError


class PolyFactory:
    """
    Polymorphic Factory


    * Base class for class internal factories
    * Maintains a list (dict, ...) of known factories from when it was initiated
    * Performs class factory discovery at initiation and on demand
        * Within a package
        * Within a user created package
        * Starting from root path
    * Can know the base type for which it is a factory
    * Will know when it has been initialized
    * Can add a class factory on command

    """

    # Maintains a list of factory methods
    _factories = {}

    # Identifies the type of base class that the factory will be responsible for
    _object_base_type = None

    # True if factory has been initialized, false otherwise
    _factory_is_initialized = False

    @classmethod
    def discover_class_factories(cls):
        
        # Not all 'modules' are modules, or are modules of interest. Below is a list of
        # those which are explicitly excluded
        excluded_packages = [
            '__init__',
            cls._object_base_type,
        ]
        
        # Identify all python classes within the base module scope (where the chile of PolyFactory is located)
        discovered_modules = cls._find_python_modules()

        admissable_modules = []

        # Find all modules which have the specified base type.
        for module in discovered_modules:

            # Remove modules that shouldn't be considered from teh get go.
            if module['module_name'] in excluded_packages:
                continue

            # Construct the module callable name
            module_name = '.'.join([module['package_path'],
                                    module['module_name']])
            
            # Load the module dynamically
            imported_module = importlib.import_module(module_name)

            members = inspect.getmembers(imported_module)

            # Find all class modules which are members of the module
            class_object_reference_list = [(member_name, object_reference) 
                                           for member_name, object_reference in members 
                                           if inspect.isclass(object_reference)]

            # For each class obtain its MRO. If in the MRO there is reference to the object_base_type,
            # then the object is admissable.
            for name, object_reference in class_object_reference_list:
                mro = inspect.getmro(object_reference)

                # Check for admissability
                for obj_reference in mro:
                    if isinstance(obj_reference(), cls._object_base_type) \
                            and obj_reference is not cls._object_base_type:

                        admissable_modules.append(obj_reference)

        # dedupe: This may not be a unique list due to imports. In this case make sure to exclude duplicates.
        admissable_modules = list(set(admissable_modules))

        # Build the factory list
        for module in admissable_modules:

            factory_label = '.'.join([module().__class__.__module__, module().__class__.__name__])
            cls._factories[factory_label] = module().Factory(cls=module).create

        cls._factory_is_initialized = True

        return None

    @classmethod
    def _find_python_modules(cls, path=None, package_path=None) -> list:
        """
        Identifies (possible) python modules. Will start from an alternative location when a path is provided.
        When path location provided has nested directories it will recursively identify modules within the
        nested structure.

        Args:
            path:
            package_path:

        Returns: list of dictionaries with protocol: {'module_name':, 'package_path':}

        Raises: ValueError

        """

        # Create a container (list) to hold all identified python classes.
        entries = list()

        # As the method is recursive, it is necessary that the directory be set to the path when
        # called recursively. Otherwise it will be set to the current working directory. This
        # means that the underlying assumption is that the derived polymorphic factory is at the
        # same or more shallow depth as the classes which it will be cataloging.
        if not path:
            directory = os.getcwd()
        else:
            directory = path

        # This is the 'python package path'. That is, it is the dot delimited package path used
        # to import modules from a package.
        if not package_path:
            package_path = os.path.basename(os.getcwd())

        # This is the meat and potatoes of the python package identification algorithm. Given the
        # current directory (as passed in or defaulted) all 'entries' within the directory are
        # iterated over. If the entry is a directory, then we call the algorithm recursively. If
        # not, then it should be a file. If it is a file AND it ends with '.py', then it is
        # capture. The capture consists of the name of the module (python file absent the extension
        # and the package_path (the dot delimited package name). Each of the calls in the algorithm
        # will either append a single entry to the list of modules or extend it with a list (from
        # recursive call).
        for entry in os.listdir(directory):

            # Extract the python files
            if os.path.isfile(os.path.join(directory, entry)) and entry.endswith('.py'):

                entries.append(
                    {
                        'module_name': entry.replace('.py', ''),
                        'package_path': package_path,
                    }
                )

            # This is a directory, make recursive call
            if os.path.isdir(entry):
                entries.extend(
                    cls._find_python_modules(path=os.path.abspath(entry),
                                             package_path='.'.join([package_path, entry])),
                )

        return entries

    @classmethod
    def add_factory(cls, object_id):

        raise NotImplementedError

    @classmethod
    def create(cls, object_id: str):
        """
        Retrieves an object's factory from the _factories class variable and returns an instance of the class.

        Args:
            object_id: string identifying the desired class inheriting a FactoryMixin

        Returns: Instance of a FactoryMixin

        """

        # Check if _factories class variable has been populated.
        if not cls._factory_is_initialized:
            cls.discover_class_factories()

        if object_id not in cls._factories.keys():
            raise SnoodlebootError("Class with factory_id '{factory_identifier}'".format(factory_identifier=object_id))

        return cls._factories[object_id]()
