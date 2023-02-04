from flask import Flask, request
from datetime import datetime, date
import time
import pandas_market_calendars as mcal

app = Flask(__name__)

DATE_FMT = "%Y-%m-%d"
DEFAULT_START_DATE = date(1817, 3, 7).strftime(DATE_FMT)

def list_trading_days():
	start_date_str = request.args.get('start_date') or DEFAULT_START_DATE
	end_date_str = request.args.get('end_date') or datetime.fromtimestamp(time.time()).strftime(DATE_FMT)

	start_date_obj = time.strptime(start_date_str, DATE_FMT)
	end_date_obj = time.strptime(end_date_str, DATE_FMT)

	if start_date_obj > end_date_obj:
		return {"trading_days": [], "error": "start_date > end_date"}

	dates = mcal.get_calendar("NYSE").valid_days(start_date=start_date_str,
											end_date=end_date_str)
	response = []
	for x in dates:
		response.append(x.to_pydatetime().strftime(DATE_FMT))

	return {"trading_days": response}

@app.route('/trading_days', methods=['GET'])
def trading_days():
	if request.method == 'GET':
		return list_trading_days()
