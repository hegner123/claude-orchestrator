# Component Builder Orchestrator - Prototype

Multi-agent workflow prototype for generating Umbraco components from design images.

## Setup

### 1. Install Dependencies

```bash
cd prototype
pip install -r requirements.txt
```

Or with a virtual environment (recommended):

```bash
cd prototype
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the `prototype/` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here
```

**Get your API key from:** https://console.anthropic.com/settings/keys

### 3. Test Connection

```bash
python orchestrator.py
```

You should see:
```
✅ API Connection successful!
✨ Ready to build components!
```

## Usage

### Current Features (Prototype)

- ✅ Environment variable loading
- ✅ Anthropic API connection validation
- ✅ Basic orchestrator structure
- ✅ Workflow directory management

### Planned Features

- [ ] Vision agent (design image analysis)
- [ ] Component Contract management
- [ ] Backend agent (UDA generation)
- [ ] TypeScript agent (type definitions)
- [ ] Style agent (CSS/SCSS generation)
- [ ] Validation gates
- [ ] Operator review interface
- [ ] Confidence-based intervention

## Architecture

```
prototype/
├── orchestrator.py       # Main orchestrator
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
├── .env                 # Your API key (gitignored)
└── workflow/            # Working directory (auto-created)
    └── component-contract.json  # Shared state
```

## Next Steps

1. **Test the connection** - Run `python orchestrator.py`
2. **Implement vision agent** - Add image analysis capability
3. **Define Component Contract schema** - Use Pydantic models
4. **Add agent execution** - Backend, TypeScript, Style agents
5. **Implement validation** - Gate system for quality checks

## Troubleshooting

### "anthropic library not installed"
```bash
pip install anthropic python-dotenv
```

### "ANTHROPIC_API_KEY not found"
- Check that `.env` file exists in `prototype/` directory
- Verify API key is on the line: `ANTHROPIC_API_KEY=sk-ant-...`
- No quotes needed around the key

### "Authentication failed"
- Verify your API key at https://console.anthropic.com/settings/keys
- Make sure you copied the entire key including `sk-ant-` prefix

### "Rate limit exceeded"
- You're making too many requests
- Wait a few seconds and try again
- Check your usage at https://console.anthropic.com/settings/usage

## References

- Anthropic API Docs: https://docs.anthropic.com/
- Multi-Agent Architecture: `../resources/multi-agend.md`
- Component Build System: `../mh-ai-compoent-build.md`
