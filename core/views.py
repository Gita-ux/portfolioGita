from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import ContactForm
from .models import Experience, Profile, Project, Skill, Stat


def index(request):
    profile = Profile.objects.first()
    skill_groups = [
        {
            "key": key,
            "label": label,
            "skills": Skill.objects.filter(category=key),
        }
        for key, label in Skill.Category.choices
    ]
    context = {
        "profile": profile,
        "stats": Stat.objects.all(),
        "skill_groups": skill_groups,
        "project_categories": Project.Category.choices,
        "projects": Project.objects.filter(featured=True),
        "works": Experience.objects.filter(kind=Experience.Kind.WORK),
        "studies": Experience.objects.filter(kind=Experience.Kind.EDU),
    }
    return render(request, "core/index.html", context)


@require_POST
def contact(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"ok": True, "message": "Message envoyé. Je te réponds très vite."})
    errors = {k: v[0] for k, v in form.errors.items()}
    return JsonResponse({"ok": False, "errors": errors}, status=400)
