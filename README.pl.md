Polski | [English]( .md)

![Status](https://img.shields.io/badge/Status-BETA-red?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.13-blue?style=for-the-badge)
![Licencja](https://img.shields.io/badge/Licencja-MIT-yellow?style=for-the-badge)

# CEngine Vehicles Generator (v0.1.0)

CEngine Vehicles Generator to generator plików `.prefab` dla silnika wyprodukowanego przez Techland (CEngine), bazujący na Pythonie, który jest w stanie generować pojazdy we wcześniej wspomnianych plikach `.prefab`. Narzędzie to jest przeznaczone do pracy z wersją silnika używaną do stworzenia *Dying Light 2*. Narzędzie to redukuje żmudną pracę nad rozkładaniem pojazdów na mapie społeczności, umożliwiając generowanie ich w wielu modelach (wciąż nie wszystkich), zmienianie tekstury danego pojazdu czy sposobu ich rozłożenia.

## Autorzy

- [@Paw3leQ](https://github.com/Paw3leQ-12)

## Funkcje

- Generowanie jedynie wybranych przez użytkownika pojazdów  
- Aktywacja i dezaktywacja tekstur dla danego pojazdu  
- Zmiany parametrów odległości  
- Zmiana proporcji  
- Dodawanie własnych plików `.prefab` do dekoracji  

## Instalacja

1. Pobierz repozytorium GitHub  
2. Rozpakuj plik `.zip` na swoim komputerze  
3. Uruchom plik `generator.exe` znajdujący się w głównym folderze  

## Dokumentacja

### Główne okno

Po uruchomieniu pliku wykonywalnego (`generator.exe`) ujrzysz główne okno aplikacji. Przystąpmy więc do szczegółowego opisu interfejsu, aby ułatwić Ci poruszanie się w nim. Zaczniemy od lewej strony.

1. Maksymalnie po lewej stronie znajduje się główny formularz. Musisz wprowadzić wszystkie dane, aby program zadziałał poprawnie. Poniżej znajdziesz opis każdego parametru:
    - **Files directory** - ustawia domyślną ścieżkę, gdzie pojawią się wygenerowane pliki. Osobiście zalecam wstawienie w tym miejscu ścieżki do Twojego projektu *Dying Light 2*, a dokładnie do folderu *Prefabs* przechowującego wszystkie pliki `.prefab`.
    - **File name** - nazwa wygenerowanego pliku, w którym znajdują się wszystkie wygenerowane pojazdy.
    - **Vehicles amount** - wskazuje, ile pojazdów ma zostać wygenerowanych.
    - **Min spacing** - minimalna odległość od poprzedniego pojazdu.
    - **Max spacing** - maksymalna odległość od poprzedniego pojazdu.
    - **Displacement** - przesunięcie aut w lewo i prawo.
    - **Auto-gen prefix** - nazwa prefiksu dla automatycznie wygenerowanych przez generator plików `.prefab`, które nie są głównym plikiem. Inaczej rzecz biorąc: są to pliki pojedynczych pojazdów, powstałe w celu utworzenia odpowiedniej hierarchii.
    - **Generate trunks** - Domyślnie jest włączone. Odpowiada za generowanie bagażników pojazdów.
    - **Generate decorations** - Odpowiada za generowanie dekoracji (twoje własne pliki `.prefab`). Domyślnie włączone.
    - **Preset** - pozycja ta umożliwia załadowanie konkretnych ustawień dla generatora (mowa tu o modelach pojazdów).

2. Druga w kolejności znajduje się sekcja z wyborem modeli pojazdów. Zaznacz odpowiednie checkboxy, aby zatwierdzić dany model w generacji.

3. Trzecia jest sekcja wyboru tekstur. Domyślnie wszystkie tekstury są uruchomione. Tekstury zmieniasz dla konkretnego pojazdu, który możesz zmienić za pomocą rozwijanej listy na górze.

4. Czwarta sekcja jest przeznaczona do ustalania proporcji pojazdów względem siebie. Lista ta jest automatycznie aktualizowana, gdy zostanie aktywowany lub dezaktywowany model pojazdu.

5. Na samej górze znajduje się mały menu bar. Znajdziesz w nim jedną zakładkę **File**, w której dostępne są dwie opcje:
    - **Close app** – zamyka okno aplikacji.
    - **Settings** – uruchamia okno ustawień, które jest omówione w następnym punkcie.

6. Okno ustawień umożliwia zapisanie ustawień w taki sposób, by wczytywały się one automatycznie po uruchomieniu aplikacji. Pamiętaj jednak, że każda zmiana wymaga ponownego uruchomienia aplikacji, gdyż interfejs głównego okna nie odświeża się automatycznie. Zmienić możesz:
    - ścieżkę zapisu pliku,
    - generowany prefiks,
    - minimalny odstęp,
    - maksymalny odstęp.

7. Wcześniej wspomniany menu bar zawiera także zakładkę **Preset**, w której dostępne są dwie opcje:
    - **Create preset** - tworzy nowy pakiet ustawień generatora który będzie możliwy do wczytania.
    - **Delete preset** - usuwa wybrany pakiet ustawień generatora.

    Warto mieć na uwadze to że podczas tworzenia pakietu, wystarczy podać jego nazwę, a wstawione dane będą odzwierciedlać stan obecnych ustawień generatora.

### Dodawanie własnych dekoracji

Aby dodać dekoracje, potrzebny będzie Ci zainstalowany silnik **CEngine**. Postępuj według następujących kroków:

1. Otwórz CEngine  
2. Uruchom dowolny projekt  
3. Postaw plik `.msh` pojazdu, dla którego tworzysz dekoracje, przykładowo `veh_sedan_a.msh`  
4. Dookoła pliku `.msh` postaw dekoracje w dowolny sposób  
5. Zapisz dekoracje (poza modelem `.msh`) do jednego pliku `.prefab` o dowolnej nazwie 
6. Skopiuj pozycję modelu pojazdu
6. Otwórz utworzony plik `.prefab` oraz wybierz opcję *Edit pivot*
7. Wejdź w zakładkę *Attributes* oraz wklej wcześniej skopiowaną pozycję modelu pojazdu
8. Zapisz zmiany
9. Przerzuć plik do odpowiedniego folderu znajdującego się w `\src\data\decorations` w rozpkaowanym pliku `.zip`  

Możesz dodać dowolną ilość dekoracji. Dekoracje zostaną losowo wybrane dla danego pojazdu lub może nie zostać wybrana żadna.

## Częste pytania

**Pytanie:** Jak długo zamierzasz wspierać ten projekt?  
**Odpowiedź:** Projekt ten jest częścią czegoś większego, czegoś, co ułatwi tworzenie map do *Dying Light 2* i przyspieszy  proces ich tworzenia kilkukrotnie więc wsparcie prędko się nie skończy.

**Pytanie:** Nad czym będą skupiać się następne aktualizacje i kiedy się ich spodziewać?  
**Odpowiedź:** W przyszłych aktualizacjach skupię się w szczególności na dodaniu brakujących modeli pojazdów, dodaniu większej liczby opcji konfiguracji, usprawnieniu UI oraz zmianach w kategorii *Quality of Life*. Daty wydania każdej nowej wersji tego narzędzia jest nieokreślona.

**Pytanie:** Czy to wszystko, co planujesz dodać?  
**Odpowiedź:** Absolutnie nie. Jest masa dodatkowych rzeczy, które chciałbym dodać w przyszłości, jak między innymi generowanie całej siatki ulic wraz z pojazdami. Jest to jednak jeszcze odległa przyszłość.

**Pytanie:** Jak mogę Ci podesłać pomysł?  
**Odpowiedź:** Dodaj mnie na Discordzie pod nickiem `paw3leq_`.

**Pytanie:** Czy mogę edytować kod i go redystrybuować?
**Odpowiedź:** W skrócie: tak, ale podaj informację na temat autora głównej aplikacji (mnie). Po szczegółowe informacje zapoznaj się z [Licencją](LICENSE.md).
