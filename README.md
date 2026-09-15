# day 2

## step 1 - create virtual machine
> python -m venv .venv

## step 1.1

## step 2 - install dependencies / python libaries
> touch requirements.txt
in the requirments.txt write (copy/paste):

openai
streamlit
python-dotenv

> pip install -r requirments.txt

## step 3 - create .env file
>touch .env
put the OPENAI_API_KEY

## step 4 - create python file entry point
>touch home.py
add these:

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv() 



## step x - save file

