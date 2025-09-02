from instagram_bot import InstagramBot

bot = InstagramBot()
results = bot.process_comments()

print("Processed Comments:\n")
for item in results:
    print(item)
