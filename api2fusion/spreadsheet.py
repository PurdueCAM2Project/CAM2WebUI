"""
Represents spreadsheet
"""
import pygsheets

class CAM2sheet(object):
    """Spreadsheet class to represent cam2 spreadsheet

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes
    ----------
    id : int
        stores id of the spreadsheet
    name: str
        stores name of the spreadsheet
    gs : Spreadsheet
        underlying spreadsheet object

    _gc : Google Client
        underlying client. User shouldn't adjust that


    """


    """
        A dictionary the maps the header names to a boolean that determines whether it should be on the sheets
    """
    _sheet_headers = {
        'Time Zone': False,
        'Time Zone ID': False,
        'Resolution Height': False,
        'Resolution Width': False,
        'City': False,
        'State': False,
        'Country': False,
        'Longitude': False,
        'Latitude': False,
        'Source': False,
        'Is Active Active Video': False,
        'Is Active Image': False,
        'ID': False,
        'Type': False,
        'Reference Logo': False,
        'Reference URl': False,
        'UTC offset': False
    }

    #TODO  error handling for invalid args
    #TODO  error handling for failed authorization

    def __init__(self, service_file, id=None, name=None):
        """

        Parameters
        ----------
        service_file :
        id :
        name :
        """


        self._gc = pygsheets.authorize(service_file=service_file)
        self.id = None
        self.name = None
        self.gs = None


        if(name):
            self.name = name
            self.gs = self._gc.open(name)
        elif(id):
            self.id = id
            gs = self._gc.open_by_key(id)
        return self.gs

    #TODO error handling for invalid args
    #TODO error handling for failed auth
    def open(self, **kwargs):
        """

        Parameters
        ----------
        kwargs :

        Returns
        -------

        """
        gs = None
        if 'name' in kwargs:
            gs = self._gc.open(kwargs.get('name'))
        elif 'id' in kwargs:
            gs = self._gc.open_by_key(kwargs.get('id'))
        self.gs = gs

        return self.gs


    def create(self):
        """

        Returns
        -------

        """




    def update(self, camera):
        """

        Parameters
        ----------
        log :

        Returns
        -------

        """



    def worksheet(self, num):
        """

        Parameters
        ----------
        num :

        Returns
        -------

        """

