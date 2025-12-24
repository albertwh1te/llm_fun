# Report: Quantitative Crypto Strategies using Machine Learning and LLMs (2024-2025)

This report highlights high-quality, recent arXiv papers specifically selected for their relevance to building quantitative trading strategies in the cryptocurrency market using cutting-edge Machine Learning and Large Language Models.
****
---

### 1. MM-DREX: Multimodal-Driven Dynamic Routing of LLM Experts for Financial Trading
*   **Date:** September 2025
*   **Focus:** Multimodal Data (Text + Price) & Dynamic Adaptation

**Why you should read it:**
This is arguably the most practical paper for modern crypto algorithmic trading. Crypto markets are driven heavily by both sentiment (Twitter/X, News) and technical market structure.
*   **Problem Solved:** Most models fail when market regimes change (e.g., from bull to bear). This paper introduces "Dynamic Routing," which treats different LLMs as experts specialized in different market conditions.
*   **Key Innovation:** It doesn't just jam data into one model; it dynamically routes the decision to the "expert" model best suited for the current volatility and news environment.
*   **Relevance:** It specifically validates its approach on cryptocurrency datasets, outperforming 15 baseline models.

**Score: 9.5/10**
*(Must-read for the architecture alone. The concept of "routing" is crucial for building robust production systems.)*

---

### 2. Trade in Minutes! (TiMi): Rationality-Driven Agentic System for Quantitative Financial Trading
*   **Date:** October 2025
*   **Focus:** Autonomous Agents & End-to-End Trading

**Why you should read it:**
If you want to build a system that *acts* rather than just *predicts*, this is your blueprint. "TiMi" represents the shift from "Predictive AI" (forecasting price) to "Agentic AI" (executing strategy).
*   **Problem Solved:** Bridges the gap between raw signals and execution. It uses LLMs not just for sentiment, but for *coding* the strategy and *reasoning* about risk.
*   **Key Innovation:** A multi-agent framework where different agents handle semantic analysis, code generation, and risk control independently but cohesively.
*   **Relevance:** Evaluated on over 200 trading pairs, explicitly including cryptocurrencies. It demonstrates stable profitability, which is rare in academic papers.

**Score: 9.0/10**
*(Excellent for system design. Read this to understand how to structure your software, not just your math.)*

---

### 3. Language Model Guided Reinforcement Learning in Quantitative Trading
*   **Date:** August 2025
*   **Focus:** Hybrid Architecture (LLM + RL)

**Why you should read it:**
Reinforcement Learning (RL) is theoretically perfect for trading but notoriously hard to train (unstable) in practice. This paper uses an LLM to "guide" the RL agent.
*   **Problem Solved:** The "Cold Start" and "Exploration" problems in RL. Instead of the RL agent learning randomly, the LLM provides a high-level observation space (context) that guides the RL agent's learning process.
*   **Key Innovation:** Augmenting the RL observation space with LLM insights. This allows the model to adapt to new market conditions (like a sudden crypto crash) without needing full retraining.
*   **Relevance:** Highly relevant for crypto where "black swan" events are common. The LLM acts as a stabilizer for the RL algorithm.

**Score: 8.5/10**
*(Strong theoretical contribution. Read this if you want to build a sophisticated "self-learning" bot.)*

---

### 4. Can LLM-based Financial Investing Strategies Outperform the Market in Long Run?
*   **Date:** July 2025
*   **Focus:** Critical Evaluation & Backtesting (FINSABER Framework)

**Why you should read it:**
You need a reality check. While the other papers sell the dream, this paper investigates the robustness.
*   **Problem Solved:** Overfitting and "look-ahead bias" are rampant in ML trading papers. This paper critically assesses whether LLM gains persist over long periods and different asset classes.
*   **Key Takeaway:** It suggests that LLM advantages might diminish over time and emphasizes the need for **Regime-Aware Risk Controls**. It highlights that LLMs are great at sentiment but can struggle with precise trend detection compared to traditional quant methods.
*   **Relevance:** Essential for "risk management." It will stop you from losing money on a strategy that only looked good in a backtest.

**Score: 9.0/10**
*(Crucial for not going broke. Read this to learn how to properly backtest your strategy.)*

---

### Summary Recommendation

1.  **Start with TiMi** to understand the *system architecture* of a modern agentic trading bot.
2.  **Read MM-DREX** to understand how to combine *news (sentiment)* with *price (technical)* data effectively.
3.  **Read the "Outperform?" paper** to design your *backtesting engine* and ensure you aren't fooling yourself with lucky results.
