class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Initializes and returns a singleton instance of the class.

        Parameters:
            cls (type): The class being instantiated.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            object: The singleton instance of the class.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]