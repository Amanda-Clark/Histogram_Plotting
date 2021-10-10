import pandas as pd
import matplotlib
import base64

from io import BytesIO
from matplotlib.figure import Figure
from flask import Flask, request, json
from flask import render_template

pd.plotting.register_matplotlib_converters()
app = Flask(__name__)

data_set = pd.DataFrame()


@app.route('/')
def index():
    global data_set
    data_set = read_data()
    categories = data_set['OffenseCategory'].unique()
    crime_cats = list(categories)
    list_of_crimes = {}
    for i in range(0, len(crime_cats)):
        list_of_crimes[crime_cats[i]] = crime_cats[i]
    return render_template("select.html", data=list_of_crimes)


def read_data():
    global data_set
    data_set = pd.read_csv("CrimeData-2020.csv")
    data_set['OccurTime'] = data_set['OccurTime'].apply(str)
    data_set['OccurTime'] = data_set['OccurTime'].apply(lambda x: x.zfill(4))
    data_set['CrimeDate'] = data_set.OccurDate + ' ' + data_set.OccurTime
    data_set['CrimeDate'] = pd.to_datetime(data_set['CrimeDate'])
    cols = list(data_set)
    data_set = data_set.loc[:, cols]
    data_set.set_index('CrimeDate', inplace=True)
    return data_set


@app.route("/get_type", methods=["POST"])
def get_type():
    global data_set
    cat_type = request.form.get("data1")
    types = data_set[data_set['OffenseCategory'] == cat_type]
    name_types = types['OffenseType'].unique()
    name_types = list(name_types)
    return json.dumps({'catnames': name_types})


@app.route("/get_graph", methods=['POST'])
def get_graph():
    global data_set
    selectedcat = request.form.get("data1")
    crime_dates = data_set.loc[data_set['OffenseType'] == selectedcat]
    crime_dates.drop(crime_dates.columns.difference(['OccurDate']), 1, inplace=True)
    crime_dates['OccurDate'] = pd.to_datetime(crime_dates['OccurDate'])
    crime_dates = crime_dates.set_index('OccurDate', drop=False)
    crime_dates = crime_dates[crime_dates['OccurDate'] > '12-31-2019']
    df = crime_dates.groupby(pd.Grouper(freq='MS')).count()
    df.index.name = 'Month'
    fig = Figure()
    ax = fig.subplots()
    ax.bar(df.index, df['OccurDate'], width=20)
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%b'))
    ax.set_title("Portland " + selectedcat + " in 2020 by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of " + selectedcat)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    img = f"<img src='data:image/png;base64,{data}'/>"
    return json.dumps({'image': img})


if __name__ == '__main__':
    app.run(debug=True, port=9000, host='0.0.0.0')
