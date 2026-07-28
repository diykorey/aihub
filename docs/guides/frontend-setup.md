# AI Hub Frontend Setup (Ultra‑Simple Version for AI Development)

## Goal
Create a **minimal frontend project** that AI agents can extend easily and quickly.

The priority is:
- **speed of development**
- **low complexity**
- **clear structure**
- **minimal dependencies**

Avoid over‑engineering.

---

# Stack (Minimal)

Use this stack unless there is a hard blocker:

- **SvelteKit**
- **TypeScript**
- **Tailwind CSS**
- **pnpm**
- **Lucide icons**
- **date-fns**

Do NOT add other libraries unless required.

Optional later (not needed initially):

- ESLint
- Prettier
- Zod

---

# Step 1 — Create the Project

Initialize a SvelteKit project.

Requirements:

- TypeScript enabled
- minimal configuration
- package manager **pnpm**

Commands example:

```bash
pnpm create svelte@latest ai-hub-frontend
cd ai-hub-frontend
pnpm install
pnpm dev
```

Verify the app runs locally.

---

# Step 2 — Add Tailwind

Install Tailwind CSS using the standard SvelteKit setup.

Requirements:

- Tailwind enabled globally
- minimal configuration
- no design system yet

Use Tailwind utility classes directly.

---

# Step 3 — Install Minimal Libraries

Install only these:

```bash
pnpm add lucide-svelte date-fns
```

Do NOT add more dependencies at this stage.

---

# Step 4 — Project Structure

Use this structure.

```
src/
  routes/
    +layout.svelte
    +page.svelte
    insights/
      [id]/
        +page.svelte
    digest/
      [year]/
        [week]/
          +page.svelte
    tags/
      [tag]/
        +page.svelte
    articles/
      new/
        +page.svelte        ← subscriber: submit own article
    admin/
      +page.svelte          ← admin: insight management dashboard
    billing/
      +page.svelte          ← subscriber/admin: usage + billing summary

  lib/
    components/
      InsightCard.svelte
      InsightHeader.svelte
      ReasoningBlock.svelte
      UsageBlock.svelte
      ExamplesBlock.svelte
      SourcesBlock.svelte
      DebateBlock.svelte
      CommentBlock.svelte      ← subscriber/admin: comments section
      SearchBar.svelte         ← global article search
      FilterPanel.svelte       ← model/topic/timeframe/content type filters
      SubscribeForm.svelte     ← email subscription widget

    api/
      client.ts
      insights.ts
      digests.ts
      comments.ts
      articles.ts
      billing.ts
      subscription.ts

    types/
      insight.ts
      comment.ts
      user.ts                  ← role: reader | subscriber | admin
      billing.ts

    utils/
      date.ts
      roles.ts                 ← role check helpers

    mocks/
      insights.ts
      digests.ts

  app.css
```

Rules:

- keep components **small**
- avoid deep nesting
- avoid premature abstraction

---

# Step 5 — Create Base Layout

Create a minimal layout.

Layout should include:

- top navigation
- main container
- footer (optional)

Navigation items:

- Home
- Weekly Digest

Keep UI minimal.

---

# Step 6 — Define Types

Create simple types in `src/lib/types`.

Example:

```ts
export interface Insight {
  id: string
  title: string
  summary: string
  reasoning?: string
  examples?: string[]
  perspectives?: Record<string, string>
  tags?: string[]
  players?: string[]
  week?: number
  year?: number
  status: 'draft' | 'published'
}

export type Role = 'reader' | 'subscriber' | 'admin'

export interface User {
  id: string
  email: string
  role: Role
}

export interface Comment {
  id: string
  insight_id: string
  author_role: Role
  body: string
  created_at: string
}

export interface BillingSummary {
  period: string
  total_requests: number
  total_tokens: number
  amount_due: number
}
```

Use roles to conditionally render UI elements (`roles.ts` helpers).

---

# Step 7 — API Client

Create a small API client in:

```
src/lib/api/client.ts
```

Example:

```ts
export async function apiFetch<T>(url: string): Promise<T> {
  const res = await fetch(url)

  if (!res.ok) {
    throw new Error("API request failed")
  }

  return res.json()
}
```

Then create small wrappers:

```
insights.ts
digests.ts
```

Example:

```ts
export function getInsights() {
  return apiFetch("/api/insights")
}
```

Keep API code simple.

---

# Step 8 — Build Core Components

Create these components first.

### InsightCard

Used in lists.

Shows:
- title
- summary
- tags

---

### InsightHeader

Used on the insight page.

Shows:
- title
- metadata
- tags

---

### ReasoningBlock

Displays AI reasoning.

---

### UsageBlock

Shows usage for:

- solo
- developers
- SMB
- enterprise

---

### ExamplesBlock

Shows real examples.

---

### SourcesBlock

Shows links to sources.

---

### DebateBlock

Shows model perspectives.

---

### CommentBlock

Shows comments on insight detail page.

Access rules:
- subscriber, admin: show comment form
- reader: view only

---

### SearchBar

Global keyword search with debounced input.

---

### FilterPanel

Sidebar/dropdown filter panel.

Filters: model, topic/tag, timeframe, content type.  
State synced to URL query params.

---

### SubscribeForm

Email subscription widget.

Shows subscribe/unsubscribe based on current state.

---

# Step 9 — Create Pages

Build these pages first.

## Home

Route:

```
/
```

Shows:

- latest insights
- link to digest

---

## Weekly Digest

Route:

```
/digest/[year]/[week]
```

Shows insights grouped by week.

---

## Insight Page

Route:

```
/insights/[id]
```

Shows:

- summary
- reasoning
- usage
- examples
- sources
- debate
- comments (subscriber/admin: comment form; reader: view only)

---

## Subscriber Article Page

Route:

```
/articles/new
```

Shows:

- draft article form
- AI feedback request button
- submit for review button

Access: subscriber, admin only

---

## Admin Dashboard

Route:

```
/admin
```

Shows:

- insight list with publish/edit actions
- subscriber article moderation queue
- agent run logs

Access: admin only

---

## Billing Page

Route:

```
/billing
```

Shows:

- usage summary for current period
- token/request breakdown
- amount due

Access: subscriber, admin only

---

# Step 10 — Use Mock Data First

Before backend exists, use mock data.

Create folder:

```
src/lib/mocks
```

Add sample JSON insights.

This allows fast UI development.

Later replace with real API calls.

---

# Step 11 — Keep Styling Simple

Use Tailwind utilities.

Example card:

```
rounded-lg
border
p-4
shadow-sm
hover:shadow
```

Avoid:

- complex animations
- heavy CSS
- large UI libraries

---

# Step 12 — Definition of Done

Frontend setup is complete when:

- project runs locally (`pnpm dev`)
- Tailwind works
- `InsightCard` renders
- Home page loads and fetches `/insights`
- Digest page loads and fetches `/digest/{year}/{week}`
- Insight detail page loads with all blocks (reasoning, debate, sources, comments)
- Search bar and filter panel are present on home/list pages
- `SubscribeForm` widget renders
- Role-based UI gates work (comment form hidden for reader)
- Mock data loads from `src/lib/mocks` when backend is unavailable
- API client structure exists (`client.ts`, `insights.ts`, `digests.ts`, `comments.ts`, `billing.ts`)

---

# Final Rule

Always prefer:

- simpler code
- fewer dependencies
- small components
- fast iteration

Do not over‑engineer the frontend.
