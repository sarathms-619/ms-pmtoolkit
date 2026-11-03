# Ask AI Worker

The chat on sarathms.com. Everything the bot knows is in `SYSTEM_PROMPT` inside `worker.js`:
edit that text to change its answers.

## Deploy

**From GitHub (no copy-paste):** Cloudflare dashboard → Workers & Pages → `sarath-digital-twin`
→ Settings → Build → Connect to Git → this repo, root directory `ask-ai-worker`.
Every push to `main` then redeploys the bot.

**Or from a terminal:**

```bash
cd ask-ai-worker && npx wrangler deploy
```

The `CLAUDE_KEY` secret stays in Cloudflare. To change it: `npx wrangler secret put CLAUDE_KEY`.
