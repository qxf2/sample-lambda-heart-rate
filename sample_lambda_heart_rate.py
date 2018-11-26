"""
This is a Flask application which calculates the target heart rate range based on the age of the user.
"""

from flask import Flask, jsonify, render_template, request
import json
import boto3
import logging
import conf.credentials as conf

# create lambda client
client = boto3.client('lambda',
                        region_name= conf.region,
                        aws_access_key_id=conf.aws_access_key_id,
                        aws_secret_access_key=conf.aws_secret_access_key)

app = Flask(__name__)
app.logger.setLevel(logging.ERROR)

@app.route("/", methods=['GET', 'POST'])
@app.route("/calculate_heartrate_range", methods=['GET', 'POST'])
def calculate_heartrate_range():
    "Endpoint for calculating the heart rate range"
    if request.method == 'GET':
        #return the form
        return render_template('sample_lambda.html')
    if request.method == 'POST':
        #return the range        
        age = int(request.form.get('age'))        
        payload = {"age":age} 
        #Invoke a lambda function which calculates the max heart rate and gives the target heart rate range              
        result = client.invoke(FunctionName=conf.lambda_function_name,
                    InvocationType='RequestResponse',                                      
                    Payload=json.dumps(payload))
        range = result['Payload'].read()      
        api_response = json.loads(range)               
        return jsonify(api_response)        

#---START OF SCRIPT
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6464, debug= True)