# MedscanRx

MedscanRx is a healthcare project designed to minimize medication errors by scanning prescriptions or medication packaging and retrieving drug information from the OpenFDA database. It processes medical images, extracts text, and queries drug information in a seamless workflow that combines OCR technology with healthcare APIs.

## Table of Contents
- [Features](#features)
- [Technologies](#technologies)
- [Architecture](#architecture)
- [Future Enhancements](#future-enhancements)

## Features

- **OCR-based Prescription Scanning**: Upload scanned images of prescriptions or medication labels.
- **Drug Information Retrieval**: Query drug data from the OpenFDA database based on scanned labels.
- **User Authentication**: Secure login and authentication for different users.
- **Image Processing**: Efficient image analysis and text extraction from medical packaging.
- **Error Management**: Helps prevent medication errors through cross-referencing medication details.

## Technologies

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **OCR**: EasyOCR for optical character recognition
- **API**: OpenFDA for drug information
- **Frontend**: React 

## Architecture

The project follows a modular architecture with the following components:
- **FastAPI Backend**: Handles authentication, image processing, and communication with the OpenFDA API.
- **Image Preprocessing pipeline: Preprocesses te image before feeding it to ocr module to boost the ocr performance
- **OCR Module**: Extracts text from uploaded images using EasyOCR.
- **Database**: Stores user data and scanned drug details in a PostgreSQL database hosted on AWS RDS.
  

## Future Enhancements

- **Mobile App**: Developing a mobile app for easy access and on-the-go scanning.
- **AI-based Drug Interaction Warnings**: Implementing AI models to predict and warn about potential drug interactions.
- **Medication Reminder System**: Adding a feature that alerts users to take their medications at scheduled times.
- **Improving performance of OCR by using Tessaract.

