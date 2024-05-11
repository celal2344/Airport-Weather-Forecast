import requests
import json
import tkintermapview
import tkinter as tk
#uygulamayı çalıştırmadan önce kütüphaneleri yüklemek için aşağıdaki komutu terminale giriniz
#python -m pip install tk tkintermapview requests 

#havaalanlarının verilerini api-ninjas sitesinin ücretsiz api'si ile alan fonksiyon
def getAirportCoords():
    offset = 0
    airportCoords = {}
    while True:#api aynı anda 30 havaalanı verisi çekebildiğinden loop ile 30'ar 30'ar tüm havaalanlarının verilerini çeken döngü
        data = json.loads(requests.get(
            f'https://api.api-ninjas.com/v1/airports?country=TR&offset={offset}',
            headers={'X-Api-Key': '/OrmH9FM+dvuTd9qP+yr+A==qfJI6uIccYQQ1WgJ'}
        ).text)
        if not data:
            break
        offset += 30
        for obj in data:#havaalanlarının koordinatları ve isimlerini tutan dictionary
            airportCoords[obj["name"]] = [float(obj["latitude"]), float(obj["longitude"])]
    return airportCoords
#hava durumu bilgisi için apiden veriyi alıp ekrana yazdıran fonksiyon
def showWeather(marker):
    coords = marker.data
    #havaalanlarının koordinat bilgisi api'ye gönderilip o konumun hava durumuna göre ekranda görünen textvariable güncellenir
    data = json.loads(requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={coords[1]}&lon={coords[2]}&appid={weatherAPIKey}').text)
    weatherInfoTxt.set(coords[0] + ": " + str(data["weather"][0]["description"] + " " + str(round((float(data["main"]["temp"]) - 273.15),1))) + "°C")
    
weatherAPIKey = "5d492bfba370a5156a3e821295f4d892"
#ekranı oluşturan variablelar
root = tk.Tk()
root.title('Türkiye')
root.geometry("900x700")

airportCoords = getAirportCoords()

label = tk.LabelFrame(root)
label.pack(pady=20)
#haritayı oluşturan variablelar
mapView = tkintermapview.TkinterMapView(label, width=800, height=600, corner_radius=0)
mapView.set_zoom(6)
mapView.set_position(39.9334, 34.8597) 

weatherInfoFrame = tk.Frame(root)
weatherInfoTxt = tk.StringVar()
weatherInfoFrame.pack(side=tk.BOTTOM)
weatherInfoLabel = tk.Label(weatherInfoFrame, textvariable=weatherInfoTxt, font=("Arial", 12))
weatherInfoLabel.pack()

#her havaalanı için bir marker oluşturulup içerisine havaalanının ismi ve koordinat bilgisi data olarak tutulur, marker a tıklanınca çalışacak fonksiyon 
#ise markerın command parametresinde tutulur bu fonksiyona parametre olarak markerın kendisi yollanır(bu tkintermapview kütüphanesinin kendi özelliği)
for airport in airportCoords:
    marker = mapView.set_marker(airportCoords[airport][0],airportCoords[airport][1],text=airport, 
                                   command=showWeather, data= [airport,airportCoords[airport][0],airportCoords[airport][1]])

mapView.pack()
root.mainloop()