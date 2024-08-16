from django import forms
from .models import Member

class MemberForms(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['fname', 'lname', 'email', 'age', 'passwd']




class CSVUploadForm(forms.Form):
    file = forms.FileField(label='Select a CSV file')
