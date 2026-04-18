# 💸 VibePay

VibePay is an intelligent, natural-language expense tracker built for the **PromptWars challenge**. Instead of manually selecting categories, dates, and amounts from dropdown menus, users can simply type what they spent (e.g., *"Bought groceries worth 800 rupees at D-Mart"*), and the AI automatically categorizes and logs the transaction.

## ✨ Features
* **Natural Language Processing:** Powered by `gemini-2.5-flash` to extract Amount, Category, Vendor, and Date from plain text.
* **Premium Dashboard:** A clean, vibrant UI built with Streamlit, featuring real-time metric cards.
* **Interactive Visualizations:** Beautiful donut charts powered by Altair to visualize spending allocations.
* **Data Management:** Instantly clear the ledger or export all your tracked expenses to a CSV file.
* **Quick Actions:** Sidebar shortcuts for frequent expenses (Coffee, Fuel, Groceries).

## 🚀 Example Prompts to Try
You can copy and paste these prompts into the app to see the AI extraction in action:

1. **Transport / Fuel**
   > *"Just filled up the car with 2000 rupees of petrol at Shell."*
   *(Extracts: Transport, Shell, 2000)*
   
2. **Utilities & Past Dates**
   > *"Paid my electricity bill of 3200 rupees to Bescom yesterday."*
   *(Extracts: Utilities, Bescom, 3200, yesterday's date)*
   
3. **Entertainment**
   > *"Bought two movie tickets for 800 rupees at PVR Cinemas."*
   *(Extracts: Entertainment, PVR Cinemas, 800)*
   
4. **Food & Groceries**
   > *"Grabbed some groceries from D-Mart for 450 rupees this morning."*
   *(Extracts: Food & Dining, D-Mart, 450)*

## 🛠️ Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tejas-18/VibePay.git
   cd VibePay
   ```

2. **Set up a virtual environment and install dependencies:**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate   # On Windows
   pip install -r requirements.txt
   ```

3. **Configure your API Key:**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

4. **Run the app:**
   ```bash
   streamlit run main.py
   ```

## ☁️ Deployment (Google Cloud Run)

This project is fully Dockerized and ready to be deployed to Google Cloud Run. 

**Steps to deploy via GitHub:**
1. Navigate to the Google Cloud Console and select **Cloud Run**.
2. Click **Deploy Container** > **Continuously deploy from a repository**.
3. Select your connected GitHub repository (`tejas-18/VibePay`).
4. Set the Build Type to **Dockerfile**.
5. *Important:* Make sure to add your `GOOGLE_API_KEY` as an environment variable in the Cloud Run deployment settings!
6. Deploy! Google Cloud Run automatically routes traffic to port `8080` (as defined in the Dockerfile).

## 🧰 Tech Stack
* **Frontend/UI:** Streamlit, Altair
* **AI/LLM:** Google Generative AI (`gemini-2.5-flash`)
* **Data Processing:** Pandas
* **Deployment:** Docker, Google Cloud Run
