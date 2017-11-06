from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Profile)
admin.site.register(Contest)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Problem)
admin.site.register(Submission)
admin.site.register(Tag)
admin.site.register(Test)
admin.site.register(ProbTag)
admin.site.register(ProbContest)
admin.site.register(Participation)
admin.site.register(regnConfirm)