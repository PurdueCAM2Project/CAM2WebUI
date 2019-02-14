import datetime
from django.utils.deconstruct import deconstructible
@deconstructible
class GraduationValidator:
    def getSemester(month, year):
        """Gets the semester that a graduation month would take place during added onto 3 times the year.
        0 : Winter
        1 : Spring
        2 : Summer
        """
        return year + (month + 2) // 4

    def __call__(self, value):
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        """Check if the person can stay for more than one semester."""
        print(value)
        
