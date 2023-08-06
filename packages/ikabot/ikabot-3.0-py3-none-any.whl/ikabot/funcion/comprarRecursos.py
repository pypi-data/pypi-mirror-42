#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
import json
import math
import re
from decimal import *
from ikabot.helpers.process import forkear
from ikabot.helpers.varios import addPuntos
from ikabot.helpers.gui import enter, banner
from ikabot.helpers.getJson import getCiudad
from ikabot.helpers.signals import setInfoSignal
from ikabot.helpers.planearViajes import esperarLlegada
from ikabot.helpers.pedirInfo import getIdsDeCiudades, read
from ikabot.config import *
from ikabot.helpers.botComm import *

def asignarRecursoBuscado(s, ciudad, recurso=None):
	if recurso is None:
		print('¿Qué tipo de recurso quiere comprar?')
		for indice, bien in enumerate(tipoDeBien):
			print('({:d}) {}'.format(indice+1, bien))
		recurso = read(min=1, max=5) - 1
		if recurso == 0:
			recurso = 'resource'
	data = {
	'cityId': ciudad['id'],
	'position': ciudad['pos'],
	'view': 'branchOffice',
	'activeTab': 'bargain',
	'type': 444,
	'searchResource': recurso,
	'range': ciudad['rango'],
	'backgroundView' : 'city',
	'currentCityId': ciudad['id'],
	'templateView': 'branchOffice',
	'currentTab': 'bargain',
	'actionRequest': s.token(),
	'ajax': 1
	}
	rta = s.post(payloadPost=data)
	return recurso

def getStoreHtml(s, ciudad):
	url = 'view=branchOffice&cityId={}&position={:d}&currentCityId={}&backgroundView=city&actionRequest={}&ajax=1'.format(ciudad['id'], ciudad['pos'], ciudad['id'], s.token())
	data = s.post(url)
	json_data = json.loads(data, strict=False)
	return json_data[1][1][1]

def obtenerOfertas(s, ciudad):
	html = getStoreHtml(s, ciudad)

	hits = re.findall(r'short_text80">(.*?) *<br/>\((.*?)\)\s *</td>\s *<td>(\d+)</td>\s *<td>(.*?)/td>\s *<td><img src="skin/resources/icon_(\w+)\.png[\s\S]*?white-space:nowrap;">(\d+)\s[\s\S]*?href="\?view=takeOffer&destinationCityId=(\d+)&oldView=branchOffice&activeTab=bargain&cityId=(\d+)&position=(\d+)&type=(\d+)&resource=(\w+)"', html)
	ofertas = []
	for hit in hits:
		oferta = {
		'ciudadDestino': hit[0],
		'jugadorAComprar' : hit[1],
		'bienesXminuto': int(hit[2]),
		'cantidadDisponible': int(hit[3].replace(',', '').replace('<', '')),
		'tipo': hit[4],
		'precio': int(hit[5]),
		'destinationCityId': hit[6],
		'cityId': hit[7],
		'position': hit[8],
		'type': hit[9],
		'resource': hit[10]
		}
		ofertas.append(oferta)
	return ofertas

def calcularCosto(ofertas, cantidadAComprar):
	costoTotal = 0
	for oferta in ofertas:
		if cantidadAComprar == 0:
			break
		comprar = oferta['cantidadDisponible'] if oferta['cantidadDisponible'] < cantidadAComprar else cantidadAComprar
		cantidadAComprar -= comprar
		costoTotal += comprar * oferta['precio']
	return costoTotal

def getOro(s, ciudad):
	url = 'view=finances&backgroundView=city&currentCityId={}&templateView=finances&actionRequest={}&ajax=1'.format(ciudad['id'], s.token())
	data = s.post(url)
	json_data = json.loads(data, strict=False)
	oro = json_data[0][1]['headerData']['gold']
	return int(oro.split('.')[0])


