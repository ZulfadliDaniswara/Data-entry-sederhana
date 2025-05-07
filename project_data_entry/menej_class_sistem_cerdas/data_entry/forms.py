from django import forms
from .models import Pengguna  # Gunakan titik untuk merujuk ke model dalam aplikasi yang sama
from .models import Content

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

    def set_pengguna(request):
        list_pengguna = Pengguna.objects.all().order_by('-id')
        context = None
        form = PenggunaForm(None)
        email_p = None

        if request.method == "POST":
            form = PenggunaForm(request.POST)
            if form.is_valid():
                # Simpan email pengguna ke dalam session saat klik sign in
                email = form.cleaned_data['email']
                request.session['email'] = email
                request.session.modified = True

                form.save()
                list_pengguna = Pengguna.objects.all().order_by('-id')
                email_p = request.session['email']
                context = {
                'form': form,
                'list_pengguna': list_pengguna,
                'email_p': email_p,
            }
            return render(request, 'data_entry/input_pengguna.html', context)

        else:
            context = {
                'form': form,
                'list_pengguna': list_pengguna,
        }
        return render(request, 'data_entry/input_pengguna.html', context)

    def set_content(request):
        form = ContentForm(None)
        context = None
        pengguna = None

        if request.session.get('email', None):
            email = request.session.get('email', None)
            pengguna = Pengguna.objects.get(email=email)
            initial_data = {'author': pengguna}
            form = ContentForm(initial=initial_data)

        if request.method == 'POST':
            form = ContentForm(request.POST)
            if form.is_valid():
                form.save()
                context = {
                    'form': form,
                }
                return render(request, 'data_entry/create_content.html', context)

        else:
            context = {
            'form': form,
            'email': email,
            'pengguna': pengguna,
        }
        return render(request, 'data_entry/create_content.html', context)
    
class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['author', 'artikel', 'set_view']

