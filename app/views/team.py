from django.shortcuts import render
from ..models import Team, Faculty, Member, TeamMember, Subteam

def team(request):
    """Renders content for the Team page

    Retrieves information from the Team database using the matching Django Model structure.

    Args:
        request: the HttpRequest corresponding to the page to be accessed.

    Returns:
        A render that displays the page team.html, complete with information from the Team database.
    """
    team_list = Team.objects.all()
    faculty_list = Faculty.objects.all()
    oldmember_list = TeamMember.objects.filter(iscurrentmember=False)
    director_list = TeamMember.objects.filter(isdirector=True)
    subteam = Subteam.objects.all()
    members = TeamMember.objects.all()

    context = {
        "team_list": team_list,
        "faculty_list": faculty_list,
        "oldmember_list": oldmember_list,
        'subteams_list': subteam,
        "members_list": members,
        "director_list": director_list,
    }
    return render(request, 'app/team.html', context)
