import discord
from settings import *
from bot_code import *
from discord.ext import commands

# Variabel intents menyimpan hak istimewa bot
intents = discord.Intents.default() 
# Mengaktifkan hak istimewa message-reading
intents.message_content = True
# Membuat bot di variabel klien dan mentransfernya hak istimewa
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Kita telah masuk sebagai {bot.user}')
    channel = bot.get_channel(channel_general)
    await channel.send("Hello world!")

@bot.command()
async def check_rice(ctx):
    if ctx.message.attachments:
        await ctx.send("Saving image(s)...")
        for num, attachment in enumerate(ctx.message.attachments):
            await attachment.save('images/' + attachment.filename)
            await ctx.send(f'Scanning image {num+1}...')
            
            # use machine learning
            result = detect_rice('images/' + attachment.filename)
            # Cek untuk keyakinan prediksi sama atau lebih dari 0.6
            if result[1] >= 0.6:
                await ctx.send("Hasil analisis gambar: " + result[0])

            # berikan saran berdasarkan hasil prediksi. jangan kaya gini kalo beneran
            # jika hasilnya "nasi basi"
                if "basi" in result[0]:
                    await ctx.send("""Sepertinya nasi ini sudah tidak layak untuk dimakan.
Sebaiknya dibuang, atau diolah menjadi produk baru.""")
                # jika hasilnya "nasi enak"
                elif "enak" in result[0]:
                    await ctx.send("Nasi ini masih bisa dikonsumsi!")

            # Jika keyakinan prediksi < 0.6
            else:
                await ctx.send("Tidak bisa dipastikan")    
    
    elif not ctx.message.attachments:
        await ctx.send("Image not detected! Try again.")

bot.run(TOKEN)