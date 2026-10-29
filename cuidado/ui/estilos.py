import streamlit as st


def aplicar_estilos() -> None:
    st.markdown(
        """
        <style>
        :root {
            --surface: #FFFFFF;
            --surface-muted: #F1F5F9;
            --page: #F8FAFC;
            --ink: #172033;
            --muted: #475569;
            --brand: #6D28D9;
            --brand-dark: #4C1D95;
            --brand-soft: #EDE9FE;
            --border: #CBD5E1;
            --focus: #B45309;
        }

        #MainMenu, footer { visibility: hidden; }
        [data-testid="stAppViewContainer"] {
            background: var(--page);
            color: var(--ink);
        }
        [data-testid="stHeader"] {
            background: var(--page);
        }
        .block-container {
            max-width: 76rem;
            padding: 2rem 2rem 4rem;
        }
        [data-testid="stAppViewContainer"] h1,
        [data-testid="stAppViewContainer"] h2,
        [data-testid="stAppViewContainer"] h3,
        [data-testid="stAppViewContainer"] p,
        [data-testid="stAppViewContainer"] label,
        [data-testid="stMarkdownContainer"] {
            color: var(--ink);
        }
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

        [data-testid="stSidebar"] {
            background: var(--surface);
            border-right: 1px solid var(--border);
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: var(--muted);
            font-size: 0.9rem;
        }
        [data-testid="stSidebar"] [role="radiogroup"] label {
            border-radius: 0.65rem;
            padding: 0.55rem 0.7rem;
            min-height: 2.75rem;
        }
        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: var(--brand-soft);
        }

        .brand-mark {
            align-items: center;
            color: var(--brand-dark);
            display: inline-flex;
            font-size: 0.78rem;
            font-weight: 800;
            gap: 0.5rem;
            letter-spacing: 0.08em;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
        }
        .brand-mark span {
            align-items: center;
            background: var(--brand);
            border-radius: 0.55rem;
            color: #FFFFFF;
            display: inline-flex;
            height: 1.7rem;
            justify-content: center;
            width: 1.7rem;
        }
        .page-intro {
            border-bottom: 1px solid var(--border);
            margin-bottom: 1.35rem;
            padding-bottom: 1rem;
        }
        .page-intro p {
            color: var(--muted) !important;
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
        .section-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 0.8rem;
            box-shadow: 0 2px 8px rgba(23, 32, 51, 0.05);
            margin: 0.5rem 0 1.25rem;
            padding: 1rem 1.1rem;
        }
        .section-card p {
            margin: 0;
        }
        .source-strip {
            background: #FFFBEB;
            border: 1px solid #FCD34D;
            border-left: 4px solid #B45309;
            border-radius: 0.65rem;
            margin: 1rem 0;
            padding: 0.7rem 0.85rem;
        }
        .source-strip p {
            color: #78350F !important;
            font-size: 0.9rem !important;
            margin: 0;
        }
        .structural-gaps {
            margin: 1.5rem 0 0.75rem;
        }
        .structural-gaps-intro {
            color: var(--muted) !important;
            margin: 0 0 0.75rem;
        }
        .structural-gap-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-left: 4px solid var(--gap-accent);
            border-radius: 0.7rem;
            min-height: 8.5rem;
            padding: 0.85rem;
        }
        .structural-gap-icon {
            font-size: 1.4rem;
            line-height: 1;
            margin-bottom: 0.45rem;
        }
        .structural-gap-card h3 {
            font-size: 1rem;
            margin: 0 0 0.35rem;
        }
        .structural-gap-card p {
            color: var(--muted) !important;
            font-size: 0.9rem !important;
            line-height: 1.35 !important;
            margin: 0;
        }
        [data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 0.75rem;
            box-shadow: 0 2px 8px rgba(23, 32, 51, 0.05);
            min-height: 6rem;
            padding: 0.85rem 1rem;
        }
        [data-testid="stMetricLabel"] {
            color: var(--muted) !important;
            font-size: 0.9rem;
            line-height: 1.25;
            white-space: normal;
        }
        [data-testid="stMetricLabel"] > div,
        [data-testid="stMetricLabel"] > div > div {
            overflow: visible;
            white-space: normal;
        }
        [data-testid="stMetricValue"],
        [data-testid="stMetricDelta"] {
            color: var(--ink) !important;
            overflow-wrap: anywhere;
            white-space: normal;
        }
        [data-testid="stMetricValue"] > div,
        [data-testid="stMetricValue"] > div > div {
            overflow: visible;
            white-space: normal;
        }
        [data-baseweb="tab-list"] {
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            gap: 0.25rem;
        }
        [data-baseweb="tab"] {
            color: var(--muted) !important;
            font-weight: 700;
            min-height: 2.75rem;
        }
        [data-baseweb="tab"][aria-selected="true"] {
            background: var(--brand-soft);
            color: var(--brand-dark) !important;
        }
        [data-testid="stAlert"] {
            border-radius: 0.7rem;
        }
        [data-testid="stButton"] button {
            border-radius: 0.6rem;
            font-weight: 700;
            min-height: 2.75rem;
        }
        [data-testid="stButton"] button[kind="primary"] {
            background: var(--brand);
            border-color: var(--brand);
            color: #FFFFFF;
        }
        [data-testid="stButton"] button[kind="primary"]:hover {
            background: var(--brand-dark);
            border-color: var(--brand-dark);
        }
        [data-testid="stButton"] button:not([kind="primary"]) {
            border-color: var(--border);
            color: var(--ink);
        }
        [data-testid="stButton"] button:disabled {
            background: #E2E8F0;
            border-color: #CBD5E1;
            color: #475569;
            opacity: 1;
        }
        [data-testid="stButton"] button:focus-visible,
        input:focus-visible,
        textarea:focus-visible,
        [role="combobox"]:focus-visible,
        [role="radio"]:focus-visible,
        [role="option"]:focus-visible {
            outline: 3px solid var(--focus) !important;
            outline-offset: 2px !important;
        }
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stTimeInput"] input,
        [data-testid="stSelectbox"] [data-baseweb="select"] > div,
        [data-testid="stMultiSelect"] [data-baseweb="select"] > div {
            background: var(--surface);
            border-color: var(--border);
            color: var(--ink);
        }
        [data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 0.7rem;
            overflow: hidden;
        }
        .mobile-step {
            background: var(--surface-muted);
            border-left: 3px solid var(--brand);
            border-radius: 0 0.6rem 0.6rem 0;
            margin: 0.6rem 0;
            padding: 0.75rem;
        }
        @media (max-width: 768px) {
            .block-container {
                padding: 1.15rem 0.8rem 3rem;
            }
            [data-testid="stAppViewContainer"] p,
            [data-testid="stAppViewContainer"] label,
            [data-testid="stMarkdownContainer"] {
                font-size: 1rem;
            }
            [data-testid="stAppViewContainer"] h1 {
                font-size: 1.75rem;
            }
            [data-testid="stAppViewContainer"] h2 {
                font-size: 1.35rem;
            }
            [data-testid="stHorizontalBlock"] {
                flex-direction: column;
                gap: 0.65rem;
            }
            [data-testid="stMetric"] {
                min-width: 100%;
            }
            [data-testid="stMetricValue"] {
                font-size: 1.45rem;
            }
            [data-testid="stButton"] button {
                min-height: 2.9rem;
                width: 100%;
            }
            [data-testid="stRadio"] > div {
                align-items: flex-start;
                flex-direction: column;
            }
            [data-baseweb="tab-list"] {
                overflow-x: auto;
                white-space: nowrap;
            }
            [data-testid="stDataFrame"] {
                max-width: 100%;
                overflow-x: auto;
            }
            section.main iframe {
                height: 390px !important;
                max-width: 100%;
            }
            .structural-gap-card {
                min-height: auto;
            }
        }
        @media (min-width: 769px) {
            section.main iframe {
                height: 560px !important;
            }
        }
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                scroll-behavior: auto !important;
                transition-duration: 0.01ms !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
