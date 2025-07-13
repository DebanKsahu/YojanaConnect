# YojanaConnect

YojanaConnect is a smart backend platform that empowers users to easily discover, match, and interact with Indian government schemes. By leveraging advanced AI, semantic search, and user profiling, YojanaConnect helps citizens find the most relevant welfare schemes based on their unique needs and eligibility. The platform offers secure authentication, personalized recommendations, and a conversational Q&A interface to make government benefits more accessible and understandable for everyone.

Whether you are a citizen looking for support, a social worker assisting others, or a developer building civic tech, YojanaConnect provides robust APIs and a modern backend to power your solutions.

---

## ✨ Features

- **User Authentication:** Secure signup and login with JWT-based authentication.
- **Profile Management:** Edit personal details and eligibility criteria.
- **Scheme Discovery:** Upload, store, and search government schemes using semantic search.
- **Personalized Matching:** AI-powered matching of user profiles to eligible schemes.
- **Conversational Q&A:** Ask questions about schemes and get context-aware answers.
- **Modern Stack:** Built with FastAPI, SQLModel, Qdrant, LangChain, and Google Gemini.

---

## 🖥️ Frontend

Looking for the frontend? Check out the YojanaConnect frontend repository here:  
[Frontend Repository](https://github.com/KrishnaKalra/yojna-connect-frontend)

---

## 🌐 Live Demo

Try the deployed project here:  
[Live Project Site](https://yojna-connect-frontend.vercel.app/)

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

**Made with ❤️ for public use.**