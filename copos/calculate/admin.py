from django.contrib import admin
from .models import PO, Course, CO, COPOMapping, COAttainment, StudentMark, Student

admin.site.register(PO)
admin.site.register(Course)
admin.site.register(CO)
admin.site.register(COPOMapping)
admin.site.register(COAttainment)
admin.site.register(StudentMark)
admin.site.register(Student)


