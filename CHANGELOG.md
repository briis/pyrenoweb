# Changelog for pyrenoweb

## Version 2.0.5

**Date**: `2024-03-xx`

### What's Changed

- Added handling of Special cases where Municipalities use the same Type for several Containers. For the identified Municipalities, we now do a second validation on other fields to place the Container in the right type.
- Handling the case where the same Road exists more than once in a Municipality. There is now a requirement to enter the Zipcode of the Address when setting up a new entity in Home Assistant.
- Fixing missing containers in Aalborg. Closing https://github.com/briis/affalddk/issues/11

## Version 2.0.4

**Date**: `2024-03-02`

### Changes

* Removed the following Municipalities as they are not supported:
  * Balleup
  * Billund
  * Fanø
  * Favrskov
  * Fredericia
  * Frederikshavn
  * Guldborgsund
  * Haderslev
  * Herning
  * Holbæk
  * Holstebro
  * Ikast-Brande
  * Ishøj - They use the API, but do not supply dates, only textual descriptions, which cannot be converted to dates.
  * Kalundborg
  * Kolding
  * Læsø
  * Lolland
  * Middelfart
  * Morsø
  * Norddjurs
  * Nordfyns
  * Nyborg
  * Odder
  * Odense
  * Silkeborg
  * Skanderborg
  * Skive
  * Struer
  * Syddjurs
  * Thisted
  * Vejle
  * Vesthimmerland
  * Viborg
  * Tønder - They use the API in a Non-Standard way. Still under investigation if I can retrieve the data
  * Vallensbæk

* Added new function to support Municipalities that only supply weekdays. (Albertslund, Furesø).
* Added new garbage type `plastmetalmadmdk` which holds *Plast, Metal, Mad & Drikkekartoner*
* Added new garbage type `pappapir` which holds *Pap & Papir*
* Added new garbage type `tekstil` which holds *Tekstilaffald*
* Added new garbage type `glasplast` which holds *Glas, Plast & Madkartoner*
* Added new garbage type `plastmetalpapir` which holds *Plast, Metal & Papir*
* Fixed bug when Garbage Type could be in more than pickup type. Happens when partial strings are the same.
