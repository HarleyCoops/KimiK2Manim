# Cline + Cerebras Configuration Guide

This guide explains how to configure Cline (in Cursor IDE) to use Cerebras inference infrastructure with DeepSeek models.

## Prerequisites

- Cursor IDE with Cline extension installed
- Cerebras API key from [cloud.cerebras.ai](https://cloud.cerebras.ai)

## Configuration Steps

### 1. Open Cline Settings

In Cursor:
- Open the Cline extension panel (sidebar)
- Click the settings/gear icon
- Navigate to API Provider settings

### 2. Configure OpenAI-Compatible Provider

**Provider Type**: Select "OpenAI Compatible" or "Custom OpenAI"

**Settings**:
```
Base URL: https://api.cerebras.ai/v1
API Key: csk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Model: deepseek-r1-distill-llama-70b
```

### 3. Available Models on Cerebras

| Model Name | Description | Best For |
|------------|-------------|----------|
| `deepseek-r1-distill-llama-70b` | DeepSeek R1 reasoning model | Complex reasoning, math, code |
| `llama-3.3-70b` | Meta Llama 3.3 70B | General purpose, fast |
| `llama-3.1-8b` | Meta Llama 3.1 8B | Quick tasks, lower cost |

### 4. Environment Variables (Optional)

If you want to store the API key securely:

```bash
# Add to .env file
CEREBRAS_API_KEY=csk-your-api-key-here
```

### 5. Testing the Connection

After configuration:
1. Ask Cline a simple question
2. Verify it responds using the Cerebras endpoint
3. Check the model name in Cline's response header

## API Compatibility

Cerebras implements the OpenAI API specification:
- Chat Completions: `/v1/chat/completions`
- Streaming: Supported via SSE
- Function Calling: Supported (model-dependent)
- Vision: Not supported on DeepSeek models

## Performance Characteristics

**Cerebras Advantage**: Extremely fast inference due to wafer-scale hardware
- Typical latency: 50-200ms for first token
- Throughput: Up to 2000 tokens/second
- Best for: Real-time coding assistance, rapid iteration

## Pricing (as of 2024)

Cerebras pricing is competitive and based on:
- Input tokens: ~$0.10 per million tokens
- Output tokens: ~$0.10 per million tokens
- No per-request charges

Check [cerebras.ai/pricing](https://cerebras.ai/pricing) for current rates.

## Troubleshooting

### "Invalid API Key" Error
- Verify API key starts with `csk-`
- Check key is active in Cerebras dashboard
- Ensure no extra spaces in configuration

### "Model Not Found" Error
- Use exact model name: `deepseek-r1-distill-llama-70b`
- Check model availability in your Cerebras account
- Try alternative model like `llama-3.3-70b`

### Slow Responses
- Cerebras should be very fast (faster than OpenAI)
- Check your internet connection
- Verify you're using Cerebras endpoint, not accidentally using another provider

### Function Calling Issues
- DeepSeek R1 supports function calling
- Ensure Cline's tool usage is enabled
- Check model capabilities in Cerebras documentation

## Comparison with Other Providers

| Provider | Speed | Cost | Reasoning Ability |
|----------|-------|------|-------------------|
| Cerebras + DeepSeek | ⚡⚡⚡ Very Fast | 💰 Low | 🧠🧠🧠 Excellent |
| OpenAI GPT-4 | ⚡ Medium | 💰💰💰 High | 🧠🧠🧠 Excellent |
| Anthropic Claude | ⚡⚡ Fast | 💰💰 Medium | 🧠🧠🧠 Excellent |

## Integration with This Repository

This repository (KimiK2Manim) uses Moonshot AI (Kimi) for its agent pipeline. You can:

1. **Use Cline with Cerebras** for interactive coding assistance in Cursor
2. **Keep Kimi** for the automated math visualization pipeline
3. **Both run independently** - no configuration conflicts

The `.env` file in this repo configures Moonshot/Kimi, not Cline.

## Next Steps

After configuration:
1. Test with a simple prompt: "Explain how async/await works in Python"
2. Try a coding task: "Write a function to validate email addresses"
3. Use for code review: "Review the code in agents/prerequisite_explorer_kimi.py"

## Resources

- [Cerebras Documentation](https://docs.cerebras.ai)
- [Cerebras Model Garden](https://cloud.cerebras.ai/models)
- [DeepSeek R1 Paper](https://arxiv.org/abs/2401.xxxxx)
- [Cline Documentation](https://github.com/cline/cline)
