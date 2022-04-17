## Zadatak1 - lak
#### Robot: doći od starta do cilja, uz prvobitno kupljenje jedne plave kutije. Kada robot pokupi kutiju može da se kreće i dijagonalno.
## Steps:
* Dodati nove elemente u board, moze biti bilo sta sta vec nema (~18lc u board.py)
* Dodati boje elementima (~245lc u game.py)
* Napraviti promenljivu u State klasi orange_box, i blue_box, isto tako i eaten_boxes i inicijalizovati ih
* Napisati kod da kad dodje na kutiju da je stavi da ju je pojeo ako treba (~105lc u state.py) i staviti lokalni parametar da treba status da se refresh
* Kod za proveru da li je final i dodati return parametar da kad je u tom trenutku pokupio kutiju da vrati true (~137lc u state.py)
* Editovati refresh za state listu u search-u (~38lc u search.py)