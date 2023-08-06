# SCOTUS Data Tools

Welcome to SCOTUS Data Tools and Utils!  This is a work in progress.

## Intro & Objectives

The primary purpose of this package is to create a set of tools that is capabile of:

+ Retrieving base SCOTUS data (e.g. case texts from https://www.supremecourt.gov/opinions/boundvolumes.aspx and case transcriptions from http://www.scotusblog.com/case-files/terms/)
+ Retrieving auxiliary SCOTUS data (not sure what this includes yet?)
+ Extracting & Segmenting texts from source documents
    + For Bound Volumes, this means extracting text from PDF and segmenting by case
    + Transcripts may involve getting the text from the PDFs and segmenting by speaker, perhaps
    + Other sources may have more involved extraction / processing requirements
+ Providing basic tools for storing the "core" extracted data in an easily accessible -- from a Data Science perspective -- format
    + Further work may perhaps involve providing tools for easily accessing the data in a more "user friendly" manner
+ Linking the data extracted from various sources
    + by Case
    + by SCOTUS Justices
    + other "indicies"
