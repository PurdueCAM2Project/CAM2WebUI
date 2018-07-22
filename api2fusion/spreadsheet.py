"""
Represents spreadsheet
"""
import pygsheets



"""
A dictionary the maps the header names to a name of parameter in the API. If None then it won't be updated on sheet.
It has to be the same order as the columns in the spreadsheet.
"""

SHEET_HEADERS = {
        'Time Zone': None,
        'Time Zone ID': None,
        'Resolution Height': None,
        'Resolution Width': None,
        'City': None,
        'State': None,
        'Country': None,
        'Longitude': None,
        'Latitude': None,
        'Source': None,
        'Is Active Active Video': None,
        'Is Active Image': None,
        'ID': None,
        'Type': None,
        'Reference Logo': None,
        'Reference URl': None,
        'UTC offset': None
    }


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
    wks: Worksheet
        underlying worksheet object
    __gc : Google Client
        underlying client. User shouldn't adjust that

    Note
    ----
    Assumptions:
        1. First worksheet only is used


    """




    #TODO Refactor errors raised

    def __init__(self, service_file, id=None, name=None, operation='create'):
        """

        Parameters
        ----------
        service_file : str
            service file path
        id : str (optional)
            id of spreadsheet. Must be provided if operation = 'open'
        name : str (optional if operation = 'open')
            name of spreadsheet. Must be provided if operation = 'create', optional otherwise.
        operation : str
            must be either 'create' or 'open'. default is create

        Raises
        ------
        TypeError
            if any of the provided arguments aren't strings
        """

        if(not isinstance(service_file, str)):
            raise TypeError('service file should be string')

        self.__gc = pygsheets.authorize(service_file=service_file)
        self.id = None
        self.name = None
        self.gs = None
        self.wks = None

        if(operation == 'open'):
            if(name):
                if (not isinstance(name, str)):
                    raise TypeError('name should be string ')
                self.name = name
                self.gs = self.__gc.open(name)
                self.wks = self.gs.worksheet1
            elif(id):
                if (not isinstance(id, str)):
                    raise TypeError('id should be a string')
                self.id = id
                self.gs = self.__gc.open_by_key(id)
                self.wks = self.gs.worksheet1
            else:
                raise Exception('Must provide either id or name')
        elif(operation == 'create'):
            if (not isinstance(name, str)):
                raise TypeError('name should be string ')
            self.name = name
            self.gs = self.__create(name)
            self.wks = self.gs.worksheet1
            self.id = self.gs.id
        else:
            raise Exception('operation parameter can be either \'create\' or \'open\'')

    def __open(self, **kwargs):
        """

        Parameters
        ----------
        kwargs :

        Returns
        -------

        """
        gs = None
        if ('name' in kwargs and kwargs['name']):
            if(not isinstance(kwargs['name'], str)):
                raise TypeError('name should be string ')
            gs = self.__gc.open(kwargs.get('name'))
        elif ('id' in kwargs and kwargs['id']):
            if (not isinstance(kwargs['id'], str)):
                raise TypeError('id should be a string')
            gs = self.__gc.open_by_key(kwargs.get('id'))

        self.gs = gs
        self.wks = self.gs.worksheet1

        return self.wks


    def __create(self, title):
        """

        Parameters
        ----------
        title : str
            title of spreadsheet

        Returns
        -------

        """
        return self.__gc.create(title=title)




    def update(self, camera):
        """

        Parameters
        ----------
        camera : Camera
            a camera object that has all its parameters stored in __dict___

        Returns
        -------

        """
        ids = self.get_ids()
        if(camera.id in ids):
            idx = ids.index(camera.id)
            self.wks.update_cells((idx, 1), [camera.__dict__[v] for (k, v) in SHEET_HEADERS.items() if(v != None) ])

        else:
            self.wks.insert_rows(ids[-1], 1, [camera.__dict__[v] for (k, v) in SHEET_HEADERS.items() if(v != None) ])




    def delete(self, **kwargs):
        """

        Parameters
        ----------
        kwargs :

        Returns
        -------

        """

    def get_ids(self):
        """

        Returns List
        -------
            list of all IDs in the sheet
        """
        return self.wks.get_col(col=1)







