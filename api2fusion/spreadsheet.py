"""
Represents spreadsheet
"""
import pygsheets


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
    _gc : Google Client
        underlying client. User shouldn't adjust that

    Note
    ----
    Assumptions:
        1. First worksheet only is used


    """


    """
        A dictionary the maps the header names to a name of parameter in the API. If None then it won't be updated on sheet.
        It has to be the same order as the columns in the spreadsheet
    """

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

        try:
            self._gc = pygsheets.authorize(service_file=service_file)
            self.id = None
            self.name = None
            self.gs = None
            self.wks = None
        except pygsheets.AuthenticationError:
            print("Error Authenticating.")


        if(name):
            try:
                self.name = name
                self.gs = self._gc.open(name)
                self.wks = self.gs.worksheet1
            except pygsheets.SpreadsheetNotFound:
                print("Spreadsheet name is incorrect.")
        elif(id):
            try:
                self.id = id
                self.gs = self._gc.open_by_key(id)
                self.wks = self.gs.worksheet1
            except:
                print("Spreadsheet ID is incorrect")

        return self.wks

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
        self.wks = self.gs.worksheet1

        return self.wks


    def create(self):
        """

        Returns
        -------

        """




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







