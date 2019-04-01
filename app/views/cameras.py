from ..forms import ReportForm
from ..models import ReportedCamera
from django.contrib import messages
from django.shortcuts import render
import datetime

# Get an instance of a logger
import logging
logger = logging.getLogger(__name__)

def cameras(request):
    """Process user reports of broken cameras in the database
    The reports are stored in the ReportedCamera model for the Camera Database team to correct the issues. """

    if request.method == 'POST':
        # The user would like to report a broken camera to CAM2
        # This feature only works when the user is logged in
        form = ReportForm(request.POST)
        if form.is_valid():
            #get info from form
            camID = form.cleaned_data['cameraID']
            #check for existing reported camera
            camidlist = ReportedCamera.objects.reverse().values_list("cameraID", flat=True)
            user = None
            if request.user.is_authenticated:
                user = request.user.username

            if camID not in camidlist:
                #add info to admin database - using a new entry
                cam_obj = ReportedCamera(username=user, cameraID=camID, reporttime=datetime.datetime.now())
                cam_obj.save()
            else:
                #add info to admin database - using the existing entry
                cams = ReportedCamera.objects.filter(cameraID__exact=camID)
                logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
                logging.debug('This is the user : ' + str(cams))

                for c in cams:
                    #theoretically, there should only one camera here, but add it to any/all of them just in case
                    if user not in str(c.username):
                        c.username = str(c.username) + ', ' +  user
                        c.save()

            form = ReportForm()
            messages.success(request, 'The unavailable image has been reported. Thank you!')

    else:
        form = ReportForm()

    return render(request, "app/cameras.html", {'form': form})
