from django.shortcuts import render

def index(request):
    context = {}
    if request.path == '/':
        context['label'] = 'Главная'
    else:
        context['label'] = request.path
    return render(request, 'menu/index.html', context)