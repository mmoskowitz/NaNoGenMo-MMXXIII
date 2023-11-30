# Incolor ac viridis furiōsē nōtio dormit (NaNoGenMo 2023)

This text is a myriad of epic nonsense.

That is to say, this is 10,006 lines of Latin dactylic hexameter, which is syntactically and metrically valid, but which makes semantic sense only accidentally. From *Lȳsidamus spatham honōret holarcticus almam* (May Lysidamus from near the North Pole honor his nourishing sword)  to *Arachnae ballia depsant*, (Arachnes knead custodies) this has been composed by a program that makes use of a lexicon extracted from the Latin entries in Wiktionary, and assembles them like Mad-Libs into different sentence structures within the constraints of dactylic hexameter. There is no narrative and a very limited set of sentence structures, but it was an interesting exercise to build (and does not contain any machine learning) and I hope it is enjoyable, though I certainly wouldn’t recommend trying to read any large part of it.

## Project notes

There were two main parts of this project: turning the Wiktionary content into usable data, and assembling that data into valid lines of dactylic hexameter.

### The lexicon

Wiktionary contains 7,630,513 individual pages, of which about 10% contain one or more Latin words. (Pages are titled without macrons, so levis and lēvis appear on the same page.) It is also designed for display and not for analysis. But the needs of Wiktionary editors have led to a lot of standardized templates that can be used to extract inflection information from a huge number of entries. It was very helpful that the Wiktionary has a page for each form rather than making me decline and conjugate every word. More difficult was fully understanding the Wiktionary tagging so that the resulting parsed data for the lexicon would be as accurate as possible. It was a very iterative process figuring out why words were not behaving as expected. In the last few days, I fixed a problem with the genders of inflected nouns by copying all of the non-inflected ones into a separate directory so that my parser could read them first and build up a store of noun genders.

The lexicon has a lot of words that are primarily used in scientific Latin names of organisms, so words like “holarcticus” in the first line are overrepresented in the text. I didn’t have any usage data, so all words are equally likely to be used, as long as they fit the rhythm.

The parsing code is in parse-alltext.py, which runs on a filtered set of Wikimedia content pages. See instructions.py for some of the filtering steps.

## The hexameter

As I parsed the wiktionary data, I produced a line for each word form that looks like this:

> aucta,VLSV,adj,f-nom-s

> aucta,VLSV,adj,f-voc-s

> aucta,VLSV,adj,n-nom-p

> aucta,VLSV,adj,n-acc-p

> aucta,VLSV,adj,n-voc-p

> auctā,VLLV,adj,f-abl-s

> auctā,VLLV,v,2-s-pres-actv-impr

> fuscā,CLLV,v,2-s-pres-actv-impr

> fusca,CLSV,adj,f-nom-s

> fusca,CLSV,adj,f-voc-s

> fusca,CLSV,adj,n-nom-p

> fusca,CLSV,adj,n-acc-p

> fusca,CLSV,adj,n-voc-p

> avidius,VSSSSC,adv,adv

> minimē,CSSLV,adv,adv

> Aviliobris,VSSSSSC,n,f-nom-s

> ūber,VLSC,n,n-nom-s

> ūber,VLSC,adj,m-nom-s

> ūber,VLSC,adv,adv

> generōsē,CSSLLV,adv,adv

> Aarōn,VSSLC,n,m-nom-s

> atrōcissimē,VSLLSLV,adv,adv

> terra,CLSV,n,f-nom-s

> vīrus,CLSC,n,n-nom-s

> abracadabra,VSSSSSV,intj,intj

This is the word (with macrons), its metrical form, its part of speech, and its inflection. The meter is an opener code, a list of long and short syllables, and an end code. (I treat all mute-liquid clusters as short.)

The `versifier.py` code takes these lines and loads them into a lexicon, which can provide random words by meter and inflection. The `verse.py` code provides line structure and code for determining what meters can come next in the line. The `sentence.py` code provides a very limited set of sentence structures and tools for getting the next inflection needed in a given sentence. The versifier progresses through both of these simultaneously to produce sentences that fit within hexameter lines, and tries different possible meters until it assembles a line. For example, this is what it does to produce the first two:

