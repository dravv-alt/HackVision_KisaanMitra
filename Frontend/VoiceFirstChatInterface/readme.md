# 🎨 Google Stitch Frontend Design Prompt
## KisanMitra Voice-First Chat Interface - Complete Design System

---

## 📋 PROJECT BRIEF

Create a **voice-first conversational chat interface** for Indian farmers that displays AI responses as **visual cards + audio + text transcripts**. This is not a traditional chatbot - it's an intelligent assistant that converts speech into actionable visual information.

---

## 🎨 DESIGN SYSTEM

### Color Palette (STRICT - Use Only These)
```css
/* Primary Colors */
--ai-response-bg: #E8F5E9        /* Light Green - AI messages */
--warning-accent: #FFF9C4         /* Yellow - Alerts, attention */
--background: #F5F5DC             /* Beige - Main background */
--card-bg: #F0E68C                /* Light Brownish Yellow - Cards */

/* Secondary Colors */
--text-primary: #2E2E2E           /* Dark text */
--text-secondary: #5C5C5C         /* Secondary text */
--user-message-bg: #FFFFFF        /* White - User messages */
--success-green: #66BB6A          /* Confirmations */
--neutral-gray: #BDBDBD           /* Cancel, neutral actions */

/* Interactive Elements */
--mic-active: #81C784             /* Microphone active state */
--mic-idle: #A5D6A7               /* Microphone idle state */
--card-border: #D4D4A8            /* Subtle card borders */
```

### Typography
```css
/* Font Stack */
font-family: 'Inter', 'Noto Sans Devanagari', sans-serif;

/* Sizes */
--heading-large: 24px / 32px (line-height)
--heading-medium: 20px / 28px
--body-large: 18px / 26px        /* For farmer-facing text */
--body-medium: 16px / 24px
--body-small: 14px / 20px
--caption: 12px / 18px

/* Weights */
--weight-bold: 600
--weight-medium: 500
--weight-regular: 400
```

### Spacing System
```css
--space-xs: 4px
--space-sm: 8px
--space-md: 16px
--space-lg: 24px
--space-xl: 32px
--space-2xl: 48px
```

### Border Radius
```css
--radius-sm: 8px
--radius-md: 12px
--radius-lg: 16px
--radius-full: 9999px      /* Circular elements */
```

---

## 📱 SCREEN LAYOUTS

### 🟢 STATE 1: VOICE AGENT HOME (IDLE STATE)

**Layout Specifications:**

