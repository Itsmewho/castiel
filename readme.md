## Overview

This plan aims to leverage APIs to fetch financial data (13-F-HR filings, 10-Q, and 10-K reports) for three companies: Renaissance Technologies, Bridgewater Associates, and Robotti Company.
The data will be processed, sorted, and analyzed to identify the top-performing companies and perform due diligence calculations.
The results will be stored in MongoDB collections and Redis will be used for caching and deduplication.
The login system belongs to my boilerplate and can be used when the application is ready.

---

## Step 1: Fetch 13-F-HR Filings

1. **Fetch Data**:
   - Use APIs to retrieve the last 3 years of 13-F-HR filings for the three companies.
   - APIs should include data such as:
     - Company name.
     - Filing date.
     - Top 30 holdings (company name, price per share, amount, and percentage growth).
2. **Process Data**:
   - Sort data to identify the top-performing 30 companies in each filing.
   - Calculate percentage growth over the last 3 years or since the first entry.
3. **Store Data**:
   - Use Redis to cache API responses and deduplicate requests.
   - Save processed data in MongoDB collections for each company.
   - Implement a rolling window:
     - Check weekly for new 13-F-HR filings.
     - If a new filing is found, pop the oldest entry and add the latest filing.
     - If the company already exists in the collection, update the data and trigger a popup notification.

---

## Step 2: Fetch 10-Q and 10-K Reports

1. **Identify Companies**:
   - From the top-performing companies identified in Step 1, fetch the last 10 years of 10-Q and 10-K reports.
2. **Fetch Data**:
   - Use APIs to retrieve the data.
   - Extract key financial metrics and raw data for analysis.
3. **Process Data**:
   - Sort data into NumPy arrays or DataFrames for analysis.
   - Perform additional sorting and categorization:
     - Create two copies of the data:
       - One for performing due diligence.
       - One for calculating famous financial ratios (P/B, P/E, PEG, etc.).
4. **Special Case Handling**:
   - If a company has made its first real profit in the last year:
     - Add its data to a `starting_profit` MongoDB collection.
     - Trigger a popup notification with a "Read Data" button to generate a PDF summary.

---

## Step 3: Due Diligence and Analysis

1. **Perform Due Diligence**:
   - Use one copy of the 10-Q and 10-K data to calculate:
     - Year-over-year growth.
     - Famous financial ratios (P/B, P/E, PEG, etc.).
2. **Store Results**:
   - Save the processed data, ratios, and year-over-year changes in a MongoDB collection named `top_companies`.
   - Implement a rolling window to remove data older than 3 years and update existing company data when new information is added. Trigger a popup notification for updates.

---

## Step 4: Sentiment Analysis for News Articles

1. **Identify News Sources**:
   - Use APIs to fetch news articles for companies in the `top_companies` collection.
   - Fetch articles related to quarterly filings or financial performance.
2. **Perform Sentiment Analysis**:
   - Categorize news sentiment as:
     - Highly Positive, Positive, Neutral, Negative, Highly Negative, or Conservative.
3. **Store Results**:
   - Aggregate sentiment data and store it in MongoDB, linked to the respective companies.
   - Trigger popup notifications when significant sentiment changes are detected.

---

## Step 5: Visualization and Reporting

1. **Generate Summary Files**:
   - Create a file for each company with:
     - Data columns.
     - Ratios.
     - Year-over-year percentage changes.
     - A graph showing the stock's historical price with filing dates marked.
   - Store these files in the `top_companies` MongoDB collection.
2. **Trigger Notifications**:
   - Whenever the `top_companies` collection is updated:
     - Trigger a popup notification.
     - Provide an option to "Read Data" and display a PDF summary.

---

## Step 6: Implementation Details

1. **Folder Structure**:

   - `analysis/`:
     - `ratios.py`: Calculate financial ratios.
     - `due_diligence.py`: Perform due diligence calculations.
   - `api/`:
     - `fetch_10q_10k.py`: Get finacial data.
     - `fetch_30f.py`: Fetch 30f filings.
     - `fetch_news.py`: Fetch corresponding news.
   - `connection/`:
     - `connect_db.py`: Connect MONGO_DB.
     - `connect_redis.py`: Connect Redis.
   - `data/`:
     - `jsons`: For seeding MONGO_DB.
   - `db/`:
     - `audit.py`: For the audits_logs.
     - `db_operations.py`: MongoDB operations.
     - `redis_operations.py`: Redis caching operations.
   - `login/`:
     - `login.py`: For main login logic.
     - `reset_pass.py`: For resseting password.
     - `unlock_account.py`: For unlocking account.
   - `models`:
     - `all_models.py`: For checking input data?.
   - `sentiment/`:
     - `news_sentiment.py`: Perform sentiment analysis on news articles.
   - `support/`:
     - `readme.md`: Read for use of folder.
   - `utils/`:
     - `auth.py`: Authentication.
     - `helpers.py`: Commonly used functions.
     - `sendmail.py`: For sending emails.
     - `session.py`: For session record.
   - `visualization/`:
     - `generate_summary.py`: Generate files and graphs.
   - `main.py`: Entry point for running the entire pipeline.
   - `admin_creation.py`: For data seeding the admin and admin_log JSON's.
   - `backend.py`: For Flask.
   - `secret_key.py`: For generating a random key.
   - `seeder.py`: For seeding MONGO_DB.
   - `celery_app.py`: Make celery and logging.
   - `celery_config.py`: Config file for schedule API .
   - `tasks.py`: For task functions celery.

2. **Tools**:

   - Bycript for passwords.
   - SHA-256 for hashing data.
   - Itsdangerous for serializer.
   - Smtplib for sending emails.
   - Celery for Redis caching.
   - NumPy for data processing and calculations.
   - Matplotlib or Plotly for graph generation.
   - ReportLab or FPDF for PDF summaries.
   - Flask for serving popups and notifications (if needed).
   - For more tools see requirements.txt

---

## Step 7: Testing and Validation

1. **Testing**:
   - Validate API connections and data fetching.
   - Test sorting and processing logic with sample data.
   - Ensure Redis and MongoDB integration work as expected.
2. **Validation**:
   - Compare calculated financial ratios with known benchmarks.
   - Verify data consistency and accuracy.

---

## Deliverables

1. Fully functional system for fetching, processing, and storing financial data.
2. Interactive visualizations and reports.
3. Notifications for new entries in MongoDB collections.
4. Clear documentation of the pipeline and its usage.
   """