> trying  Lȳsidamus

> trying  Lȳsidamus spatham

> trying  Lȳsidamus spatham ablūsum

> trying  Lȳsidamus spatham honōret

> trying  Lȳsidamus spatham honōret Iālysius

> trying  Lȳsidamus spatham honōret Iālysius trifidam.

> trying  Lȳsidamus spatham honōret Iālysius fabram.

> trying  Lȳsidamus spatham honōret Iālysius fabram. Apēs

> trying  Lȳsidamus spatham honōret Iālysius fabram. Ovis

> trying  Lȳsidamus spatham honōret Iālysius fabram. Helix

> trying  Lȳsidamus spatham honōret Iālysius fabram. Umī

> trying  Lȳsidamus spatham honōret Iālysius fabram. Hera

> trying  Lȳsidamus spatham honōret Iālysius fabram. Oleum

> trying  Lȳsidamus spatham honōret Iālysius chthoniam.

> trying  Lȳsidamus spatham honōret Iālysius rigua.

> trying  Lȳsidamus spatham honōret Iālysius riguā.

> trying  Lȳsidamus spatham honōret Iālysius strabam.

> trying  Lȳsidamus spatham honōret Iālysius strabam. Oneum

> trying  Lȳsidamus spatham honōret Iālysius strabam. Ina

> trying  Lȳsidamus spatham honōret Iālysius strabam. Emys

> trying  Lȳsidamus spatham honōret Iālysius strabam. Amā

> trying  Lȳsidamus spatham honōret Iālysius strabam. Hiems

> trying  Lȳsidamus spatham honōret Iālysius strabam. Halōs

> trying  Lȳsidamus spatham honōret Iālysius celebrēs.

> trying  Lȳsidamus spatham honōret holarcticus

> trying  Lȳsidamus spatham honōret holarcticus almam.

> trying  Lȳsidamus spatham honōret holarcticus almam. Opharus

> trying  Lȳsidamus spatham honōret holarcticus almam. Aqua

> trying  Lȳsidamus spatham honōret holarcticus almam. Aqua crū̆stās

> Lȳsidamus spatham honōret holarcticus almam. Aqua crū̆stās

> trying  paulum

> trying  paulum interloquar.

> trying  paulum interloquar. Antrum

> trying  paulum interloquar. Altar

> trying  paulum interloquar. Altar amoebās

> trying  paulum interloquar. Altar amoebās possit.

> trying  paulum interloquar. Altar amoebās possit. Hosae

> trying  paulum interloquar. Altar amoebās possit. Apēs

> trying  paulum interloquar. Altar amoebās possit. Ebor

> trying  paulum interloquar. Altar amoebās possit. Afa

> trying  paulum interloquar. Altar amoebās possit. Ulex

> trying  paulum interloquar. Altar amoebās possit. Oneum

> trying  paulum interloquar. Altar amoebās ferbueram.

> trying  paulum interloquar. Altar amoebās fābulat.

> trying  paulum interloquar. Altar amoebās fābulat. Ōllae

> paulum interloquar. Altar amoebās fābulat. Ōllae

As you can see, it has to do some work to complete the line!

## Known issues

- The data does not contain (as far as I could determine) information on what verbs are transitive and Intransitive or on verbs that take irregular noun cases.
- The scanner for the meters of words doesn’t do a great job with edge cases of vowel diphthongs. Some of this is not having a good way to know from the data if “eu” is one syllable as in “heu” or two as in “eunt” but my scanning algorithm also thinks “vehitur” is two syllable because I told it to ignore “h” and I didn’t have time to fix it.
- Wiktionary is known not to have all its macrons correct.
- I’ve certainly missed some of the subtleties of the Wiktionary grammatical tagging.

Thanks to my wife Becca and my frequent collaborators [@cdel](https://github.com/cdel), [@lorelei-sakai](https://github.com/lorelei-sakai), and [@denismm](https://github.com/denismm) for being very helpful sounding boards during this project!
