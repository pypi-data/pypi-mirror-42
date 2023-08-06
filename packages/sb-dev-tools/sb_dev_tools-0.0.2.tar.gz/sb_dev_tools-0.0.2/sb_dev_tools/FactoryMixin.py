

class FactoryMixin:
    """
    Provides internal Factory functionality for a class.
    """

    class Factory:
        """
        Internal factory.
        """

        def __init__(self, cls):
            """
            Constructs with a reference to another class. not sure that this is the best design. For now, to get other
            parts working as desired this will be done. A better solution would be through a decorator.
            Args:
                cls: class definition for class to be constructed
            """

            self.__cls__ = cls

        def create(self):
            """
            Factory method used to create a class instance.

            Returns: Instance of the class for which it is a mixin.

            """
            return self.__cls__()
