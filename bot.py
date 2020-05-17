# -*- coding: utf-8 -*-
import discord

from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get

import asyncio
import os
import time

import math

##--------------------Global Variables--------------------##

DNDBot = discord.Client()  # Initialize Client
dndbot = commands.Bot(command_prefix="?")  # Initialize client bot
dndbot.remove_command("help")

versionnumber = "0.5"

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
        
        embed=discord.Embed(color=0xaa0000)
        embed.add_field(name="//Send Greeting", value="Hello **" + str(member.name) + "**, and welcome to the Giant's Ring. I am the local AI. For more information on how I can help you, send me a DM with ?help.", inline=False)
        
        await message_channel.send(embed=embed)
        
## Kill Command
@dndbot.command(name='quit')
async def botquit(ctx):
        user = ctx.message.author
        if user.top_role.name == "DM":
                await ctx.send("Shutting down.")
                await dndbot.close()
                await DNDBot.close()
                quit()

## Version
@dndbot.command(name='version')
async def version(ctx):
        displayversion = ["Version: ", versionnumber]
        await ctx.send(''.join(displayversion))

## About
@dndbot.command(name='about')
async def about(ctx):
        bot = dndbot.get_user(710630587366375446)
        path = 'files/'
        numRecords = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])
        
        embed=discord.Embed(color=0xaa0000)
        embed.set_author(name=bot.name,icon_url=bot.avatar_url)
        embed.add_field(name="//Send Greeting", value="Hello! I am the Archive AI, keeper of the history of the Giant's Ring.", inline=False)
        embed.add_field(name="//State Directive", value="I exist to help preserve the history of the Giant's Ring for those who seek it. As you search records, you will find that any __underlined__ keyword can be searched in the Archives, if you have the clearance. Simply query me with ?info `query`\n \n The Archives currently contain " + str(numRecords) + " accessible records.", inline=False)

        await ctx.send(embed=embed)

## Stats
@dndbot.command(name="stats",aliases=['update'])
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

                embed=discord.Embed(color=0xaa0000)
                embed.add_field(name="//Sessions", value=sessions, inline=True)
                embed.add_field(name="//Combat", value=combat, inline=True)
                embed.add_field(name="//World", value=world, inline=True)

                await ctx.send(embed=embed)

        if args:
                if len(args) == 3:
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
                        embed.add_field(name="//Send Confirmation", value="**Success**", inline=True)

                        await ctx.send(embed=embed)

                elif len(args) < 3:
                        embed=discord.Embed(color=0xaa0000)
                        embed.add_field(name="//Send Confirmation", value="**Failure, missing parameters!**", inline=True)

                        await ctx.send(embed=embed)
                else:
                        embed=discord.Embed(color=0xaa0000)
                        embed.add_field(name="//Send Confirmation", value="**Failure, unexpected parameters!**", inline=True)

                        await ctx.send(embed=embed)

## Info Command (Primary Functionality)
@dndbot.command(name='info')
async def info(ctx, query, *subrecord):
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

                await ctx.send("Retrieving known information about your query.")
                
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
                                        embed=discord.Embed(title=name, color=0xaa0000)
                                        embed.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
                                        embed.add_field(name="Known Info:", value=newContents[i], inline=True)
                                        embed.set_footer(text="Last Updated: " + modified + " | Part 1 of " + str(math.ceil(numOut)))
                        
                                        await ctx.author.send(embed=embed)
                                else:
                                        embed=discord.Embed(color=0xaa0000)
                                        embed.add_field(name="Continued:", value=newContents[i], inline=True)
                                        embed.set_footer(text="Last Updated: " + modified + " | Part " + str(i + 1) + " of " + str(math.ceil(numOut)))
                        
                                        await ctx.author.send(embed=embed)

                                i += 1
                else:
                        embed=discord.Embed(title=name, color=0xaa0000)
                        embed.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
                        embed.add_field(name="Known Info:", value=fileContents, inline=True)
                        embed.set_footer(text="Last Updated: " + modified)

                        await ctx.author.send(embed=embed)
                
                print("Sent " + ctx.author.name + " the contents of the " + query + ".txt file.")
        else:
                await ctx.send("Your party has not discovered any information about that yet!")

## Help Command
@dndbot.command(name='help')
async def help(ctx, *command):
        if not command:
                embed=discord.Embed(title="Available Commands", color=0xaa0000)
                embed.add_field(name="?info", value="Returns information on a specified record.", inline=False)
                embed.add_field(name="?version", value="Shows the current version of the bot.", inline=False)
                embed.set_footer(text="Use ?help and a command name for more information on a specific command.")
                
                await ctx.send(embed=embed)

        if command:
                commandName = ''.join(command)
                if commandName == "info":
                        embed=discord.Embed(title="?info", color=0xaa0000)
                        embed.add_field(name="Syntax", value="?info `query` `subrecord`", inline=False)
                        embed.add_field(name="Notes", value="`query` must be \"surrounded by double quotations\" if it consists of multiple words.\n eg. ?info \"query name\"\n \n Subrecords only exist if specified in a main record file.", inline=False)
                        
                        await ctx.send(embed=embed)
                else:
                        await ctx.send("No help log exists for the specified command.")

# Replace token with your bot's token
dndbot.run("Private Key")
