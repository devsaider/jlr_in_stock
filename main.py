#encoding: utf-8
# Velar 249 hp
# https://jlr-connect.com/carstock/api/v1/queries/5c1c0857b3c77a025394c51f/result?per_page=100&page=0&sort=-state_active_at

# All RR sports 5c70033eb110ea009a156b84
import requests
import re

r = requests.get("https://jlr-connect.com/carstock/api/v1/queries/5c70033eb110ea009a156b84/result?per_page=100&page=0")

for vehicle in r.json():
	# for k in vehicle['optionsUpdate']:
	# 	if k['id'] != '025ln':
	# 		continue

	# 	print (vehicle['id'])
	# 070av = багажник
	# 025l* меридиан
	# 041c(x|z) крыша
	# 030nl затемнение наружных зеркал
	# 064q(c|h) - матричные фары
	# 017ta — пакет драйв
	required_options = ['070(ba|av)', '025l', '041c(x|z)', '(064qc|064qh)', '030nl'] #, '039ib']
	restricted_options = ['tou'] # 'tou' - ebony

	if vehicle['user_metadata']['quote_price'] >0:
		print ("AAAAAAAAAA", vehicle['user_metadata']['quote_price'], 'https://cars.landrover.ru/#/cars/' + vehicle['id'])

	options_to_print = []
	is_failed_restricted_check = False

	for option_group in vehicle['options']:
		for option in option_group['items']:
			for o in required_options:
				if option['id'].lower().startswith(o) or re.search(o, option['id'].lower()):
					required_options.remove(o)

			if option['id'].lower() in restricted_options:
				is_failed_restricted_check = True

			if not option['default']:
				if [option['id'], option['name']] not in options_to_print:
					options_to_print.append([option['id'], option['name']])					

			# if 'панор' in option['name']:
			# 	print (option['id'], option['name'])

	if len(required_options) > 0 or is_failed_restricted_check:
		continue

	print("=" * 80)
	print("%s - %dhp - %s - %s RUB - %s" % (vehicle['model'] + ' ' + vehicle['grade'], vehicle['engine_power'], vehicle['color']['name'], vehicle['price']['value'][0][0], vehicle['dealerName'])) # - vehicle['price']['discount'][0]
	print (vehicle['in_stock_days'], 'https://cars.landrover.ru/#/cars/' + vehicle['id'])
	print('\n'.join(' - '.join(x) for x in options_to_print))
	print ("=" * 80)

	#if vehicle['user_metadata']['hasPTS']:
	#	print (vehicle["dealer"]["title"])