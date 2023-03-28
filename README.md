# matkareitin-optimoija

Ohjelma tutkii kaupunkien välisiä etäisyyksiä ja niiden välisiä reittejä.
Ohjelman käyttöä varten tarvitaan CSV-muodossa formatoitu TXT-tiedosto.
Ohjelman alussa ohjelma yrittää avata tätä tiedostoa ohjelman ajokansiosta.
Mikäli avaaminen epäonnistuu, tulostuu poikkeuskäsittelyssä virheviesti ja
ohjelma suljetaan. Jos tiedoston avaaminen puolestaan onnistuu, sen sisältö
lisätään silmukassa rivi riviltä sanakirjaan.

Ohjelman tietorakenne on sisäkkäinen sanakirja, ts. sanakirja,
jonka hyötykuormana on toinen sanakirja. Arvot luetaan sanakirjaan niin, että
uloin avain on lähtökaupunki, sisemmän sanakirjan avain on kohdekaupunki ja
sisemmän sanakirjan hyötykuorma on näiden välinen etäisyys.

Ohjelmassa on lukuisia toimintoja. Se osaa mm. etsiä reittejä, lisätä uusia
reittejä, poistaa vanhoja reittejä kuin myös selvittää reittien olemassaoloa.
Suurimpaan osaan näistä operaatioista käytetään vain edellä mainittua
sanakirjaa, mutta välillä käytetään myös listaa, kuten halutun reitin
kaupunkien listaamiseen ja läpikäymiseen.
