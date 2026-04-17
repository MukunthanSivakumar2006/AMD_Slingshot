<div align="center">

# 🛍️ RetailAI — Intelligent Retail & E-commerce Assistant

**An AI-powered retail system that enhances the shopping experience and optimizes retailer operations using smart recommendations, a chatbot assistant, and real-time inventory intelligence.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask)
![Pandas](https://img.shields.io/badge/Pandas-2.x-darkblue?style=flat-square&logo=pandas)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
- [How to Run](#how-to-run)
- [Pages & Routes](#pages--routes)
- [AI Modules Explained](#ai-modules-explained)
- [Dataset](#dataset)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)

---

## Overview

**RetailAI** is a beginner-friendly, fully modular AI-powered retail prototype built with **Python + Flask**. It simulates a real-world e-commerce store with:

- 🤖 A **recommendation engine** that suggests products based on browsing context
- 💬 A **smart chatbot** that handles customer FAQs and product queries
- 📊 An **inventory intelligence dashboard** that predicts demand and flags stock risks
- 🛒 A **fully functional cart & checkout** with session storage, wishlist, and order confirmation

This project is designed to be **simple, clean, and modular** — perfect as a learning prototype or a starting point for more advanced retail AI systems.

---

## Features

| Feature | Description |
|---|---|
| 🎯 **Personalized Recommendations** | Suggests products from the same category as the currently viewed item |
| 💬 **Smart Chatbot** | Regex-based NLP assistant answering returns, delivery, and product queries |
| 📦 **Inventory Intelligence** | Flags Low Stock, High Demand Risk, and Overstock items from sales data |
| 🛒 **Shopping Cart** | Add, remove, update quantity; auto-calculates subtotal, tax, and total |
| ♡ **Wishlist** | Save items for later; move directly to cart with one click |
| ✅ **Full Checkout Flow** | 3-step form (contact → shipping → payment) with order confirmation page |
| 📱 **Responsive UI** | Clean, modern design with Inter typography, gradients, and micro-animations |

---

## Project Structure

```
retail_app/
│
├── app.py                    # Main Flask app — all routes and session logic
├── requirements.txt          # Python dependencies
│
├── data/
│   ├── products.csv          # Product catalog (10 items across 4 categories)
│   └── sales.csv             # Historical sales data for inventory prediction
│
├── retail_ai/
│   ├── __init__.py
│   ├── recommendation.py     # Category-based product recommendation logic
│   ├── chatbot.py            # Regex + keyword chatbot engine
│   └── inventory.py          # Sales velocity & stock threshold analysis
│
├── templates/
│   ├── layout.html           # Shared base template with navbar
│   ├── index.html            # Storefront with recommendations + product grid
│   ├── product.html          # Product detail page with Add to Cart / Wishlist
│   ├── cart.html             # Shopping cart with item controls & order summary
│   ├── wishlist.html         # Saved items with move-to-cart functionality
│   ├── checkout.html         # 3-step checkout form with payment options
│   ├── confirmation.html     # Order confirmation with reference & summary
│   ├── chat.html             # AI chatbot interface
│   └── inventory.html        # Retailer inventory insights dashboard
│
└── static/
    └── style.css             # Complete custom CSS design system
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, Flask 3.x |
| **Data Processing** | Pandas 2.x |
| **Templating** | Jinja2 (via Flask) |
| **Frontend** | Vanilla HTML5, CSS3 (no frameworks) |
| **Session Storage** | Flask server-side sessions (cookie-based) |
| **Data** | CSV flat files (no external database required) |
| **Fonts** | Google Fonts — Inter |

---

## Installation & Setup

### Prerequisites

Make sure you have **Python 3.10+** installed. You can verify with:

```bash
python --version
```

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AMD_SingleSlot.git
cd AMD_SingleSlot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:

```
flask
pandas
werkzeug
```

> All three are likely already present in a standard Python environment. The install step is instant if they are.

---

## How to Run

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

The Flask development server will auto-reload on file changes. No build step required.

---

## Pages & Routes

| Route | Page | Description |
|---|---|---|
| `GET /` | Storefront | Browse all products + AI recommendations |
| `GET /product/<id>` | Product Detail | Full product info, stock badge, related items |
| `POST /add_to_cart/<id>` | (API) | Add product to session cart via AJAX |
| `GET /cart` | Shopping Cart | View items, adjust quantities, see totals |
| `POST /remove_from_cart/<id>` | (Action) | Remove an item from cart |
| `POST /update_cart/<id>` | (Action) | Update qty (stepper buttons) |
| `GET /checkout` | Checkout | 3-step contact/shipping/payment form |
| `POST /place_order` | (Action) | Submit order, clear cart, redirect to confirmation |
| `GET /order_confirmation` | Confirmation | Order reference, summary, shipping details |
| `POST /add_to_wishlist/<id>` | (API) | Toggle wishlist via AJAX |
| `GET /wishlist` | Wishlist | View and manage saved items |
| `POST /move_to_cart/<id>` | (Action) | Move wishlist item to cart |
| `GET /chat` | Chatbot UI | Interactive AI chat assistant |
| `POST /api/chat` | (API) | Process chatbot query, return response JSON |
| `GET /admin` | Inventory Dashboard | Demand prediction & stock insights for retailers |

---

## AI Modules Explained

### 🎯 `retail_ai/recommendation.py`

Uses **content-based filtering** by category:

1. Identifies the category of the currently viewed product
2. Filters all other products matching that category
3. Falls back to random sampling if there aren't enough category matches
4. Returns up to `N` product suggestions

```python
get_recommendations(products_df, current_product_id=101, limit=3)
```

---

### 💬 `retail_ai/chatbot.py`

A **rule-based NLP engine** using Python `re` (regex):

- Matches user messages to patterns like `return|refund`, `delivery|shipping`, `hello|hi`
- Falls back to a **keyword product search** across the product catalog
- Returns natural language responses with product suggestions when relevant

```python
get_chatbot_response("do you have a smartwatch?", products_df)
# → "I found these products: Smart Watch ($199.99)."
```

**Sample questions to try:**
| Question | Response Type |
|---|---|
| "How do I return an item?" | Return policy FAQ |
| "When will my order arrive?" | Delivery time FAQ |
| "Do you have earbuds?" | Product keyword match |
| "Hello" | Greeting & guide |

---

### 📦 `retail_ai/inventory.py`

Analyzes historical sales against current stock levels using **threshold logic**:

| Condition | Status | Action |
|---|---|---|
| `stock < 10` | 🟡 Low Stock | Reorder soon |
| `total_sold > stock × 0.5` AND `stock < 20` | 🔴 High Demand Risk | Immediate Reorder |
| `stock > 100` AND `total_sold < 5` | 🔵 Overstock | Consider Discount |
| Otherwise | 🟢 Normal | None |

---

## Dataset

Two CSV files power the system — no external database needed.

### `data/products.csv`

| Column | Type | Example |
|---|---|---|
| `product_id` | int | `101` |
| `name` | string | `Smartphone X` |
| `category` | string | `Electronics` |
| `price` | float | `799.99` |
| `stock` | int | `50` |
| `description` | string | `Latest smartphone with AI features` |
| `image_url` | string | Unsplash image URL |

**Categories included:** Electronics · Home & Kitchen · Clothing · Fitness

### `data/sales.csv`

| Column | Type | Example |
|---|---|---|
| `date` | string | `2024-05-01` |
| `product_id` | int | `101` |
| `quantity_sold` | int | `3` |

---

## Future Improvements

| Enhancement | Description |
|---|---|
| 🔐 User Authentication | Login/signup so cart & history persist across sessions |
| 🗄️ Real Database | Replace CSV files with SQLite or PostgreSQL |
| 🤖 ML Recommendations | Replace category-filter with collaborative filtering (scikit-learn) |
| 🧠 NLP Chatbot | Upgrade regex bot with a transformer model (e.g. GPT / Gemini API) |
| 📈 Sales Dashboard | Charts for sales trends using Chart.js |
| 📧 Email Confirmation | Send order confirmation emails via Flask-Mail |
| 🔍 Search | Full-text product search with filtering |
| 💳 Payment Gateway | Integrate Stripe or Razorpay for real payments |

---

## License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

<div align="center">

Built with ❤️ using Python · Flask · Pandas

</div>