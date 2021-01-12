import mysql.connector
from discord.ext import commands
import random
import discord
from decouple import config


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=config('mydbpassword'),
    database="userlevels",
    auth_plugin="mysql_native_password"

)
print(mydb)
print('Database Connected')

def generateXP():
    return random.randint(1, 100)

class xp(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        elif message.content.startswith('!'):
            pass
        elif message.content.lower() == '!ugg':
            pass
        else:
            xp = generateXP()
            print(message.author.name+' will receive '+str(xp)+'xp')

            cursor = mydb.cursor()
            cursor.execute('SELECT user_xp FROM users WHERE client_id = ' + str(message.author.id))
            result = cursor.fetchall()
            if(len(result) == 0):
                print('User is not in db... add them')
                cursor.execute('INSERT INTO users VALUES(' + str(message.author.id) + ',' + str(xp) + ', 1' + ',' + "'" + str(message.author.name) + "'" + ')')
                mydb.commit()
                print('Inserted...')

            else:
                newXP = result[0][0] + xp
                print('New xp ' + str(newXP))
                cursor.execute('UPDATE users SET user_xp = ' + str(newXP) + ' WHERE client_id = ' + str(message.author.id))
                mydb.commit()
                print('Updated...')

    @commands.command(name='balance', help='Returns your balance')
    async def balance(self, ctx):
        cursor = mydb.cursor(buffered=True)

        cursor.execute('SELECT user_xp FROM users WHERE client_id = ' + str(ctx.author.id))

        result = cursor.fetchall()
        mydb.commit()


        if (len(result) > 0):
            currentXP = result[0][0]
            mydb.commit()



            print(f'{ctx.author.name} has $' + str(currentXP) + '')

            await ctx.send(f'{ctx.author.name} has **$' + str(currentXP) + '**')

        else:
            mydb.commit()
            await ctx.send(f'Adding New Account {ctx.author.name} to the database...')

    @commands.command(name='betcoin', help='!betcoin <xp-value> <heads/tails>')
    async def betcoin(self, ctx, betamount, value):
        cursor = mydb.cursor(buffered=True)
        cursor.execute('SELECT user_xp FROM users WHERE client_id = ' + str(ctx.author.id))
        result = cursor.fetchall()
        mydb.commit()

        bank = int(result[0][0])
        print(bank)

        if int(betamount) <= bank:
            choices = ['heads', 'tails']
            coinflip = random.choice(choices)
            if coinflip == value:
                bank += int(betamount)

                cursor.execute(f'UPDATE users SET user_xp ={bank} WHERE client_id ={str(ctx.author.id)}')
                mydb.commit()
                await ctx.send(f'Congrats, you won {int(betamount)}! Your balance is now {bank}.')
            else:
                bank += -(int(betamount))

                cursor.execute(f'UPDATE users SET user_xp ={bank} WHERE client_id ={str(ctx.author.id)}')
                mydb.commit()
                await ctx.send(f'Boohoo, you lost {int(betamount)}. Your balance is now {bank}.')

        elif int(betamount) > bank:

            await ctx.send('Sorry, you don\'t have enough xp...')









def setup(bot):
    bot.add_cog(xp(bot))