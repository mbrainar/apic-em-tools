from flask import Flask
from flask import render_template
from uniq.apis.nb.client_manager import NbClientManager

def login():
    apic = "sandboxapic.cisco.com"
    username = "devnetuser"
    password = "Cisco123!"

    try:
        client = NbClientManager(server=apic,
                                 username=username,
                                 password=password,
                                 connect=True)
        return client
    except:
        return None

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
    session = login()
    device_list = get_inventory(session)
    html = []
    for device in device_list.response:
        location = None
        if device.location:
            location = get_location(session, device.location).response.locationName
        html.append({
                     'hostname':device.hostname,
                     'platformId':device.platformId,
                     'serialNumber': device.serialNumber,
                     'location': location if location else "None"})
    return render_template('index.html', table=html, title="Network Device Inventory")


def get_inventory(session):
    return session.networkdevice.getAllNetworkDevice()

def get_location(session, id):
    return session.location.getLocationById(id=id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
