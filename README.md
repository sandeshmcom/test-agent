# test-agent

## Getting an Anthropic API key

1. Go to https://console.anthropic.com/ and sign in or create an account.
2. Complete any required email and billing setup.
3. Open **Settings → API Keys** (or **API Keys** in the left nav).
4. Click **Create key**, give it a name, and copy the value.
5. Store it securely (do not commit it to git). For example:

   ```bash
   export ANTHROPIC_API_KEY="your_key_here"
   ```

   Or add it to a local `.env` file:

   ```env
   ANTHROPIC_API_KEY=your_key_here
   ```

If you ever suspect a key is exposed, revoke it in the console and create
a new one.