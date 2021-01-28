import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import aiohttp
import mysql.connector
from decouple import config
from dateutil import parser
from datetime import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=config('mydbpassword'),
    database="userlevels",
    auth_plugin="mysql_native_password"

)

async def getPrice(ticker):
    url = f'https://www.marketwatch.com/investing/stock/{ticker}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            soups = await response.read()
    response = soups
    soup = BeautifulSoup(response, 'html.parser')
    companyName = soup.title.text
    currentPrice = soup.find('div', class_="intraday__data").h3.text.strip()[2:]
    getTimestamp = soup.find('div', class_='intraday__timestamp')
    geTimestamp = getTimestamp.find('span', class_='timestamp__time').text
    Timestamp = geTimestamp[14:-3].strip()

    return float(currentPrice)
async def getDate(ticker):
    url = f'https://www.marketwatch.com/investing/stock/{ticker}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            soups = await response.read()
    response = soups
    soup = BeautifulSoup(response, 'html.parser')
    getTimestamp = soup.find('div', class_='intraday__timestamp')
    geTimestamp = getTimestamp.find('span', class_='timestamp__time').text
    Timestamp = geTimestamp[14:-3].strip()
    return Timestamp
    # Date = parser.parse(Timestamp)
    # return Date


async def addStockToPurchases(ctx, ticker, value, type):
    price = await getPrice(ticker)

    client_id = ctx.author.id
    cursor = mydb.cursor()
    cursor.execute(f'''INSERT INTO purchases (client_id, stock, price_of_stock, number_of_stock, transaction_type)
        VALUES ('{client_id}', '{ticker.upper()}', '{price}', '{value}', '{type}')
        ''')
    mydb.commit()



async def addPortfolio(ctx, ticker, value, price):
    client_id = ctx.author.id
    cursor = mydb.cursor()
    cursor.execute(f'''SELECT number_of_stock FROM portfolio WHERE client_id = '{client_id}' AND stock ='{ticker}'
                    ''')
    result = cursor.fetchall()
    mydb.commit()
    if (len(result) == 0):
        print('User is not in the portfolio db... inserting them')

        cursor.execute(f'''INSERT INTO portfolio (client_id, stock, number_of_stock, avg_price)
                    VALUES ('{client_id}', '{ticker.upper()}', '{value}', '{price}')
                    ''')
        mydb.commit()
        print(price)
        print('Inserted...')
    else:
        pass
        # stockCounter = result[0][0] + int(value)
        #
        # cursor.execute(f'''UPDATE portfolio SET number_of_stock = '{stockCounter}' WHERE client_id = '{client_id}' AND stock ='{ticker}'
        #                 ''')
        # print(f'{client_id} now owns {stockCounter} of {ticker.upper()}')

async def getBalance(ctx):
    client_id = ctx.author.id
    cursor = mydb.cursor()
    cursor.execute(f'''SELECT user_xp FROM users WHERE client_id = {client_id}''' )
    result = cursor.fetchall()
    mydb.commit()
    return(result[0][0])

async def updateAVG(ctx, stock, amount, price):

    client_id = ctx.author.id
    cursor = mydb.cursor()
    cursor.execute(f'''SELECT avg_price, number_of_stock FROM portfolio WHERE client_id = {client_id}''')
    result = cursor.fetchall()
    mydb.commit()
    # print(result)
    first_tuple_element = []
    for a_tuple in result:
        first_tuple_element = (float(a_tuple[0]))
    # print(first_tuple_element)

    for a_tuple in result:
        second_tuple_element = (int(a_tuple[1]))
    # print(second_tuple_element)

    total_amount = second_tuple_element+int(amount)
    # print(total_amount)
    total_cost = round((float(price)*int(amount)) + ((first_tuple_element)*(second_tuple_element)),2)
    # print(total_cost)
    avg_cost = round((total_cost/total_amount), 2)

    # print(avg_cost)

    return(avg_cost)

    # cursor = mydb.cursor()
    # cursor.execute(f'''UPDATE portfolio SET avg_price ={avg_cost} WHERE client_id ={client_id} AND stock ='{stock.upper()}'
    #                                 ''')
    # mydb.commit()


