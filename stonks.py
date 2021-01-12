import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import aiohttp


class stonks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('stonks.py injected')

    @commands.command(name='stock', help='!stock <ticker> (Returns Stock Data)')
    async def stock(self, ctx, ticker):
        #Grabs URL
        url = f'https://www.marketwatch.com/investing/stock/{ticker}'

        async with aiohttp.ClientSession(loop=self.bot.loop) as session:
            async with session.get(url) as response:
                soups = await response.read()
        response = soups
        soup = BeautifulSoup(response, 'html.parser')

        companyName = soup.title.text

        currentPrice = soup.find('div', class_="intraday__data").h3.text.strip()[1:]

        grabpriceChange = soup.find('div', class_='intraday__data')

        priceChange = grabpriceChange.find('bg-quote', class_='intraday__change positive')

        if priceChange is not None:
            grabpriceChange = grabpriceChange.find('bg-quote', class_='intraday__change positive')
            priceChange = grabpriceChange.find('span', class_='change--point--q').text
            percentChange = grabpriceChange.find('span', class_='change--percent--q').text
            change = 'positive'
            changeEmoji = '796806879878709311'
            # print(percentChange)
            # print(f'{priceChange}({percentChange}) {change}')
            priceChange = f'+{priceChange}'

        elif grabpriceChange.find('bg-quote', class_='intraday__change negative') is not None:
            priceChange = grabpriceChange.find('bg-quote', class_='intraday__change negative')
            priceChange = grabpriceChange.find('span', class_='change--point--q').text
            percentChange = grabpriceChange.find('span', class_='change--percent--q').text
            change = 'negative'
            changeEmoji = '796806879879757844'
            # print(f'{priceChange}({percentChange}) {change}' )
            priceChange = f'{priceChange}'

        else:
            priceChange = grabpriceChange.find('bg-quote', class_='intraday__change neutral')
            priceChange = grabpriceChange.find('span', class_='change--point--q').text
            percentChange = grabpriceChange.find('span', class_='change--percent--q').text
            change = 'neutral'
            changeEmoji = '796807665422303272'
            # print(f'{priceChange}({percentChange}) {change}')

        getTimestamp = soup.find('div', class_='intraday__timestamp')
        Timestamp = getTimestamp.find('span', class_='timestamp__time').text
        getPreviousclose = soup.find('div', class_='intraday__close')
        Previousclose = getPreviousclose.find('td', class_='table__cell u-semi').text

        ###############################embed##########################################

        embed = discord.Embed(
            title=f'<:icon:{changeEmoji}> ${currentPrice[1:]}',
            description = f'''{priceChange} ({percentChange})
            
                            __**Previous Close:**__ {Previousclose}
                            \u200b
    
                            ''',

            color = discord.Colour.green()
        )

        embed.set_author(name=f'{companyName[:-13]}', icon_url='')

        embed.set_thumbnail(url='https://mw4.wsj.net/mw5/content/images/favicons/apple-touch-icon.png')

        embed.set_footer(text=f"Powered by MarketWatch, {Timestamp}")

        await ctx.send(embed=embed)

    @commands.command(name='stockdata', help='!stockdata <ticker> (Returns in depth stock data)')
    async def stockdata(self, ctx, ticker):
        # Grabs URL
        url = f'https://www.marketwatch.com/investing/stock/{ticker}'

        async with aiohttp.ClientSession(loop=self.bot.loop) as session:
            async with session.get(url) as response:
                soups = await response.read()
        response = soups
        soup = BeautifulSoup(response, 'html.parser')

        companyName = soup.title.text

        currentPrice = soup.find('div', class_="intraday__data").h3.text.strip()[1:]

        grabpriceChange = soup.find('div', class_='intraday__data')

        priceChange = grabpriceChange.find('bg-quote', class_='intraday__change positive')

        if priceChange is not None:
            grabpriceChange = grabpriceChange.find('bg-quote', class_='intraday__change positive')
            priceChange = grabpriceChange.find('span', class_='change--point--q').text
            percentChange = grabpriceChange.find('span', class_='change--percent--q').text
            change = 'positive'
            changeEmoji = '796806879878709311'
            # print(percentChange)
            # print(f'{priceChange}({percentChange}) {change}')
            priceChange = f'+{priceChange}'



        elif grabpriceChange.find('bg-quote', class_='intraday__change negative') is not None:
            priceChange = grabpriceChange.find('bg-quote', class_='intraday__change negative')
            priceChange = grabpriceChange.find('span', class_='change--point--q').text
            percentChange = grabpriceChange.find('span', class_='change--percent--q').text
            change = 'negative'
            changeEmoji = '796806879879757844'
            # print(f'{priceChange}({percentChange}) {change}' )
            priceChange = f'{priceChange}'

        else:
            priceChange = grabpriceChange.find('bg-quote', class_='intraday__change neutral')
            priceChange = grabpriceChange.find('span', class_='change--point--q').text
            percentChange = grabpriceChange.find('span', class_='change--percent--q').text
            change = 'neutral'
            changeEmoji = '796807665422303272'
            # print(f'{priceChange}({percentChange}) {change}')

        getTimestamp = soup.find('div', class_='intraday__timestamp')
        Timestamp = getTimestamp.find('span', class_='timestamp__time').text

        getPreviousclose = soup.find('div', class_='intraday__close')
        Previousclose = getPreviousclose.find('td', class_='table__cell u-semi').text

        def getNumber(str):
            str = str.encode()

        keyData = []
        for item in soup.findAll('li', class_='kv__item'):
            keyData.append(item.get_text(strip=True))

        openData = (keyData[0])[4:]
        # print(openData)

        dayRangeData = (keyData[1])[9:]
        # print(dayRangeData)

        fiftytwoweekRange = (keyData[2])[13:]
        # print(fiftytwoweekRange)

        marketCap = (keyData[3])[10:]
        # print(marketCap)

        sharesOutstanding = (keyData[4])[18:]
        # print(sharesOutstanding)

        publicFloat = (keyData[5])[12:]
        # print(publicFloat)

        beta = (keyData[6])[4:]
        # print(beta)

        revperEmployee = (keyData[7])[18:]
        # print(revperEmployee)

        ratioData = (keyData[8])[9:]
        # print(ratioData)

        EPSData = (keyData[9])[3:]
        # print(EPSData)

        yieldData = (keyData[10])[5:]
        # print(yieldData)

        dividend = (keyData[11])[8:]
        # print(dividend)

        exdividendDate = (keyData[12])[16:]
        # print(exdividendDate)

        shortInterest = (keyData[13])[14:-8]
        # print(shortInterest)
        shortInterestDate = (keyData[13])[-8:]
        # print(shortInterestDate)

        percFloatShorted = (keyData[14])[18:]
        # print(percFloatShorted)

        avgVolume = (keyData[15])[14:]
        # print(avgVolume)

        ###############################embed##########################################

        embed = discord.Embed(
            title=f'<:icon:{changeEmoji}> ${currentPrice[1:]}',
            description=f'''{priceChange} ({percentChange})

                                __**Previous Close:**__ {Previousclose}
                                \u200b

                                ''',

            color=discord.Colour.green()
        )

        embed.set_author(name=f'{companyName[:-13]}', icon_url='')

        embed.set_thumbnail(url='https://mw4.wsj.net/mw5/content/images/favicons/apple-touch-icon.png')

        # embed.add_field(name='Key Data',
        #                 value=f'''
        #                 {getkeyDataLists}
        #                         ''', inline=True)
        embed.add_field(name='__Key Data:__',
                        value=f'''
                                    \u200b
                                    **Open**
                                    {openData}
                                    **52 Week Range** 
                                    {fiftytwoweekRange}
                                    **Shares Outstanding**
                                    {sharesOutstanding}
                                    **Beta**
                                    {beta}
                                    **P/E Ratio**
                                    {ratioData}
                                    **Yield**
                                    {yieldData}
                                    **Ex-Dividend Date**
                                    {exdividendDate}
                                    **% of Float Shorted**
                                    {percFloatShorted}

                                    ''', inline=True)
        embed.add_field(name='\u200b',
                        value=f'''
                                    \u200b
                                    **Day Range** 
                                    {dayRangeData}
                                    **Market Cap**
                                    {marketCap}
                                    **Public Float**
                                    {publicFloat}
                                    **Rev. Per Employee**
                                    {revperEmployee}
                                    **EPS**
                                    {EPSData}
                                    **Dividend**
                                    {dividend}
                                    **Short Interest**
                                    {shortInterest} ({shortInterestDate})
                                    **Average Volume**
                                    {avgVolume}


                                    ''', inline=True)

        embed.set_footer(text=f"Powered by MarketWatch, {Timestamp}")

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(stonks(bot))