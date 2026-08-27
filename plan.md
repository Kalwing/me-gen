## Goal: 
Generate 30min-1h long text describing the events and lore of mass effect in the style of different characters.

## Execution
### 0. Scrape data
#### Plan 
0.1 Scrape the Mass effect wiki to get all pages (keeping only the relevant text without style, js and images. In markdown). Maybe store them in kind of a hierarchical way.
0.2 Some lore text will be added manually in a folder.
0.3 Build a proper lore codex, in it's own folder, readable for references.

### 1. Build a hierarchical timeline

Instead of extracting "keypoints linked to files", I'd make several levels:

| Level           | Size                       | Purpose            |
| --------------- | -------------------------- | ------------------ |
| Master timeline | ~50 events                 | Overall structure  |
| Event summaries | 200–500 words each         | What happened      |
| Source excerpts | paragraphs from wiki pages | Details and flavor |
| Full pages      | original articles          | Fallback reference |

For example:

```yaml
Mass Relay Discovery
  date: 2148
  importance: high
  related pages:
    - Charon Relay
    - Humanity
    - Systems Alliance
  summary:
    Humanity discovers the Charon relay, opening interstellar travel...
```

This becomes your "index".

---

### 2. Separate lore extraction from storytelling

Don't ask one agent to do both.

### recursive summarization

```
Wiki pages
     ↓
Page summaries
     ↓
Event summaries
     ↓
Master timeline
     ↓
Narration chunks
     ↓
Transition pass
     ↓
Final episode
```

This scales extremely well and lets you swap narrators easily.

You could generate the entire trilogy from the perspective of:

* Garrus Vakarian
* Liara T'Soni
* Mordin Solus
* Legion
* Javik

without ever touching the original wiki again after the extraction stage.

If I were implementing this today, I'd probably use a RAG pipeline with a vector database and a multi-stage generation process rather than relying on a single huge context window. That gives much more consistent results and makes it easy to regenerate sections when you want a different narrator.


I’d build it like this:

```text
Mass Effect wiki pages
        ↓
Clean + chunk text
        ↓
Metadata extraction
        ↓
Vector database + keyword index
        ↓
Timeline/event database
        ↓
Narration generator
        ↓
Transition/smoothing pass
```

## 1. Ingest the wiki

Download pages, but store them as individual documents with metadata:

```json
{
  "title": "Virmire",
  "url": "...",
  "game": "Mass Effect",
  "type": "mission",
  "characters": ["Shepard", "Saren", "Ashley", "Kaidan"],
  "text": "..."
}
```

Keep the raw page text. Don’t try to summarize too early.

## 2. Chunk the pages

Split each page into chunks of maybe 500–1,000 tokens.

Each chunk should carry metadata:

```json
{
  "chunk_id": "virmire_004",
  "page": "Virmire",
  "section": "Mission",
  "game": "Mass Effect",
  "text": "...",
  "url": "..."
}
```

Use overlap, maybe 100–150 tokens, so events are not split too harshly.

## 3. Build two indexes

Use both:

### Vector index

Good for semantic retrieval:

```text
"What happened on Virmire and why was it important?"
```

### Keyword/BM25 index

Good for names and exact lore terms:

```text
"Sovereign"
"Rachni Queen"
"Collector Base"
```

Hybrid retrieval is better than vector-only for lore-heavy material.

Tools you could use:

```text
Vector DB: Chroma, Qdrant, LanceDB, Weaviate
Embeddings: OpenAI embeddings, bge, e5, nomic-embed
BM25: Elasticsearch, OpenSearch, Tantivy, rank-bm25
```

For a personal project, I’d probably use **LanceDB or Qdrant + BM25**.

## 4. Extract a structured timeline

Run an extraction pass over the corpus:

```json
{
  "event_id": "virmire_decision",
  "title": "The Virmire mission",
  "game": "Mass Effect",
  "chronological_order": 42,
  "summary": "Shepard leads a mission against Saren's base...",
  "characters": ["Shepard", "Saren", "Ashley", "Kaidan", "Wrex"],
  "consequences": [
    "Saren's research base is destroyed",
    "One squadmate dies",
    "Sovereign is revealed as a Reaper"
  ],
  "source_chunks": ["virmire_003", "virmire_004", "sovereign_002"]
}
```

This becomes your main control layer. The timeline is much smaller than the wiki, but every event links back to retrievable source chunks.


### 5. Add memory about the narrator

Create a "voice bible":

```yaml
Garrus:
  tone:
    dry humor
    soldier perspective
    admiration for Shepard
  favorite expressions:
    calibrations
  dislikes:
    bureaucracy
```

or

```yaml
Mordin:
  tone:
    rapid.
    analytical.
    fragmented sentences.
```


## 6. Make an outline for the script

For 30 minutes-1h, target around **5000–10 000 words**.The user will give some pointers on thematics to drop by.

Create something like:

```json
[
  {
    "section": "Humanity enters the galactic stage",
    "events": ["mars_discovery", "charon_relay", "first_contact_war"],
    "target_words": 500
  },
  {
    "section": "Eden Prime and the hunt for Saren",
    "events": ["eden_prime", "spectre_induction"],
    "target_words": 600
  }
]
```

The outline controls pacing. Without it, the model will over-explain early events and rush the ending.
The user must approve of the plan.

## 7. Retrieve per section

For each section:

1. Load the relevant event summaries.
2. Retrieve top chunks using event names, characters, and consequences.
3. Deduplicate chunks.
4. Feed only those chunks into the writing prompt.

Example prompt structure:

```text
You are writing a 30-minute Mass Effect recap.

Narrator voice:
Garrus Vakarian — dry, tactical, slightly sarcastic, loyal to Shepard, exasperated by bureaucracy.

Current section:
Virmire and the revelation of Sovereign.

Required facts:
- Shepard assaults Saren's base.
- Wrex confronts Shepard over the genophage cure.
- Sovereign reveals itself as a Reaper.
- One squadmate is left behind.

Source material:
[retrieved chunks]

Write 450 words.
Preserve facts.
Do not invent events.
Use Garrus's voice without parodying him.
```

## 8. Generate section drafts independently

Each section should be self-contained. Save outputs like:

```json
{
  "section_id": "virmire",
  "narrator": "garrus",
  "draft": "...",
  "used_sources": [...]
}
```

This makes regeneration easy.

## 9. Smooth transitions afterward

Don’t smooth the whole script at once. Use a sliding window:

```text
Previous section ending
Current section
Next section beginning

Revise only the current section for continuity.
Do not change factual content.
Preserve narrator voice.
```

This avoids context overflow.

## 10. Add a final consistency pass

Run checks for:

```text
- chronology errors
- repeated explanations
- missing major events
- inconsistent narrator voice
- invented lore
- overlong sections
```

You can make the model output only issues first, then patch the sections.

## My preferred architecture

For a first version:

```text
Python
+ requests / BeautifulSoup for scraping
+ markdownify for page cleanup
+ LanceDB or Qdrant for vectors
+ SQLite for timeline/events
+ BM25 with rank-bm25
+ LLM calls for extraction and generation
```

SQLite is useful because your timeline is structured data, not just embeddings.

## The key idea

Don’t RAG directly from wiki → narration.

Use:

```text
Wiki → structured event database → retrieved evidence → narration
```

The structured timeline gives you control over pacing and chronology. RAG gives you detail and source grounding. The narrator prompt gives you style.
