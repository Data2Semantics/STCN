# STCN2RDF

=Author=
	Rinke Hoekstra
=Date=
	13 November 2012

This document briefly describes the first naive efforts to publish the STCN MySQL database (produced through Paul Huygen's script) as RDF.

We create the RDF by means of a [D2RQ](http://d2rq.org/) mapping file. This file can be [obtained from Github](https://raw.github.com/RinkeHoekstra/STCN/master/stcn.ttl).

### First step

We created and filled a MySQL database as per Paul Huygen's instructions. This database contains a number of tables the details of which we will not discuss here (Paul's documentation is quite elaborate)

We then generated a D2RQ mapping file using the `generate-mapping` script of D2RQ. This provides a 1:1 mapping of the database contents to RDF, where all URI's are constructed using the database table name, and the unique identifier of each record.

### Merging and Smushing

This section briefly discusses the mappings for each (relevant) table in the database.

Highlights:
* Fingerprints with the same literal value are linked via `skos:exactMatch` properties
* Publications link directly to illustrations
* Publications have separate links for first-tenth authors
* Use the open annotation format for timestamping locations of publications (e.g. Amsterdam in 1646)
* Use a separate class for all formats and sizes of publications
* 

#### The `auteurs` table

Feature | Description 
--- | ---
Class		| `vocab:Auteur` 
URI			| `http://[SERVER_NAME]/resource/auteur/[auteurs.ppn]`
Label		| `auteurs.name`
Relations	| `vocab:publicatie` points to every publication of that author (join using the `auteur_pubs` and `publications` tables)


#### The `bibliografische_bijzonderheden_pubs` table

Feature | Description 
--- | ---
Class		| `vocab:Bibliografische_Bijzonderheid`
URI			| `http://[SERVER_NAME]/resource/bibliografische_bijzonderheid/[bibliografische_bijzonderheden_pubs.content]`
Label		| `[bibliografische_bijzonderheden_pubs.content]`


#### The `drukkersthesaurus` table

Feature | Description
--- | ---
Class		| `vocab:Drukker`
URI			| `http://[SERVER_NAME]/resource/drukker/[drukkersthesaurus.ppn]`
Label		| `[drukkersthesaurus.content]`


#### The `engelse_annotatie_pubs` table

Feature | Description
--- | ---
Class		| `vocab:Engelse_Annotatie`
URI			| `http://[SERVER_NAME]/resource/engelse_annotatie/[engelse_annotatie_pubs.id]`
Label		| `[engelse_annotatie_pubs.content]`



#### The `extra_zoeksleutel_pubs` table

Feature | Description
--- | ---
Class		| `vocab:Zoeksleutel`
URI			| `http://[SERVER_NAME]/resource/zoeksleutel/[extra_zoeksleutel_pubs.id]`
Label		| `[extra_zoeksleutel_pubs.content]`
Attributes	| `vocab:kmc` with value `[extra_zoeksleutel_pubs.kmc]`


#### The `geografische_thesaurus` table

Feature | Description
--- | ---
Class		| `vocab:Plaats`
URI			| `http://[SERVER_NAME]/resource/plaats/[geografische_thesaurus.content]`
Label		| `[geografische_thesaurus.content]`

#### The `geografische_thesaurus_pubs` table

Feature | Description
--- | ---
Class		| `vocab:Plaats_Annotatie`, `ao:Annotation`
URI			| `http://[SERVER_NAME]/resource/plaats/annotatie/[geografische_thesaurus_pubs.content]_[geografische_thesaurus_pubs.kmc]`
Label		| `[geografische_thesaurus_pubs.content] ([geografische_thesaurus_pubs.kmc])`
Relations	| `oa:hasBody` to the year (`kmc`) for which this place name holds, <br/> `oa:hasTarget` both to the publication and the place.
Condition	| Instances of this class are only generated if there is a value for the `geografische_thesaurus_pubs.kmc` field. 


#### The `koepeltitel` table

Feature | Description
--- | ---
Class		| `vocab:Koepeltitel`
URI			| `http://[SERVER_NAME]/resource/koepeltitel/[koepeltitel.ppn]`
Label		| `[koepeltitel.content]`

#### The `onderwerpsontsluiting` table

Feature | Description
--- | ---
Class		| `vocab:Onderwerp`
URI			| `http://[SERVER_NAME]/resource/onderwerp/[onderwerpsontsluiting.content]`
Label		| `[onderwerpsontsluiting.content]`


#### The `publications` table

Feature | Description
--- | ---
Class		| `vocab:Publicatie`
URI			| `http://[SERVER_NAME]/resource/publicatie/[publications.ppn]`
Label		| `[publications.kmc4000]` (title)
Attributes	| various KMC codes
Relations	| `vocab:first_author` […] `vocab:tenth_author` to the authors of the publication, <br/> `vocab:onderwerp` to the subject (onderwerpsontsluiting) of the publication, <br/> `vocab:drukker` to the printer of the publication, <br/> `vocab:koepeltitel` to the koepeltitel of the publication, <br/> `vocab:plaats` to the place of the publication (note that this may or may not be a timestamped place indicated through a `vocab:Plaats_Annotatie`), <br/> `vocab:selectie` to the selectie indicaiton,<br/> `vocab:vingerafdruk` to the fingerprint of the publication, <br/> `vocab:werkaantekening` to an annotation on the publication,<br/> `vocab:engelse_annotatie` to the english annotation of the publication,<br/> `vocab:bibliografische_bijzonderheid` to the bibliographic peculiarity codes of the publication,<br/> `vocab:extra_zoeksleutel` to one or more extra search 'keys' for the publication, <br/> `vocab:illustration` to the URL of an illustration (!),<br/> `vocab:formaat` to the format/print size of the publication (taken from `kmc4062`),<br/> `vocab:jaar` to the year of publication (not an integer value, so may contain X'es)<br/> `vocab:titeluitgave_van` to other publications with the **same fingerprint**.


#### Extra `vocab:Jaar` class

Aggregates all values for the `publications.kmc1100` fields in the database.

Feature | Description
--- | ---
Class		| `vocab:Jaar`
URI			| `http://[SERVER_NAME]/resource/jaar/[publications.kkmc1100]`
Label		| `[publications.kmc1100]`


#### Extra `vocab:Formaat` class

Aggregates all values for the `publications.kmc4062` fields in the database.

Feature | Description
--- | ---
Class		| `vocab:Formaat`
URI			| `http://[SERVER_NAME]/resource/formaat/[publications.kmc4062]`
Label		| `[publications.kmc4062]`


#### The `selectie_pubs` table

Feature | Description
--- | ---
Class		| `vocab:Selectie`
URI			| `http://[SERVER_NAME]/resource/selectie/[selectie_pubs.id]`
Label		| `[selectie_pubs.content]`
Attributes	| `vocab:kmc` with value `[selectie_pubs.kmc]`

#### The `vingerafdruk_pubs` table

Feature | Description
--- | ---
Class		| `vocab:Vingerafdruk`
URI			| `http://[SERVER_NAME]/resource/vingerafdruk/[vingerafdruk_pubs.id]`
Label		| `[vingerafdruk_pubs.content]`
Relations	| `skos:exactMatch` relations to all instances of `vocab:Vingerafdruk` that have exactly the same string as value for the `vingerafdruk_pubs.content` record.


#### The `werkaantekening_pubs` table

Feature | Description
--- | ---
Class		| `vocab:Werkaantekening`
URI			| `http://[SERVER_NAME]/resource/werkaantekening/[werkaantekening_pubs.id]`
Label		| `[werkaantekening_pubs.content]`