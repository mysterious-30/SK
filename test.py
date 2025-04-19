import os , re
import logging
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, MessageMediaWebPage

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('bot.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Global variables
api_id = "23915082"
api_hash = "a00045e3df8dd8b92f2699b6d6a14157"
authorized_users = ["1438010651","7435290339","6922149657","6677195452"]

is_fetching = False
target_channel = None
receiver_channel = None

# Channel options with names and IDs
TARGET_CHANNELS = {
    "A1": {"name": "𝗢𝗸𝗪𝗶𝗻 𝗥𝗶𝗰𝗵 𝘅 𝗣𝗿𝗲𝗱𝗶𝗰𝘁𝗶𝗼𝗻𝘀", "id": -1002197194162},
    "A2": {"name": "OᴋWɪɴ SᴜʀᴇSʜᴏᴛ", "id": -1002326633829},
    "A3": {"name": "[EARNING HUB]", "id": -1002225131515},
    "A4": {"name": "Testing Channel", "id": -1002292392756},
    "A5": {"name": "𝐎𝐤𝐰𝐢𝐧 [𝐎𝐟𝐟𝐢𝐜𝐢𝐚𝐥]", "id": -1002137722031},
}

RECEIVER_CHANNELS = {
    "B1": {"name": "OK WIN VIP", "id": -1002263563494},
    "B2": {"name": "Reciver Channel", "id": -1002460898166},
    "B3": {"name": "Aadhvan", "id": "@Aadhvan0890"},
	"B4": {"name": "Aarav", "id": "@Arav_3003"},
}

# Initialize Telegram client
client = TelegramClient('Vanshika', api_id, api_hash)

# Helper functions
def reformat_message(text: str) -> str:
    """Clean and reformat message text."""
    if not text:
        return ""
    text = re.sub(r'[*_]', '', text)
    text = re.sub(r'(https?://\S*okwin\S*)', 'https://okwinslots3.com/#/register?invitationCode=86118638894', text, flags=re.IGNORECASE)
    return re.sub(r'https?://(?!.*okwin)\S+', '', text)

async def send_response(event, message: str):
    """Send a formatted response."""
    await event.reply(f"```\n{message}\n```")

# Command handlers
async def handle_start(event):
    global is_fetching, target_channel, receiver_channel
    if is_fetching:
        await send_response(event, "🔁 Already fetching messages! Use 'STOP' to pause.")
        return

    # Check if setup is complete
    if not target_channel or not receiver_channel:
        await send_response(event, "❌ Setup incomplete! Use 'SETUP' to configure channels.")
        return

    is_fetching = True
    await send_response(event, "🚀 Started fetching messages.")

async def handle_stop(event):
    global is_fetching
    if not is_fetching:
        await send_response(event, "❌ Not currently fetching messages.")
        return
    is_fetching = False
    await send_response(event, "⏹️ Stopped fetching messages.")

async def handle_show(event):
    """Show the current target and receiver channels."""
    global target_channel, receiver_channel

    # Get the target channel name
    target_channel_name = None
    for key, value in TARGET_CHANNELS.items():
        if value["id"] == target_channel:
            target_channel_name = value["name"]
            break

    # Get the receiver channel name
    receiver_channel_name = None
    for key, value in RECEIVER_CHANNELS.items():
        if value["id"] == receiver_channel:
            receiver_channel_name = value["name"]
            break

    # Prepare the response message
    response_message = (
        f"Target Channel: {target_channel_name if target_channel_name else 'Not set'}\n"
        f"Receiver Channel: {receiver_channel_name if receiver_channel_name else 'Not set'}"
    )

    # Send the response
    await send_response(event, response_message)

async def handle_setup(event):
    """Handle the SETUP command."""
    menu_message = (
        "Please select an option:\n\n"
        "**Target Channels:**\n"
        "A1. 𝗢𝗸𝗪𝗶𝗻 𝗥𝗶𝗰𝗵 𝘅 𝗣𝗿𝗲𝗱𝗶𝗰𝘁𝗶𝗼𝗻𝘀\n"
        "A2. OᴋWɪɴ SᴜʀᴇSʜᴏᴛ\n"
        "A3. [EARNING HUB]\n"
        "A4. Testing Channel\n"
        "A5. 𝐎𝐤𝐰𝐢𝐧 [𝐎𝐟𝐟𝐢𝐜𝐢𝐚𝐥]\n\n"
        "**Receiver Channels:**\n"
        "B1. OK WIN VIP\n"
        "B2. Reciver Channel"
    )
    await send_response(event, menu_message)

async def handle_channel_selection(event, option: str):
    """Handle target or receiver channel selection."""
    global target_channel, receiver_channel
    option = option.upper()
    if option in TARGET_CHANNELS:
        target_channel = TARGET_CHANNELS[option]["id"]
        await send_response(event, f"✅ Target channel set to: {TARGET_CHANNELS[option]['name']}")
    elif option in RECEIVER_CHANNELS:
        receiver_channel = RECEIVER_CHANNELS[option]["id"]
        await send_response(event, f"✅ Receiver channel set to: {RECEIVER_CHANNELS[option]['name']}")
    else:
        await send_response(event, "❌ Invalid option. Use 'A1', 'B1', etc.")

# Event handlers
@client.on(events.NewMessage(func=lambda e: e.is_private))
async def handle_private_message(event):
    """Handle commands from private messages with auth check"""
    sender = await event.get_sender()
    command = event.text.strip().upper()

    # Only process recognized commands
    if command in {"START", "STOP", "SETUP", "SHOW", "HELP"}:
        # Authorization check only for commands
        if str(sender.id) not in authorized_users and sender.username not in authorized_users:
            logger.warning(f"Unauthorized command attempt from {sender.id}")
            await send_response(event, "⛔ Unauthorized access. You don't have permission to use commands.")
            return

        # Process authorized commands
        if command == "START":
            await handle_start(event)
        elif command == "STOP":
            await handle_stop(event)
        elif command == "SETUP":
            await handle_setup(event)
        elif command == "SHOW":
            await handle_show(event)
        elif command == "HELP":
            await send_response(event, "Commands:\nSTART - Start forwarding\nSTOP - Stop forwarding\nSETUP - Configure channels\nSHOW - Current configuration")

    # Ignore non-command messages completely
    elif command in TARGET_CHANNELS or command in RECEIVER_CHANNELS:
        # Handle channel selection commands
        if str(sender.id) not in authorized_users and sender.username not in authorized_users:
            logger.warning(f"Unauthorized channel selection attempt from {sender.id}")
            await send_response(event, "⛔ Unauthorized access. You don't have permission to configure channels.")
            return
        await handle_channel_selection(event, command)

@client.on(events.NewMessage())
async def handle_channel_message(event):
    """Fetch and forward messages from the target channel."""
    global is_fetching, target_channel, receiver_channel
    if not is_fetching or event.chat_id != target_channel:
        return

    try:
        if event.message.media:
            if isinstance(event.message.media, MessageMediaPhoto):
                await client.send_file(receiver_channel, file=event.message.media, caption=reformat_message(event.message.text))
            elif isinstance(event.message.media, MessageMediaDocument):
                await client.send_file(receiver_channel, file=event.message.media, caption=reformat_message(event.message.text), force_document=True)
            elif isinstance(event.message.media, MessageMediaWebPage):
                await client.send_message(receiver_channel, message=reformat_message(event.message.text), link_preview=True)
        else:
            await client.send_message(receiver_channel, message=reformat_message(event.message.text))

        logger.info(f"Forwarded message {event.message.id} from {target_channel} to {receiver_channel}")
    except Exception as e:
        logger.error(f"Error forwarding message: {str(e)}")

# Main function
async def main():
    await client.start()
    logger.info("🤖 Bot started successfully")
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())