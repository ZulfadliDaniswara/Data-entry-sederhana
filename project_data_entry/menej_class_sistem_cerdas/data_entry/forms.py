from django import forms
from .models import Pengguna  # Gunakan titik untuk merujuk ke model dalam aplikasi yang sama

STATES = (
    ('', 'Choose...'),
    ('MG', 'Minas Gerais'),
    ('SP', 'Sao Paulo'),
    ('RJ', 'Rio de Janeiro')
)

class AddressForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput())
    address_1 = forms.CharField(
        label='Address',
        widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    )
    address_2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor'})
    )
    city = forms.CharField()
    state = forms.ChoiceField(choices=STATES)
    zip_code = forms.CharField(label='Zip')
    check_me_out = forms.BooleanField(required=False)

class PenggunaForm(forms.ModelForm):  # Harus pakai ModelForm, bukan Form
    state = forms.ChoiceField(choices=STATES)

    class Meta:
        model = Pengguna
        exclude = ['tanggal_join']

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)  # Memastikan field dari model tetap ada
        self.fields['state'].required = True  # Contoh jika ingin membuat state wajib diisi