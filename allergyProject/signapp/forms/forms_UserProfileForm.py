from django import forms
from signapp.models import Customer
from searchapp.models import Allergy

class UserProfileForm(forms.ModelForm):
    
    # 알러지 정보를 쉼표로 구분하여 저장할 TextField로 정의
    allerinfo = forms.ModelMultipleChoiceField(
        queryset=Allergy.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Customer
        fields = ['email', 'phone', 'birthdate', 'gender', 'allerinfo']

    # 이메일 필드를 선택적으로 만듦
    email = forms.EmailField(required=False)