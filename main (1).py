import discord
import subprocess

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.content.startswith('/ping'):
        args = message.content.split()
        if len(args) < 2:
            await message.channel.send('Error: No IP specified')
            return
        computer = args[1]
        port = None
        if len(args) > 2:
            try:
                port = int(args[2])
            except ValueError:
                await message.channel.send('Error: Invalid port number')
                return
        if port is None:
            try:
                result = subprocess.run(['ping', '-c', '1', computer], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    await message.channel.send('Server is up! :ok_hand:')
                else:
                    await message.channel.send('Server is down! :fire:')
            except Exception as e:
                await message.channel.send('Error: {}'.format(e))
        else:
            try:
                result = subprocess.run(['nc', '-z', computer, str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    await message.channel.send('Port is open')
                else:
                    await message.channel.send('Port is closed')
            except Exception as e:
                await message.channel.send('Error: {}'.format(e))
    elif message.content == '/help':
        await message.channel.send('To use this bot, type `/ping [IP] [Port]` to ping an IP and port.')


def run_discord_bot():

    @client.event
    async def on_ready():
        print(f'{client.user} is running')

    client.run('TOKEN')

if __name__ == '__main__':
    run_discord_bot()
