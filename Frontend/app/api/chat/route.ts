import { cookies, headers } from "next/headers"
import { decrypt } from "@/app/lib/sessions"

function extractTextFromMessage(message: any): string {
  if (typeof message.content === 'string' && message.content.trim().length > 0) {
    return message.content;
  }
  if (Array.isArray(message.parts)) {
    return message.parts
      .filter((part: any) => part.type === 'text')
      .map((part: any) => part.text)
      .join("");
  }
  return String(message.content || "");
}

export const maxDuration = 30

async function chatOwnerId() {
  const session = await decrypt((await cookies()).get('session')?.value)
  if (session?.user?.userId) return session.user.userId

  const visitorId = (await headers()).get('x-chat-visitor-id') || ''
  return /^[a-zA-Z0-9-]{8,100}$/.test(visitorId) ? `guest:${visitorId}` : null
}

export async function POST(req: Request) {
  try {
    const { messages } = await req.json()
    const userId = await chatOwnerId()
    if (!messages || messages.length === 0) {
      return new Response("No messages provided", { status: 400 })
    }

    const lastMessage = messages[messages.length - 1]

    const userText = extractTextFromMessage(lastMessage);

    if (!userText.trim()) {
        return new Response("Message content is required", { status: 400 })
    }

    // Prepare clean history for the backend
    const history = messages.slice(0, -1).map((m: any) => ({
        role: m.role,
        content: extractTextFromMessage(m)
    }));

    const baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    // Call the Main Backend Proxy
    const response = await fetch(`${baseUrl}/api/ai/chat/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: userText.trim(),
        history: history,
        user_id: userId,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text().catch(() => "Unknown error");
      console.error("[Chat API] Backend Error:", errorText);
      return new Response(`Expert System Error: ${response.status}`, { status: response.status });
    }

    const data = await response.json();
    const replyText = data.reply || "I'm sorry, I couldn't process your aquaculture query.";

    return Response.json({ reply: replyText });

  } catch (error: any) {
    console.error("[Chat API] Critical Error:", error);
    return new Response("AquaBot service is temporarily unavailable", { status: 500 });
  }
}
