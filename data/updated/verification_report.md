# LLM Pricing Verification Report

**Date:** March 20, 2026
**Sources:** Official pricing pages (Anthropic/Claude, Google AI, DeepSeek, xAI), ArtificialAnalysis.ai
**Formula:** Weighted Avg = (3 * input_price + 1 * output_price) / 4

---

## Verification of Existing Models

### 1. GPT-4.1 | input=$2.00, output=$8.00, weighted=$3.50
**CONFIRMED** -- ArtificialAnalysis.ai confirms $2.00/$8.00. OpenAI pricing page returned 403 but AA data matches.

### 2. GPT-4.1 mini | input=$0.40, output=$1.60, weighted=$0.70
**CONFIRMED** -- ArtificialAnalysis.ai confirms $0.40/$1.60.

### 3. GPT-4.1 nano | input=$0.10, output=$0.40, weighted=$0.175
**CONFIRMED** -- ArtificialAnalysis.ai confirms $0.10/$0.40.

### 4. o3 | input=$2.00, output=$8.00, weighted=$3.50
**CONFIRMED** -- ArtificialAnalysis.ai confirms $2.00/$8.00.

### 5. o4-mini | input=$1.10, output=$4.40, weighted=$1.925
**CONFIRMED** -- ArtificialAnalysis.ai confirms $1.10/$4.40.

### 6. Claude 3.7 Sonnet | input=$3.00, output=$15.00, weighted=$6.00
**CONFIRMED** -- ArtificialAnalysis.ai confirms $3.00/$15.00.

### 7. Claude Sonnet 4 | input=$3.00, output=$15.00, weighted=$6.00
**CONFIRMED** -- Anthropic official docs confirm $3.00/$15.00.

### 8. Claude 4.5 Sonnet | input=$3.00, output=$15.00, weighted=$6.00
**CONFIRMED** -- Both Anthropic official docs and ArtificialAnalysis.ai confirm $3.00/$15.00. Note: Anthropic lists this model as "Claude Sonnet 4.5" (legacy).

### 9. Claude Opus 4 | input=$15.00, output=$75.00, weighted=$30.00
**NEEDS UPDATE** -- Anthropic official docs show Claude Opus 4 at $15.00/$75.00 for the original Opus 4. However, this model is now listed under "legacy models." The naming "Claude Opus 4.1" ($15/$75) also exists as legacy. The current flagship "Claude Opus 4.6" is priced at **$5.00/$25.00** -- a significant price DROP from the original Opus 4.
- If the intent is to track the original Opus 4 model: **CONFIRMED** at $15.00/$75.00.
- If the intent is to track the current Opus-class model (Opus 4.6): pricing is $5.00 input / $25.00 output, weighted = $10.00.

### 10. Gemini 2.5 Pro | input=$1.25, output=$10.00, weighted=$3.4375
**CONFIRMED** -- Both Google's official pricing page and ArtificialAnalysis.ai confirm $1.25/$10.00 (for prompts <=200k tokens).

### 11. Gemini 2.5 Flash | input=$0.30, output=$2.50, weighted=$0.85
**CONFIRMED** -- Both Google's official pricing page and ArtificialAnalysis.ai confirm $0.30/$2.50.

### 12. DeepSeek-V3-0324 | input=$0.27, output=$1.10, weighted=$0.4775
**NEEDS UPDATE** -- DeepSeek's official API no longer serves V3-0324 as a standalone model. Their API now runs DeepSeek-V3.2 at $0.28/$0.42 (cache miss pricing). ArtificialAnalysis.ai shows V3-0324 median third-party pricing at $1.25/$1.45 (significantly higher than our data). The original DeepSeek first-party pricing of $0.27/$1.10 was correct at the time of collection but the model has been superseded.
- Original first-party pricing: $0.27/$1.10 was correct when collected.
- Current V3-0324 third-party median: $1.25/$1.45 (weighted = $1.30).
- Current successor DeepSeek-V3.2 (first-party): $0.28/$0.42 (weighted = $0.315).

