export async function GET() {
  const segments = [
    { speaker: 'Arjun K.', text: 'Thanks for joining. Before we dive in, can you walk me through your current meeting workflow?' },
    { speaker: 'Maya L.', text: 'Honestly, it is a mess. We use three tools and nothing talks to each other. We spend about two hours after every call just catching up on action items.' },
    { speaker: 'Arjun K.', text: 'Has leadership prioritized fixing this? Budget allocation must be a factor.', hint: 'Strong follow-up — listen carefully for budget authority signals in the next response.', confidence: 91 },
    { speaker: 'Maya L.', text: 'Our VP of Ops has sign-off authority up to fifty thousand annually. Anything above that needs board approval. We are well within that range.' },
    { speaker: 'Arjun K.', text: 'Got it. What would a successful rollout look like in the first ninety days?', hint: 'Excellent discovery question. Note: decision timeline not yet established — address this before closing.', confidence: 88 },
    { speaker: 'Maya L.', text: 'Full adoption across our product team — about forty people. Measurable reduction in post-meeting overhead by week eight.' },
  ]

  const encoder = new TextEncoder()
  let i = 0

  const stream = new ReadableStream({
    start(controller) {
      const interval = setInterval(() => {
        if (i >= segments.length) {
          clearInterval(interval)
          controller.close()
          return
        }
        controller.enqueue(encoder.encode(`data: ${JSON.stringify(segments[i++])}\n\n`))
      }, 2200)
    },
  })

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive',
    },
  })
}
