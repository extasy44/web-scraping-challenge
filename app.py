from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

Table to create

country: id, name
discipline: id, discpline, event, country
athlete: id, name, FK: country.id FK: discipline.id
coaches: id, name, FK: country.id FK: discipline.id
country_displine
displine_athlethe