async def getInvested(ctx):
    client_id = ctx.author.id
    cursor = mydb.cursor()
    cursor.execute(f'''SELECT avg_price, number_of_stock FROM portfolio WHERE client_id = {client_id}''')
    result = cursor.fetchall()

    mydb.commit()

    first_tuple_elements = []
    for a_tuple in result:
        first_tuple_elements.append(float(a_tuple[0]))
    # print('.')
    # print(first_tuple_elements)

    second_tuple_elements = []
    for a_tuple in result:
        second_tuple_elements.append(a_tuple[1])
    # print(second_tuple_elements)
    total_cost = 0
    for num1, num2 in zip(first_tuple_elements, second_tuple_elements):
        total_cost += (num1*num2)

    # print(total_cost)
    return (total_cost)
async def iterate(ctx, list):
    for i in list:
        return i

async def getMarket(ctx):
    client_id = ctx.author.id
    cursor = mydb.cursor()
    cursor.execute(f'''SELECT stock, number_of_stock FROM portfolio WHERE client_id = {client_id}''')
    result = cursor.fetchall()

    mydb.commit()
    first_tuple_elements = []
    for a_tuple in result:
        first_tuple_elements.append(str(a_tuple[0]))
    # print('.')
    print(first_tuple_elements)

    second_tuple_elements = []
    for a_tuple in result:
        second_tuple_elements.append(a_tuple[1])
    print(second_tuple_elements)

    prices = []
    for i in first_tuple_elements:
        marketPrice = await getPrice(i)
        prices.append(marketPrice)
    print(prices)

    market_cost = 0
    for num1, num2 in zip(prices, second_tuple_elements):
        market_cost += (num1 * num2)

    print(market_cost)
    return (market_cost)

