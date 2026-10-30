import streamlit as st


def aplicar_estilos() -> None:
    st.markdown(
        """
        <style>
        :root {
            --page: #F8FAFC;
            --surface: #FFFFFF;
            --ink: #172033;
            --muted: #475569;
            --brand: #6D28D9;
            --brand-dark: #4C1D95;
            --brand-soft: #EDE9FE;
            --border: #CBD5E1;
            --focus: #B45309;
        }
        #MainMenu, footer { visibility: hidden; }
        [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background: var(--page);
            color: var(--ink);
        }
        .block-container {
            max-width: 75rem;
            padding: 1.25rem 1.5rem 4rem;
        }
        [data-testid="stAppViewContainer"] h1,
        [data-testid="stAppViewContainer"] h2,
        [data-testid="stAppViewContainer"] h3,
        [data-testid="stAppViewContainer"] p,
        [data-testid="stAppViewContainer"] label,
        [data-testid="stMarkdownContainer"] { color: var(--ink); }
        [data-testid="stAppViewContainer"] p {
            font-size: 1rem;
            line-height: 1.55;
        }
        [data-testid="stAppViewContainer"] h1 {
            font-size: clamp(1.75rem, 3vw, 2.45rem);
            line-height: 1.15;
            letter-spacing: -0.02em;
        }
        [data-testid="stAppViewContainer"] h2 {
            font-size: clamp(1.3rem, 2vw, 1.75rem);
            line-height: 1.25;
            margin-top: 1.4rem;
        }
        [data-testid="stAppViewContainer"] h3 {
            font-size: 1.15rem;
            line-height: 1.3;
        }
        .app-header {
            align-items: center;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.8rem;
            padding: 0.15rem 0 0.8rem;
        }
        .brand-mark {
            align-items: center;
            color: var(--brand-dark);
            display: inline-flex;
            font-size: 0.88rem;
            font-weight: 800;
            gap: 0.5rem;
            letter-spacing: 0.04em;
        }
        .brand-mark span {
            align-items: center;
            background: var(--brand);
            border-radius: 0.55rem;
            color: #FFFFFF;
            display: inline-flex;
            height: 1.8rem;
            justify-content: center;
            width: 1.8rem;
        }
        .territory-label {
            color: var(--ink);
            font-size: 1rem;
            font-weight: 800;
            margin-top: 0.35rem;
        }
        .territory-label span {
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 500;
        }
        .st-key-nav-mobile { display: none; }
        .st-key-menu-items {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 0.9rem;
            margin: 0.35rem 0 0.75rem;
            padding: 0.75rem;
        }
        .action-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 1rem;
            min-height: 7rem;
            padding: 1rem;
        }
        .action-card h3 {
            margin: 0 0 0.35rem;
        }
        .action-card p {
            color: var(--muted) !important;
            font-size: 0.92rem !important;
            margin: 0;
        }
        .section-kicker {
            color: var(--brand-dark);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
        }
        .section-card, .info-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 1.5rem;
            box-shadow: 0 2px 8px rgba(23, 32, 51, 0.05);
            margin: 0.5rem 0 1.25rem;
            padding: 1.2rem 1.3rem;
        }
        .territorial-kpi {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 20px;
            padding: 1rem;
            min-height: 132px;
        }
        .territorial-kpi-label { color: #475569; font-size: .95rem; font-weight: 650; }
        .territorial-kpi-value { color: #172033; font-size: 1.45rem; font-weight: 750; margin-top: .55rem; }
        .territorial-kpi-meta, .territorial-kpi-note { color: #475569; font-size: .8rem; margin-top: .4rem; }
        .info-card {
            height: auto;
            min-height: 8rem;
            margin: 0;
        }
        .info-card h3 { margin-top: 0; }
        .info-card p { color: var(--muted) !important; margin-bottom: 0; }
        .context-note {
            background: var(--brand-soft);
            border-radius: 1rem;
            color: var(--ink);
            line-height: 1.5;
            margin: 1rem 0;
            padding: 0.85rem 1rem;
        }
        .source-strip {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 1rem;
            margin: 1rem 0;
            padding: 0.8rem 1rem;
        }
        .source-strip p { color: var(--muted) !important; font-size: 0.9rem !important; margin: 0; }
        .status-pill {
            background: var(--brand-soft);
            border-radius: 999px;
            color: var(--brand-dark);
            display: inline-block;
            font-size: 0.85rem;
            font-weight: 800;
            padding: 0.35rem 0.75rem;
        }
        [data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 1.25rem;
            box-shadow: 0 2px 8px rgba(23, 32, 51, 0.05);
            min-height: 6rem;
            padding: 0.85rem 1rem;
        }
        [data-testid="stMetricLabel"], [data-testid="stMetricValue"],
        [data-testid="stMetricDelta"] {
            overflow-wrap: anywhere;
            white-space: normal;
        }
        [data-testid="stMetricLabel"] > div,
        [data-testid="stMetricLabel"] > div > div,
        [data-testid="stMetricValue"] > div,
        [data-testid="stMetricValue"] > div > div {
            overflow: visible;
            white-space: normal;
        }
        [data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.9rem; }
        [data-testid="stMetricValue"], [data-testid="stMetricDelta"] { color: var(--ink) !important; }
        [data-testid="stAlert"] { border-radius: 1rem; }
        [data-testid="stButton"] button {
            border-radius: 999px;
            font-weight: 800;
            min-height: 2.75rem;
            padding: 0.55rem 1.2rem;
        }
        [data-testid="stButton"] button[kind="primary"],
        [data-testid="stBaseButton-primary"] {
            background: var(--brand);
            border-color: var(--brand);
            color: #FFFFFF !important;
        }
        [data-testid="stBaseButton-primary"] * { color: #FFFFFF !important; }
        [data-testid="stButton"] button[kind="primary"]:hover,
        [data-testid="stBaseButton-primary"]:hover {
            background: var(--brand-dark);
            border-color: var(--brand-dark);
        }
        [data-testid="stButton"] button:not([kind="primary"]) {
            border-color: var(--border);
            color: var(--ink);
        }
        [data-testid="stButton"] button:focus-visible,
        input:focus-visible, textarea:focus-visible,
        [role="combobox"]:focus-visible, [role="radio"]:focus-visible,
        [role="option"]:focus-visible {
            outline: 3px solid var(--focus) !important;
            outline-offset: 2px !important;
        }
        [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input,
        [data-testid="stTimeInput"] input,
        [data-testid="stSelectbox"] [data-baseweb="select"] > div,
        [data-testid="stMultiSelect"] [data-baseweb="select"] > div {
            background: var(--surface);
            border-color: var(--border);
            color: var(--ink);
        }
        [data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 1rem;
            overflow: hidden;
        }
        @media (max-width: 768px) {
            .block-container { padding: 1rem 0.8rem 2.5rem; }
            .st-key-nav-desktop { display: none; }
            .st-key-nav-mobile { display: block; }
            [data-testid="stHorizontalBlock"] { flex-direction: column; gap: 0.65rem; }
            [data-testid="stButton"] button { width: 100%; }
            [data-testid="stDataFrame"] { max-width: 100%; overflow-x: auto; }
            section.main iframe { height: 390px !important; max-width: 100%; }
        }
        @media (min-width: 769px) { section.main iframe { height: 560px !important; } }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after { scroll-behavior: auto !important; transition-duration: 0.01ms !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