```
┌─────────────────────────────────────────┐
│ ☰  KisanMitra                      👤   │ ← Top Bar (60px height)
├─────────────────────────────────────────┤
│                                         │
│                                         │
│           ┌─────────────┐              │
│           │             │              │
│           │      🎤      │              │ ← Microphone Button
│           │   (Pulsing)  │              │   (120px diameter)
│           │             │              │   Soft shadow
│           └─────────────┘              │   Idle green glow
│                                         │
│        Bolo, main sun raha hoon        │ ← Instruction Text
│        (Speak, I am listening)         │   (body-large, centered)
│                                         │
│                                         │
├─────────────────────────────────────────┤
│  TRY ASKING ABOUT                      │ ← Hint Section
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 💰 Mandi prices?                 │  │ ← Example Chips
│  └─────────────────────────────────┘  │   (card-bg color)
│                                         │   (Tappable)
│  ┌─────────────────────────────────┐  │
│  │ 🌾 Crop advice?                  │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 🔬 Check crop disease?           │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 🏛️ Schemes?                      │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

**Component Details:**

**Top Bar:**
- Height: `60px`
- Background: `--background` (Beige)
- Left: Menu icon (☰) - `32px × 32px`, padding `16px`
- Center: "KisanMitra" text - `heading-medium`, `weight-bold`
- Right: Profile icon - `32px` circular avatar

**Microphone Button:**
- Size: `120px × 120px`
- Background: Gradient from `--mic-idle` to lighter shade
- Border: `4px solid white`
- Shadow: `0 8px 24px rgba(0,0,0,0.15)`
- Icon: White microphone icon, `48px`
- Animation: Subtle pulse (scale 1.0 → 1.05, 2s ease-in-out loop)

**Instruction Text:**
- Font: `body-large` (18px)
- Color: `--text-secondary`
- Position: `24px` below mic button
- Alignment: Center

**Example Chips:**
- Title: "TRY ASKING ABOUT" - `caption`, `weight-medium`, uppercase
- Each chip:
  - Height: `56px`
  - Background: `--card-bg`
  - Border: `1px solid --card-border`
  - Border radius: `--radius-md`
  - Padding: `16px`
  - Margin between: `12px`
  - Icon: Left-aligned, `24px`
  - Text: `body-medium`, left-aligned
  - Hover: Slight elevation increase

---

### 🟡 STATE 2: LISTENING MODE (ACTIVE)

**UI Changes from Idle State:**

```
┌─────────────────────────────────────────┐
│ ☰  KisanMitra                      👤   │
├─────────────────────────────────────────┤
│                                         │
│         [DIMMED BACKGROUND]            │ ← Background opacity: 0.6
│                                         │
│           ┌─────────────┐              │
│           │             │              │
│           │   🎤        │              │ ← Microphone Button
│           │  (ACTIVE)   │              │   (140px - expanded)
│           │ ┌─────────┐ │              │   Strong green glow
│           │ │ ○ ○ ○ ○ │ │              │   Audio wave animation
│           │ └─────────┘ │              │
│           └─────────────┘              │
│                                         │
│          Sun raha hoon...              │ ← Status Text
│        (Listening to you...)           │   (weight-medium)
│                                         │
│                                         │
│          ┌──────────┐                  │
│          │  Cancel  │                  │ ← Cancel Button
│          └──────────┘                  │   (neutral-gray)
│                                         │
└─────────────────────────────────────────┘
```

**Component Changes:**

**Background Overlay:**
- Adds semi-transparent dark layer: `rgba(0,0,0,0.3)`
- Blurs non-active elements

**Microphone Button (Active):**
- Size: `140px × 140px` (scale up animation)
- Background: Solid `--success-green`
- Glow: `0 0 32px rgba(102,187,106,0.6)` (strong green glow)
- Audio wave: Animated bars inside button
  - 4-5 vertical bars
  - Heights animate based on audio input level
  - Color: White with 80% opacity

**Status Text:**
- Changes to: "Sun raha hoon..." (Listening...)
- Color: `--success-green`
- Font weight: `weight-medium`

**Cancel Button:**
- Size: `120px × 44px`
- Background: `--neutral-gray`
- Border radius: `--radius-full`
- Text: "Cancel" / "बंद करें"
- Position: `32px` below status text

---

### 🟢 STATE 3: CONVERSATION VIEW (CHAT MODE)

```
┌─────────────────────────────────────────┐
│ ☰  KisanMitra                      👤   │
├─────────────────────────────────────────┤
│ [SCROLLABLE CHAT AREA]                 │
│                                         │
│ ┌─────────────────────────────────┐    │
│ │ Namaste, Ramesh! 🙏             │    │ ← AI Greeting
│ │                                 │    │   (ai-response-bg)
│ │ How can I help with your       │    │
│ │ farm today?                    │    │
│ └─────────────────────────────────┘    │
│ 10:23 AM                               │ ← Timestamp
│                                         │
│                    ┌─────────────────┐ │
│                    │ Which crop is   │ │ ← User Message
│                    │ best this month?│ │   (user-message-bg)
│                    └─────────────────┘ │   Right-aligned
│                              10:24 AM   │
│                                         │
│ ┌─────────────────────────────────────┐│
│ │ 🌾 Wheat (Rabi Season)              ││ ← AI Response
│ │                                     ││   with Card
│ │ Given current date and your soil   ││
│ │ report, Wheat (Sharbati) is best.  ││
│ │                                     ││
│ │ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  ││
│ │ ┃ 💧 Medium Water                ┃  ││ ← Inline Card
│ │ ┃ 📅 120 Days                    ┃  ││   (card-bg)
│ │ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  ││
│ │                                     ││
│ │ [AUDIO PLAYING: 0:08 / 0:15] 🔊    ││ ← Audio Player
│ │ ━━━━━━━●━━━━━━━━━━━━━━━━━━━━━━━   ││   (Progress bar)
│ │                                     ││
│ │ "Given the current date and your   ││ ← Transcript
│ │ soil report from last week, Wheat  ││   (text-secondary)
│ │ Sharbati is your best option."     ││
│ └─────────────────────────────────────┘│
│ 10:24 AM                               │
│                                         │
│ ┌─────────────────────────────────────┐│
│ │ 🔍 Based on: Your soil type (Black),││ ← Context Indicator
│ │ Location (Pune), Season (Rabi)      ││   (warning-accent)
│ └─────────────────────────────────────┘│
│                                         │
├─────────────────────────────────────────┤
│                                         │
│  [Type or speak...]          [🎤]      │ ← Input Area
│                                         │
└─────────────────────────────────────────┘
```

**Component Specifications:**

**User Message Bubble:**
- Background: `--user-message-bg` (White)
- Border: `1px solid --card-border`
- Border radius: `--radius-lg` (top-left, top-right, bottom-left), `4px` (bottom-right)
- Padding: `12px 16px`
- Max width: `75%`
- Alignment: Right (flexbox `justify-content: flex-end`)
- Font: `body-medium`
- Color: `--text-primary`
- Shadow: `0 2px 8px rgba(0,0,0,0.08)`

**AI Message Bubble:**
- Background: `--ai-response-bg` (Light Green)
- Border radius: `--radius-lg` (all corners except bottom-left: `4px`)
- Padding: `16px`
- Max width: `85%`
- Alignment: Left
- Font: `body-medium`
- Color: `--text-primary`
- Shadow: `0 2px 8px rgba(0,0,0,0.08)`

**Timestamp:**
- Font: `caption` (12px)
- Color: `--text-secondary`
- Position: Below message, aligned with message side
- Margin: `4px`

---

### 🟢 STATE 4: CARD COMPONENTS (DETAILED DESIGNS)

#### **1️⃣ Crop Recommendation Card**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🌾 Wheat (Rabi Season)              ┃ ← Card Header
┃                                     ┃   (heading-medium)
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                     ┃
┃ Recommended for your farm           ┃ ← Description
┃                                     ┃   (body-small)
┃ ┌─────────────────────────────────┐┃
┃ │ 💧 Water Need    Medium         ││ ← Stat Rows
┃ │ 📅 Duration      120 Days       ││
┃ │ 💰 Expected      ₹45k/acre      ││
┃ │ ⚠️ Risk Level    Low            ││
┃ └─────────────────────────────────┘┃
┃                                     ┃
┃ ┌───────────────────────────────┐  ┃
┃ │     View Full Details    →    │  ┃ ← CTA Button
┃ └───────────────────────────────┘  ┃   (success-green bg)
┃                                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Specifications:**
- Background: `--card-bg`
- Border: `2px solid --card-border`
- Border radius: `--radius-lg`
- Padding: `20px`
- Margin: `16px 0`
- Shadow: `0 4px 12px rgba(0,0,0,0.1)`

**Card Header:**
- Icon: `32px` emoji/icon
- Text: `heading-medium`, `weight-bold`
- Spacing: `12px` between icon and text

**Stat Rows:**
- Layout: CSS Grid (2 columns)
- Each row:
  - Icon: `20px`
  - Label: `body-small`, `weight-medium`
  - Value: `body-small`, `weight-regular`
  - Spacing: `8px` vertical between rows

**CTA Button:**
- Height: `48px`
- Background: `--success-green`
- Border radius: `--radius-md`
- Text: `body-medium`, `weight-medium`, white color
- Icon: Right arrow `→`
- Hover: Darken by 10%

---

#### **2️⃣ Market Price Card**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 💰 Mandi Price - Wheat              ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                     ┃
┃ ┌─────────────────────────────────┐┃
┃ │  Current Price                  ││
┃ │  ₹2,850 per quintal             ││ ← Large Price
┃ │                                 ││   (heading-large)
┃ └─────────────────────────────────┘┃
┃                                     ┃
┃ ┌─────────────────────────────────┐┃
┃ │ Trend this week:                ││
┃ │ 📈 Rising ~+2.4%                ││ ← Trend Indicator
┃ │                                 ││   (success-green)
┃ └─────────────────────────────────┘┃
┃                                     ┃
┃ Last updated: 2 hours ago          ┃ ← Metadata
┃                                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Specifications:**
- Same base styling as Crop Card
- Price text: `heading-large` (24px), `weight-bold`
- Trend indicator:
  - Green for rising (`--success-green`)
  - Red for falling (`#EF5350`)
  - Gray for stable (`--neutral-gray`)
