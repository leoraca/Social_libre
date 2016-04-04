
# Copyright [2016] [Leoncio Ramos Carrasco]
#Licensed under the Apache License, Version 2.0 you may not use this file except in compliance You may obtain a copy of the License at

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from gestionchismes.models import Chismero, Mensaje, Favorito, Retweet
from gestionchismes.forms import UserCreationForm, ChismenewForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render_to_response
from random import sample
from django.core.urlresolvers import reverse_lazy
# Create your views here.
#Vamos hacer las vistas a partir de clases

@login_required(login_url='/gestionchismes/logueo/')
def mostrar (request):
	"""Por si es la primera vez que nos conectamos con bd vacia"""
	try:
		Chismero.objects.get(username=request.user.username)
	except Chismero.DoesNotExist:
		return HttpResponseRedirect('/gestionchismes/logoff')
	
	q=Chismero.objects.get(username=request.user.username)
	p=Chismero.objects.filter(seguidores=q)
	todos=suguerido(request)
	"""Sacamos todos los mensajes de las personas a quien seguimos"""
	mensajes=Mensaje.objects.filter(username=p).order_by('-fecha_registro')
	return render(request, 'usuario.html', {'Mensajes':mensajes, 'siguiendo':p, 'seguido':q, 'elegidos':todos,})

@login_required(login_url='/gestionchismes/logueo/')
def suguerido(request):
	q=Chismero.objects.get(username=request.user.username)
	p=Chismero.objects.filter(seguidores=q)
	contador=Chismero.objects.all().count()
	if contador > 4:
		rand_ids=sample(xrange(1, contador), 4)
		final=Chismero.objects.filter(id__in=rand_ids).exclude(seguidores=q).exclude(username=q)
		return final
	else:
		rand_ids=sample(xrange(1, contador), contador-1);
		final=Chismero.objects.filter(id__in=rand_ids).exclude(seguidores=q).exclude(username=q)
		return final

@login_required(login_url='/gestionchismes/logueo/')
def seguir(request, user_id):
	following=Chismero.objects.get(username=user_id)
	user_actual=Chismero.objects.get(username=request.user.username)
	try:
		Chismero.objects.get(username=following, seguidores=user_actual)
	except Chismero.DoesNotExist:
		if user_actual.username != user_id:
			nativo=Chismero.objects.get(username=following)
			nativo.seguidores.add(user_actual)
			nativo.save()
			return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/')
		
	return HttpResponseRedirect('/')
@login_required(login_url='/gestionchismes/logueo/')
def buscar(request):
	query=request.GET.get('q', '')
	try:
		Chismero.objects.get(username=query)
	except Chismero.DoesNotExist:
		return HttpResponseRedirect('/')
	buscado=Chismero.objects.get(username=query)
	siguiendo=Chismero.objects.filter(seguidores=buscado)
	mensajes=Mensaje.objects.filter(username=buscado).order_by('-fecha_registro')
	return render(request, 'buscar.html',{'Mensajes':mensajes, "Usuarios":siguiendo, "Seguidme":buscado,})

@login_required(login_url='/gestionchismes/logueo/')
def dejar(request, user_id):
	siguiendo=Chismero.objects.get(username=user_id)
	tu=Chismero.objects.get(username=request.user.username)
	siguiendo.seguidores.remove(tu)
	siguiendo.save()
	return HttpResponseRedirect('/gestionchismes/cuenta')

@login_required(login_url='/gestionchismes/logueo/')
def eliminarchisme(request, mens_id):
	tu=Chismero.objects.get(username=request.user.username)
	mensajes=Mensaje.objects.filter(username=tu, mensaje_id=mens_id)
	mensajes.delete()
	return HttpResponseRedirect('/gestionchismes/cuenta')

def cuenta(request):
	p=Chismero.objects.get(username=request.user.username)
	usuarios=Chismero.objects.filter(seguidores=p)
	mensajes=Mensaje.objects.filter(username=p).order_by('-fecha_registro')
	return render(request, 'cuenta.html', {'Mensajes':mensajes, 'Usuarios':usuarios, 'Seguidme':p,})

