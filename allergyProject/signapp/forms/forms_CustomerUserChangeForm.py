from django import forms
from signapp.models import Customer
from searchapp.models import Allergy

class CustomUserChangeForm(forms.ModelForm):
    gender = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    allerinfo = forms.ModelMultipleChoiceField(
        queryset=Allergy.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Customer  # 폼과 연결될 모델 (Customer 모델)
        fields = ['email', 'phone', 'birthdate', 'gender','allerinfo']  # 폼에 사용될 필드들

    # 이메일 중복 검사를 위한 메서드
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # 이미 등록된 이메일이 존재하면 에러 발생
        if Customer.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("이미 있는 이메일입니다.")
        
        return email