- Trend icon: `📈` or `📉`
- Last updated: `caption`, `--text-secondary`

---

#### **3️⃣ Government Scheme Card**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🏛️ PM-KISAN Subsidy                ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                     ┃
┃ ✅ You are eligible                 ┃ ← Eligibility Badge
┃                                     ┃   (success-green bg)
┃ Benefits:                           ┃
┃ • ₹6,000 per year                   ┃
┃ • Direct bank transfer              ┃
┃                                     ┃
┃ ⏰ Deadline: 15 days left           ┃ ← Deadline
┃                                     ┃   (warning-accent)
┃ ┌───────────────────────────────┐  ┃
┃ │      Apply Now    →           │  ┃ ← CTA
┃ └───────────────────────────────┘  ┃
┃                                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Specifications:**
- Eligibility badge:
  - Background: `--success-green` with 20% opacity
  - Border: `2px solid --success-green`
  - Border radius: `--radius-sm`
  - Padding: `8px 12px`
  - Text: `body-small`, `weight-medium`

- Deadline section:
  - Background: `--warning-accent` with 30% opacity
  - Padding: `8px`
  - Border radius: `--radius-sm`
  - Icon: Clock `⏰`

---

### 🔊 AUDIO PLAYER COMPONENT

```
┌─────────────────────────────────────────┐
│ 🔊 Playing response...           [⏸]   │ ← Audio Status
├─────────────────────────────────────────┤
│ ━━━━━━━━●━━━━━━━━━━━━━━━━━━━━━━━━━━━   │ ← Progress Bar
│ 0:08                            0:15    │ ← Time Display
└─────────────────────────────────────────┘
```

**Specifications:**
- Background: Transparent or slight `--ai-response-bg`
- Progress bar:
  - Height: `4px`
  - Background: `--neutral-gray` with 30% opacity
  - Progress: `--success-green`
  - Handle: `12px` circle, `--success-green`
- Controls:
  - Play/Pause button: `32px`, circular
  - Icon: White
- Time display: `caption`, `--text-secondary`

---

### 📝 TRANSCRIPT SECTION

