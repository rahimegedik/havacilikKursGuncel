import requests

# Infobip API anahtarınızı buraya girin
infobip_api_key = '06463fcd7a4fe673ce3178b05c5b7ca5-4d7fcd36-6d95-4350-9f59-af4bfa4fa30d'

def send_sms(receiver_number, message):
    url = 'https://dmv2qg.api.infobip.com'
    headers = {
        'Authorization': f'App {infobip_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'from': 'SENDER_NAME',
        'to': receiver_number,
        'text': message
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

if __name__ == '__main__':
    receiver_number = '905061058792'  # Alıcı telefon numarası
    message = 'Merhaba, bu bir test mesajıdır.'  # Göndermek istediğiniz mesaj
    result = send_sms(receiver_number, message)
    print(result)
