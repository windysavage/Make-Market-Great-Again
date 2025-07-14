# Make Market Great Again 🇺🇸📈

AI-powered monitoring system that tracks Trump's Truth Social posts and alerts subscribers when posts might impact the stock market.

## Overview

When Trump posts something that could move markets, our AI agent analyzes the content and automatically sends email alerts to subscribers. Perfect for getting ahead of market volatility caused by unexpected political statements.

## Features

- 🔍 **Truth Social monitoring** via Dagster scheduled jobs  
- 🤖 **AI analysis** of potential market impact using AI agent
- 📧 **Instant email alerts** to subscribers

## Quick Start

```bash
git clone https://github.com/windysavage/Make-Market-Great-Again
cd Make-Market-Great-Again

# Copy env template and configure
cp .env.template .env
vim .env  # or use any editor

# Build images
make build

# Start all services
make up

# Access API container shell
make shell
```

## Services

- **FastAPI**: `http://localhost:8888` – Subscription management  
- **Dagster**: `http://localhost:3000` – Job monitoring  

## How It Works

1. **Monitor**: Dagster continuously watches Trump's Truth Social posts  
2. **Analyze**: AI agent evaluates potential market impact  
3. **Alert**: Automatic email notifications sent to subscribers when significant impact detected  

## Use Case

Stay ahead of market volatility by getting early warnings when Trump's posts might affect stock prices. Ideal for day traders and investors who want to react quickly to political market movers.

## LLM Provider Support

Currently, the system supports the following LLM providers as an AI agent:

- [x] OpenAI (`gpt-4`, `gpt-3.5-turbo`, etc.)
- [ ] Local models (planned)

---

**Disclaimer**: For informational purposes only. Not financial advice.
