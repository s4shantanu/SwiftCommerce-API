# 🚀 SwiftCommerce-API

SwiftCommerce-API ek modern, high-performance E-commerce backend hai jise **FastAPI**, **PostgreSQL**, **Redis**, aur **GraphQL** ka upyog karke banaya gaya hai. Ye project scalability aur speed ko dhyan mein rakh kar design kiya gaya hai.

---

## ✨ Features

* **🔒 Secure Authentication:** JWT based login aur Bcrypt password hashing.
* **⚡ High Performance:** Redis caching ka use karke products load karne ki speed 100x fast.
* **📡 Hybrid API:** REST endpoints ke saath-saath **GraphQL (Graphene)** integration.
* **🗄️ Async Database:** SQLAlchemy 2.0 aur `asyncpg` ke saath fully asynchronous operations.
* **💳 Payments:** Stripe integration checkout sessions handle karne ke liye.
* **📜 Auto-Migrations:** Alembic ka upyog karke database schema management.

---

## 🛠️ Tech Stack

| Technology | Usage |
| :--- | :--- |
| **FastAPI** | Web Framework |
| **PostgreSQL** | Primary Database |
| **Redis** | Caching Layer |
| **Graphene** | GraphQL Framework |
| **SQLAlchemy** | Async ORM |
| **Stripe** | Payment Gateway |

---

python3 -m alembic upgrade head