```
┌─────────────────────────────────────────┐
│ 💬 Transcript                           │
├─────────────────────────────────────────┤
│                                         │
│ "Given the current date and your soil   │
│ report from last week, Wheat (Sharbati) │
│ is your best option. It requires medium │
│ water and will be ready in 120 days."   │
│                                         │
└─────────────────────────────────────────┘
```

**Specifications:**
- Background: `rgba(255,255,255,0.5)` (semi-transparent white)
- Border: `1px dashed --card-border`
- Border radius: `--radius-md`
- Padding: `16px`
- Font: `body-small`
- Color: `--text-secondary`
- Italic style
- Icon: Speech bubble `💬`

---

### 🟡 STATE 5: AGENTIC ACTION CONFIRMATION

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ⚡ Action Required                  ┃ ← Warning Header
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                     ┃
┃ Main tractor rental ke liye        ┃ ← Confirmation Text
┃ apply kar doon?                     ┃   (Hindi/Local)
┃                                     ┃
┃ ┌─────────────────────────────────┐┃
┃ │ 🚜 Tractor - Mahindra 575       ││ ← Details
┃ │ 💰 ₹800 per day                 ││
┃ │ 📅 Available: Tomorrow          ││
┃ │ 📍 Distance: 5 km               ││
┃ └─────────────────────────────────┘┃
┃                                     ┃
┃ ┌──────────┐      ┌──────────┐    ┃
┃ │   Yes    │      │    No    │    ┃ ← Action Buttons
┃ │  (हाँ)   │      │  (नहीं)  │    ┃
┃ └──────────┘      └──────────┘    ┃
┃                                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Specifications:**
- Background: `--warning-accent` (Yellow)
- Border: `3px solid #F9A825` (darker yellow)
- Header icon: `⚡` or `⚠️`

**Action Buttons:**
- **Yes Button:**
  - Background: `--success-green`
  - Width: `45%`
  - Height: `56px`
  - Border radius: `--radius-md`
  - Text: Bilingual (English + Hindi)
  - Font: `body-large`, `weight-bold`
  - Color: White

- **No Button:**
  - Background: `--neutral-gray`
  - Same dimensions as Yes
  - Text color: `--text-primary`

- Layout: Flexbox with `space-between`
- Gap: `16px`

---

### 🔁 STATE 6: CONTEXT MEMORY INDICATOR

```
┌─────────────────────────────────────────┐
│ 🧠 Context Used                         │
├─────────────────────────────────────────┤
│ • Soil Type: Black Soil                 │
│ • Location: Pune, Maharashtra           │
│ • Season: Rabi 2024                     │
│ • Last Crop: Soybean                    │
└─────────────────────────────────────────┘
```

**Specifications:**
- Background: `rgba(255, 249, 196, 0.3)` (light yellow with transparency)
- Border: `1px solid --warning-accent`
- Border radius: `--radius-md`
- Padding: `12px 16px`
- Icon: Brain `🧠` or Info `ℹ️`
- Font: `body-small`
- Color: `--text-secondary`
- Bullet points: Simple dots
- Appears ABOVE AI response cards

---

## 💬 INPUT AREA (BOTTOM BAR)

```
┌─────────────────────────────────────────┐
│                                         │
│  [Type or speak...]              [🎤]  │
│  ────────────────────────────   ─────  │
│                                         │
└─────────────────────────────────────────┘
```

**Specifications:**
- Height: `72px`
- Background: `--background` (Beige)
- Border top: `1px solid --card-border`
- Padding: `12px 16px`

**Text Input:**
- Width: `calc(100% - 80px)`
- Height: `48px`
- Background: White
- Border: `1px solid --card-border`
- Border radius: `--radius-full`
- Padding: `12px 20px`
- Placeholder: "Type or speak..." (multi-language)
- Font: `body-medium`

**Mic Button (Small):**
- Size: `56px × 56px`
- Background: `--success-green`
- Border radius: `--radius-full`
- Icon: White mic, `28px`
- Position: Right of input
- Shadow: `0 2px 8px rgba(102,187,106,0.3)`
- Active state: Scale to 1.1

---

## 🎭 ANIMATIONS & INTERACTIONS

### Microphone Pulse (Idle)
```css
@keyframes pulse-idle {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.8; }
}
/* Duration: 2s, ease-in-out, infinite */
```

### Microphone Active Glow
```css
@keyframes glow-active {
  0%, 100% { box-shadow: 0 0 20px rgba(102,187,106,0.4); }
  50% { box-shadow: 0 0 40px rgba(102,187,106,0.8); }
}
/* Duration: 1s, ease-in-out, infinite */
```

### Card Slide-In
```css
@keyframes slide-in-bottom {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
/* Duration: 0.3s, ease-out */
```

### Audio Wave Animation
```css
/* For listening state bars */
@keyframes audio-wave {
  0%, 100% { height: 4px; }
  50% { height: 20px; }
}
/* Apply with staggered delays: 0s, 0.1s, 0.2s, 0.3s */
```

