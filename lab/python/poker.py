# -*- coding: latin-1 -*-

#
#  IS-105 LAB11
#  Implementer alt som er markert med OPPGAVE.
#  I tillegg skal du i filen lab11defs.txt beskrive et program (så detaljert du kan)
#	for en poker server, hvor spillere kan melde seg på et poker spill, 
#	få utdelt en hånd hver, legge inn en sats eller kaste sin hånd 
#	og få utpekt en (eller flere i tilfelle uavgjort) vinner.
#	Det er lagt ut flere implementasjoner av sockets klient-tjener modell i Class Fronter.
#	Det som er aktuelt å se på er de som er implementert i Python.
#
#  lab11.py - kildekode som inneholder studentenes løsning.
#         
#
#
import random # brukes for å dele ut kort

# Skriv inn fullt navn på gruppemedlemene (erstatte '-' med navn slikt 'Kari Trå')
gruppe = {  'student1': 'Nadia', \
			'student2': 'Kristian', \
           
}

# Oppgave 
# 	Implementere pokerspill. Vi begynner med representasjon og testing.
#
#	Testing i Python kan gjøres med assert. Eksemplet under skal være selvforklarende.
#
#   Det er gitt et kortstokk http://en.wikipedia.org/wiki/Playing_card med 52 kort.
#	I denne oppgaven prøver vi å lage et prototype som gir svar på følgende:
#	Hvordan representere alle kort? Hvordan finne ut hvilken hånd er best? Hvordan dele ut kort?
#
#   Les deg opp på hva poker er og hvordan det spilles, hvis du ikke kjenner til det fra før.
#	Domenkunnskap i systemutvikling er viktigst!!!
#	http://no.wikipedia.org/wiki/Poker
#	http://en.wikipedia.org/wiki/Poker
#
#	Her er et forslag for representasjon av kort og hender, som jeg anbefaler dere å bruke.
#	Dere kan gjøre egne modifikasjoner, med de må være begrunnet i lab11defs.txt filen.
#
#   Typer (kind): H - heart, S - spade, C - club, D - diamond (13 kort av hver type)
#   Verdi (rank): A - ace, K - king, Q - queen, J - jack, T - ten, 9, 8, 7, 6, 5, 4, 3, 2
#   En hånd (hand): består av 5 kort http://en.wikipedia.org/wiki/Hand_rankings
#   Hånd rangeres fra høyest til lavest (i paranteser anbefalt navn på variabelen på en hånd): 
#		 8 - Straight flush (sf) (finnes også Royal Flush, som er den beste av Straight flush)
#		 7 - Four of a Kind (fk) 
#		 6 - Full House (fh) 
#	     5 - Flush (fl)
#		 4 - Straight (st) 
#		 3 - Three of a kind (tk) 
#	     2 - Two Pair (tp) 
#        1 - One Pair (op) 
#        0 - High Card (hc)
#   
#
# OPPGAVE: erstatt max med en funksjon allmax, som tar hensyn til uavgjort mellom to eller flere hender 
def poker(hands):
	"""
		Denne funksjonene må omdefineres for å ta hensyn til spesialtilfelle med flere like "Straight Flush" hender
		dvs. uavgjort
		Returnerer en eller flere hender: poker([hand, ...]) => [[hand], ...]
		hand_rank er en funksjon som må skrives og brukes i sammenligningen av "hender"
	"""
	return max(hands, key=hand_rank)

