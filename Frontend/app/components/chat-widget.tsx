"use client"

import { useEffect, useRef, useState } from "react"
import Image from "next/image"
import { useChat } from "@ai-sdk/react"
import { MessageCircle, X, Send, Loader2 } from "lucide-react"
import { Button } from "./ui/button"

const SUGGESTIONS = [
  "White spots on my fish, what could it be?",
  "How much feed for 1000 tilapia?",
  "Ideal pond water quality parameters?",
  "How to prevent seasonal diseases?",
]

export function ChatWidget() {
  const [open, setOpen] = useState(false)
  const [input, setInput] = useState("")
  const { messages, sendMessage, status } = useChat()
  const scrollRef = useRef<HTMLDivElement>(null)
  const isBusy = status === "submitted" || status === "streaming"

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages, open])

  const handleSend = (text: string) => {
    const trimmed = text.trim()
    if (!trimmed || isBusy) return
    sendMessage({ text: trimmed })
    setInput("")
  }

  return (
    <>
      {/* Launcher button */}
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-label={open ? "Close chat assistant" : "Open chat assistant"}
        aria-expanded={open}
        className="fixed bottom-5 right-5 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-lg shadow-primary/30 transition-transform hover:scale-105 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
      >
        {open ? <X className="h-6 w-6" /> : <MessageCircle className="h-6 w-6" />}
      </button>

      {/* Chat panel */}
      {open && (
        <div className="fixed bottom-24 right-5 z-50 flex h-[70vh] max-h-[560px] w-[calc(100vw-2.5rem)] max-w-sm flex-col overflow-hidden rounded-2xl border border-border bg-card shadow-2xl">
          {/* Header */}
          <header className="flex items-center gap-3 bg-primary px-4 py-3 text-primary-foreground">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-background p-1">
              <Image
                src="/images/kanan-logo.png"
                alt="Kanan Biotech Pvt. Ltd. logo"
                width={32}
                height={32}
                className="h-full w-full object-contain"
              />
            </div>
            <div className="flex flex-col leading-tight">
              <span className="text-sm font-semibold">AquaBot Assistant</span>
              <span className="text-xs text-primary-foreground/80">KBTech Pvt. Ltd. · Aquaculture help</span>
            </div>
          </header>

          {/* Messages */}
          <div ref={scrollRef} className="flex-1 space-y-4 overflow-y-auto px-4 py-4">
            {messages.length === 0 ? (
              <div className="flex flex-col gap-4">
                <p className="text-pretty text-sm text-muted-foreground">
                  Hi! I&apos;m AquaBot. Ask me about fish &amp; shrimp diseases, feed, or water quality.
                </p>
                <div className="flex flex-col gap-2">
                  {SUGGESTIONS.map((s) => (
                    <button
                      key={s}
                      type="button"
                      onClick={() => handleSend(s)}
                      className="rounded-lg border border-border bg-background px-3 py-2 text-left text-sm text-foreground transition-colors hover:bg-accent hover:text-accent-foreground"
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[85%] whitespace-pre-wrap rounded-2xl px-3 py-2 text-sm leading-relaxed ${
                      message.role === "user"
                        ? "rounded-br-sm bg-primary text-primary-foreground"
                        : "rounded-bl-sm bg-muted text-foreground"
                    }`}
                  >
                    {message.parts.map((part, i) =>
                      part.type === "text" ? <span key={`${message.id}-${i}`}>{part.text}</span> : null,
                    )}
                  </div>
                </div>
              ))
            )}
            {status === "submitted" && (
              <div className="flex justify-start">
                <div className="flex items-center gap-2 rounded-2xl rounded-bl-sm bg-muted px-3 py-2 text-sm text-muted-foreground">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Thinking…
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <form
            onSubmit={(e) => {
              e.preventDefault()
              handleSend(input)
            }}
            className="flex items-center gap-2 border-t border-border bg-card px-3 py-3"
          >
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing && e.keyCode !== 229) {
                  e.preventDefault()
                  handleSend(input)
                }
              }}
              placeholder="Ask about diseases, feed, water…"
              aria-label="Message AquaBot"
              className="flex-1 rounded-full border border-input bg-background px-4 py-2 text-sm text-foreground outline-none placeholder:text-muted-foreground focus-visible:ring-2 focus-visible:ring-ring"
            />
            <Button
              type="submit"
              size="icon"
              className="h-10 w-10 shrink-0 rounded-full"
              disabled={isBusy || !input.trim()}
              aria-label="Send message"
            >
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </div>
      )}
    </>
  )
}