---

## 📐 RESPONSIVE BREAKPOINTS

### Mobile (Default: 320px - 768px)
- All designs above are mobile-first
- Full-width cards
- Single column layout
- Large touch targets (min 48px)

### Tablet (768px - 1024px)
- Cards max-width: `600px`, centered
- Increased padding: `24px`
- Side margins for chat area

### Desktop (1024px+)
- Chat area max-width: `800px`, centered
- Sidebar visible (not designed here)
- Floating mic button (bottom-right when on other screens)

---

## ♿ ACCESSIBILITY REQUIREMENTS

1. **High Contrast:**
   - All text meets WCAG AA (4.5:1 ratio)
   - Important elements meet AAA (7:1 ratio)

2. **Touch Targets:**
   - Minimum: `48px × 48px`
   - Spacing between: `8px`

3. **Sunlight Readability:**
   - Avoid pure white backgrounds
   - Use beige/cream tones
   - High contrast borders on cards

4. **Screen Reader Support:**
   - Semantic HTML
   - ARIA labels for icons
   - Role attributes for chat bubbles

5. **Keyboard Navigation:**
   - Tab order: Menu → Input → Mic → Cards
   - Enter key submits
   - Escape cancels listening

---

## 🎯 FINAL DESIGN PRINCIPLES

1. **Voice is Hero:** Microphone is always the most prominent element
2. **Visual Hierarchy:** Cards > Text > Metadata
3. **Calm Palette:** No aggressive colors, trust-building tones
4. **Large Text:** Readable in bright sunlight
5. **Bilingual Support:** Space for Hindi/Marathi alongside English
6. **Progressive Disclosure:** Show simple first, details on tap
7. **Confidence Building:** Context indicators, confirmation cards
8. **Forgiving UX:** Easy cancel, undo, retry options

---

## 📦 DELIVERABLE CHECKLIST

### Required Screens:
- ✅ State 1: Idle Home Screen
- ✅ State 2: Listening Mode
- ✅ State 3: Conversation View
- ✅ State 4: AI Response with Cards (3 card types minimum)
- ✅ State 5: Confirmation Dialog
- ✅ State 6: Context Indicator

### Required Components:
- ✅ Microphone button (idle + active states)
- ✅ User message bubble
- ✅ AI message bubble
- ✅ Crop Recommendation Card
- ✅ Market Price Card
- ✅ Government Scheme Card
- ✅ Audio player
- ✅ Transcript section
- ✅ Confirmation card
- ✅ Context indicator
- ✅ Input bar with mic

### Design Assets:
- High-fidelity mockups (Figma/PNG)
- Component library
- Color palette documentation
- Typography scale
- Spacing system
- Animation specifications

---

## 🚀 IMPLEMENTATION NOTES FOR DEVELOPERS

1. **React Components Structure:**
```
VoiceChatInterface/
├── VoiceButton.jsx
├── ChatTimeline.jsx
├── MessageBubble.jsx
├── cards/
│   ├── CropCard.jsx
```jsx
├── cards/
│   ├── CropCard.jsx
│   ├── MarketPriceCard.jsx
│   ├── SchemeCard.jsx
│   └── ConfirmationCard.jsx
├── AudioPlayer.jsx
├── TranscriptBox.jsx
├── ContextIndicator.jsx
└── InputBar.jsx
```

2. **State Management:**
```javascript
const [voiceState, setVoiceState] = useState('idle'); // idle | listening | processing
const [messages, setMessages] = useState([]);
const [isAudioPlaying, setIsAudioPlaying] = useState(false);
const [currentAudio, setCurrentAudio] = useState(null);
```

3. **Web Speech API Integration:**
```javascript
// Speech-to-Text
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'hi-IN'; // or 'en-IN'
recognition.continuous = false;
recognition.interimResults = true;

// Text-to-Speech
const utterance = new SpeechSynthesisUtterance();
utterance.lang = 'hi-IN';
utterance.rate = 0.9; // Slightly slower for clarity
```

4. **Card Rendering Logic:**
```javascript
const renderCard = (cardType, cardData) => {
  switch(cardType) {
    case 'cropRecommendation':
      return <CropCard data={cardData} />;
    case 'marketPrice':
      return <MarketPriceCard data={cardData} />;
    case 'governmentScheme':
      return <SchemeCard data={cardData} />;
    case 'confirmation':
      return <ConfirmationCard data={cardData} onConfirm={handleConfirm} />;
    default:
      return null;
  }
};
```

5. **Audio Player Integration:**
```javascript
const playAudioResponse = async (speechText, language = 'hi-IN') => {
  // Stop any currently playing audio
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.currentTime = 0;
  }
  
  // Option 1: Web Speech Synthesis (Free, built-in)
  const utterance = new SpeechSynthesisUtterance(speechText);
  utterance.lang = language;
  utterance.rate = 0.9;
  utterance.pitch = 1.0;
  
  utterance.onstart = () => setIsAudioPlaying(true);
  utterance.onend = () => setIsAudioPlaying(false);
  
  window.speechSynthesis.speak(utterance);
  
  // Option 2: Use pre-generated audio from backend
  // const audio = new Audio(audioUrl);
  // audio.play();
};
```

6. **Responsive Adjustments for Web:**
```css
/* Web-First Responsive Design */