# OPPGAVE: fullføre denne funksjonene for alle hender i poker og lage tester med assert
# ---------------- OK -----------------
def hand_rank(hand):
	"""
		Returnerer en verdi som indikerer verdi av en hånd. 
		Vi har gitt verdien til hendene i spesifikasjonen (8 Straight Flush, ...)
		Vi må også kunne skille mellom "like" hender (breaking ties).
		9 9 9 9 5 => (7,9,5) Four of Kind (7) and fife kicker
		3 3 3 3 2 => (7,3,2) Four of Kind (7) and two kicker
		TD 8D 7D 5D 3D => (5, [10,8,7,5,3]) Flush (5) men alle kort må spesifiseres for å kunne sammenligne
		JC TC 9C 8C 7C => (8, 11) Straight Flush (8) Jack (11) High
		AS AH AC AD QH => (7, 14, 12) Four Aces (7, 14)  and a Queen kicker (12)
	"""
	ranks = card_ranks(hand)
	if straight(ranks) and flush(hand):
		return (8, max(ranks)) # 2 3 4 5 6 => (8, 6)
	elif kind(4, ranks): # kan returnere både boolean og tall, i Java 0 er False
		return (7, kind(4, ranks), kind(1, ranks)) # 9 9 9 9 3 (7, 9, 3)
	elif kind(3,ranks) and kind(2,ranks):
		return (6,kind(3,ranks),kind(2,ranks))	
	elif flush(hand):
		return (5,max(ranks))
	elif straight(ranks):
		return (4,max(ranks))
	elif kind(3, ranks):
		return (3,kind(3,ranks),max(filter(lambda value: not value == kind(3,ranks),ranks)))
	elif two_pair(ranks):
		two_pairs = two_pair(ranks)
		return (2,two_pairs[0],two_pairs[1])
	elif kind(2,ranks):
		return (1,kind(2,ranks),max(filter(lambda value: not value == kind(2,ranks),ranks)))
	else:
		return (0,max(ranks))
	
	
	
# Funksjonene card_ranks(hand) returnerer en ORDNET (sorted) tuple av verdier (ranks)
# Verdier for J, Q, K og A er tilsvarende 11, 12, 13, 14. 
# En hånd TD TC TH 7C 7D skal returnere [10,10,10,7,7]
def card_ranks(hand):
	ranks = ['--23456789TJQKA'.index(r) for r,s in hand]	
	ranks.sort(reverse = True)
	return [5,4,3,2,1] if( ranks == [14,5,4,3,2]) else ranks

# OPPGAVE: Implementer denne funksjonen
# ---------------- OK -----------------
# Funksjonen straight(ranks) returner True hvis hånden er en Straight.
def straight(ranks):

	if max(ranks) - min(ranks) == 4  and len(set(ranks)) == 5:
		return True
	else:
		return False

# OPPGAVE: Implementere denne funksjonen
# ---------------- OK -----------------
# Funksjonen flush(hand) returnerer True hvis hånden er en Flush.
def flush(hand):
	
	types = [t for v,t in hand]
	if len(set(types)) == 1:
		return True
	else:
		return False
	

# OPPGAVE: Implementer denne funksjonen
# ---------------- OK -----------------
# Funksjonen kind(nr, ranks) returnerer den første verdien (rank) som hånden har nøyaktig n av.
# For en hånd med 4 syvere, skal denne funksjonen returnere 7.
def kind(nr, ranks):
	for r in ranks:
		if ranks.count(r) == nr: return r
	return None

# OPPGAVE: Implementer denne funksjonen
# ---------------- OK -----------------
# Funksjonen two_pair(ranks) gjør følgende:
# hvis det er Two Pair, skal funksjonen returnere deres verdi (rank) som en tuple.
# For eksempel, en hånd med to toere og 2 firere vil gi en returverdi på (4, 2).
def two_pair(ranks):
	
	high_pair = kind(2,ranks)
	low_pair = kind(2, filter(lambda value: not value == high_pair,ranks))

	if high_pair and low_pair:
		return [high_pair, low_pair]
	else:
		return None

# OPPGAVE: Implementer denne funksjonen (brukes i poker funksjonen for å løse uavgjort tilfeller)
# For eksempel, gitt 4 følgende hender
#   [['6C', '7C', '8C', '9C', 'TC'],
#   ['6D', '7D', '8D', '9D', 'TD'],
#   ['9D', '9H', '9S', '9C', '7D'],
#   ['TD', 'TC', 'TH', '7C', '7D']]
# skal allmax returnere to hender [['6C', '7C', '8C', '9C', 'TC'], ['6D', '7D', '8D', '9D', 'TD']]
def allmax(iterable, key=None):
	return None

# Denne strukturen definerer et kortstokk for poker
mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']

# Denne funksjonen deler ut numhands med n kort i hver hånd
def deal(numhands, n=5, deck=mydeck):
    # Your code here.
	random.shuffle(deck)
	return [deck[n*i:n*(i+1)] for i in range(numhands)]