@login_required(login_url='/gestionchismes/logueo/')
def fav(request, user_id, mens_id):
	mensajes=Mensaje.objects.get(mensaje_id=mens_id)
	retuiteado=Chismero.objects.get(username=user_id)
	pulsa_favorito=Chismero.objects.get(username=request.user.username)
	try:
		Favorito.objects.get(mensaje_id=mensajes, relacion_favoritos=pulsa_favorito)
	except Favorito.DoesNotExist:
		try:
			Favorito.objects.get(mensaje_id=mensajes)
		except Favorito.DoesNotExist:
			encontrar_original=Mensaje.objects.filter(texto=mensajes.texto).exclude(username=user_id)
			original=Mensaje.objects.get(mensaje_id=encontrar_original)
			try:
				Favorito.objects.get(mensaje_id=original, relacion_favoritos=pulsa_favorito)
			except Favorito.DoesNotExist:
				agrega_favorito=Favorito.objects.get(mensaje_id=original)
				agrega_favorito.relacion_favoritos.add(pulsa_favorito)
				agrega_favorito.save();
				original.num_favorito +=1
				original.save()
				mensajes.num_favorito +=1
				mensajes.save()
				return HttpResponseRedirect('/')
			elimina_favorito=Favorito.objects.get(mensaje_id=original)
			elimina_favorito.relacion_favoritos.remove(pulsa_favorito)
			elimina_favorito.save()
			original.num_favorito -=1
			original.save()
			mensajes.num_favorito -=1
			mensajes.save()
			return HttpResponseRedirect('/')	
		agrega_favorito=Favorito.objects.get(mensaje_id=mensajes)
		agrega_favorito.relacion_favoritos.add(pulsa_favorito)
		agrega_favorito.save();
		mensajes.num_favorito +=1
		mensajes.save()
		
		return HttpResponseRedirect('/')
	elimina_favorito=Favorito.objects.get(mensaje_id=mensajes)
	elimina_favorito.relacion_favoritos.remove(pulsa_favorito)
	elimina_favorito.save()
	mensajes.num_favorito -=1
	mensajes.save()
	return HttpResponseRedirect('/')


@login_required(login_url='/gestionchismes/logueo/')
def retuit(request, user_id, mens_id):
	mensajes=Mensaje.objects.get(mensaje_id=mens_id)
	retuiteado=Chismero.objects.get(username=user_id)
	pulsa_retweet=Chismero.objects.get(username=request.user.username)
	try:
		Retweet.objects.get(mensaje_id=mensajes, relacion_retweet=pulsa_retweet)
	except Retweet.DoesNotExist:
		try:
			Retweet.objects.get(mensaje_id=mensajes)
		except Retweet.DoesNotExist:
			encontrar_original=Mensaje.objects.filter(texto=mensajes.texto).exclude(username=user_id)
			original=Mensaje.objects.get(mensaje_id=encontrar_original)
			try:
				Retweet.objects.get(mensaje_id=original, relacion_retweet=pulsa_retweet)
			except Retweet.DoesNotExist:
				agrega_retweet=Retweet.objects.get(mensaje_id=original)
				agrega_retweet.relacion_retweet.add(pulsa_retweet)
				agrega_retweet.save();
				original.num_retweet +=1
				original.save()
				mensajes.num_retweet +=1
				mensajes.save()
				Mensaje.objects.create(texto=original.texto, username=pulsa_retweet)
				creado=Mensaje.objects.get(texto=original.texto, username=pulsa_retweet)
				creado.num_retweet=original.num_retweet
				creado.num_favorito=original.num_favorito
				creado.save()
				return HttpResponseRedirect('/')
			elimina_retweet=Retweet.objects.get(mensaje_id=original)
			elimina_retweet.relacion_retweet.remove(pulsa_retweet)
			elimina_retweet.save()
			original.num_retweet -=1
			original.save()
			mensajes.num_retweet -=1
			mensajes.save()
			eliminame=Mensaje.objects.get(texto=original.texto, username=pulsa_retweet)
			eliminame.delete()
			return HttpResponseRedirect('/')	
		agrega_retweet=Retweet.objects.get(mensaje_id=mensajes)
		agrega_retweet.relacion_retweet.add(pulsa_retweet)
		agrega_retweet.save();
		mensajes.num_retweet +=1
		mensajes.save()
		Mensaje.objects.create(texto=mensajes.texto, username=pulsa_retweet)
		creado=Mensaje.objects.get(texto=mensajes.texto, username=pulsa_retweet)
		creado.num_retweet=mensajes.num_retweet
		creado.num_favorito=mensajes.num_favorito
		creado.save()
		return HttpResponseRedirect('/')
	elimina_retweet=Retweet.objects.get(mensaje_id=mensajes)
	elimina_retweet.relacion_retweet.remove(pulsa_retweet)
	elimina_retweet.save()
	mensajes.num_retweet -=1
	mensajes.save()
	eliminame=Mensaje.objects.get(texto=mensajes.texto, username=pulsa_retweet)
	eliminame.delete()
	return HttpResponseRedirect('/')

