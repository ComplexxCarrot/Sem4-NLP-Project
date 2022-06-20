import os
import discord
import datetime
from discord.ext import commands
from replit import db
from machine_learning import run_ML
from machine_learning import count_vect
from keep_alive import keep_alive

clf = run_ML()

intents = discord.Intents().all();
client = commands.Bot(intents=intents, command_prefix="$");
#client.session = aiohttp.ClientSession()
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

# async def timeout_user(*, user_id: int, guild_id: int, until):
# 		headers = {"Authorization": f"Bot {client.http.token}"}
# 		url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
# 		timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=until)).isoformat()
# 		json = {'communication_disabled_until': timeout}
# 		async with client.session.patch(url, json=json, headers=headers) as session:
# 			if session.status in range(200, 299):
# 				return True
# 			return False

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$setlog'):
		await client.process_commands(message)
		return
	
	inp = [message.content]
	X_test_tfidf = count_vect.transform(inp)
	prediction = clf.predict(X_test_tfidf)

	if prediction == ['promo'] or prediction == ['penipuan']:
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

		embed=discord.Embed()
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

  #   handshake = await timeout_user(user_id=ctx.author.id, guild_id=ctx.guild.id, until=until)
		# if handshake:
		# 	return await ctx.send(f"Successfully timed out user for {until} minutes.")
		# else:
		# 	await ctx.channel.send(f"failed to timeout <@{ctx.author.id}>")

keep_alive()
client.run(os.environ['TOKEN'])
