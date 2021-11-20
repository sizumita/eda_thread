from typing import Optional
import discord
import os
import json
import io
client = discord.Client()

with open("channels.json") as f:
    channels = json.load(f)


@client.event
async def on_ready():
    for channel_id, data in channels.items():
        channel: Optional[discord.TextChannel] = client.get_channel(int(channel_id))
        if channel is None:
            print(f"channel {channel_id} is not found. continue...")
            continue
        webhook = await channel.create_webhook(name="Edaさん")
        for pair in data:
            thread_id = pair[0]
            base_id = pair[1]
            thread = channel.get_thread(int(thread_id))
            if thread is None:
                print(f"thread {thread_id} is not found. continue...")
                continue
            base_channel: Optional[discord.TextChannel] = client.get_channel(int(base_id))
            if base_channel is None:
                print(f"base channel {base_id} is not found. continue...")
            async for msg in base_channel.history(limit=None, oldest_first=True):
                await webhook.send(
                    content=msg.content + f"\n\n`{msg.created_at.strftime('%Y/%m/%d %H:%M:%S')}`",
                    username=msg.author.name,
                    avatar_url=msg.author.avatar.url,
                    files=[discord.File(io.BytesIO(await x.read()), x.filename, spoiler=x.is_spoiler()) for x in msg.attachments],
                    embeds=msg.embeds,
                    allowed_mentions=discord.AllowedMentions.none(),
                    thread=thread,
                )

client.run(os.environ["DISCORD_BOT_TOKEN"])
