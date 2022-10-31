from django.contrib import admin
from prescription_app.models import Prescription
from prescription_app.models import Reports
from prescription_app.models import Symptoms
from prescription_app.models import ReportFile
from prescription_app.models import OnlinePrescription
from prescription_app.models import OnlineReports
from prescription_app.models import OnlineSymptoms
from prescription_app.models import OnlineReportFile



# Register your models here.
admin.site.register(Prescription)
admin.site.register(Reports)
admin.site.register(Symptoms)
admin.site.register(ReportFile)
admin.site.register(OnlinePrescription)
admin.site.register(OnlineReports)
admin.site.register(OnlineSymptoms)
admin.site.register(OnlineReportFile)
