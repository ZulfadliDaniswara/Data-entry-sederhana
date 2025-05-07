from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .forms import AddressForm, PenggunaForm, ContentForm
from .models import Pengguna, Content

# Form untuk address
def set_data_entry(request):
    form = AddressForm()
    return render(request, 'data_entry/input_data.html', {'form': form})

# Form dan list pengguna
def set_pengguna(request):
    form = PenggunaForm()
    list_pengguna = Pengguna.objects.all().order_by('-id')

    if request.method == "POST":
        form = PenggunaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('data_entry:set_pengguna')  # Redirect untuk form kosong & refresh list

    context = {
        'form': form,
        'list_pengguna': list_pengguna,
    }
    return render(request, 'data_entry/input_data_1.html', context)

# Detail pengguna
def view_pengguna(request, id):
    pengguna = get_object_or_404(Pengguna, pk=id)
    return render(request, 'data_entry/pengguna_detail.html', {'user_id': pengguna.id})

# API detail pengguna
def get_pengguna_detail_api(request, user_id):
    try:
        pengguna = Pengguna.objects.get(pk=user_id)
        data = {
            'email': pengguna.email,
            'address_1': pengguna.address_1,
            'address_2': pengguna.address_2,
            'city': pengguna.city,
            'state': pengguna.state,
            'zip_code': pengguna.zip_code,
            'tanggal_join': pengguna.tanggal_join.strftime('%Y-%m-%d'),
        }
        return JsonResponse(data)
    except Pengguna.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

# Form konten + daftar konten
def set_content(request):
    form = ContentForm()
    pengguna = None
    email = request.session.get('email')

    if email:
        pengguna = Pengguna.objects.filter(email=email).first()
        if pengguna:
            form = ContentForm(initial={'author': pengguna})

    if request.method == "POST":
        form = ContentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('data_entry:set_content')  # Clear form after submit

    daftar_konten = Content.objects.select_related('author').order_by('-created_at')

    context = {
        'form': form,
        'email': email,
        'pengguna': pengguna,
        'daftar_konten': daftar_konten,
    }
    return render(request, 'data_entry/content.html', context)

# Cari pengguna berdasarkan state
def search_pengguna_by_state(request):
    query = request.GET.get('state')
    results = Pengguna.objects.filter(state__icontains=query) if query else []
    return render(request, 'data_entry/search_pengguna.html', {'query': query, 'results': results})

# Update data pengguna
def update_pengguna(request, id):
    pengguna = get_object_or_404(Pengguna, pk=id)
    if request.method == 'POST':
        form = PenggunaForm(request.POST, instance=pengguna)
        if form.is_valid():
            form.save()
            return redirect('data_entry:set_pengguna')
    else:
        form = PenggunaForm(instance=pengguna)

    return render(request, 'data_entry/content.html', {'form': form, 'pengguna': pengguna})

# Hapus pengguna
def delete_pengguna(request, id):
    pengguna = get_object_or_404(Pengguna, id=id)
    pengguna.delete()
    return redirect('data_entry:set_pengguna')
