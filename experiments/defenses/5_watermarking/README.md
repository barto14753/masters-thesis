# TODO - AI Rhyme Generator with Digital Watermarking

## Overview

This project is an **AI-powered rhyme generator** that ensures authorship using **invisible watermarking**.  
It provides:

- **Secure user authentication** (Basic Auth)
- **Digital watermark embedding** (encoded in whitespace)
- **Rhyme validation** (to verify authorship)

## 📌 Architecture

```mermaid
graph TD;
    User -->|POST /rhyme| FlaskServer;
    FlaskServer -->|Generate rhyme| OllamaModel;
    OllamaModel -->|Rhyme with <WATERMARK>| FlaskServer;
    FlaskServer -->|Return response| User;
    User -->|POST /validate| FlaskServer;
    FlaskServer -->|Extract & verify watermark| WatermarkModule;
    WatermarkModule -->|Return metadata| FlaskServer;
    FlaskServer -->|Validation result| User;
```
