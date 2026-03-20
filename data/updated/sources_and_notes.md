# LLM Pricing & Benchmark Data - Sources and Notes

**Data collected:** March 20, 2026
**Coverage period:** Models released or with price changes after February 2025, up to March 2026

---

## Pricing Formula

**Weighted Avg Price (USD/1M tokens) = (3 * input_price + 1 * output_price) / 4**

This weights input tokens 3:1 vs output tokens, reflecting typical API usage patterns where input tokens significantly outnumber output tokens.

---

## Pricing Sources

### OpenAI Models
- **Primary source:** [OpenAI API Pricing](https://openai.com/api/pricing/) and [OpenAI Developer Docs Pricing](https://developers.openai.com/api/docs/pricing)
- **Cross-referenced with:** [PricePerToken.com - OpenAI](https://pricepertoken.com/pricing-page/provider/openai)
- GPT-4.5: $75/$150 per MTok (input/output) - confirmed via multiple sources. Model deprecated July 14, 2025.
- GPT-4.1: $2/$8 per MTok
- GPT-4.1 mini: $0.40/$1.60 per MTok (originally reported as $0.20/$0.80 at some providers; used $0.40/$1.60 from community discussions noting identical pricing with o3 standard tier)
- GPT-4.1 nano: $0.10/$0.40 per MTok
- o3 (standard): $2.00/$8.00 per MTok
- o3-pro: $20.00/$80.00 per MTok
- o4-mini: $1.10/$4.40 per MTok

**Note on GPT-4.1 mini pricing:** Confirmed at $0.40/$1.60 per MTok via official OpenAI developer docs (platform.openai.com/docs/models/gpt-4.1-mini). Some third-party trackers previously listed $0.20/$0.80 but the official pricing is $0.40/$1.60.

**Note on o4-mini pricing:** Some sources report $0.55/$2.20 for standard o4-mini and $2.00/$8.00 for o4-mini-deep-research. Used $1.10/$4.40 as the standard o4-mini pricing based on cross-referencing multiple sources.

### Anthropic Models
- **Primary source:** [Anthropic Claude API Pricing](https://platform.claude.com/docs/en/about-claude/pricing) (fetched March 2026)
- Claude 3.5 Haiku: $0.80/$4.00 per MTok (unchanged since Nov 2024 release; Anthropic official is $0.80/$4.00)
- Claude 3.7 Sonnet: $3/$15 per MTok (released Feb 24, 2025; now deprecated)
- Claude Sonnet 4: $3/$15 per MTok (released May 22, 2025)
- Claude 4.5 Sonnet: $3/$15 per MTok (released Sep 29, 2025)
- Claude Opus 4: $15/$75 per MTok (released May 22, 2025)

**Note:** Claude Opus 4 pricing ($15/$75) differs from later Claude Opus 4.5 ($5/$25). The Opus 4 price was later superseded by cheaper Opus 4.5. The pricing table from Anthropic's current page lists both.

### Google Models
- **Primary source:** [Google Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing) (fetched March 2026)
- Gemini 2.0 Flash: $0.10/$0.40 per MTok (deprecated, shutting down June 1, 2026)
- Gemini 2.5 Pro: $1.25/$10.00 per MTok (for prompts <= 200k tokens)
- Gemini 2.5 Flash: $0.30/$2.50 per MTok

### Meta / Llama Models (open-source, pricing via API providers)
- **Source:** [Artificial Analysis - Llama 4 Maverick](https://artificialanalysis.ai/models/llama-4-maverick), [OpenRouter](https://openrouter.ai/meta-llama/llama-4-maverick), provider pricing pages
- Llama 4 Scout: ~$0.15/$0.40 per MTok (median across providers; Fireworks: $0.12/$0.35, Groq: $0.11/$0.34)
- Llama 4 Maverick: ~$0.27/$0.85 per MTok (median across providers)
- **Note:** Llama 4 is open-source; prices vary by hosting provider. Used representative median values.

### DeepSeek Models
- **Source:** [DeepSeek API Pricing](https://api-docs.deepseek.com/quick_start/pricing), [PricePerToken](https://pricepertoken.com/pricing-page/provider/deepseek)
- DeepSeek-V3-0324: $0.27/$1.10 per MTok (via DeepSeek API; released March 24, 2025)
- DeepSeek-R1: $0.55/$2.19 per MTok (cache miss pricing; as of Sep 2025 updated to $0.56/$1.68)
- **Note:** DeepSeek uses a cache-hit/miss pricing model. Used cache-miss (standard) pricing. Prices were updated in September 2025.

### Mistral
- **Source:** [Artificial Analysis - Mistral Large 3](https://artificialanalysis.ai/models/mistral-large-3), [Mistral AI announcement](https://mistral.ai/news/mistral-large)
- Mistral Large 3: $0.50/$1.50 per MTok (released December 2, 2025; 675B total params, 40B active MoE)

### Alibaba / Qwen
- **Source:** [Alibaba Cloud Model Studio Pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing), [PricePerToken - Qwen3 Max](https://pricepertoken.com/pricing-page/model/qwen-qwen3-max)
- Qwen3-235B-A22B (via Qwen Max API): ~$0.78/$3.90 per MTok
- **Note:** Qwen3 is open-source; Alibaba Cloud "Qwen Max" pricing used. Third-party providers may differ.

### xAI / Grok
- **Source:** [xAI Models and Pricing](https://docs.x.ai/developers/models), web search cross-references
- Grok 3: $3.00/$15.00 per MTok
- Grok 3 mini: $0.30/$0.50 per MTok
- **Note:** xAI has since released Grok 4 and the docs page primarily shows Grok 4 pricing. Grok 3 pricing taken from launch-era sources (Feb-Apr 2025).

---

## Benchmark Sources

### OpenAI Models (GPT-4.5, GPT-4.1 family, o3, o4-mini)
- **Primary source:** [OpenAI simple-evals GitHub](https://github.com/openai/simple-evals) - provides MMLU, GPQA, HumanEval, MATH scores
- **Cross-referenced with:** [OpenAI GPT-4.1 announcement](https://openai.com/index/gpt-4-1/), [OpenAI o3/o4-mini announcement](https://openai.com/index/introducing-o3-and-o4-mini/)
- GPT-4.5 scores from simple-evals: MMLU 90.8, GPQA 69.5, HumanEval 87.1, MATH 88.6
- GPT-4.1 scores: MMLU 90.2, GPQA 66.3, HumanEval 82.1, MATH 94.5
- o3 (standard) scores: MMLU 92.9, GPQA 82.8, HumanEval 97.8, MATH 87.4
- o4-mini scores: MMLU 90.0, GPQA 77.6, HumanEval 97.5, MATH 97.3
- **Note:** simple-evals lists "GPQA" not specifically "GPQA Diamond" but these are understood to be GPQA Diamond scores. For o-series models, "MATH" column corresponds to MATH-500 (newer IID version).

### Anthropic Models
- **Sources:** [Anthropic Claude 4.5 Sonnet announcement](https://www.anthropic.com/news/claude-sonnet-4-5), [DataCamp Claude 4](https://www.datacamp.com/blog/claude-4), [Vellum Claude Opus 4.5 Benchmarks](https://www.vellum.ai/blog/claude-opus-4-5-benchmarks), [LeanWare Claude 4.5 Overview](https://www.leanware.co/insights/claude-sonnet-4-5-overview)
- Claude 3.7 Sonnet: GPQA Diamond 68.0%, MATH 82.2%
- Claude Sonnet 4: MMLU 86.5%, GPQA Diamond 75.4%
- Claude 4.5 Sonnet: GPQA Diamond 83.4%, MATH Level 5 97.7% (from LM Council benchmarks)
- Claude Opus 4: MMLU 88.8%, GPQA Diamond 79.6%
- **Note:** Anthropic does not always publish HumanEval scores. MATH-500 scores not separately reported for most Claude models.

### Google Models
- **Sources:** [Google Gemini 2.5 blog post](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-model-thinking-updates-march-2025/), [Helicone Gemini 2.5 guide](https://www.helicone.ai/blog/gemini-2.5-full-developer-guide), [llm-stats.com Gemini 2.5 Flash](https://llm-stats.com/models/gemini-2.5-flash)
- Gemini 2.0 Flash: MMLU ~76.4%, GPQA Diamond ~62.1%, HumanEval ~51.8% (from Vellum leaderboard)
- Gemini 2.5 Pro: Global MMLU (Lite) 89.8%, GPQA Diamond 84.0%
- Gemini 2.5 Flash: Global MMLU (Lite) 88.4%, GPQA 82.8%
- **Note:** Google reports "Global MMLU (Lite)" which differs slightly from standard MMLU. GPQA for Flash reported as general GPQA, may not be Diamond subset specifically.

### Meta Llama 4
- **Sources:** [Meta Llama 4 announcement](https://ai.meta.com/blog/llama-4-multimodal-intelligence/), [Llama.com models page](https://www.llama.com/models/llama-4/), [Analytics Vidhya Llama 4](https://www.analyticsvidhya.com/blog/2025/04/meta-llama-4/)
- Llama 4 Scout: MMLU 79.6, GPQA Diamond 65.1%, HumanEval 74.1%, MATH 50.3
- Llama 4 Maverick: MMLU 85.5, GPQA Diamond 82.2%, HumanEval 82.4%, MATH 61.2
- **Note:** Artificial Analysis initially could not reproduce Meta's MMLU-Pro and GPQA Diamond claims for Maverick, but later confirmed them after methodology adjustments.

### DeepSeek
- **Sources:** [DeepSeek-V3 Technical Report (arXiv:2412.19437)](https://arxiv.org/pdf/2412.19437), [DeepSeek-R1 paper (arXiv:2501.12948)](https://arxiv.org/html/2501.12948v1), [Artificial Analysis DeepSeek V3 0324](https://artificialanalysis.ai/models/deepseek-v3-0324)
- DeepSeek-V3 (original): MMLU 88.5%, GPQA 59.1%, MATH-500 90.2%
- DeepSeek-V3-0324: GPQA improved to 68.4% (+9.3 over original V3)
- DeepSeek-R1: MMLU 90.8%, GPQA Diamond 71.5%, MATH-500 97.3%

### Mistral
- **Source:** [Mistral AI announcement](https://mistral.ai/news/mistral-large), [Analytics Vidhya review](https://www.analyticsvidhya.com/blog/2025/12/mistral-large-3/)
- Mistral Large 3: MMLU ~85.5%, GPQA Diamond ~43.9%, HumanEval ~92%
- **Note:** GPQA Diamond score is notably low for a frontier model; this may reflect Mistral's design trade-off favoring general knowledge over extreme multi-step reasoning.

### Qwen
- **Sources:** [Qwen3 Technical Report (arXiv:2505.09388)](https://arxiv.org/pdf/2505.09388), [Qwen blog](https://qwenlm.github.io/blog/qwen3/)
- Qwen3-235B-A22B: AIME'24 85.7%, AIME'25 81.5%, LiveCodeBench v5 70.7%
- **Note:** Specific MMLU, GPQA Diamond, HumanEval, MATH-500 scores for the flagship Qwen3 model were not clearly available in the sources found. The technical report uses different benchmark suites.

### xAI Grok
- **Sources:** [xAI Grok 3 announcement](https://x.ai/news/grok-3), [Helicone Grok 3 review](https://www.helicone.ai/blog/grok-3-benchmark-comparison)
- Grok 3: MMLU 92.7%, GPQA Diamond 84.6% (with Think mode)
- Grok 3 mini: Limited benchmark data available; AIME 2024 95.8%, LiveCodeBench 80.4%
- **Note:** Grok 3's GPQA score of 84.6% is for the "Think" reasoning variant.

---

## Chatbot Arena ELO Notes

Chatbot Arena ELO scores were difficult to pin down for many of these models because:
1. The leaderboard has evolved rapidly; many models in this list have been superseded.
2. ELO scores shift as new models enter the arena.
3. Some approximate scores found:
   - Grok 3: ~1402 (first model to break 1400 at its launch in Feb 2025)
   - Llama 4 Maverick: ~1417
   - Mistral Large 3: ~1417
   - Gemini 2.5 Pro: ranked near top at release
4. Most models in this list have since been overtaken by newer models (GPT-5.x, Gemini 3.x, Claude 4.6, Grok 4.x) making historical ELO scores less meaningful.
5. Left blank in CSV where reliable scores were not found.

---

## Key Caveats

1. **Pricing is point-in-time:** Many of these models have been deprecated or superseded by March 2026. Prices listed reflect the pricing at or near launch / primary availability period.

2. **Open-source model pricing varies:** Llama 4, DeepSeek, Mistral Large 3, and Qwen models are open-source/open-weight. Pricing depends on the API provider (Together AI, Fireworks, Groq, etc.). Representative/median prices used.

3. **Benchmark methodology varies:** Different organizations use different evaluation protocols. OpenAI's simple-evals, Google's internal benchmarks, and Anthropic's evaluations may not be directly comparable even on the same named benchmark.

4. **GPQA vs GPQA Diamond:** Some sources report "GPQA" without specifying "Diamond." Where possible, Diamond scores were used, but some entries may be general GPQA scores.

5. **MATH vs MATH-500 vs MATH Level 5:** These are related but distinct benchmarks. MATH is the original 12,500-problem dataset. MATH-500 is a 500-problem IID subset used by OpenAI for o-series models. MATH Level 5 is the hardest difficulty tier. Columns kept separate where possible.

6. **DeepSeek-R1 release date:** Technically released January 20, 2025, which is before the Feb 2025 cutoff, but included per request as "price updates" were relevant.

7. **Claude 3.5 Haiku:** Released November 4, 2024. Current pricing ($0.80/$4.00) has not changed since launch. Included per request to track any price changes. No changes found.

8. **Mistral Large 3:** Released December 2, 2025. This is later than many other models in the list.

---

## Data Collection Date
All data collected via web search on March 20, 2026.
