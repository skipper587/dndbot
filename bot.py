# -*- coding: utf-8 -*-
import discord

from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get

import asyncio
import os
import time

import math

import random

##--------------------Global Variables--------------------##

DNDBot = discord.Client()  # Initialize Client
dndbot = commands.Bot(command_prefix="-")  # Initialize client bot
dndbot.remove_command("help")

versionnumber = "Beta 0.11"

##--------------------Global Functions--------------------##



##----------------------Bot Functions---------------------##

@dndbot.event
async def on_ready():
        # This will be called when the bot connects to the server.
        print("DND Bot is ready.")

@dndbot.event
async def on_member_join(member):
        bot = dndbot.get_user(710630587366375446)
        message_channel = dndbot.get_channel(710611293484220498)
        
        embed=discord.Embed(color=0x00c600)
        embed.add_field(name="//Send Greeting", value="Hello %s, and welcome to the Giant's Ring. I am the local AI. For more information on how I can help you, send me a DM with ?help." % member.mention, inline=False)
        
        await message_channel.send(embed=embed)
        
## Kill Command
@dndbot.command(name='quit')
async def botquit(ctx):
        user = ctx.message.author
        if user.top_role.name == "DM":
                embed=discord.Embed(color=0x00c600)
                embed.add_field(name="//Credentials Verified", value="Shutting down.", inline=True)

                await ctx.send(embed=embed)
                
                await dndbot.close()
                await DNDBot.close()
                quit()
        else:
                embed=discord.Embed(color=0xaa0000)
                embed.add_field(name="//Invalid Credentials", value="Failure, you lack the authorization to execute this subroutine!", inline=True)

                await ctx.send(embed=embed)

## Version
@dndbot.command(name='version',aliases=['v'])
async def version(ctx):
        displayversion = ["Version: ", versionnumber]

        embed=discord.Embed(color=0x00c600)
        embed.add_field(name="//Local Version", value=''.join(displayversion), inline=True)

        await ctx.send(embed=embed)

## About
@dndbot.command(name='about')
async def about(ctx):
        bot = dndbot.get_user(710630587366375446)
        path = 'files/'
        numRecords = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])
        
        embed=discord.Embed(color=0x00c600)
        embed.add_field(name="//Send Greeting", value="Hello! I am the Archives AI, keeper of the history of the Giant's Ring.", inline=False)
        embed.add_field(name="//State Directive", value="I exist to help preserve the history of the Giant's Ring for those who seek it. As you search records, you will find that any __underlined__ keyword can be searched in the Archives, if you have the clearance. Simply query me with ?info `query`\n \n The Archives currently contain " + str(numRecords) + " accessible records.", inline=False)

        await ctx.send(embed=embed)

## Stats
@dndbot.command(name="stats",aliases=['update','s'])
async def stats(ctx, *args):
        bot = dndbot.get_user(710630587366375446)
                
        if not args:
                fileName = "stats/sessions.txt"

                fr = open(fileName, 'r')
                sessions = fr.read()
                fr.close()

                fileName = "stats/combat.txt"

                fr = open(fileName, 'r')
                combat = fr.read()
                fr.close()

                fileName = "stats/world.txt"

                fr = open(fileName, 'r')
                world = fr.read()
                fr.close()

                embed=discord.Embed(color=0x00c600)
                embed.add_field(name="//Sessions", value=sessions, inline=True)
                embed.add_field(name="//Combat", value=combat, inline=True)
                embed.add_field(name="//World", value=world, inline=True)

                await ctx.send(embed=embed)

        if args:
                if len(args) == 3 and ctx.message.author.top_role.name == "DM":
                        file = ''.join(args[0])
                        line = int(''.join(args[1]))
                        value = ''.join(args[2])

                        fileName = "stats/" + file + ".txt"

                        fr = open(fileName, 'r')
                        data = fr.readlines()
                        fr.close()
                        
                        data[line - 1] = value + "\n"

                        fr = open(fileName, 'w')
                        fr.writelines(data)

                        embed=discord.Embed(color=0x00c600)
                        embed.add_field(name="//Send Confirmation", value="Success, updated campaign stats.", inline=True)

                        await ctx.send(embed=embed)

                elif len(args) < 3:
                        embed=discord.Embed(color=0xaa0000)
                        embed.add_field(name="//Send Confirmation", value="Failure, missing parameters!", inline=True)

                        await ctx.send(embed=embed)
                else:
                        embed=discord.Embed(color=0xaa0000)
                        embed.add_field(name="//Send Confirmation", value="Failure, unexpected parameters!", inline=True)

                        await ctx.send(embed=embed)

## Dice roller (since Bogue doesn't like the other one)
@dndbot.event
async def on_message(message):
        rolls = []
        i = 0
        total = 0
        modifier = ''

        if message.content[0:2] == '-r':

                try:
                        export = message.content[2:]
                        numbers = export.split('d')
                        numbers2 = numbers[1].split(' ')
                        
                        roll = int(numbers[0])
                        dice = int(numbers2[0])
                        
                        if len(numbers2) > 1:
                                modifier = numbers2[1]

                        if int(numbers[0]) > 24:
                                embed=discord.Embed(color=0xaa0000)
                                embed.add_field(name="//Subroutine Error", value="Cannot roll more than 24 dice at a time.", inline=True)

                                await message.channel.send(embed=embed)
                        else:
                                print("Rolling " + numbers[0] + " d" + numbers2[0]+ " for " + message.author.name + ".")
                                embed=discord.Embed(title="Results of " + numbers[0] + " d" + ''.join(numbers2) + " for " + message.author.name + ".", color=0x00c600)
                                embed.set_author(name=message.author.name,icon_url=message.author.avatar_url)
                                while i < roll:
                                        rolls.append(random.randint(1, dice))
                                        total = total + int(rolls[i])
                                        embed.add_field(name="//Roll #" + str(i+1), value=rolls[i], inline=True)
                                        i += 1
                                if modifier:
                                        if modifier[0] == "-":
                                                total = total - int(modifier[1:])
                                        if modifier[0] == "+":
                                                total = total + int(modifier[1:])
                                        embed.add_field(name="//Modifier", value=modifier, inline=False)
                                embed.set_footer(text="Total: " + str(total))

                                await message.channel.send(embed=embed)
                except:
                        embed=discord.Embed(color=0xaa0000)
                        embed.add_field(name="//Subroutine Error", value="Invalid input. Please check your input and try again.", inline=True)

                        await message.channel.send(embed=embed)
        await dndbot.process_commands(message)
                

