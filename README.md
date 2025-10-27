# 💬 ChatSight — WhatsApp Chat Analyzer



> **Turn your WhatsApp chats into beautiful, interactive insights with timelines, word clouds, emoji analysis, and more! Effortless, private, and mobile-friendly.** 🚀📊😊

---

## 🌐 Live Demo

🔗 [Open App on Streamlit Cloud](https://chatsight.streamlit.app/)

*(<img width="2790" height="972" alt="image" src="https://github.com/user-attachments/assets/33a619e0-a467-4475-b432-7808fd338fe8" />
)*

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Folder Structure](#-folder-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Features

| Feature                | Description                                                                   |
|------------------------|-------------------------------------------------------------------------------|
| 📊 Timeline Charts     | Visualize chat activity by day and month                                      |
| 👥 User Leaderboard    | See who sends the most messages                                               |
| 😊 Emoji & Word Stats  | Discover top emojis, word clouds, and most common words                       |
| 🔥 Activity Heatmaps   | Analyze busiest days, peak times, and weekly chat rhythms                     |
| 🎚 Display Slider      | Choose how many top words, emojis, or users to show dynamically               |
| 📱 Responsive Design   | Works smoothly on mobile, tablet, and desktop                                 |
| 🛡️ Privacy-Friendly    | All analysis runs locally—no chat data is uploaded or stored anywhere else    |

---

## 🛠 Tech Stack

| Technology    | Purpose                           |
|---------------|-----------------------------------|
| Streamlit     | Web app and interactive UI        |
| Python        | Data processing & backend logic   |
| Pandas        | Data manipulation                 |
| Matplotlib    | Charts and plotting               |
| Seaborn       | Heatmaps and stylish charts       |
| wordcloud     | Word cloud generation             |
| emoji         | Emoji extraction & analysis       |
| urlextract    | URL finding                       |
| plotly        | (Optional) Interactive charts     |

---

## 📝 Getting Started

### 1. **Export Your WhatsApp Chat**

- In WhatsApp, open the group or personal chat.
- Tap on `⋮` > `More` > `Export chat` > Choose `Without Media`.
- Email or transfer the `.txt` file to your computer.

### 2. **Clone & Setup**

- git clone https://github.com/Ayush-Raj189/whatsapp-chat-analyzer.git
- cd whatsapp-chat-analyzer
- pip install -r requirements.txt
- streamlit run app.py


---

## 🚦 Usage

1. **Upload** your WhatsApp chat `.txt` file in the sidebar.
2. **Select** a user or "Overall" for group-wide stats.
3. **Click** "Show Analysis" to generate:
   - Timelines, most active users, word clouds, emoji pie charts, heatmaps, and more.
4. Use the **display count slider** to control how many top items to show in charts.
5. Enjoy reviewing your interactive insights!

---

## 👥 Contributing

Pull requests and feature suggestions are welcome!  
- Fork this repo and propose your changes.
- Please write clear commit messages and keep your code clean.

---

**Made with ❤️ by [Ayush](https://github.com/Ayush-Raj189)**  
*Analyze, visualize, celebrate your chats!*