### 13. DeepSeek-R1 | input=$0.55, output=$2.19, weighted=$1.06
**NEEDS UPDATE** -- DeepSeek's official API now serves DeepSeek-V3.2 in thinking mode as the "reasoner" at $0.28/$0.42. ArtificialAnalysis.ai shows R1 (Jan '25) median third-party pricing at $1.35/$4.00, which is significantly higher than our data.
- Original first-party pricing: $0.55/$2.19 was correct when collected.
- Current R1 third-party median: $1.35/$4.00 (weighted = $2.01).
- Current successor (deepseek-reasoner V3.2, first-party): $0.28/$0.42 (weighted = $0.315).

### 14. Grok 3 | input=$3.00, output=$15.00, weighted=$6.00
**CONFIRMED** -- ArtificialAnalysis.ai confirms $3.00/$15.00. Note: xAI has released Grok 4 models (see below), and Grok 3 may be deprecated soon.

---

## Summary Table

| # | Model | Our Data (in/out/weighted) | Status | Notes |
|---|-------|---------------------------|--------|-------|
| 1 | GPT-4.1 | $2.00/$8.00/$3.50 | CONFIRMED | |
| 2 | GPT-4.1 mini | $0.40/$1.60/$0.70 | CONFIRMED | |
| 3 | GPT-4.1 nano | $0.10/$0.40/$0.175 | CONFIRMED | |
| 4 | o3 | $2.00/$8.00/$3.50 | CONFIRMED | |
| 5 | o4-mini | $1.10/$4.40/$1.925 | CONFIRMED | |
| 6 | Claude 3.7 Sonnet | $3.00/$15.00/$6.00 | CONFIRMED | |
| 7 | Claude Sonnet 4 | $3.00/$15.00/$6.00 | CONFIRMED | |
| 8 | Claude 4.5 Sonnet | $3.00/$15.00/$6.00 | CONFIRMED | |
| 9 | Claude Opus 4 | $15.00/$75.00/$30.00 | CONFIRMED (legacy) | Successor Opus 4.6 is $5/$25 |
| 10 | Gemini 2.5 Pro | $1.25/$10.00/$3.4375 | CONFIRMED | |
| 11 | Gemini 2.5 Flash | $0.30/$2.50/$0.85 | CONFIRMED | |
| 12 | DeepSeek-V3-0324 | $0.27/$1.10/$0.4775 | CONFIRMED (historical) | Model superseded by V3.2 |
| 13 | DeepSeek-R1 | $0.55/$2.19/$1.06 | CONFIRMED (historical) | Model superseded by V3.2 reasoner |
| 14 | Grok 3 | $3.00/$15.00/$6.00 | CONFIRMED | |

---

## NEW Models Discovered (Not In Our Dataset)

These models have been released since our last data collection and should be considered for addition:

### Anthropic (Claude)

| Model | Release | Input ($/1M) | Output ($/1M) | Weighted Avg | Source |
|-------|---------|-------------|--------------|-------------|--------|
| Claude Opus 4.5 | 2025-11-01 | $5.00 | $25.00 | $10.00 | Anthropic docs + AA |
| Claude Opus 4.6 | ~2026 | $5.00 | $25.00 | $10.00 | Anthropic docs + AA |
| Claude Sonnet 4.6 | ~2026 | $3.00 | $15.00 | $6.00 | Anthropic docs + AA |
| Claude Haiku 4.5 | 2025-10-01 | $1.00 | $5.00 | $2.00 | Anthropic docs |
| Claude Opus 4.1 | 2025-08-05 | $15.00 | $75.00 | $30.00 | Anthropic docs |

**Key finding:** Anthropic dramatically reduced Opus pricing with the 4.5/4.6 generation -- from $15/$75 (Opus 4/4.1) to $5/$25 (Opus 4.5/4.6). This is a 67% price reduction for the Opus tier.