## Info Command (Primary Functionality)
@dndbot.command(name='info',aliases=['i'])
async def info(ctx, query, *subrecord):
        bot = dndbot.get_user(710630587366375446)
    
        if subrecord:
                subrecord = ''.join(subrecord)
                query = query + " " + subrecord

        fileName = "files/" + query + ".txt"
        
        if os.path.exists(fileName):
                modified = time.ctime(os.path.getmtime(fileName))
                
                fr = open(fileName, 'r')
                
                name = str(fr.readline())
                name = name.strip("['']")
                name = name.rstrip()
                
                fileContents = fr.read()

                fr.close()

                if ctx.author.dm_channel is None:
                        await ctx.author.create_dm()
                
                try:
                        if len(fileContents) > 1024:
                                numOut = len(fileContents) / 1024
                                i = 0
                                index1 = 0
                                index2 = 1024
                                newContents = []

                                while i < math.ceil(numOut):
                                        newContents.append(fileContents[index1:index2])
                                        index1 = index1 + 1024
                                        index2 = index2 + 1024
                                        
                                        if not (i + 1) > 1:     
                                                embed=discord.Embed(title=name, color=0x00c600)
                                                embed.set_author(name=bot.name,icon_url=bot.avatar_url)
                                                embed.add_field(name="Known Info:", value=newContents[i], inline=True)
                                                embed.set_footer(text="Last Updated: " + modified + " | Part 1 of " + str(math.ceil(numOut)))
                                
                                                await ctx.author.send(embed=embed)
                                        else:
                                                embed=discord.Embed(color=0x00c600)
                                                embed.add_field(name="Continued:", value=newContents[i], inline=True)
                                                embed.set_footer(text="Last Updated: " + modified + " | Part " + str(i + 1) + " of " + str(math.ceil(numOut)))
                                
                                                await ctx.author.send(embed=embed)

                                        i += 1
                        else:
                                embed=discord.Embed(title=name, color=0x00c600)
                                embed.set_author(name=bot.name,icon_url=bot.avatar_url)
                                embed.add_field(name="Known Info:", value=fileContents, inline=True)
                                embed.set_footer(text="Last Updated: " + modified)

                                await ctx.author.send(embed=embed)
                        
                        print("Sent " + ctx.author.name + " the contents of the " + query + " record.")
                        embed=discord.Embed(color=0x00c600)
                        embed.add_field(name="//Retrieve Record", value="Success, retrieving known information about your query.", inline=True)

                        await ctx.send(embed=embed)
                except discord.Forbidden:
                        embed=discord.Embed(color=0xaa0000)
                        embed.add_field(name="//Subroutine Error", value="Failure, I cannot send you the retrieved record. Please activate DMs.", inline=True)

                        await ctx.send(embed=embed)
                        print("Caught exception, failed to send the contents of the record to " + ctx.author.name + ".")
        else:
                embed=discord.Embed(color=0xaa0000)
                embed.add_field(name="//Invalid Credentials", value="Failure, your party does not have access to that information yet!", inline=True)

                await ctx.send(embed=embed)

## Error handling for -info
@info.error
async def info_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
                embed=discord.Embed(color=0xaa0000)
                embed.add_field(name="//Subroutine Error", value="Failure, missing required argument.", inline=True)

                await ctx.send(embed=embed)
                print("Caught exception, couldn't find a query in " + ctx.author.name + "'s execution.")


## Help Command
@dndbot.command(name='help',aliases=['h'])
async def help(ctx, *command):
        if not command:
                embed=discord.Embed(title="Available Commands", color=0x00c600)
                embed.add_field(name="-info", value="Returns information on a specified record.", inline=False)
                embed.add_field(name="-version", value="Shows the current version of the bot.", inline=False)
                embed.set_footer(text="Use ?help and a command name for more information on a specific command.")
                
                await ctx.send(embed=embed)

        if command:
                commandName = ''.join(command)
                if commandName == "info":
                        embed=discord.Embed(title="-info - Basic query command, returns a record.", color=0x00c600)
                        embed.add_field(name="Syntax", value="-info `query` `subrecord`", inline=False)
                        embed.add_field(name="Notes", value="`query` must be \"surrounded by double quotations\" if it consists of multiple words.\n eg. -info \"query name\"\n \n Subrecords only exist if specified in a main record file.", inline=False)
                        
                        await ctx.send(embed=embed)
                elif commandName == "r":
                        embed=discord.Embed(title="-r - Dice roll command.", color=0x00c600)
                        embed.add_field(name="Syntax", value="-r`#`d`#` `+/-#`", inline=False)
                        embed.add_field(name="Example", value="-r2d20 +5", inline=False)
                        
                        await ctx.send(embed=embed)
                else:
                        embed=discord.Embed(color=0xaa0000)
                        embed.add_field(name="//Exception", value="Failure, no help log exists for that subroutine.", inline=True)

                        await ctx.send(embed=embed)

# Replace token with your bot's token
dndbot.run("Private Key")