/* Desktop Large (1920px+) */
@media (min-width: 1920px) {
  .chat-container {
    max-width: 900px;
    margin: 0 auto;
  }
  
  .voice-button {
    width: 160px;
    height: 160px;
  }
}

/* Desktop Standard (1280px - 1920px) */
@media (min-width: 1280px) and (max-width: 1919px) {
  .chat-container {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .voice-button {
    width: 140px;
    height: 140px;
  }
  
  .card {
    max-width: 600px;
  }
}

/* Laptop (1024px - 1279px) */
@media (min-width: 1024px) and (max-width: 1279px) {
  .chat-container {
    max-width: 700px;
    padding: 0 32px;
  }
  
  .voice-button {
    width: 120px;
    height: 120px;
  }
}

/* Tablet (768px - 1023px) */
@media (min-width: 768px) and (max-width: 1023px) {
  .chat-container {
    max-width: 600px;
    padding: 0 24px;
  }
  
  .message-bubble {
    max-width: 80%;
  }
}

/* Mobile (up to 767px) */
@media (max-width: 767px) {
  .chat-container {
    padding: 0 16px;
  }
  
  .voice-button {
    width: 100px;
    height: 100px;
  }
  
  .card {
    padding: 16px;
  }
  
  /* Stack action buttons vertically on small screens */
  .confirmation-actions {
    flex-direction: column;
    gap: 12px;
  }
  
  .confirmation-actions button {
    width: 100%;
  }
}
```

7. **Performance Optimizations:**
```javascript
// Lazy load cards
const CropCard = lazy(() => import('./cards/CropCard'));
const MarketPriceCard = lazy(() => import('./cards/MarketPriceCard'));

// Memoize expensive components
const ChatMessage = memo(({ message, type, cardData }) => {
  return (
    <div className={`message ${type}`}>
      {type === 'ai' && cardData && (
        <Suspense fallback={<CardSkeleton />}>
          {renderCard(cardData.type, cardData.data)}
        </Suspense>
      )}
    </div>
  );
});

// Virtualize long chat lists
import { FixedSizeList } from 'react-window';
```

8. **Error Handling:**
```javascript
const handleVoiceError = (error) => {
  const errorMessages = {
    'no-speech': 'कोई आवाज़ नहीं सुनाई दी। कृपया फिर से बोलें।',
    'audio-capture': 'माइक्रोफोन एक्सेस नहीं मिला। कृपया अनुमति दें।',
    'network': 'इंटरनेट कनेक्शन की समस्या। कृपया जांचें।',
    'not-allowed': 'माइक्रोफोन एक्सेस अस्वीकृत किया गया।'
  };
  
  const message = errorMessages[error.error] || 'कुछ गलत हुआ। कृपया फिर से कोशिश करें।';
  
  // Show error toast/notification
  showNotification(message, 'error');
  
  // Reset to idle state
  setVoiceState('idle');
};
```

---

## 🌐 WEB-SPECIFIC CONSIDERATIONS

### Browser Compatibility
```javascript
// Check for required APIs
const checkBrowserSupport = () => {
  const hasWebSpeech = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
  const hasSpeechSynthesis = 'speechSynthesis' in window;
  const hasAudioAPI = 'AudioContext' in window || 'webkitAudioContext' in window;
  
  if (!hasWebSpeech) {
    showWarning('Voice input not supported in this browser. Please use Chrome or Edge.');
  }
  
  return {
    webSpeech: hasWebSpeech,
    speechSynthesis: hasSpeechSynthesis,
    audioAPI: hasAudioAPI
  };
};
```

### Desktop-Specific Features
```javascript
// Keyboard shortcuts
useEffect(() => {
  const handleKeyPress = (e) => {
    // Space bar to toggle mic (when not typing)
    if (e.code === 'Space' && !e.target.matches('input, textarea')) {
      e.preventDefault();
      toggleVoiceInput();
    }
    
    // Escape to cancel listening
    if (e.code === 'Escape' && voiceState === 'listening') {
      cancelListening();
    }
    
    // Ctrl/Cmd + K for quick voice input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      startListening();
    }
  };
  
  window.addEventListener('keydown', handleKeyPress);
  return () => window.removeEventListener('keydown', handleKeyPress);
}, [voiceState]);
```

### Desktop Layout Enhancements
```css
/* Desktop: Two-panel layout option */
@media (min-width: 1280px) {
  .app-container {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 0;
  }
  
  .sidebar {
    display: block; /* Hidden on mobile, visible on desktop */
    background: var(--background);
    border-right: 1px solid var(--card-border);
    padding: 24px;
  }
  
  .chat-main {
    display: flex;
    flex-direction: column;
    max-width: 900px;
    margin: 0 auto;
  }
  
  /* Floating mic button on other screens (desktop) */
  .floating-mic {
    position: fixed;
    bottom: 32px;
    right: 32px;
    width: 72px;
    height: 72px;
    border-radius: 50%;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    z-index: 1000;
  }
}
```

### Web Notifications
```javascript
// Request permission for browser notifications
const requestNotificationPermission = async () => {
  if ('Notification' in window && Notification.permission === 'default') {
    await Notification.requestPermission();
  }
};

