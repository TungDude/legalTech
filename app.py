from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import numpy as np

app = Flask(__name__, template_folder="template")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/method1', methods=['POST'])
def method1():
    try:
        T = float(request.form['T'])
        t = float(request.form['t'])
        MAI = float(request.form['MAI'])

    except Exception as e:
        print(e)
        return redirect('/')

    result = T * t * MAI * 0.001

    return render_template('result.html', result=result)


@app.route('/method2', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return redirect('/')

    if (file.filename).split('.')[1] == 'csv':
        df = pd.read_csv(file)
        
        CF = 0.47
        R = 0.2

        C_aboveGround = {}
        C_belowGround = {}
        CTT_i = {}
        a_i = {}
        A_i = {}


        # Step 1
        def sbl(coeff, d, h, power):
            return coeff * ((d * d * h) ** power)

        for i in set(list(df['i'])):
            criteria = [i]

            mask = df['i'].isin(criteria)
            layer = df[mask]

            a_i[i] = sum(layer['a'])
            A_i[i] = sum(layer['A'])

            sigma_M = 0
            for k, j in layer.iterrows():
                if j['j'] == 'ปาล์ม':
                    sigma_M += 6.666 + (12.826 * (j['H'] ** 0.5) * np.log(j['H']))
                elif j['j'] == 'เถาวัลย์':
                    sigma_M += 0.8622 * (j['D'] ** 2.0210)
                elif j['j'] == 'พรรณไม้ชายเลน':
                    sigma_M += sbl(0.05466, j['D'], j['H'], 0.945) + sbl(0.01579, j['D'], j['H'], 0.9124) + sbl(0.0678, j['D'], j['H'], 0.5806)
                elif j['j'] == 'ป่าดิบแล้ง':
                    sigma_M += sbl(0.0509, j['D'], j['H'], 0.919) + sbl(0.00893, j['D'], j['H'], 0.977) + sbl(0.0140, j['D'], j['H'], 0.669)
            
            C_aboveGround[i] = sigma_M * CF * 44 / 12

        # Step 2
        for key, value in C_aboveGround.items():
            C_belowGround[key] = value * R

        # Step 3
        for i in set(list(df['i'])):
            CTT_i[i] = (C_aboveGround[i] + C_belowGround[i]) * (A_i[i] / a_i[i])
        
        # Result
        result = sum(CTT_i.values())

        return render_template('result.html', result=result)

    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)