# Nexora

**Invest in Tomorrow's Unicorns, Today**

Nexora is a **Web3 solution for early-stage startups** to raise funding through cryptocurrency and find like-minded people who are ready to work in high-potential startups. It is also a platform for **aspiring entrepreneurs** to receive **AI mentorship**, validate their startup journey, and build confidence through resources such as checklists, templates, and quizzes.

---

## 🚀 What Makes Nexora Different?

Unlike platforms like **Upwork**, **Solvearn**, or **Fiverr**, where jobs are posted and people apply passively, **Nexora** is built **for startups, by startups**. It’s not just about getting a job done — it's about:

- 🤝 **Finding investors who believe in your vision**
- 👥 **Connecting with collaborators who want to grow something from zero**
- 🧠 **Receiving AI-powered mentorship**
- 🧰 **Using actionable tools to assess and improve your startup**

---

## 🌟 Features

- 🔍 **Explore Projects**: Discover and fund early-stage startups using Ethereum (ETH).
- 💡 **Create Your Own Project**: Founders can post their startup needs, whether it's hiring, funding, or both.
- 💬 **AI Mentorship & Guidance**: Personalized AI-driven startup advice.
- 📊 **Startup Toolkit**:
  - **Startup Readiness Quiz** — Assess your entrepreneurial preparedness.
  - **Pitch Deck Template** — Downloadable presentation format used by real founders.
  - **Funding Checklist** — Ensure you’re investment-ready.
  - **Market Size Calculator** — Estimate your TAM with clarity.
- 🔗 **Web3-Powered**: Transparent and secure transactions via crypto.
- 🔐 **User Authentication**: Secure sign-in and personalized project management.

---

---

## ⚙️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript (Bootstrap 5)
- **Backend**: Django (Python)
- **Database**: SQLite/PostgreSQL
- **Web3 Integration**: Ethereum smart contract interactions (MetaMask and solidity)
- **Authentication**: Django Auth
- **AI Mentorship**: Groq-based startup guidance with specialized entrepreneur prompts

---

## 🆕 Latest Updates

### Major Platform Improvements (Latest Release)

**🔧 MetaMask Integration Fixes:**

- Fixed modal closing issues after wallet connection
- Resolved button state problems without page reload
- Enhanced wallet connection state management
- Improved error handling and user feedback

**🌐 New Pages Added:**

- **About Page**: Company mission, vision, and values
- **Features Page**: Comprehensive platform capabilities and pricing plans
- **Contact Page**: Contact form, FAQ, and company information

**🤖 Enhanced AI Chatbot:**

- Specialized for entrepreneur mentorship
- Quick action buttons for common startup questions
- Improved UI with professional design
- 24/7 availability for business guidance

**🎨 UI/UX Improvements:**

- Professional design with gradient backgrounds
- Fully responsive across all devices
- Enhanced navigation and footer
- Consistent branding throughout

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js (for frontend dependencies)
- MetaMask browser extension
- Groq API key (for AI chatbot)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Jugadveer/Nexora.git
   cd Nexora
   ```

2. **Set up virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env file with your API keys and configuration
   ```

5. **Run migrations**

   ```bash
   python manage.py migrate
   ```

6. **Start the development server**

   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to `http://localhost:8000`
   - Install MetaMask extension for crypto funding features

### Environment Variables

Create a `.env` file in the root directory with:

```env
GROQ_API_KEY=your_groq_api_key_here
DEBUG=True
SECRET_KEY=your_django_secret_key
```

Get your Groq API key from: https://console.groq.com/

---