def comprarRecursos(s):
	banner()

	ids = getIdsDeCiudades(s)[0]
	ciudades_comerciales = []
	for idCiudad in ids:
		html = s.get(urlCiudad + idCiudad)
		ciudad = getCiudad(html)
		esComercial = False
		for pos, edificio in enumerate(ciudad['position']):
			if edificio['building'] == 'branchOffice':
				ciudad['pos'] = pos
				html = getStoreHtml(s, ciudad)
				rangos = re.findall(r'<option.*?>(\d+)</option>', html)
				ciudad['rango'] = max(rangos)

				ciudades_comerciales.append(ciudad)
				break

	if len(ciudades_comerciales) == 0:
		print('No hay una Tienda contruida')
		enter()
		return

	ciudad = ciudades_comerciales[0] # por ahora solo uso la primera ciudad

	recurso = asignarRecursoBuscado(s, ciudad)
	banner()

	ofertas = obtenerOfertas(s, ciudad)

	if len(ofertas) == 0:
		print('No se encontraron ofertas.')
		return

	precio_total   = 0
	cantidad_total = 0
	for oferta in ofertas:
		cantidad = oferta['cantidadDisponible']
		unidad   = oferta['precio']
		costo    = cantidad * unidad
		print('cantidad :{}'.format(addPuntos(cantidad)))
		print('precio   :{:d}'.format(unidad))
		print('costo    :{}'.format(addPuntos(costo)))
		print('')
		precio_total += costo
		cantidad_total += cantidad
	print('Total disponible para comprar: {}, por {}\n'.format(addPuntos(cantidad_total), addPuntos(precio_total)))
	cantidadAComprar = read(msg='¿Cuánta cantidad comprar? ', min=0, max=cantidad_total)
	if cantidadAComprar == 0:
		return

	oro = getOro(s, ciudad)
	costoTotal = calcularCosto(ofertas, cantidadAComprar)

	print('\nOro actual : {}.\nCosto total: {}.\nOro final  : {}.'. format(addPuntos(oro), addPuntos(costoTotal), addPuntos(oro - costoTotal)))
	print('¿Proceder? [Y/n]')
	rta = read(values=['y', 'Y', 'n', 'N', ''])
	if rta.lower() == 'n':
		return

	print('Se comprará {}'.format(addPuntos(cantidadAComprar)))
	enter()

	forkear(s)
	if s.padre is True:
		return

	info = '\ninfo sobre el proceso\n'
	setInfoSignal(s, info)
	try:
		do_it(s, ciudad, ofertas, cantidadAComprar, recurso)
	except:
		msg = 'Error en:\n{}\nCausa:\n{}'.format(info, traceback.format_exc())
		sendToBot(msg)
	finally:
		s.logout()

def buy(s, ciudad, oferta, cantidad):
	barcos = int(math.ceil((Decimal(cantidad) / Decimal(500))))
	data = {
	'action': 'transportOperations',
	'function': 'buyGoodsAtAnotherBranchOffice',
	'cityId': oferta['cityId'],
	'destinationCityId': oferta['destinationCityId'],
	'oldView': 'branchOffice',
	'position': ciudad['pos'],
	'avatar2Name': oferta['jugadorAComprar'],
	'city2Name': oferta['ciudadDestino'],
	'type': 444,
	'activeTab': 'bargain',
	'transportDisplayPrice': 0,
	'premiumTransporter': 0,
	'tradegood3Price': oferta['precio'],
	'cargo_tradegood3': cantidad,
	'capacity': 5,
	'max_capacity': 5,
	'jetPropulsion': 0,
	'transporters': barcos,
	'backgroundView': 'city',
	'currentCityId': oferta['cityId'],
	'templateView': 'takeOffer',
	'currentTab': 'bargain',
	'actionRequest': s.token(),
	'ajax': 1
	}
	rta = s.post(payloadPost=data)

def do_it(s, ciudad, ofertas, cantidadAComprar, recurso):
	while cantidadAComprar > 0:
		barcosDisp = esperarLlegada(s)
		capacidad  = barcosDisp * 500
		aComprar = capacidad if capacidad < cantidadAComprar else cantidadAComprar

		for oferta in ofertas:
			if aComprar == 0:
				break
			if oferta['cantidadDisponible'] == 0:
				continue
			comprar = aComprar if oferta['cantidadDisponible'] > aComprar else oferta['cantidadDisponible']
			aComprar -= comprar
			cantidadAComprar -= comprar
			oferta['cantidadDisponible'] -= comprar
			buy(s, ciudad, oferta, comprar)