@login_required(login_url='/gestionchismes/logueo/')
def pulsan_favorito(request, mens_id):
	mensaje=Mensaje.objects.get(mensaje_id=mens_id)
	try:
		Favorito.objects.get(mensaje_id=mens_id)
	except Favorito.DoesNotExist:
		mensaje22=Mensaje.objects.filter(texto=mensaje.texto).exclude(mensaje_id=mensaje.mensaje_id)
		mensaje2=Mensaje.objects.get(mensaje_id=mensaje22)
		fav=Favorito.objects.get(mensaje_id=mensaje2.mensaje_id)
		pulsan_favorito=fav.relacion_favoritos.all()
		return render(request, 'favorito.html', {'Mensaje':mensaje2, 'Pulsan_favorito':pulsan_favorito,})
	fav=Favorito.objects.get(mensaje_id=mens_id)
	pulsan_favorito=fav.relacion_favoritos.all()
	return render(request, 'favorito.html', {'Mensaje':mensaje, 'Pulsan_favorito':pulsan_favorito,})
@login_required(login_url='/gestionchismes/logueo/')
def pulsan_retweet(request, mens_id):
	mensaje=Mensaje.objects.get(mensaje_id=mens_id)
	try:
		Retweet.objects.get(mensaje_id=mens_id)
	except Retweet.DoesNotExist:
		mensaje22=Mensaje.objects.filter(texto=mensaje.texto).exclude(mensaje_id=mensaje.mensaje_id)
		mensaje2=Mensaje.objects.get(mensaje_id=mensaje22)
		ret=Retweet.objects.get(mensaje_id=mensaje2.mensaje_id)
		pulsan_retweet=ret.relacion_retweet.all()
		return render(request, 'retweet.html', {'Mensaje':mensaje2, 'Pulsan':pulsan_retweet,})
	ret=Retweet.objects.get(mensaje_id=mens_id)
	pulsan_retweet=ret.relacion_retweet.all()
	return render(request, 'retweet.html', {'Mensaje':mensaje, 'Pulsan':pulsan_retweet,})

@login_required(login_url='/gestionchismes/logueo/')
def crearchisme(request):
	if request.method == 'POST':
		form=ChismenewForm(data=request.POST)
		if form.is_valid(): 
			p=Chismero.objects.get(username=request.user.username)
			Mensaje.objects.create(texto=form.cleaned_data['texto'], username=p)
			nuevo=Mensaje.objects.get(texto=form.cleaned_data['texto'], username=p)
			Favorito.objects.create(mensaje_id=nuevo)
			Retweet.objects.create(mensaje_id=nuevo)
			return HttpResponseRedirect('/')
	else:
		form=ChismenewForm()
        
	return render(request, 'newchisme.html', {'form':form,})

@login_required(login_url='/gestionchismes/logueo/')
def dardebaja(request, user_id):
	usuario=Chismero.objects.get(username=user_id)
	usuario.delete()
	return HttpResponseRedirect('/gestionchismes/logueo/')

def logueo(request):
	if request.method == 'POST':
		form=AuthenticationForm(data=request.POST)
		if form.is_valid(): 
			login(request, form.get_user())
			return HttpResponseRedirect('/')
	else:
		form=AuthenticationForm()
        
	return render(request, 'login.html', {'form':form,})


def logoff(request):
    logout(request)
    return redirect('/')

def create(request):
	if request.method=='POST':
		form=UserCreationForm(data=request.POST)
		if form.is_valid():
			if form.clean_username() and form.clean():
				form.save()

				return redirect('/')
			else:
				
				return HttpResponse('no ha sido posible crearlo')
	else:
		form=UserCreationForm()
		
	return render(request, 'crear.html', {'form':form,})
