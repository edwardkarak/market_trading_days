from flask import Flask, request
from datetime import datetime
import time
import pandas_market_calendars as mcal

app = Flask(__name__)

# @app.route('/trading_days')
def list_trading_days():
	# start_date, end_date: UNIX timestamps (time ignored)
	# Now start_date_str, end_date_str are yyyy-mm-dd formatted strings

	DATE_FMT = "%Y-%m-%d"

	start_date_str = request.args.get('start_date') or '1900-01-01'
	end_date_str = request.args.get('end_date') or datetime.fromtimestamp(time.time()).strftime(DATE_FMT)

	start_date_obj = time.strptime(start_date_str, DATE_FMT)
	end_date_obj = time.strptime(end_date_str, DATE_FMT)

	if start_date_obj > end_date_obj:
		return {"trading_days": [], "error": "start_date > end_date"}
	

	# if int(start_date) > int(end_date):
	# 	return {"trading_days": [], "error": "start_date > end_date"}

	# start_date_str = datetime.fromtimestamp(int(start_date)).strftime("%Y-%m-%d")
	# end_date_str = datetime.fromtimestamp(int(end_date)).strftime("%Y-%m-%d")

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

"""if __name__ == "__main__":
	# run with: python3 [name-of-this-file]
    app.run(host='139.144.237.124', port=5000)"""

