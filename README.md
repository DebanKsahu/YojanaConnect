# YojanaConnect

YojanaConnect is an intelligent platform designed to help users discover, match, and interact with Indian government schemes. Leveraging advanced AI and vector search, it personalizes scheme recommendations and provides a conversational Q&A interface for users.

---

## ✨ Features

- **User Authentication:** Secure signup and login with JWT-based authentication.
- **Profile Management:** Edit personal details and eligibility criteria.
- **Scheme Discovery:** Upload, store, and search government schemes using semantic search.
- **Personalized Matching:** AI-powered matching of user profiles to eligible schemes.
- **Conversational Q&A:** Ask questions about schemes and get context-aware answers.
- **Modern Stack:** Built with FastAPI, SQLModel, Qdrant, LangChain, and Google Gemini.

---

## 🚀 Quickstart

### 1. **Clone the Repository**

```sh
git clone https://github.com/your-org/yojanaconnect.git
cd yojanaconnect
```

### 2. **Install [uv](https://github.com/astral-sh/uv) (if not already installed)**

```sh
pip install uv
```

### 3. **Install Dependencies**

```sh
uv sync
```

### 4. **Set Up Environment Variables**

Create a `.env` file in the project root with the following keys:

```
GOOGLE_API_KEY=your_google_api_key
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_CLUSTER_URL=your_qdrant_url
ALGORITHM=HS256
SECRET_KEY=your_secret_key
DATABASE_NAME=your_db_name
HOST=your_db_host
PASSWORD=your_db_password
USERNAME=your_db_username
DATABASE_URL=your_db_url
TESTING_DATABASE_URL=your_testing_db_url
```

### 5. **Run the Application**

```sh
uvicorn main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

---

## 🛠️ Project Structure

```
.
├── Auth/                 # Authentication logic
├── Dashboard/            # User profile and scheme dashboard
├── Database/             # ORM models and vector DB integration
├── Http_Exceptions/      # Custom HTTP exceptions
├── utilities/            # Utility functions
├── main.py               # FastAPI entrypoint
├── config.py             # Settings management
├── pyproject.toml        # Project metadata & dependencies
└── README.md             # You're here!
```

---

## 📚 API Overview

- **Auth:** `/auth/login`, `/auth/signup`
- **Profile:** `/profile`, `/profile/edit`, `/profile/criteria`, `/profile/add_criteria`, `/profile/edit_criteria`
- **Schemes:** `/scheme/add_scheme`, `/scheme/show_all`, `/scheme/{scheme_id}`

Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📝 License

MIT License. See [LICENSE](LICENSE) for details.

---

**Made with ❤️ for public