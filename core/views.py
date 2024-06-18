from django.shortcuts import render, redirect
from .models import Pessoa
import logging

logger = logging.getLogger(__name__)

def home(request):
    pessoas = Pessoa.objects.all()
    return render(request, 'index.html', {"pessoas": pessoas})

def salvar(request):
    vnome = request.POST.get('nome')
    Pessoa.objects.create(nome=vnome)
    pessoas = Pessoa.objects.all()
    return render(request, 'index.html', {"pessoas": pessoas})

def editar(request, id):
    pessoa = Pessoa.objects.get(id=id)
    return render(request, 'update.html', {"pessoa": pessoa})

def update(request, id):
    if request.method == 'POST':
        vnome = request.POST.get("nome")
        logger.debug(f'Nome recebido: {vnome}')
        
        try:
            pessoa = Pessoa.objects.get(id=id)
            pessoa.nome = vnome
            pessoa.save()
            logger.debug('Pessoa atualizada com sucesso')
            return redirect(home)
        except Pessoa.DoesNotExist:
            logger.error(f'Pessoa com id {id} não encontrada')
            return render(request, 'error.html', {"message": "Pessoa não encontrada"})
    else:
        logger.error('Método não permitido')
        return render(request, 'error.html', {"message": "Método não permitido"})
    
def delete(request, id):
    try:
        pessoa = Pessoa.objects.get(id=id)
        pessoa.delete()
        logger.debug(f'Pessoa com id {id} deletada com sucesso')
        return redirect(home)
    except Pessoa.DoesNotExist:
        logger.error(f'Pessoa com id {id} não encontrada')
        return render(request, 'error.html', {"message": "Pessoa não encontrada"})