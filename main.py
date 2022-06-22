import os
import discord
import datetime
from discord.ext import commands
from replit import db
from machine_learning import run_ML
from keep_alive import keep_alive

model = run_ML()

intents = discord.Intents().all();
client = commands.Bot(intents=intents, command_prefix="$");
game = discord.Game(name="Cleaning Spams");

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.command()
async def setlog(ctx): 
	id = ctx.guild.id
	channel = ctx.channel.id
	db[id] = channel
	await ctx.channel.send('setlog successful')

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$setlog'):
		await client.process_commands(message)
		return
	
	inp = [message.content]
	prediction = model.predict(inp)

	if prediction == ['spam']:
		output_channel = ''
		# output_channel = message.channel

		db_keys = db.keys()
    
		if str(message.guild.id) in db_keys:
			output_channel = client.get_channel(db[str(message.guild.id)])
		else:
			output_channel = message.channel

		until = 10
		# ctx = message
		delete_status = True
    
		try:
			await message.delete()
		except:
			delete_status = False

		embed=discord.Embed(color=0xff0000)
		embed.timestamp = datetime.datetime.utcnow()
		if delete_status == False:
			embed.add_field(
				name=f'@{message.author.name} spam message detected in #{message.channel.name}',  
				value=f'cannot delete <@{message.author.id}> spam message (⋟﹏⋞)')
		else:
			embed.add_field(
        name=f'@{message.author.name} spam deleted in #{message.channel.name} (>.<")', 
        value=f"{message.content}", inline=False)
		embed.add_field(name="Reason", value="Spam message", inline=False)
    
		await output_channel.send(embed=embed)

keep_alive()
client.run(os.environ['TOKEN'])