class trader(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('trader.py injected')


    @commands.command(name= 'buy', help='!buy <ticker> <amount>')
    async def buy(self, ctx, ticker, value, type='buy'):
        now = datetime.now()
        day = int(now.weekday())
        # print(day)
        # print(now)
        # print(now.hour)
        # print(now.minute)
        if int(now.hour) >= 9 and int(now.hour) <=16 and day < 5:
            print('ok')


            if int(value) > 0:
                price = await getPrice(ticker)
                client_id = ctx.author.id
                await ctx.send(f'{ticker.upper()} price is {price}')

                cursor = mydb.cursor()
                cursor.execute('SELECT user_xp FROM users WHERE client_id = ' + str(ctx.author.id))
                results = cursor.fetchall()
                mydb.commit()
                buyingPower = float(results[0][0])
                #print(buyingPower)

                numberofStock = float(value)
                #print(numberofStock)
                priceofStock = float((numberofStock*price))

                #print(priceofStock)


                if priceofStock <= buyingPower:

                    buyingPower += -priceofStock
                    #print(buyingPower)

                    cursor.execute(f'UPDATE users SET user_xp ={buyingPower} WHERE client_id ={str(ctx.author.id)}')
                    mydb.commit()

                    await addStockToPurchases(ctx, ticker, value, type)

                    await addPortfolio(ctx, ticker, 0, price)

                    avg_cost = await updateAVG(ctx, ticker, value, price)

                    # print(avg_cost)
                    cursor = mydb.cursor()
                    cursor.execute(
                        f'''UPDATE portfolio SET avg_price ={avg_cost} WHERE client_id ={client_id} AND stock ='{ticker.upper()}'
                                                        ''')
                    mydb.commit()

        ###################################################
                    cursor = mydb.cursor()
                    cursor.execute(
                        f'''SELECT number_of_stock FROM portfolio WHERE client_id = '{client_id}' AND stock ='{ticker}'
                                                ''')
                    results = cursor.fetchall()


                    stockCounter = results[0][0] + int(value)

                    mydb.commit()

                    cursor.execute(
                        f'''UPDATE portfolio SET number_of_stock = '{stockCounter}' WHERE client_id = '{client_id}' AND stock ='{ticker}'
                                            ''')
                    mydb.commit()


                    print(f'{client_id} now owns {stockCounter} of {ticker.upper()} at an average cost of ${avg_cost}')
        #####################################################
                    await ctx.send(f'''You bought **{numberofStock}** _{ticker.upper()}_ share(s) at a price of ${price} for a total of **${round(priceofStock, 2)}** ''')
                    await ctx.send(f'Your balance is now **${round(buyingPower, 2)}**.')



                    #########UPDATE PORTFOLIO TABLE TO ADD STOCK IF NOT THERE OR ADD NUMBER OF STOCK BOUGHT TO EXISTING VALUE##########
                    # cursor.execute(f'UPDATE users SET {ticker}')

                else:

                    await ctx.send(f'You don\'t have enough buying power to purchase {numberofStock} {ticker.upper()} share(s)')
            else:
                await ctx.send(f'YOU CAN\'T FOOL THE MASTER')

        else:
            await ctx.send(f'The Market is currently closed.')

    @commands.command(name='sell', help='!sell <ticker> <amount>')
    async def sell(self, ctx, ticker, value, type='sell'):
        price = await getPrice(ticker)
        client_id = ctx.author.id
        await ctx.send(f'{ticker.upper()} price is **${price}**')

        cursor = mydb.cursor()
        cursor.execute(
            f'''SELECT number_of_stock FROM portfolio WHERE client_id = '{client_id}' AND stock ='{ticker}'
                            ''')
        results = cursor.fetchall()
        mydb.commit()
        if (len(results) == 0):
            print('User is not in the portfolio db... ')
            await ctx.send(f'''You don't own any {ticker} stock''')
        # elif (results[0][0]==int(value)):
        #     cursor=mydb.cursor()
        #     cursor.execute(f'''DELETE FROM portfolio WHERE client_id = {client_id} AND stock = '{ticker}'
        #                 ''')
        #     await ctx.send(f'''You sold ''')
        elif (results[0][0]<int(value)):
            await ctx.send(f'''You cannot sell {value} stock, You only own {results[0][0]} of {ticker.upper()}''')
        else:
            if results[0][0] > 0:

                await addStockToPurchases(ctx, ticker, value, type)
                cursor = mydb.cursor()
                cursor.execute('SELECT user_xp FROM users WHERE client_id = ' + str(ctx.author.id))
                result = cursor.fetchall()
                mydb.commit()
                buyingPower = float(result[0][0])
                # print(buyingPower)
                numberofStock = float(value)
                # print(numberofStock)
                priceofStock = float((numberofStock * price))
                # print(priceofStock)

                buyingPower += priceofStock
                # print(buyingPower)

                if (results[0][0] == int(value)):
                    cursor.execute(f'UPDATE users SET user_xp ={buyingPower} WHERE client_id ={str(ctx.author.id)}')
                    mydb.commit()
                    cursor = mydb.cursor()
                    cursor.execute(f'''DELETE FROM portfolio WHERE client_id = {client_id} AND stock = '{ticker}'
                                                ''')
                    mydb.commit()
                    await ctx.send(f'You sold **{value}** _${ticker.upper()}_ share(s) for a total of **${price}**')
                    await ctx.send(f'Your balance is now ${round(buyingPower, 2)}')
                else:
                    cursor.execute(f'UPDATE users SET user_xp ={buyingPower} WHERE client_id ={str(ctx.author.id)}')
                    mydb.commit()

                    stockCounter = results[0][0] - int(value)
                    # print(stockCounter)
                    cursor.execute(f'''UPDATE portfolio SET number_of_stock = '{stockCounter}' WHERE client_id = '{client_id}' AND stock ='{ticker}'
                                            ''')
                    mydb.commit()



                    print(f'{client_id} now owns {stockCounter} of {ticker.upper()}')



                    await ctx.send(f'You sold **{value}** _${ticker.upper()}_ share(s) for a total of **${price}**')

                    await ctx.send(f'Your balance is now ${round(buyingPower, 2)}')


            else:
                await ctx.send(f'You currently have **0** shares of _{ticker.upper()}_ to sell :sob:')

    @commands.command(name='portfolio', help='Returns your stock portfolio')
    async def portfolio(self, ctx):
        client_id = ctx.author.id
        author = ctx.message.author
        pfp = author.avatar_url
        Timestamp = await getDate('tsla')
        cursor = mydb.cursor(buffered=True)
        cursor.execute(f'''SELECT stock, number_of_stock, avg_price FROM portfolio WHERE client_id = {client_id}
                                   ''')
        stock = cursor.fetchall()
        if (len(stock) == 0):
            await ctx.send(f'You currently do not own any stocks.')
        else:
            mydb.commit()

            #############Retrieves stock and amount from tuple############

            first_tuple_elements = []
            for a_tuple in stock:
                first_tuple_elements.append(a_tuple[0])

            # print(first_tuple_elements)

            second_tuple_elements = []
            for a_tuple in stock:
                second_tuple_elements.append(a_tuple[1])
            # print(second_tuple_elements)

            # print(len(first_tuple_elements))

            third_tuple_elements = []
            for a_tuple in stock:
                third_tuple_elements.append(float(a_tuple[2]))

            # print(third_tuple_elements)

            stock_string = ''
            for i in first_tuple_elements:
                stock_string += ('\n' + i)

            #######list of int to list of string#######
            second_tuple = [str(x) for x in second_tuple_elements]
            amount_string = ''
            for i in second_tuple:
                amount_string += ('\n' + i)


            third_tuple = [str(x) for x in third_tuple_elements]
            avg_string = ''
            for i in third_tuple:
                avg_string += ('\n$' + i)


            balance = await getBalance(ctx)

            invested = await getInvested(ctx)


            market = await getMarket(ctx)

            total_return = (market - invested)

            perctotreturn = ((total_return)/invested)*100

            embed = discord.Embed(
                title=f'''Balance = ${balance}''',
                color=discord.Colour.gold()
            )

            if len(stock) < 1:
                embed.add_field(name='__Stock__',
                                value=f'''
                                        None
                                        ''',
                                inline=True)
                embed.add_field(name='__Amount__',
                                value=f'''
                                        0
                                        ''',
                                inline=True)

                embed.add_field(name='__$__',
                                value=f'''
                                        0
                                        ''',
                                inline=True)
            else:
                embed.add_field(name='__Stocks__',
                                value=f'''{stock_string}''',
                                inline=True)

                embed.add_field(name='__Amount__',
                                value=f'''{amount_string}''',
                                inline=True)
                embed.add_field(name='__AVG__',
                                value=f'''{avg_string}''',
                                inline=True)

                embed.add_field(name='Total Invested',
                                value=f'''${round(invested, 2)}''',
                                inline=False)
                embed.add_field(name='Market Value',
                                value=f'''${(round(market, 2))}''',
                                inline=False)
                embed.add_field(name='Total Return',
                                value=f'''${round(total_return, 2)}      ({round(perctotreturn, 2)}%)''',
                                inline=False)





            embed.set_footer(text=f"Market Prices last updated {Timestamp}")

            embed.set_thumbnail(url=pfp)

            embed.set_author(name=f'''{ctx.author.name}'s Stonk Portfolio''', icon_url='https://cdn.iconscout.com/icon/free/png-512/apple-stock-493158.png')

            await ctx.send(embed=embed)





def setup(bot):
    bot.add_cog(trader(bot))