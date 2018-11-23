from ..forms import ReportForm
from ..models import ReportedCamera
from django.shortcuts import render

# Get an instance of a logger
import logging
logger = logging.getLogger(__name__)

def cameras(request):
#    context = {'google_api_key': settings.GOOGLE_API_KEY,
#               'google_client_id': settings.GOOGLE_CLIENT_ID}
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            #recaptcha_response = request.POST.get('g-recaptcha-response')
            #url = 'https://www.google.com/recaptcha/api/siteverify'
            #values = {
            #    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            #    'response': recaptcha_response
            #}
            #data = urllib.parse.urlencode(values).encode()
            #req = urllib.request.Request(url, data=data)
            #response = urllib.request.urlopen(req)
            #result = json.loads(response.read().decode())
            #if result['success']:

            #get info from form
            camID = form.cleaned_data['cameraID']
            #add info to email template
            #content = render_to_string('app/cam_report_email_template.html', {
            #    'cameraID': camID,
            #})
            #send_mail("Camera with Unavailable Image Reported", content, EMAIL_HOST_USER, [MANAGER_EMAIL])#email admin
            #check for existing reported camera
            camidlist = ReportedCamera.objects.reverse().values_list("cameraID", flat=True)
            user = None
            if (request.user.is_authenticated):
                user = request.user.username

            if camID not in camidlist:
                #add info to admin database - using cleaned_data


                cam_obj = ReportedCamera(username=user, cameraID=camID, reporttime=datetime.datetime.now())
                cam_obj.save()

            else:
                cams = ReportedCamera.objects.filter(cameraID__exact=camID)
                logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
                logging.debug('This is the user : ' + str(cams))
                if(cams):
                    for c in cams:
                        if (not user in str(c.username)):
                            c.username = str(c.username) + ', ' +  user
                            c.save()


            #return redirect('email_sent')
            form = ReportForm()
            messages.success(request, 'The unavailable image has been reported. Thank you!')



    else:
        form = ReportForm()

    return render(request, "app/cameras.html", {'form': form})
