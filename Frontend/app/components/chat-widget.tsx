"use client"

import { useEffect, useRef, useState } from "react"
import Image from "next/image"
import { MessageCircle, X, Send, Loader2, User, Bot, Clock, RotateCcw, Sparkles } from "lucide-react"
import { Button } from "./ui/button"
import { Input } from "./ui/input"

const SUGGESTIONS = [
  "White spots on my fish, what could it be?",
  "How much feed for 1000 tilapia?",
  "Ideal pond water quality parameters?",
  "How to prevent seasonal diseases?",
]

export function ChatWidget() {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState<any[]>([])
  const [input, setInput] = useState("")
  const [isBusy, setIsBusy] = useState(false)
  const [visitorId, setVisitorId] = useState("")
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const key = 'kbtech-chat-visitor-id'
    const existing = window.localStorage.getItem(key)
    const id = existing || crypto.randomUUID()
    if (!existing) window.localStorage.setItem(key, id)
    setVisitorId(id)
  }, [])

  useEffect(() => {
    if (!visitorId) return
    fetch('/api/chat/history', { headers: { 'x-chat-visitor-id': visitorId } })
      .then((response) => response.ok ? response.json() : { messages: [] })
      .then(({ messages: savedMessages }) => {
        if (Array.isArray(savedMessages) && savedMessages.length) {
          setMessages(savedMessages.map((message: any) => ({
            id: `${message.created_at}-${message.role}-${message.content.slice(0, 12)}`,
            role: message.role,
            content: message.content,
            createdAt: new Date(message.created_at),
          })))
        }
      })
      .catch(() => undefined)
  }, [visitorId])

  const safeInput = input;

  // Ensure chat automatically scrolls to the bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages, open, isBusy])

  const sendMessage = async (text: string) => {
    const content = text.trim()
    if (!content || isBusy) return
    const userMessage = { id: crypto.randomUUID(), role: 'user', content, createdAt: new Date() }
    const nextMessages = [...messages, userMessage]
    setMessages(nextMessages)
    setInput("")
    setIsBusy(true)
    try {
      const response = await fetch('/api/chat', {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'x-chat-visitor-id': visitorId },
        body: JSON.stringify({ messages: nextMessages.map(({ role, content }) => ({ role, content })) }),
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.error || data.message || 'Unable to get a response')
      setMessages((current) => [...current, { id: crypto.randomUUID(), role: 'assistant', content: data.reply, createdAt: new Date() }])
    } catch (error) {
      setMessages((current) => [...current, { id: crypto.randomUUID(), role: 'assistant', content: 'Sorry, AquaBot is unavailable right now. Please try again.', createdAt: new Date() }])
    } finally {
      setIsBusy(false)
    }
  }

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    void sendMessage(input)
  }

  const handleSuggestion = async (text: string) => {
    if (isBusy) return
    try {
      await sendMessage(text)
    } catch (err) {
      console.error("Chat Error:", err)
    }
  }

  const formatTime = (date?: Date) => {
    try {
      const d = date || new Date()
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    } catch (e) {
      return ""
    }
  }

  return (
    <>
      {/* Floating Launcher Button */}
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="fixed bottom-5 right-5 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-xl transition-all hover:scale-110 active:scale-95 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
      >
        {open ? <X className="h-6 w-6" /> : <MessageCircle className="h-6 w-6" />}
      </button>

      {open && (
        <div className="fixed bottom-24 right-5 z-50 flex h-[70vh] max-h-[620px] w-[calc(100vw-2rem)] max-w-[420px] flex-col overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-2xl animate-in fade-in zoom-in duration-300">

          {/* Branding Header */}
          <header className="flex items-center gap-3 bg-primary px-5 py-4 text-primary-foreground shadow-lg">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-white p-1.5 shadow-md">
              <Image
                src="/images/kanan-logo.png"
                alt="KBTech Logo"
                width={32}
                height={32}
                className="h-full w-full object-contain"
              />
            </div>
            <div className="flex flex-col">
              <h2 className="text-sm font-bold m-0 p-0 leading-tight">AquaBot Assistant</h2>
              <p className="text-[10px] opacity-90 font-medium m-0 p-0">KBTech Pvt. Ltd. · Aquaculture help</p>
            </div>
            <div className="ml-auto flex items-center gap-1">
              <button
                onClick={async () => {
                  await fetch('/api/chat/history', { method: 'DELETE', headers: { 'x-chat-visitor-id': visitorId } }).catch(() => undefined)
                  setMessages([])
                }}
                className="p-1.5 opacity-60 hover:opacity-100 transition-opacity"
                title="Clear Chat"
              >
                <RotateCcw className="h-4 w-4" />
              </button>
              <button onClick={() => setOpen(false)} className="p-1.5 opacity-60 hover:opacity-100">
                <X className="h-5 w-5" />
              </button>
            </div>
          </header>

          {/* Chat Content Section */}
          <div ref={scrollRef} className="flex-1 space-y-6 overflow-y-auto px-4 py-6 bg-[#fcfcfc]">
            {messages.length === 0 ? (
              <div className="flex flex-col gap-6">
                <div className="bg-white p-5 rounded-3xl rounded-tl-none border border-slate-100 shadow-sm">
                  <div className="flex items-center gap-2 mb-2 text-primary">
                    <Sparkles className="h-4 w-4" />
                    <span className="text-[10px] font-bold uppercase tracking-widest">Expert Advice</span>
                  </div>
                  <p className="text-sm text-slate-700 leading-relaxed italic">
                    "Hello! I am your <strong>AquaBot</strong> expert assistant.
                    I can provide daily advice for your fish farm. How can I assist you today?"
                  </p>
                </div>
                <div className="space-y-2">
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest ml-1">Suggested for you</p>
                  <div className="flex flex-col gap-2">
                    {SUGGESTIONS.map((s) => (
                      <button
                        key={s}
                        onClick={() => handleSuggestion(s)}
                        className="rounded-2xl border border-slate-100 bg-white px-4 py-3 text-left text-xs text-slate-600 hover:border-primary hover:text-primary transition-all shadow-sm active:scale-95"
                      >
                        {s}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              messages.map((m) => (
                <div
                  key={m.id}
                  className={`flex flex-col ${m.role === "user" ? "items-end" : "items-start"}`}
                >
                  <div className={`flex gap-2 ${m.role === "user" ? "flex-row-reverse" : "flex-row"}`}>
                    <div className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full shadow-sm border ${
                      m.role === "user" ? "bg-primary text-primary-foreground border-primary" : "bg-white text-primary border-slate-200"
                    }`}>
                      {m.role === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                    </div>
                    <div className={`max-w-[85%] whitespace-pre-wrap rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-sm ${
                      m.role === "user"
                        ? "rounded-tr-none bg-primary text-primary-foreground font-medium"
                        : "rounded-tl-none bg-white text-slate-700 border border-slate-100 shadow-sm"
                    }`}>
                      {m.content}
                    </div>
                  </div>
                  <span className="text-[9px] text-slate-400 mt-1.5 flex items-center gap-1 mx-10 font-medium">
                    <Clock className="h-2.5 w-2.5" /> {formatTime(m.createdAt)}
                  </span>
                </div>
              ))
            )}

            {/* Thinking / Typing Animation */}
            {isBusy && (
              <div className="flex gap-2 animate-in fade-in duration-500">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-white text-primary border border-slate-100 shadow-sm">
                  <Bot className="h-4 w-4" />
                </div>
                <div className="flex items-center gap-1.5 rounded-2xl rounded-tl-none bg-white border border-slate-100 px-5 py-4 shadow-sm">
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-primary/40"></span>
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-primary/60 [animation-delay:0.2s]"></span>
                  <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-primary/80 [animation-delay:0.4s]"></span>
                </div>
              </div>
            )}
          </div>

          {/* Input Form with Fix for onChange and Undefined error */}
          <form
            onSubmit={handleSubmit}
            className="flex items-center gap-2 border-t border-slate-100 bg-white p-5"
          >
            <Input
              name="prompt"
              value={safeInput}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Ask AquaBot..."
              className="flex-1 rounded-2xl border border-slate-200 bg-slate-50 px-5 py-3 text-sm text-slate-700 outline-none transition-all focus:bg-white focus:ring-2 focus:ring-primary/20 h-auto"
              autoComplete="off"
            />
            <Button
              type="submit"
              size="icon"
              className="h-11 w-11 shrink-0 rounded-2xl shadow-lg transition-transform active:scale-90"
              disabled={isBusy || !safeInput.trim()}
            >
              {isBusy ? <Loader2 className="h-5 w-5 animate-spin" /> : <Send className="h-5 w-5" />}
            </Button>
          </form>
        </div>
      )}
    </>
  )
}
