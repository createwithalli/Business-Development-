/**
 * Cloudflare Pages Function — /agent
 *
 * Acts as a secure proxy between the frontend and the Claude API.
 * The CLAUDE_API_KEY is stored as a Cloudflare secret — it never
 * appears in the browser or in source code.
 *
 * Set it once in Cloudflare Pages dashboard:
 *   Settings → Environment variables → Add variable
 *   Name: CLAUDE_API_KEY   Value: sk-ant-...   (mark as Secret)
 */

const CLAUDE_API = "https://api.anthropic.com/v1/messages";
const MODEL      = "claude-haiku-4-5-20251001";

const CORS = {
  "Access-Control-Allow-Origin":  "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function onRequestPost(context) {
  const { request, env } = context;

  if (!env.CLAUDE_API_KEY) {
    return Response.json(
      { error: "CLAUDE_API_KEY is not configured. Add it in Cloudflare Pages → Settings → Environment variables." },
      { status: 500, headers: CORS }
    );
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return Response.json({ error: "Invalid JSON body." }, { status: 400, headers: CORS });
  }

  const { type, prices } = body;

  // Build the agent prompt based on what the frontend requests
  let prompt = "";

  if (type === "crypto") {
    const lines = Object.entries(prices)
      .map(([ticker, { price, change }]) =>
        `${ticker}: $${price.toLocaleString()} (${change >= 0 ? "+" : ""}${change.toFixed(2)}% 24h)`)
      .join("\n");

    prompt = `You are a concise crypto market analyst for CreateWithAlli, a content creator audience.

Current prices:
${lines}

Give a 3-bullet summary (max 20 words each) of what's notable right now — big movers, trends, or anything worth posting about. Use plain language, no jargon. Start each bullet with an emoji.`;
  }

  if (type === "amazon") {
    prompt = `You are a trend spotter for CreateWithAlli, an Amazon influencer.

Suggest 3 product categories that are trending RIGHT NOW on Amazon (consider the season and current date: ${new Date().toDateString()}).
Format as 3 bullets, each with: emoji, category name, one sentence on why it's hot.
Keep it practical for a lifestyle/creator audience.`;
  }

  if (!prompt) {
    return Response.json({ error: "Unknown request type." }, { status: 400, headers: CORS });
  }

  try {
    const res = await fetch(CLAUDE_API, {
      method: "POST",
      headers: {
        "x-api-key":         env.CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type":      "application/json",
      },
      body: JSON.stringify({
        model:      MODEL,
        max_tokens: 400,
        messages:   [{ role: "user", content: prompt }],
      }),
    });

    if (!res.ok) {
      const err = await res.text();
      return Response.json({ error: `Claude API error: ${err}` }, { status: res.status, headers: CORS });
    }

    const data  = await res.json();
    const reply = data?.content?.[0]?.text ?? "No response from Claude.";
    return Response.json({ reply }, { headers: CORS });

  } catch (err) {
    return Response.json({ error: `Request failed: ${err.message}` }, { status: 500, headers: CORS });
  }
}
