from app.models import Section

def navbar(request):
    sections = Section.objects.all()
    return {'navbar_sections': sections}
