# Raw Data Directory

This directory is intended to store the raw IMDb dataset files (`.tsv.gz`).


## How to get the data
To run this dbt project locally, download the required datasets from the [IMDb Non-Commercial Datasets](https://datasets.imdbws.com/) page and place them inside this folder.

## Required Files:
1. `title.basics.tsv.gz` (Movie and TV show metadata)
2. `title.akas.tsv.gz` (Localized and alternative titles)
3. `title.crew.tsv.gz` (Directors and writers link)
4. `title.principals.tsv.gz` (Detailed cast and crew roles)
5. `title.ratings.tsv.gz` (User ratings and vote counts)
6. `title.episode.tsv.gz` (TV episode to series mapping)
7. `name.basics.tsv.gz` (Industry personnel metadata)
