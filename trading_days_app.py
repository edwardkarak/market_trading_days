from flask import Flask, request
from datetime import datetime
import time
import pandas_market_calendars as mcal

app = Flask(__name__)

# @app.route('/trading_days')
def list_trading_days():
	# start_date, end_date: UNIX timestamps (time ignored)

	start_date = request.args.get('start_date') or '0'
	end_date = request.args.get('end_date') or str(int(time.time()))

	if int(start_date) > int(end_date):
		return {"trading_days": [], "error": "start_date > end_date"}

	start_date_str = datetime.fromtimestamp(int(start_date)).strftime("%Y-%m-%d")
	end_date_str = datetime.fromtimestamp(int(end_date)).strftime("%Y-%m-%d")

	dates = mcal.get_calendar("NYSE").valid_days(start_date=start_date_str,
											end_date=end_date_str)
	response = []
	for x in dates:
		response.append(x.to_pydatetime().strftime("%Y-%m-%d"))

	return {"trading_days": response}

@app.route('/trading_days', methods=['GET'])
def trading_days():
	if request.method == 'GET':
		return list_trading_days()

