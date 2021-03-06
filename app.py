from flask import Flask, render_template, request
import pandas as pd 
from filter import filtered_hostel_df

app = Flask(__name__)

hostels = pd.read_json('all_hostels_coords_pop_density.json').reset_index(drop=True)
#hostels['rating'] = hostels['rating'] * hostels['n_reviews'] / (hostels['n_reviews']+3)

#hostels = hostels[hostels['lat'].isnull() == False]

@app.route('/', methods=['POST','GET'])
def index():
    
    if request.method == 'POST':
        print(request.args)
        return render_template('index.html', hostels = filtered_hostel_df(hostels,request.args))
    else:
        print(request.args)
        return render_template('index.html', hostels = filtered_hostel_df(hostels,request.args))

@app.route('/json', methods=['GET'])
def json():
    print(filtered_hostel_df(hostels,request.args))
    return filtered_hostel_df(hostels,request.args).to_json(orient='index')

if __name__ == "__main__":
    app.run(debug=True)