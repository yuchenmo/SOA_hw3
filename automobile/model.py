import json
import requests

# Microsoft-styled WONDERFUL Document=)


def predict(inp):
    columns = {
        'make': 2,
        'body-style': 6,
        'wheel-base': 9,
        'engine-size': 14,
        'horsepower': 21,
        'peak-rpm': 22,
        'highway-mpg': 24
    }
    key_data = json.load(open("key/apikey.json", 'r'))
    workspace_id, service_id, api_key = key_data[
        'workspace_id'], key_data['service_id'], key_data['ml_api_key']
    url = 'https://ussouthcentral.services.azureml.net/workspaces/{}/services/{}/execute?api-version=2.0&details=true'.format(
        workspace_id, service_id)
    columnnames = ["symboling", "normalized-losses", "make", "fuel-type", "aspiration", "num-of-doors", "body-style",
                   "drive-wheels", "engine-location", "wheel-base", "length", "width", "height", "curb-weight",
                   "engine-type", "num-of-cylinders", "engine-size", "fuel-system", "bore", "stroke",
                   "compression-ratio", "horsepower", "peak-rpm", "city-mpg", "highway-mpg", "price"]
    values = []
    value_sample = ["0", "0", "value", "value", "value", "value", "value", "value", "value", "0", "0", "0", "0", "0",
                    "value", "value", "0", "value", "0", "0", "0", "0", "0", "0", "0", "0"]

    for item in inp:
        value_sample[columns[item]] = str(inp[item])

    values.append(value_sample)

    Inputs = {'input1': {"ColumnNames": columnnames, "Values": values}}

    body = {
        'Inputs': Inputs,
        'GlobalParameters': {}
    }

    body = json.dumps(body)
    headers = {'Content-Type': 'application/json',
               'Authorization': ('Bearer ' + api_key)}

    t = requests.post(url, data=body, headers=headers).json()
    ans = float(t['Results']['output1']['value']['Values'][0][-1])
    return ans


if __name__ == "__main__":
    input_sample = {
        'make': 'alfa-romero',
        'body-style': 'convertible',
        'wheel-base': 88.6,
        'engine-size': 130,
        'horsepower': 111,
        'peak-rpm': 5000,
        'highway-mpg': 27
    }
    print(predict(input_sample))