def test():
   
	# Dette ble gjort i LAB 5
	# Den innebygde (built-in) funksjonen max kan brukes for å finne den beste hånden
	# Skriv test for den innebygde funksjonen max på flere "list of numbers" (lon)
	# Eksemplene er gitt, du må kommentere disse ut og sette på en verdi som ikke gir feil
	lon1 = [6, 7, 8, 0]
	lon2 = [6, 7, -9, 0]
	assert max(lon1) == 8
	assert max(lon2, key=abs) == -9

	sf = "6C 7C 8C 9C TC".split() # Straight Flush => ['6C', '7C', '8C', '9C', 'TC']
	fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
	fh = "TD TC TH 7C 7D".split() # Full House
	st = "9S 8B 7S 6H 5C".split() # //Straight
	fl = "3H 2H 6H 8H TH".split() # flush
	tp = "KS KH 9H 9S JH".split() # //Two Pair
	tk = "3S 3H 3C 4S 9D".split() # Three of a kind
	op = "5S 5C 6D TD KH".split() # One Pair
	hc = "AC 5H 3D 6H QC".split() 
	st54321 = "AH 5S 4C 3D 2H".split()
	assert poker([sf, fk, fh]) == sf
	# Disse testtilfellene ble skrevet i LAB 5
	# Skriv tre nye testtilfeller som sammenligner hender basert på eksemplet overfor
	# 1) Four of Kind (fk) mot Full House (fh) skal returnere Four of Kind (fk)
	# 2) Full House (fh) mot Full House (fh) skal returnere Full House (fh)
	# 3) Straight (st) skal slå Two pair (tp) OBS! Du må selv lage eksempler på hender her
	


	# Dette ble gjort i LAB 5
	# 1) teste et tilfelle der det kun er en hånd og at poker returnerer den samme hånden
	# 2) teste et tilfelle hvor man sammenligner en Straight Flush med 100 Full Houses
	# og det må da returnere Straight Flush (urealistisk med så mange spillere, men 
	# vi tar høyde for det).
	# Hva skjer hvis man har en tom liste som inn-data, dvs. ingen hender?
	assert poker([sf]) == sf
	assert poker([sf, 100*fh]) == sf

	# Dette ble gjort i LAB 5
	# Implementer funksjonen card_rank(hand) og legg til tester for 
	# sf, fk og fh variabler som er definert i denne testfunksjonen
	# Du kan gjerne definere flere hender og legge til flere tester :)
	assert card_ranks(sf) == [10,9,8,7,6]
	assert card_ranks(fk) == [9,9,9,9,7]
	assert card_ranks(st54321) == [5,4,3,2,1]
	assert card_ranks(["AH","KH","QH","JH","TH"]) == [14,13,12,11,10]
	assert card_ranks(st) == [9, 8, 7, 6, 5]


	assert straight([9, 8, 7, 6, 5]) == True
	assert straight([9, 8, 7, 6, 4]) == False
	assert flush(sf) == True
	assert flush(fk) == False
	assert kind(4,[7,5,7,7,7]) == 7
	assert kind(4,[4,4,4,4,2]) == 4
	assert kind(4,[3,4,5,4,2]) == None
	assert two_pair([13, 13, 11, 9, 9]) == [13,9]
	assert two_pair([13, 12, 11, 10, 9]) == None
    # 
    # hand_rank(..) implementere i denne laben (LAB 11)
	# Her er gitt noen eksempler på testing av denne funksjonen som man kan bruke på et senere tidspunkt
    #
	assert hand_rank(sf) == (8,10)
	assert hand_rank(fk) == (7,9,7)
	assert hand_rank(fh) == (6,10,7)
	assert hand_rank(fl) == (5,10)
	assert hand_rank(st) == (4,9)
	assert hand_rank(tk) == (3,3,9)
	assert hand_rank(tp) == (2,13,9)
	assert hand_rank(op) == (1,5,13)
	assert hand_rank(hc) == (0,14)
	
	return "Done testing"

print test()
hands = deal(3)
print hands
print poker(hands)



