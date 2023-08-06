# pyktionary

[![pyktionary 0.6 build status](https://gitlab.com/flow.gunso/pyktionary/badges/0.6/pipeline.svg)](https://gitlab.com/flow.gunso/pyktionary/commits/0.6)

Simple Wiktionary scraper. Get information from words in Wiktionary.

__The module is at an early stage, be advised that:__
- **Only [french Wiktionary](https://fr.wiktionary.org/) is supported.**
- **The following sections are not scraped:**
  - **_Prononciation_**
  - **_Anagrammes_**
  - **_Voir aussi_**
  - **_Références_**
  - **_Forme de verbe_**
- __Any section not matching _Étymologie_ is scraped as _Définition_.__

# What pyktionary is

A scraper that gets data on words from Wiktionary.
Sections of a word are scraped as raw HTML into a dict, see [Example](#Example).

# What pyktionary is not

An interface to make changes to Wiktionary. You can NOT send data to Wiktionary with this module.

# What's next ?

This module is at a very early stage. It only cover my specific use case, which is scraping a word's etymology and definitions from french Wiktionary.

The module will improve over time. Priorities are for the following features and fixes:
- Scrap all sections from a word.
- Support wiktionaries from other languages.

You can read the [TODO](TODO.md) for more stuff to do.

# Usage

```python
from pyktionary import Wiktionary

# ...

wik = Wiktionary()
word = wik.word("oui")

# ...
```

# Example

###### With word [oui](https://fr.wiktionary.org/wiki/oui):

The following code:
```python
    from pyktionary import Wiktionary
    wik = Wiktionary()
    word = wik.word("oui")
    pprint.pprint(word, compact=True)
```
output:
```bash
{
	'Étymologie': '<dl> <dd> <span class="date"><i>(<span class="texte"> 1380</span>)</i> </span> De l’ancien français <i><span class="lang-fro" lang="fro"><a href="https://fr.wiktionary.org/wiki/o%C3%AFl#fro" title="oïl"> oïl</a></span> </i> <span class="date"><i>(<span class="texte"> 1080</span>)</i> </span> , forme composée de <i>o </i> «\xa0cela\xa0» <span class="date"><i>(<span class="texte"> 842</span>)</i> </span> , au sens de «\xa0oui\xa0» (à comparer de <i><a href="https://fr.wiktionary.org/wiki/%C3%B2c" title="òc">òc</a> </i> «\xa0oui\xa0» en <a href="https://fr.wiktionary.org/wiki/occitan" title="occitan">occitan </a> ), renforcé par le pronom personnel <i><a href="https://fr.wiktionary.org/wiki/il" title="il">il</a> </i> (on trouve aussi <i>o-je </i> , <i>o-tu </i> , <i>o nos </i> , <i>o vos </i> ). <span id="ref-1"><small></small><sup><a href="#reference-1"> [1]</a></sup> </span> <span id="ref-2"><small></small><sup><a href="#reference-2"> [2]</a></sup> </span> Les mots «\xa0oui\xa0» et «\xa0òc\xa0» sont des calques celtiques <sup class="reference" id="cite_ref-1"><a href="#cite_note-1">[1]</a> </sup> . </dd></dl>',
	'Définition': '<ol> <li> Réponse de <i><a href="https://fr.wiktionary.org/wiki/oui#fr-interj" title="oui">oui</a> </i> . Vote pour. <strong>Note d’usage\xa0: </strong> L’ <a href="https://fr.wiktionary.org/wiki/article" title="article">article </a> défini ne s’ <a href="https://fr.wiktionary.org/wiki/%C3%A9lider" title="élider">élide </a> pas devant ce mot. <ul><li><i> Les résultats, qui seront annoncés lundi, devraient confirmer l’avance du « <b> oui </b> » au changement constitutionnel, mais les partisans de cette consultation controversée ont déjà concédé leur défaite.</i><span class="sources"> <span class="tiret"> — </span> ( <cite class="ouvrage" style="font-style:normal"> Ouest-France, « <a class="external text" href="https://www.ouest-france.fr/europe/roumanie/roumanie-l-abstention-fait-echouer-un-referendum-contre-le-mariage-gay-6006771" rel="nofollow">Roumanie\u2009: l’abstention fait échouer un référendum contre le mariage gay </a> » sur <i>Ouest-France.fr </i> . Mis en ligne le 7 octobre 2018 </cite> )</span></li><li><i> Une ballade, une ballade\xa0! s’écria l’ermite, cela vaut mieux que tous les oc et les <b> oui </b> de France.</i><span class="sources"> <span class="tiret"> — </span> ( <a class="extiw" href="https://fr.wikipedia.org/wiki/Walter_Scott" title="w:Walter Scott"> Walter <span class="petites_capitales" style="font-variant: small-caps">Scott </span> </a> , <i> <a class="extiw" href="https://fr.wikipedia.org/wiki/Ivanho%C3%A9" title="w:Ivanhoé">Ivanhoé </a> </i> , traduit de l’anglais par <a class="extiw" href="https://fr.wikipedia.org/wiki/Alexandre_Dumas" title="w:Alexandre Dumas"> Alexandre <span class="petites_capitales" style="font-variant: small-caps">Dumas </span> </a> , <a class="extiw" href="https://fr.wikisource.org/wiki/Ivanho%C3%A9_(Scott_-_Dumas)" title="s:Ivanhoé (Scott - Dumas)"> 1820 </a> )</span></li><li><i> Le <b> oui </b> et le non.</i></li><li><i> Il a dit ce <b> oui </b> -là de bon cœur.</i></li><li><i> Il ne faut pas tant de discours, on ne vous demande qu’un <b> oui </b> ou un non. Dites un bon <b> oui </b> .</i></li> </ul> </li></ol>'
}
```

# Licence

This module is licenced under GNU GPL v3.