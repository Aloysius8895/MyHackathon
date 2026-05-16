import sys
import os
import time
import streamlit as st
import pandas as pd
import yfinance as yf
import re

# Ensure project root is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from orchestration.main_adk import StockOrchestrator

REGION_SUFFIXES = {
    "": "USA",
    ".NS": "India",
    ".L": "UK",
    ".DE": "Germany",
    ".T": "Japan"
}

def clean_text(text):
    # Remove markdown formatting, extra spaces, line breaks
    text = re.sub(r'[_*`~]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def render_news(news_data):
    if isinstance(news_data, list) and news_data:
        for item in news_data:
            title = clean_text(item.get("title", ""))
            summary = clean_text(item.get("summary", item.get("description", "")))
            link = item.get("link", item.get("url", ""))

            clamped_title = title if len(title) <= 80 else title[:77] + "..."
            clamped_summary = summary if len(summary) <= 200 else summary[:197] + "..."

            st.markdown(f"""
            <div style="padding: 10px; background-color: #1f2330; border-radius: 8px; margin-bottom: 10px;">
                <h4 style="margin: 0;">🔹 {clamped_title}</h4>
                <p style="font-size: 14px; color: #ddd;">{clamped_summary}</p>
                {'<a href="' + link + '" target="_blank" style="color:#38a;">🔗 Read More</a>' if link else ''}
            </div>""", unsafe_allow_html=True)
    else:
        # Fall back for string or unexpected types
        if isinstance(news_data, str) and news_data.strip():
            st.markdown(f"📝 *{clean_text(news_data)}*")
        else:
            st.info("No recent news found.")

def find_global_ticker(ticker: str):
    for suffix, region in REGION_SUFFIXES.items():
        full_ticker = ticker + suffix
        try:
            data = yf.Ticker(full_ticker).info
            if data and data.get("regularMarketPrice") is not None:
                return full_ticker, region, data.get("currency", "USD")
        except Exception:
            continue
    return None, None, None

def interpret_volume(volume):
    try:
        volume = int(volume)
        if volume > 50_000_000:
            return f"{volume:,} (📈 High)"
        elif volume > 10_000_000:
            return f"{volume:,} (↗️ Moderate)"
        else:
            return f"{volume:,} (📉 Low)"
    except (ValueError, TypeError):
        return "N/A"

def display_real_time_data(data: dict):
    price = data.get("price", "N/A")
    currency = data.get("currency", "")
    updated_at = data.get("updated_at", "N/A")
    volume = data.get("volume", "N/A")
    st.metric("Price", f"{price} {currency}")
    st.metric("Volume", f"{volume}")
    st.caption(f"Last updated at: {updated_at}")

def main():
    st.set_page_config(page_title="AI Stock Analyst", layout="wide")

    # 🔹 Project Title & Subtitle
    st.title("📊 AI Stock Analyst Dashboard")
    st.caption("Powered by multi-agent AI for real-time stock insights and portfolio strategy.")

    # Sidebar configuration
    with st.sidebar:
        region = st.selectbox("Region", ["USA", "India", "UK", "Germany", "Japan"])
        st.header("Configuration")
        ticker = st.text_input("Stock Ticker", "AAPL").upper()
        risk_profile = st.selectbox("Risk Profile", ["low", "medium", "high"])

    orchestrator = StockOrchestrator()

    if st.button("Analyze"):
        with st.spinner("Running analysis..."):
            start_time = time.time()
            analysis = orchestrator.full_analysis(ticker, risk_profile, region)

            # Check if no valid price; try fallback
            if not analysis["real_time_data"].get("price"):
                fallback_ticker, detected_region, currency = find_global_ticker(ticker)
                if fallback_ticker:
                    if detected_region != region:
                        st.warning(
                            f"⚠️ The stock '{ticker}' appears to be listed under region '{detected_region}', "
                            f"but you selected '{region}'. Please switch the region to '{detected_region}' and try again."
                        )
                        return
                    else:
                        ticker = fallback_ticker
                        region = detected_region
                        analysis = orchestrator.full_analysis(ticker, risk_profile, region)
                        if not analysis["real_time_data"].get("price"):
                            st.error("❌ Could not fetch valid data even after region detection.")
                            return
                else:
                    st.error("❌ Could not find this stock in any supported exchange.")
                    return

            exec_time = time.time() - start_time
            col1, col2 = st.columns(2)

            with col1:
                with st.expander("📊 Real-Time Data", expanded=True):
                    if "volume" in analysis["real_time_data"]:
                        analysis["real_time_data"]["volume"] = interpret_volume(analysis["real_time_data"]["volume"])
                    display_real_time_data(analysis["real_time_data"])
                    st.caption(f"🌍 Stock detected in {region} exchange | Currency: {analysis['real_time_data'].get('currency', '')}")

                with st.expander("📈 Technical Analysis", expanded=True):
                    price_df = pd.DataFrame(analysis["technical_analysis"]["prices"])
                    if not price_df.empty and "date" in price_df.columns:
                        st.line_chart(price_df.set_index("date")["price"])
                        st.metric("RSI", f'{analysis["technical_analysis"]["rsi"]}')
                        st.metric("Volatility", f'{analysis["technical_analysis"]["volatility"]}%')

                        st.markdown("### 📉 Moving Averages")
                        ma_data = analysis["technical_analysis"].get("moving_averages", {})
                        cols = st.columns(len(ma_data) if ma_data else 1)
                        for i, (period, value) in enumerate(ma_data.items()):
                            with cols[i]:
                                st.metric(label=f"{period} Avg", value=f"{value:.2f}")
                    else:
                        st.warning("📉 No trend data available for this ticker and region.")

            with col2:
                with st.expander("📰 Latest News", expanded=True):
                    render_news(analysis.get("news_summary", []))

                with st.expander("🤖 AI Recommendations", expanded=True):
                    st.write(analysis["ai_insights"])
                    st.write("📁 Portfolio Suggestion")
                    st.write(analysis["portfolio_recommendation"])

            st.caption(f"✅ Analysis completed in {exec_time:.2f} seconds")

if __name__ == "__main__":
    main()