// Send notification when AI response is ready (if tab not focused)
const notifyResponse = (message) => {
  if (document.hidden && Notification.permission === 'granted') {
    new Notification('KisanMitra Response', {
      body: message.substring(0, 100) + '...',
      icon: '/icon-192.png',
      badge: '/badge-72.png',
      tag: 'kisanmitra-response'
    });
  }
};
```

### Progressive Web App (PWA) Configuration
```javascript
// manifest.json
{
  "name": "KisanMitra - Voice Assistant",
  "short_name": "KisanMitra",
  "description": "AI-powered farming assistant for Indian farmers",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#F5F5DC",
  "theme_color": "#66BB6A",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "categories": ["agriculture", "productivity"],
  "lang": "hi-IN"
}
```

---

## 🎨 ADDITIONAL WEB UI PATTERNS

### Loading States
```jsx
// Skeleton loader for cards
const CardSkeleton = () => (
  <div className="card-skeleton">
    <div className="skeleton-header" />
    <div className="skeleton-line" />
    <div className="skeleton-line short" />
    <div className="skeleton-button" />
  </div>
);

// CSS for skeleton animation
@keyframes skeleton-loading {
  0% { background-position: -200px 0; }
  100% { background-position: calc(200px + 100%) 0; }
}

.skeleton-header,
.skeleton-line,
.skeleton-button {
  background: linear-gradient(
    90deg,
    #f0f0f0 0px,
    #e0e0e0 40px,
    #f0f0f0 80px
  );
  background-size: 200px 100%;
  animation: skeleton-loading 1.5s infinite;
}
```

### Empty States
```jsx
// When no conversation exists
const EmptyState = () => (
  <div className="empty-state">
    <div className="empty-icon">🌾</div>
    <h2>Namaste! 🙏</h2>
    <p>Main aapke kheti ke saath madad karne ke liye yahan hoon.</p>
    <p className="secondary">Kuch bhi poochein - fasal, mandi, mausam, yojana...</p>
  </div>
);
```

### Offline Indicator
```jsx
const OfflineBanner = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);
  
  if (isOnline) return null;
  
  return (
    <div className="offline-banner">
      <span>⚠️ Internet connection lost. Limited features available.</span>
    </div>
  );
};
```

---

## 🔧 BACKEND API CONTRACT

### Expected Request Format
```typescript
// POST /api/voice-query
interface VoiceQueryRequest {
  transcript: string;
  userId: string;
  sessionId: string;
  context: {
    location: {
      lat: number;
      lng: number;
      district: string;
      state: string;
    };
    activeCrops: Array<{
      cropId: string;
      name: string;
      stage: string;
      plantedDate: string;
    }>;
    soilData?: {
      type: string;
      ph: number;
      moisture: string;
      lastTested: string;
    };
    language: 'hi' | 'en' | 'mr'; // Hindi, English, Marathi
    timestamp: string;
  };
  conversationHistory?: Array<{
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
  }>;
}
```

### Expected Response Format
```typescript
// Response from /api/voice-query
interface VoiceQueryResponse {
  intent: 'crop_recommendation' | 'market_price' | 'weather' | 'scheme' | 'diagnosis' | 'confirmation' | 'general';
  
  message: {
    text: string; // Human-readable response
    speechText: string; // Optimized for TTS (may differ from text)
    language: string;
  };
  
  card?: {
    type: 'cropRecommendation' | 'marketPrice' | 'governmentScheme' | 'confirmation' | 'weatherForecast';
    data: Record<string, any>; // Type-specific data
  };
  
  context?: {
    sources: string[]; // Data sources used
    confidence: number; // 0-1 confidence score
    usedContext: string[]; // Which context was considered
  };
  
  actions?: Array<{
    id: string;
    type: 'apply_scheme' | 'book_service' | 'view_details';
    label: string;
    requiresConfirmation: boolean;
  }>;
  
  audioUrl?: string; // Optional: Pre-generated audio file
  
