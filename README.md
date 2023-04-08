# The-Py-Scraper-Telegram
Python Version Of The Scraper In Telegram
 <br>50 Stars For Token and Combo Scraping!

**Commands**
| command        | args           | output  |
| ------------- |:-------------:| -----:|
| /combos [keyword]      | [keyword], str | a txt file of the combos |
| /tokens [amount]     | [amount], int      |   a txt file of the tokens |
| /count | N/A      |    shows how many lines are in the db |


### Requirements

A Linux Cloud Server
Python3 and pip
 <br>Everything else from the-scraper

### Setup

* Download the files in the github and transfer them to your linux server
* Download the pip packages needed using this command,
```python
pip install telebot mysql.connector 
```
* cd into the directory where its located
* Edit the file
```
nano main.py
```
* Replace the bot_token, db_host, db_user, db_pass and db_name with your own
* Start the bot by running
```
python3 main.py
```
