from requests import post, get
import json
import datetime

# send the data
# have a counter

def send_data(temp, j, url):
    #j = 0
    
    local_image_path = '../images/image_{}.jpg'.format(j)

    #latest_idx_from_server = int(get(url + "latest_id/").text) + 1
    timestamp = datetime.datetime.now()
    
    latest_idx_from_server = 99

    path = "img" + str(latest_idx_from_server) + ".jpg"
    label = None
    
    print("temp to send to server:", str(temp[0]))
    
    data = {'temp': str(temp[0]),
           'pressure': "300.2",
            'timestamp': str(timestamp),
            'filepath': path,
            'label': str(label)}
    print(local_image_path)

    

    f = {'file': (path, open(local_image_path, 'rb'))}

    answer1 = post(url + "save_picture/", files=f)
    answer2 = post(url + "save_data/", json=data)
    results = json.loads(answer2.text.replace("'",'"'))
    cal_perc = results['cal_perc']
    bites = results['bites']

    print(answer1.text)
    print(answer2.text)
    print("cal_perc:", cal_perc)
    
    return cal_perc, bites