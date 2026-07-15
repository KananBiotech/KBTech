import { UIMessage } from "ai"

export const maxDuration = 30

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json()

  // Get the last message
  const lastMessage = messages[messages.length - 1]

  // Prepare history for the backend (excluding the last message)
  const history = messages.slice(0, -1).map(m => ({
    role: m.role,
    content: m.content
  }))

  try {
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    // Call the Main Backend Proxy which connects to RAG Backend
    const response = await fetch(`${baseUrl}/api/ai/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: lastMessage.content,
        history: history
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to get AI response');
    }

    const data = await response.json();

    // The AI SDK expect a specific stream or response format.
    // Since our backend is currently non-streaming, we return a standard Response
    // that the useChat hook can handle (it will treat it as a single chunk).
    return new Response(data.reply);

  } catch (error: any) {
    console.error("Chat API Error:", error);
    return new Response(error.message || "An error occurred", { status: 500 });
  }
}
