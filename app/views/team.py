from django.shortcuts import render
from ..models import Team, Leader, Member, TeamMember, Subteam

def team(request):
    """Renders content for the Team page

    Retrieves information from the Team database using the matching Django Model structure.

    Args:
        request: the HttpRequest corresponding to the page to be accessed.

    Returns:
        A render that displays the page team.html, complete with information from the Team database.
    """
    team_list = Team.objects.reverse()
    leader_list = Leader.objects.reverse()
    curmember_list = Member.objects.filter(iscurrentmember=True).order_by("membername")
    oldmember_list = TeamMember.objects.filter(iscurrentmember=False).order_by("name")
    director_list = TeamMember.objects.filter(isdirector=True).order_by("name")
    subteam = Subteam.objects.all()
    members = TeamMember.objects.all()

    context = {
        "team_list": team_list,
        "leader_list": leader_list,
        "curmember_list": curmember_list,
        "oldmember_list": oldmember_list,
        'subteams_list': subteam,
        "members_list": members,
        "director_list": director_list,
    }
    return render(request, 'app/team.html', context)
