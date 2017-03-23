import datetime
import requests
import json
import pandas
from flask import Flask, render_template, request, redirect, current_app
from bokeh.charts import Line, show, output_file, save
from bokeh.models import Label
from bokeh.embed import components

app = Flask(__name__)

app.vars=''

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
	if request.method == 'GET':
  		return render_template('entry.html')
	else:
		app.vars=request.form['name']
		f=open('history.txt','a')
		f.write(app.vars)
		f.write("\n")
		f.close()
		return redirect('/trying')

@app.route('/trying',methods=['GET','POST'])
def trying():
	now=datetime.datetime.now().strftime("%Y%m%d")
	now_30=(datetime.datetime.now()-datetime.timedelta(days=30)).strftime("%Y%m%d")
	tick=app.vars
	stock_data = requests.get("https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte="+now_30+"&date.lt="+now+"&ticker="+tick+"&api_key=yvSB52TFjUsFTyZU-n--")
	unp_data=stock_data.json()["datatable"]["data"]
	unp_label=stock_data.json()["datatable"]["columns"]
	label=[]
	for entries in unp_label:
		label.append(str(entries["name"]))
	df=pandas.DataFrame(unp_data)
	df.columns=label
	close_mean="%.2f" %df[["close"]].mean()
	close_std="%.2f" %df[["close"]].std()
	captions="mean="+ close_mean +", std="+ close_std
	df2=df[["date","close"]]
	li=Line(df2,x="date",y="close",xlabel="date",ylabel="closing price",legend=False,title=tick+" stock chart from "+now_30+" to "+now)
	caption1=Label(x=400, y=100, x_units='screen', y_units='screen', text=captions, text_font_size='9pt', text_font_style="bold")
	li.add_layout(caption1)
	script, div = components(li)
	return render_template('trying.html', script=script, div=div)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=33507)