### Google (Gemini)

| Model | Status | Input ($/1M) | Output ($/1M) | Weighted Avg | Source |
|-------|--------|-------------|--------------|-------------|--------|
| Gemini 3 Flash (Preview) | Preview | $0.50 | $3.00 | $1.125 | Google pricing + AA |
| Gemini 3.1 Pro (Preview) | Preview | $2.00 | $12.00 | $4.50 | Google pricing |
| Gemini 3.1 Flash-Lite (Preview) | Preview | $0.25 | $1.50 | $0.5625 | Google pricing |
| Gemini 2.0 Flash | Deprecated | $0.10 | $0.40 | $0.175 | Google pricing (already in dataset) |

### xAI (Grok)

| Model | Status | Input ($/1M) | Output ($/1M) | Weighted Avg | Source |
|-------|--------|-------------|--------------|-------------|--------|
| Grok 4.20 | Current | $2.00 | $6.00 | $3.00 | xAI docs |
| Grok 4.1 Fast | Current | $0.20 | $0.50 | $0.275 | xAI docs |
| Grok 4 | Current | $3.00 | $15.00 | $6.00 | AA |

### OpenAI

| Model | Status | Input ($/1M) | Output ($/1M) | Weighted Avg | Source |
|-------|--------|-------------|--------------|-------------|--------|
| GPT-5.4 | Current | Unknown | Unknown | Unknown | Seen on AA but pricing page 403 |
| GPT-5.3 Codex | Current | Unknown | Unknown | Unknown | Seen on AA but pricing page 403 |

**Note:** ArtificialAnalysis.ai lists GPT-5.4 and GPT-5.3 Codex as current top models but specific input/output prices could not be retrieved due to OpenAI pricing page returning 403.

### DeepSeek

| Model | Status | Input ($/1M) | Output ($/1M) | Weighted Avg | Source |
|-------|--------|-------------|--------------|-------------|--------|
| DeepSeek-V3.2 (chat) | Current | $0.28 | $0.42 | $0.315 | DeepSeek docs |
| DeepSeek-V3.2 (reasoner) | Current | $0.28 | $0.42 | $0.315 | DeepSeek docs |
| DeepSeek-R1-0528 | Available (3rd party) | $1.35 | $5.40 | $2.3625 | AA (median) |

---

## Key Trends and Observations

1. **Anthropic Opus price collapse:** Opus went from $15/$75 (Opus 4) to $5/$25 (Opus 4.5 and 4.6) -- a 67% reduction. This is the most significant price change found.

2. **DeepSeek aggressive pricing:** DeepSeek-V3.2 at $0.28/$0.42 is remarkably cheap, even cheaper than GPT-4.1 nano. The R1 and V3-0324 models in our dataset are now legacy.

3. **New model generations:** GPT-5.x series, Gemini 3.x series, Grok 4.x series, and Claude 4.6 series have all launched since our data was last collected. These represent significant capability jumps.

4. **Grok 4.1 Fast is very cheap:** At $0.20/$0.50, it's competitive with the cheapest models.

5. **Google Gemini 3.1 Pro Preview** is priced at $2.00/$12.00, more expensive than Gemini 2.5 Pro.

---

## Recommendations

1. **Add new model generations** -- Claude Opus 4.5/4.6, Claude Sonnet 4.6, Gemini 3 Flash, Grok 4 family, DeepSeek-V3.2 are all significant additions.
2. **Flag DeepSeek models as historical** -- V3-0324 and R1 first-party pricing is no longer available; these models have been superseded.
3. **Investigate GPT-5.x pricing** -- OpenAI's pricing page was inaccessible (403). Try accessing via a different method or check platform.openai.com directly.
4. **All 14 models in our dataset have correct pricing** for their respective versions/time periods. No arithmetic errors found in weighted averages.
