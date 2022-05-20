import discord
from machine_learning import run_ML
from machine_learning import count_vect
# from datetime import datetime

print('starting the ML process...')
clf = run_ML()
# Machine Learning Result saved in clf
print('result saved, running discord now...')

class DiscordClient(discord.Client):
  # When the bot is ready to be used
  async def on_ready(self):
    print('Logged in as')
    print(self.user.name)
    print(self.user.id)
    print('------')
    
  # timeout function
  # coming soon
  
  # on bot receive message
  async def on_message(self, message):
    # trigger to message other than the bot
    if message.author.id == self.user.id:
      return
    
    inp = [message.content]
    X_test_tfidf = count_vect.transform(inp)
    prediction = clf.predict(X_test_tfidf)

    if prediction == ['spam']:
      # delete message
      try:
        await message.delete()
        await message.channel.send(f'delete <@{message.author.id}> spam message (>.<")')
      except:
        await message.channel.send(f'cannot delete <@{message.author.id}> spam message (⋟﹏⋞)')
        
      # timeout member

      # create log
      # z = bot.get_channel()
      # embed = discord.Embed(title = f"{message.author}'s Message was Deleted", description = f"Deleted Message: {message.content}\nAuthor: {message.author.mention}\nLocation: {message.channel.mention}", timestamp = datetime.now(), color = discord.Colour.red())
      # embed.set_author(name = message.author.name, icon_url = message.author.avatar)
      # await z.send(embed = embed)

      await message.channel.send(f'delete <@{message.author.id}> spam message (>.<"): {message.content}')
      
    else:
      await message.channel.send('your message is not a spam (>v<)b')