  followUp?: {
    suggestions: string[]; // Quick reply suggestions
  };
}
```

### Example Response
```json
{
  "intent": "crop_recommendation",
  "message": {
    "text": "Given the current date and your soil report from last week, Wheat (Sharbati) is your best option.",
    "speechText": "Aapki mitti aur mausam ko dekhte hue, Gehun Sharbati variety sabse acchi rahegi. Isमें paani medium chahiye aur 120 din mein taiyar ho jayegi.",
    "language": "hi"
  },
  "card": {
    "type": "cropRecommendation",
    "data": {
      "cropName": "Wheat (Sharbati)",
      "season": "Rabi",
      "waterRequirement": "Medium",
      "duration": "120 days",
      "expectedYield": "45 quintal/acre",
      "profitPotential": "₹45,000/acre",
      "riskLevel": "Low",
      "reasons": [
        "Black soil suitable",
        "Optimal Rabi season",
        "Good market demand"
      ]
    }
  },
  "context": {
    "sources": ["soil_report_2024_01_15", "weather_forecast", "market_data"],
    "confidence": 0.92,
    "usedContext": ["soilType", "season", "location"]
  },
  "followUp": {
    "suggestions": [
      "Where to buy Sharbati seeds?",
      "What's the current wheat price?",
      "Show me planting guide"
    ]
  }
}
```

---

## 🧪 TESTING CHECKLIST

### Functional Testing
- [ ] Microphone permission request works
- [ ] Speech-to-text converts correctly (Hindi & English)
- [ ] Text-to-speech plays responses
- [ ] Cards render based on response type
- [ ] Audio player controls work (play/pause/seek)
- [ ] Transcript displays correctly
- [ ] Confirmation dialogs work
- [ ] Context indicator shows relevant data
- [ ] Conversation history persists
- [ ] Input bar sends messages
- [ ] Keyboard shortcuts function

### Cross-Browser Testing
- [ ] Chrome (latest)
- [ ] Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Test on Windows, macOS, Linux

### Performance Testing
- [ ] Page load time < 2 seconds
- [ ] Audio playback starts within 500ms
- [ ] Card animations smooth (60fps)
- [ ] No memory leaks in long conversations
- [ ] Chat scrolling remains smooth with 100+ messages

### Accessibility Testing
- [ ] Screen reader compatibility
- [ ] Keyboard navigation complete
- [ ] Color contrast ratios meet WCAG AA
- [ ] Touch targets meet 48px minimum
- [ ] Focus indicators visible

### Network Condition Testing
- [ ] Works on slow 3G
- [ ] Graceful degradation when offline
- [ ] Error messages clear when API fails
- [ ] Retry mechanisms functional

---

## 📝 DESIGN HANDOFF NOTES

### For Figma/Design Tool Users

1. **Create Component Library:**
   - Button variations (primary, secondary, mic)
   - Card templates (all 3 types)
   - Message bubbles (user, AI)
   - Input fields
   - Icons set

2. **Use Auto Layout:**
   - All cards should resize based on content
   - Chat messages should stack vertically
   - Buttons should have consistent padding

3. **Define Variants:**
   - Microphone: idle, listening, disabled
   - Cards: default, hover, pressed
   - Messages: user, AI, system

4. **Export Assets:**
   - Icons as SVG
   - Illustrations at 2x resolution
   - Provide design tokens JSON

5. **Prototype Interactions:**
   - Mic tap → listening state
   - Card tap → detail view
   - Action button → confirmation

---

## 🚀 DEPLOYMENT RECOMMENDATIONS

### Staging Environment
```bash
# Environment variables
VITE_API_BASE_URL=https://api-staging.kisanmitra.in
VITE_ENABLE_ANALYTICS=false
VITE_LOG_LEVEL=debug
```

### Production Environment
```bash
VITE_API_BASE_URL=https://api.kisanmitra.in
VITE_ENABLE_ANALYTICS=true
VITE_LOG_LEVEL=error
VITE_SENTRY_DSN=your_sentry_dsn
```

### Performance Monitoring
```javascript
// Track key metrics
import { onCLS, onFID, onLCP, onTTFB } from 'web-vitals';

onCLS(metric => sendToAnalytics('CLS', metric));
onFID(metric => sendToAnalytics('FID', metric));
onLCP(metric => sendToAnalytics('LCP', metric));
onTTFB(metric => sendToAnalytics('TTFB', metric));

// Custom metrics
const trackVoiceInteraction = (duration, success) => {
  sendToAnalytics('voice_interaction', {
    duration,
    success,
    timestamp: Date.now()
  });
};
```

---

## ✅ FINAL ACCEPTANCE CRITERIA

### Visual Design
- [ ] Matches color palette exactly
- [ ] Typography hierarchy clear
- [ ] Spacing consistent throughout
- [ ] All 6 states designed
- [ ] Animations specified
- [ ] Responsive behavior documented

### User Experience
- [ ] Voice input feels natural
- [ ] Visual feedback immediate
- [ ] Cards actionable and clear
- [ ] Error states helpful
- [ ] Loading states smooth
- [ ] Bilingual support complete

### Technical
- [ ] Component structure logical
- [ ] State management planned
- [ ] API contract defined
- [ ] Performance optimized
- [ ] Accessibility compliant
- [ ] Browser support confirmed

---

**END OF DESIGN SPECIFICATION**

This comprehensive design system provides everything needed to implement the KisanMitra Voice-First Chat Interface for web. When moving to mobile, the core components and design language remain the same—only layout proportions and interaction patterns will need adjustment.