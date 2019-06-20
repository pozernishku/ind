# ind
Some test task from Upwork.

Parameters:
Date range, format DD/MM/YYYY

Defaults if arguments are not set:
start_date = 01/01/2010
end_date = date.today()


How to run:
scrapy crawl ind_sp -s LOG_FILE=prices.log -t csv -o - > prices.csv
    OR
scrapy crawl ind_sp -a start_date=02/05/2012 -a end_date=04/05/2012 -s LOG_FILE=prices.log -t csv -o - > prices.csv