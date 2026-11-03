# sarathms.com

- `site/` is the deployable website (Netlify: base directory `portfolio/site`, no build command).
  - Put your resume at `site/resume/sarathms_resume_2026.pdf`.
  - `site/_redirects` sends the chat through `/api/twin` on your own domain.
  - The chat bot itself lives in its own repo: https://github.com/sarathms-619/ask-ai-worker
- `source/` rebuilds `site/index.html` from the original page plus every change
  (resume links, Toolkit page, mobile tab bar, chat landing, new debriefs):

```bash
cd portfolio/source && python3 build.py
```

New Delivery Dilemmas live in `source/essays/`.
