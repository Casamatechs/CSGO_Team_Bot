#!usr/bin/env python

"""
	This is a bot that helps to create and organize teams of CSGO in telegram.
	The bot make it easier to people to get ready and wait for the others while
	letting them know that you're ready and waiting.
"""

import telebot
import token.py

bot = telebot.TeleBot(TOKEN, threaded=False)
bot.skip_pending = True

team = 0
ppl_ready = ['Empty','Empty','Empty','Empty','Empty']
ppl_ready_id = ['Empty','Empty','Empty','Empty','Empty']
ver = 0.3

@bot.message_handler(commands=['welcome'])
def send_welcome(message):
	bot.reply_to(message, 'Hello, this is the CSGO Team Bot')

@bot.message_handler(commands=['ready'])
def ready_status(message):
	global team
	if message.from_user.id in ppl_ready_id:
		bot.reply_to(message, 'You can\'t be ready twice')
	else:
		team += 1
		if team == 1:
			bot.reply_to(message, 'You are ready\n' + str(team) + ' person ready.')
			ppl_ready[ppl_ready.index('Empty')]=message.from_user.username
			ppl_ready_id[ppl_ready_id.index('Empty')]=message.from_user.id
		elif team == 5:
			bot.reply_to(message, 'You are ready\n' + 'The team is full')
			ppl_ready[ppl_ready.index('Empty')]=message.from_user.username
			ppl_ready_id[ppl_ready_id.index('Empty')]=message.from_user.id
		elif team > 5:
			bot.reply_to(message, 'The team is already full\n' + 'You\'re not in')
			team = 5
		else:
			bot.reply_to(message, 'You are ready\n' + str(team) + ' people ready')
			ppl_ready[ppl_ready.index('Empty')]=message.from_user.username
			ppl_ready_id[ppl_ready_id.index('Empty')]=message.from_user.id

@bot.message_handler(commands=['notready'])
def notready_status(message):
	global team
	if message.from_user.id in ppl_ready_id:
		team -= 1
		ppl_ready[ppl_ready.index(message.from_user.username)]='Empty'
		if team == 1:
			bot.reply_to(message, 'You aren\'t ready anymore\n' + str(team) + ' person ready.')
		elif team <= 0:
			team = 0
			bot.reply_to(message, 'You aren\'t ready anymore\n' + str(team) + ' people ready')
		else:
			bot.reply_to(message, 'You aren\'t ready anymore\n' + str(team) + ' people ready')
	else:
		if team == 1:
			bot.reply_to(message, 'You weren\'t ready\n' + str(team) + ' person ready')
		else:
			bot.reply_to(message, 'You weren\'t ready\n' + str(team) + ' people ready')

@bot.message_handler(commands=['status'])
def team_status(message):
	global team
	if team==1:
		bot.reply_to(message, str(team) +' person is ready.')
	elif team >= 5:
		bot.reply_to(message, 'The team is full')
		team = 5
	else:
		bot.reply_to(message, str(team) + ' people ready')

@bot.message_handler(commands=['reset'])
def reset_team(message):
	global team
	global ppl_ready
	team = 0
	ppl_ready = ['Empty','Empty','Empty','Empty','Empty']
	ppl_ready_id = ['Empty','Empty','Empty','Empty','Empty']
	bot.reply_to(message, 'Team reset')

@bot.message_handler(commands=['ver'])
def show_ver(message):
	global ver
	bot.reply_to(message, str(ver))

@bot.message_handler(commands=['list'])
def show_list(message):
	bot.reply_to(message, ppl_ready[0]+'\n'+ppl_ready[1]+'\n'+ppl_ready[2]+'\n'+ppl_ready[3]+'\n'+ppl_ready[4])
	print ppl_ready

@bot.message_handler(commands=['idlist'])
def show_list(message):
	print ppl_ready_id

bot.polling()