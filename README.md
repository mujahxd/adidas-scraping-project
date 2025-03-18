# Adidas Product Scraper

## 📌 Project Overview
This Python script scrapes Adidas product data from the Adidas Indonesia website using **GraphQL API**. It extracts SKUs from category pages, retrieves detailed product information, and saves the data into a CSV file.

## 🚀 Features
- **Multi-page scraping**: Extracts SKUs from multiple category pages.
- **Product details retrieval**: Fetches name, price, launch date, description, and product links.
- **HTML entity handling**: Converts special characters (e.g., `&#039;` → `'`).
- **Newline formatting**: Cleans up `\r\n\r\n` and excess spaces.
- **Rate limiting**: Prevents request throttling by introducing delays.
- **UTF-8 CSV Export**: Saves structured data in `products.csv`.

## 📂 Output Format
The script generates a CSV file with the following columns:

| Product ID | SKU   | Name       | Regular Price | Final Price | Launch Date | Link Product | Description |
|------------|------|------------|--------------|------------|--------------|--------------|-------------|
| 1234567    | IF0704 | Adidas Running Shoes | 1500000 | 1200000 | 2024-03-01 | [Link](https://www.adidas.co.id/IF0704.html) | High-performance running shoes. |

## 🛠️ Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/adidas-scraping-project.git
cd adidas-scraping-project
```

## Install Dependencies
```bash
pip install curl_cffi
```
## Run the Script
```bash
python main.py
```

## How It Works
1. Scrapes category pages to get SKUs.
2. Fetches product details from Adidas GraphQL API.
3. Cleans up text formatting (HTML entities, extra newlines).
4. Saves the final data into a structured products.csv file.

## 📌 Configuration
```python
scrape_adidas(max_pages=3, rate_limit=2)  # Change max_pages and rate_limit as needed
```
