# KisaanMitra Frontend Implementation Plan

## 1. Technology Stack
- **Framework**: React (Vite)
- **Language**: JavaScript (JSX)
- **Styling**: Vanilla CSS (CSS Variables for theming)
- **Routing**: react-router-dom
- **Icons**: lucide-react
- **HTTP Client**: fetch (native)

## 2. Project Structure
```
Frontend/
├── src/
│   ├── assets/            # Images, static files
│   ├── components/        # Reusable UI components
│   │   ├── Layout.jsx     # Global wrapper (Sidebar + Mic)
│   │   ├── Sidebar.jsx    # Hamburger & Navigation
│   │   ├── VoiceAgent.jsx # Floating Mic Button
│   │   └── Card.jsx       # Standard card container
│   ├── pages/             # Main feature pages
│   │   ├── Dashboard.jsx
│   │   ├── Planning.jsx   # Crop Selection, Schemes
│   │   ├── Farming.jsx    # Doctor, Irrigation, Input
│   │   ├── PostHarvest.jsx
│   │   ├── Inventory.jsx
│   │   ├── Collaborative.jsx
│   │   ├── Finance.jsx
│   │   ├── Schemes.jsx
│   │   └── Alerts.jsx
│   ├── styles/
│   │   ├── global.css     # Variables, resets, typography
│   │   └── layout.css     # Specific layout styles
│   ├── App.jsx            # Routing configuration
│   └── main.jsx           # Entry point
├── index.html
└── package.json
```

## 3. Design Tokens (CSS Variables)
To strictly adhere to the "Calm Farmer" theme:
```css
:root {
  /* Palette */
  --color-primary-green: #4CAF50;    /* Light Soft Green */
  --color-accent-yellow: #FFEB3B;    /* Warning/Highlight */
  --color-bg-beige: #F5F5DC;         /* Calm Background */
  --color-card-brown: #FFF8E1;       /* Light Brownish Yellow (Cards) */
  --color-text-dark: #2E3B2E;        /* Soft Black/Green for text */
  --color-text-muted: #5C6B5C;       /* Secondary text */
  
  /* Spacing & Radius */
  --radius-card: 16px;               /* Friendly, rounded corners */
  --spacing-unit: 8px;
  
  /* Typography */
  --font-body: 'Inter', sans-serif;  /* Clean, readable */
}
```

## 4. Implementation Steps

### Phase 1: Setup & Foundation
1.  Initialize Vite project.
2.  Install `react-router-dom` and `lucide-react`.
3.  Define `global.css` with the strict color palette and reset.
4.  Set up the Router in `App.jsx`.

### Phase 2: Core Layout (The "Shell")
1.  **Sidebar (`Sidebar.jsx`)**:
    -   Hamburger menu (Top-Left).
    -   Drawer animation.
    -   Navigation links matching the roadmap.
2.  **Voice Agent (`VoiceAgent.jsx`)**:
    -   Floating Action Button (Bottom-Right).
    -   Microphone icon.
3.  **Layout Wrapper (`Layout.jsx`)**:
    -   Combines Sidebar, Main Content, and Voice Agent.

### Phase 3: Dashboard (MVP View)
1.  **Overview Cards**:
    -   Active Crops, Mandi Prices, Weather.
    -   Use CSS Grid/Flexbox for responsive card layout.
2.  **Mock Data**:
    -   Hardcode initial data to demonstrate "State 1: Overview".

### Phase 4: Farm Management Pages
1.  **Planning Stage**: Crop Selection UI.
2.  **Farming Stage**: Crop Doctor (Image upload placeholder), Smart Irrigation.
3.  **Post-Harvest**: Sell vs Hold cards.

### Phase 5: Polish
1.  Verify "Sunlight Readability" (High contrast text on beige).
2.  Ensure large touch targets (Mobile-ready feel).
3.  Check Navigation flow.

## 5. Execution Rule
-   All CSS will be written in `src/styles` or component-specific CSS files if needed (e.g., `Dashboard.css`).
-   No complex build steps.
-   Adhere to "Future Native" rule: Keep state logic simple and decoupled from complex DOM events.
