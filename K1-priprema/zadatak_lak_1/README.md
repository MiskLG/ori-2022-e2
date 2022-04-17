## Zadatak1 - lak
#### Robot: doći od starta do cilja, uz prvobitno kupljenje jedne plave kutije. Kada robot pokupi kutiju može da se kreće i dijagonalno.
## Steps:
* Dodati novi element u board, moze biti bilo sta sta vec nema (~18lc u board.py)
* Napraviti da ima boju taj element (~245lc u game.py)
* Napraviti promenljivu u State klasi number_of_boxes, isto tako i eaten_boxes i inicijalizovati ih
* Dodati nova legal stanja kad pokupi kutiju (~123lc u state.py)
* Napisati kod da se prosledjuju number_of_boxes i eaten_boxes u child state (parametri klasa i ~ 20lc u state.py)
* Napisati kod da kad dodje na kutiju da je stavi da ju je pojeo ako treba (~105lc u state.py)
* Kod za proveru da li je final i dodati return parametar da kad je u tom trenutku pokupio kutiju da vrati true (~137lc u state.py)
* Editovati refresh za state listu u search-u (~38lc u search.py)