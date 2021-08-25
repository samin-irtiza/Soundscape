import discord
import os
from discord.ext import commands
from subprocess import Popen
import shlex

client=commands.Bot(command_prefix='%')
errcolor = discord.Colour.from_rgb(251,0,0)

for fName in os.listdir('./cogs'):
  if fName.endswith('.py'):
    client.load_extension(f"cogs.{fName[:-3]}")

def is_me(ctx):
  return client.is_owner(ctx.author)

@client.event
async def on_ready():
  custom=discord.ActivityType.listening
  await client.change_presence(status=discord.Status.online,activity=discord.Activity(type=custom,name="Wiretap"))
  print(f"{client.user} says Let's JAM!")
  return

# @client.event
# async def on_disconnect():
#   print("disconnected and reloaded")
#   for fName in os.listdir('./cogs'):
#     if fName.endswith('.py'):
#       client.unload_extension(f"cogs.{fName[:-3]}")
#       client.load_extension(f"cogs.{fName[:-3]}")
#   return

@client.command()
@commands.check(is_me)
async def load(ctx,extension):
  client.load_extension(f"cogs.{extension}")
  await ctx.send("Loaded Successfully")
  return
  
@client.command()
@commands.check(is_me)
async def unload(ctx,extension):
  client.unload_extension(f"cogs.{extension}")
  await ctx.send("Unloaded Successfully")

@client.command()
@commands.check(is_me)
async def reload(ctx,extension):
  client.unload_extension(f"cogs.{extension}")
  client.load_extension(f"cogs.{extension}")
  await ctx.send("Reloaded Successfully")

@client.command(name="clean",aliases=['cls'])
async def clean_(ctx,amount:str="10"):
  """Scans amount of lines entered and delete's only the bot's messages"""
  await ctx.channel.purge(limit=1)
  deleted=await ctx.channel.purge(limit=int(amount.strip()),check=lambda message: message.author == client.user,bulk=False)
  await ctx.send(embed=discord.Embed(description=f"Deleted last **{len(deleted)}** messages",color=errcolor),delete_after=5)
  return

@client.command(name="purge")
@commands.has_permissions(manage_messages=True)
@commands.bot_has_permissions(manage_messages=True)
async def purge_(ctx,user,amount:str="10"):
  await ctx.message.delete()
  user=user.translate({ord(i):None for i in '<@!>'})
  user= await client.fetch_user(int(user))
  deleted=await ctx.channel.purge(limit=int(amount.strip()),check=lambda message: message.author==user,bulk=True)
  await ctx.send(embed=discord.Embed.from_dict({
   'description': f"Deleted last **{len(deleted)}** messages from `{user}`",
   'color': errcolor.value
   }),delete_after=5)
  return
  
@purge_.error
async def purge_error(ctx,e):
  if isinstance(e,commands.errors.MissingPermissions) and issubclass(type(e),commands.CheckFailure):
    await ctx.send(embed=discord.Embed(title='',description="It seems you don't have the necessary permissions to use this command",color=errcolor))
  elif isinstance(e,discord.ext.commands.BotMissingPermissions):
    await ctx.send(embed=discord.Embed(title='',description="The bot might not have manage messages permission",color=errcolor))
  else:
    raise e
  return

@client.command(name='reboot')
@commands.check(is_me)
async def reboot_(ctx):
  command = shlex.split("busybox reboot")
  Popen(command)
  await ctx.send("Rebooting")
  return
token=os.environ['SCTOK']
app = client.run(token)