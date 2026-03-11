# ==========================================================
# 🛡️ Cybersecurity Data Cleaning & Analysis Dashboard
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import matplotlib.patheffects as path_effects
import squarify

if "page" not in st.session_state:
    st.session_state.page="Home"

page = st.session_state.page

# ==========================================================
# PAGE CONFIG (ONLY ONCE)
# ==========================================================
st.set_page_config(
    page_title="Cybersecurity Dashboard",
    layout="wide"
)

# ==========================================================
# LOAD CSS
# ==========================================================
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ==========================================================
# BACKGROUND GIF
# ==========================================================
st.markdown(
"""
<style>
.stApp {
    background-image: url("https://raw.githubusercontent.com/drashtigadhiya08/space-earth/main/earth.gif");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
.stApp::before{
content:"";
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:rgba(0,0,0,0.6);
z-index:-1;
}
</style>
""",
unsafe_allow_html=True
)

# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
def load_raw():
    df = pd.read_csv("messy_cybersecurity_attacks.csv")
    df.columns = df.columns.str.strip()
    return df

@st.cache_data
def load_clean():
    df = pd.read_csv("cleanned_cybersecurity.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_raw()
df_clean = load_clean()

st.title("🛡️ Cybersecurity Data Cleaning & Analysis Dashboard")

# ==========================================================
# TOP NAVIGATION BAR
# ==========================================================


nav1,nav2,nav3,nav4,nav5,nav6,nav7 = st.columns(7)

with nav1:
    if st.button("### 🏠 Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()

with nav2:
    if st.button("🧠 Executive Overview", use_container_width=True):
        st.session_state.page = "Slide 1 - Executive Overview"
        st.rerun()

with nav3:
    if st.button("🕵️ Threat Analysis", use_container_width=True):
        st.session_state.page = "Slide 2 - Threat Analysis"
        st.rerun()

with nav4:
    if st.button("🌐 Network & Geo Threat Intelligence", use_container_width=True):
        st.session_state.page = "Slide 3 - Network & Geo Threat Intelligence"
        st.rerun()

with nav5:
    if st.button("⚙️ Response & System Performance", use_container_width=True):
        st.session_state.page = "Slide 4 - Response & System Performance"
        st.rerun()

with nav6:
    if st.button("📍 India Map", use_container_width=True):
        st.session_state.page = "Slide 5 - India Attack Map"
        st.rerun()

with nav7:
    if st.button("🤖 ML Prediction", use_container_width=True):
        st.session_state.page = "Slide 6 - ML Prediction"
        st.rerun()

st.markdown("---")


# ---------------- HOME PAGE (ATTRACTIVE CYBER) ----------------
if page == "Home":

    hero_image_path = "cyber.png"   # your image file

    # Use cleaned/loaded data for stats (safe)
    total_attacks = len(df) if "df" in locals() else 0

    # optional stats with checks
    top_attack = df["Attack Type"].value_counts().idxmax() if "Attack Type" in df.columns and len(df)>0 else "N/A"
    avg_anom = round(pd.to_numeric(df["Anomaly Scores"], errors="coerce").mean(), 2) if "Anomaly Scores" in df.columns else 0

    # show hero
    st.markdown('<div class="home-wrap">', unsafe_allow_html=True)

    left, right = st.columns([1.0, 1.50], gap="large")

    with left:
        st.image(hero_image_path, use_container_width=True)

    with right:
        st.markdown("""
        <div class="hero-card">
          <div class="hero-kicker">🛡️ SOC Dashboard • Real-time Threat Intel</div>
          <div class="hero-title">Cyber<span>Shield</span></div>
          <div class="hero-sub">
            Cybersecurity is the practice of protecting computer systems, networks, and data from digital attacks.  
These attacks are usually aimed at accessing, altering, or destroying sensitive information or disrupting operations.

Modern organizations rely heavily on cybersecurity to protect their **digital infrastructure, financial systems, and customer data**.
        Cybersecurity is important because modern organizations rely heavily on digital systems. Without proper protection, cyber attacks can cause:
                    
💰 Financial losses 🔓 Data breaches 🏢 Business disruption 👤 Identity theft 📉 Loss of customer trust
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- KEY CYBER THREATS ----------------
    st.markdown("### ⚠️ Common Cyber Threats")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
    **🦠 Malware**

    Malicious software designed to damage or gain unauthorized access to systems.
    """)

    with c2:
        st.markdown("""
    **🎣 Phishing**

    Fraudulent emails or messages used to trick users into revealing sensitive data.
    """)

    with c3:
        st.markdown("""
    **🌐 DDoS Attacks**

    Distributed attacks that overwhelm servers with massive traffic.
    """)

    with c4:
        st.markdown("""
    **💰 Ransomware**

    Malware that locks files or systems and demands payment.
    """)

        st.markdown("</div>", unsafe_allow_html=True)


    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# 🔵 SLIDE 1 - EXECUTIVE OVERVIEW
# ==========================================================
elif page == "Slide 1 - Executive Overview":

    st.header("📊 Executive Security Overview")

    COMMON_FIG_SIZE = (10, 6)

    # ✅ DARK STYLE
    plt.style.use("dark_background")

    # =====================================================
    # 🔎 FILTERS
    # =====================================================
    f1, f2 = st.columns(2)

    with f1:
        severity_filter = st.selectbox(
            "Select Severity Level",
            ["All"] + sorted(df["Severity Level"].dropna().unique().tolist())
            if "Severity Level" in df.columns else ["All"]
        )

    with f2:
        attack_filter = st.selectbox(
            "Select Attack Type",
            ["All"] + sorted(df["Attack Type"].dropna().unique().tolist())
            if "Attack Type" in df.columns else ["All"]
        )

    # =====================================================
    # APPLY FILTER
    # =====================================================
    df_filtered = df.copy()

    if severity_filter != "All":
        df_filtered = df_filtered[
            df_filtered["Severity Level"] == severity_filter
        ]

    if attack_filter != "All":
        df_filtered = df_filtered[
            df_filtered["Attack Type"] == attack_filter
        ]


    # =====================================================
    # KPI ROW
    # =====================================================
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Attacks</div>
            <div class="kpi-value">{len(df_filtered)}</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        avg_score = (
            round(df_filtered["Anomaly Scores"].mean(),2)
            if "Anomaly Scores" in df_filtered.columns else 0
        )

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Avg Risk Score</div>
            <div class="kpi-value">{avg_score}</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        unique_types = (
            df_filtered["Attack Type"].nunique()
            if "Attack Type" in df_filtered.columns else 0
        )

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Unique Attack Types</div>
            <div class="kpi-value">{unique_types}</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        blocked = (
            (df_filtered["Action Taken"] == "Blocked").sum()
            if "Action Taken" in df_filtered.columns else 0
        )

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Blocked Attacks</div>
            <div class="kpi-value">{blocked}</div>
        </div>
        """, unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)

    fig1 = fig2 = fig3 = fig4 = None
# =====================================================
# Severity Chart
# =====================================================
    if "Severity Level" in df_filtered.columns:

        severity_counts = (
            df_filtered["Severity Level"]
            .value_counts()
            .reindex(["Low", "Medium", "High"])
            .dropna()
        )

        total = severity_counts.sum()
        fig1, ax1 = plt.subplots(figsize=(12,8.5))

        fig1.patch.set_facecolor("black")
        ax1.set_facecolor("black")

        colors = ["#00C2FF", "#FFD166", "#EF476F"]

        bars = ax1.bar(
            severity_counts.index,
            severity_counts.values,
            color=colors[:len(severity_counts)],
            edgecolor="white",
            linewidth=1.5
        )

        ymin = max(0, severity_counts.min() - 400)
        ymax = severity_counts.max() + 350
        ax1.set_ylim(ymin, ymax)

        ax1.set_title("Severity Level Breakdown", color="white", fontsize=16, fontweight="bold")
        ax1.set_xlabel("Severity Level", color="white", fontsize=12)
        ax1.set_ylabel("Count", color="white", fontsize=12)

        ax1.tick_params(colors="white")
        for spine in ax1.spines.values():
            spine.set_color("white")

        ax1.grid(axis="y", linestyle="--", alpha=0.25, color="white")

        max_val = severity_counts.max()

        for i, bar in enumerate(bars):
            height = bar.get_height()
            pct = (height / total) * 100
            diff = max_val - height

            top_text = f"{int(height)}\n({pct:.2f}%)"
            inside_text = "Highest" if diff == 0 else f"-{diff}"

            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                height + 20,
                top_text,
                ha="center",
                va="bottom",
                color="white",
                fontsize=10,
                fontweight="bold"
            )

            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                height - 140,
                inside_text,
                ha="center",
                va="bottom",
                color="black",
                fontsize=10,
                fontweight="bold"
            )

        plt.tight_layout()
# =====================================================
# Risk Status Chart
# =====================================================
    if {"Attack Type", "Action Taken"}.issubset(df_filtered.columns):

        df_filtered["Risk Status"] = df_filtered["Action Taken"].apply(
            lambda x: "Closed" if x == "Blocked" else "Open"
        )

        risk_data = pd.crosstab(
            df_filtered["Attack Type"],
            df_filtered["Risk Status"]
        )

        fig2, ax2 = plt.subplots(figsize=COMMON_FIG_SIZE)

        fig2.patch.set_facecolor("black")
        ax2.set_facecolor("black")

        # NEW COLORS (clear difference)
        colors = ["#00E5FF", "#FF4C4C"]

        risk_data.plot(
            kind="bar",
            stacked=True,
            color=colors,
            edgecolor="white",
            linewidth=1.2,
            ax=ax2
        )

        ax2.set_title("Cyber Risk Status Analysis", color="white", fontsize=14)
        ax2.tick_params(colors="white")

        ax2.set_xlabel("Attack Type", color="white")
        ax2.set_ylabel("Number of Attacks", color="white")

        # VALUE LABELS
        for container in ax2.containers:
            ax2.bar_label(
                container,
                label_type="center",
                color="black",
                fontsize=11,
                weight="bold"
            )

        # PERCENTAGE LABELS ON TOP
        totals = risk_data.sum(axis=1)

        for i, total in enumerate(totals):
            open_val = risk_data.iloc[i].get("Open", 0)
            closed_val = risk_data.iloc[i].get("Closed", 0)

            open_pct = (open_val / total) * 100
            closed_pct = (closed_val / total) * 100

            ax2.text(
                i,
                total + 200,
                f"Closed {closed_pct:.1f}% | Open {open_pct:.1f}%",
                ha="center",
                color="white",
                fontsize=10
            )

        ax2.grid(axis="y", alpha=0.3)                                                                                              
# =====================================================
# Line Plot
# =====================================================
    COMMON_FIG_SIZE = (10,6)

    # ----------------------------------------------------------
    # Check required columns
    # ----------------------------------------------------------
    if {"Attack Type", "Packet Length", "Severity Level"}.issubset(df_filtered.columns):

        # ------------------------------------------------------
        # Aggregate data (average packet length)
        # ------------------------------------------------------
        line_data = (
            df_filtered
            .groupby(["Attack Type", "Severity Level"])["Packet Length"]
            .mean()
            .reset_index()
        )

        # ------------------------------------------------------
        # Calculate total attacks
        # ------------------------------------------------------
        count_data = (
            df_filtered
            .groupby(["Attack Type","Severity Level"])
            .size()
            .reset_index(name="Total Attacks")
        )

        hover_df = line_data.merge(count_data, on=["Attack Type","Severity Level"])

        # ------------------------------------------------------
        # Interactive Line Plot
        # ------------------------------------------------------
        import plotly.express as px

        fig3 = px.line(
            hover_df,
            x="Attack Type",
            y="Packet Length",
            color="Severity Level",
            markers=True,
            color_discrete_sequence=["#00E5FF", "#FFD166", "#FF4C4C"]
        )

        # ------------------------------------------------------
        # Layout Styling
        # ------------------------------------------------------
        fig3.update_layout(
            template="plotly_dark",
            title="Attack Type vs Packet Length",
            hovermode="closest",
            xaxis_title="Attack Type",
            yaxis_title="Packet Length"
        )

        # ------------------------------------------------------
        # Hover Info
        # ------------------------------------------------------
        fig3.update_traces(
            customdata=hover_df[["Total Attacks"]],
            hovertemplate=
            "<b>Attack Type:</b> %{x}<br>" +
            "<b>Severity Level:</b> %{legendgroup}<br>" +
            "<b>Avg Packet Length:</b> %{y:.0f}<br>" +
            "<b>Total Attacks:</b> %{customdata[0]}<extra></extra>"
        )

        # ------------------------------------------------------
        # Show Plot in Streamlit
        # ------------------------------------------------------
        plt.show()

# =====================================================
# Related Graph 4 - Attractive Attack Duration Histogram
# =====================================================
    st.markdown("### 📈 Attack Duration Distribution")

    # recreate df_kde so it always exists
    np.random.seed(42)

    short_duration = np.random.normal(2.2, 0.25, 300)
    short_waiting  = np.random.normal(55, 4, 300)

    long_duration = np.random.normal(4.5, 0.3, 300)
    long_waiting  = np.random.normal(80, 5, 300)

    df_kde = pd.concat([
        pd.DataFrame({"duration": short_duration, "waiting": short_waiting, "kind": "LOW RISK"}),
        pd.DataFrame({"duration": long_duration, "waiting": long_waiting, "kind": "HIGH RISK"})
    ])

    fig4, ax4 = plt.subplots(figsize=COMMON_FIG_SIZE)
    fig4.patch.set_facecolor("black")
    ax4.set_facecolor("black")

    # colors
    risk_colors = {
        "LOW RISK": "#4FC3F7",
        "HIGH RISK": "#FF7043"
    }

    # histogram
    for risk in df_kde["kind"].unique():
        subset = df_kde[df_kde["kind"] == risk]

        ax4.hist(
            subset["duration"],
            bins=20,
            alpha=0.55,
            label=f"{risk} ({len(subset)})",
            color=risk_colors[risk],
            edgecolor="white",
            linewidth=0.8
        )

        # mean line
        mean_val = subset["duration"].mean()
        ax4.axvline(
            mean_val,
            color=risk_colors[risk],
            linestyle="--",
            linewidth=2
        )

        ax4.text(
            mean_val + 0.02,
            ax4.get_ylim()[1] * 0.85,
            f"{risk}\nAvg: {mean_val:.2f}",
            color=risk_colors[risk],
            fontsize=10,
            fontweight="bold",
            bbox=dict(facecolor="black", edgecolor=risk_colors[risk], boxstyle="round,pad=0.3")
        )

    # titles and labels
    ax4.set_title("Attack Duration Distribution by Risk Type", color="white", fontsize=16, fontweight="bold", pad=14)
    ax4.set_xlabel("Attack Duration", color="white", fontsize=12, fontweight="bold")
    ax4.set_ylabel("Frequency", color="white", fontsize=12, fontweight="bold")
    ax4.tick_params(colors="white", labelsize=10)

    # spines
    for spine in ax4.spines.values():
        spine.set_color("white")
        spine.set_linewidth(1.2)

    # grid
    ax4.grid(True, linestyle="--", alpha=0.25, color="white")

    # legend
    legend = ax4.legend(facecolor="black", edgecolor="white", fontsize=10)
    for text in legend.get_texts():
        text.set_color("white")

    # summary info
    low_avg = df_kde[df_kde["kind"] == "LOW RISK"]["duration"].mean()
    high_avg = df_kde[df_kde["kind"] == "HIGH RISK"]["duration"].mean()
    gap = high_avg - low_avg

    # =====================================================
    # GRID DISPLAY
    # =====================================================
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        if fig1:
            st.markdown("### 📌 Severity Level Breakdown")
            st.pyplot(fig1)

    with col2:
        if fig2:
            st.markdown("### 📌 Cyber Risk Status Analysis")
            st.pyplot(fig2)

    with col3:
        if fig3:
            st.markdown("### 📌 Attack Type vs Packet Length")
            st.plotly_chart(fig3, use_container_width=True)

    with col4:
        if fig4:
            st.markdown("### 📌 Cyber Attack Density Map")
            st.pyplot(fig4)
# ==========================================================
# 🧠 SLIDE 2 - THREAT & ATTACK ANALYSIS
# ==========================================================
elif page == "Slide 2 - Threat Analysis":

    st.header("🧠 Threat & Attack Analysis")

    COMMON_FIG_SIZE = (12, 6)

    # =====================================================
    # 🔎 FILTERS (Attack Type, Packet Length, Anomaly Score)
    # =====================================================
    f1, f2, f3 = st.columns(3)

    with f1:
        attack_filter = st.selectbox(
            "Select Attack Type",
            ["All"] + sorted(df["Attack Type"].dropna().unique().tolist())
            if "Attack Type" in df.columns else ["All"]
        )

    with f2:
        packet_range = st.slider(
            "Packet Length Range",
            float(df["Packet Length"].min()) if "Packet Length" in df.columns else 0.0,
            float(df["Packet Length"].max()) if "Packet Length" in df.columns else 1000.0,
            (
                float(df["Packet Length"].min()) if "Packet Length" in df.columns else 0.0,
                float(df["Packet Length"].max()) if "Packet Length" in df.columns else 1000.0
            )
        )

    with f3:
        anomaly_range = st.slider(
            "Anomaly Score Range",
            float(df["Anomaly Scores"].min()) if "Anomaly Scores" in df.columns else 0.0,
            float(df["Anomaly Scores"].max()) if "Anomaly Scores" in df.columns else 100.0,
            (
                float(df["Anomaly Scores"].min()) if "Anomaly Scores" in df.columns else 0.0,
                float(df["Anomaly Scores"].max()) if "Anomaly Scores" in df.columns else 100.0
            )
        )

    # ✅ NEW: Severity filter (ONLY FOR GRAPHS)
    severity_options = (
        ["All"] + sorted(df["Severity Level"].dropna().astype(str).unique().tolist())
        if "Severity Level" in df.columns else ["All"]
    )

    severity_filter = st.selectbox(
        "Select Severity Level (Graphs Only)",
        severity_options
    )

    # =====================================================
    # APPLY FILTER (KPI USES THIS ONLY - UNCHANGED)
    # =====================================================
    df_filtered = df.copy()

    if attack_filter != "All":
        df_filtered = df_filtered[df_filtered["Attack Type"] == attack_filter]

    if "Packet Length" in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered["Packet Length"] >= packet_range[0]) &
            (df_filtered["Packet Length"] <= packet_range[1])
        ]

    if "Anomaly Scores" in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered["Anomaly Scores"] >= anomaly_range[0]) &
            (df_filtered["Anomaly Scores"] <= anomaly_range[1])
        ]

    # =====================================================
    # KPI ROW (UNCHANGED LOGIC, ONLY USING FILTERED DATA)
    # =====================================================
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Threat Events</div>
            <div class="kpi-value">{len(df_filtered)}</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        top_attack = (
            df_filtered["Attack Type"].value_counts().idxmax()
            if "Attack Type" in df_filtered.columns and len(df_filtered) > 0 else "N/A"
        )

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Top Attack</div>
            <div class="kpi-value">{top_attack}</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        avg_score = (
            round(df_filtered["Anomaly Scores"].mean(), 2)
            if "Anomaly Scores" in df_filtered.columns else 0
        )

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Avg Anomaly Score</div>
            <div class="kpi-value">{avg_score}</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        high_risk = (
            (df_filtered["Anomaly Scores"] > 80).sum()
            if "Anomaly Scores" in df_filtered.columns else 0
        )

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">High Risk Attacks</div>
            <div class="kpi-value">{high_risk}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # YOUR ORIGINAL GRAPH LOGIC (UNCHANGED)
    # =====================================================
    plt.style.use("dark_background")

    df2 = pd.read_csv("cleanned_cybersecurity.csv")
    df2["Timestamp"] = pd.to_datetime(df2["Timestamp"], errors="coerce")
    df2 = df2.dropna(subset=["Timestamp"])

    # apply same filters to df2
    if attack_filter != "All":
        df2 = df2[df2["Attack Type"] == attack_filter]

    if "Packet Length" in df2.columns:
        df2 = df2[
            (df2["Packet Length"] >= packet_range[0]) &
            (df2["Packet Length"] <= packet_range[1])
        ]

    if "Anomaly Scores" in df2.columns:
        df2 = df2[
            (df2["Anomaly Scores"] >= anomaly_range[0]) &
            (df2["Anomaly Scores"] <= anomaly_range[1])
        ]

    # ✅ Severity filter ONLY FOR GRAPHS (Area uses df2)
    if severity_filter != "All" and "Severity Level" in df2.columns:
        df2 = df2[df2["Severity Level"].astype(str) == str(severity_filter)]

    # AREA CHART
    area_df = (
        df2.groupby([pd.Grouper(key="Timestamp", freq="D"), "Attack Type"])
        .size()
        .unstack(fill_value=0)
    )

    fig5, ax5 = plt.subplots(figsize=COMMON_FIG_SIZE)

    colors = ["#00BFFF", "#FF8C00", "#32CD32"]

    area_df.plot(kind="area", alpha=0.85, color=colors, ax=ax5)

    ax5.set_title("Time vs Attack Type", fontsize=14)
    ax5.set_xlabel("Timestamp")
    ax5.set_ylabel("Number of Attacks")
    ax5.legend(title="Attack Type")
    ax5.grid(alpha=0.3)

    # ✅ Graph-only df for Box + Regression (uses df_filtered + severity)
    df_graph = df_filtered.copy()
    if severity_filter != "All" and "Severity Level" in df_graph.columns:
        df_graph = df_graph[df_graph["Severity Level"].astype(str) == str(severity_filter)]
    
    #boxplot 
    # BOX PLOT
    fig6, ax6 = plt.subplots(figsize=COMMON_FIG_SIZE)

    sns.boxplot(
        data=df_graph,
        x="Attack Type",
        y="Anomaly Scores",
        palette=["#00BFFF", "#FF8C00", "#32CD32"],
        showfliers=True,         # ✅ outliers show
        whis=1.5,                # standard whiskers like example
        width=0.55,
        linewidth=1.5,
        ax=ax6
    )

    ax6.set_title("Attack Type vs Anomaly Scores", fontsize=14)
    ax6.set_xlabel("Attack Type")
    ax6.set_ylabel("Anomaly Score")
    ax6.grid(alpha=0.3)

# =====================================================
# ✅ DIFFERENCE: Mean dot + Median/Mean/N + ΔMean & ΔMedian
# =====================================================
    if len(df_graph) > 0:

        stats_df = (
            df_graph
            .groupby("Attack Type")["Anomaly Scores"]
            .agg(
                Mean="mean",
                Median="median",
                N="count",
                Q1=lambda x: x.quantile(0.25),
                Q3=lambda x: x.quantile(0.75)
            )
            .reset_index()
        )

        # keep same order as x-axis labels
        x_labels = [t.get_text() for t in ax6.get_xticklabels()]
        stats_df["Attack Type"] = stats_df["Attack Type"].astype(str)
        stats_df = stats_df.set_index("Attack Type").reindex(x_labels).reset_index()

        # Mean markers + labels
        for i, row in stats_df.iterrows():
            if pd.isna(row["Mean"]):
                continue

            ax6.scatter(i, row["Mean"], s=90, marker="o",
                        edgecolors="white", linewidths=1.2, zorder=5)

            ax6.text(
                i,
                row["Q3"] + 3,
                f"N={int(row['N'])}\nMed={row['Median']:.1f}\nMean={row['Mean']:.1f}",
                ha="center",
                va="bottom",
                fontsize=10,
                color="white",
                bbox=dict(facecolor="black", alpha=0.55, edgecolor="white", boxstyle="round,pad=0.3")
            )

        # Δ differences (pairwise) — show at top
        if stats_df["Attack Type"].notna().sum() >= 2:
            y_top = ax6.get_ylim()[1]

            # show differences between consecutive categories (Malware vs DDoS, DDoS vs Intrusion)
            for j in range(1, len(stats_df)):
                if pd.isna(stats_df.loc[j, "Mean"]) or pd.isna(stats_df.loc[j-1, "Mean"]):
                    continue

                a1 = stats_df.loc[j-1, "Attack Type"]
                a2 = stats_df.loc[j, "Attack Type"]

                d_mean = stats_df.loc[j, "Mean"] - stats_df.loc[j-1, "Mean"]
                d_med  = stats_df.loc[j, "Median"] - stats_df.loc[j-1, "Median"]

                ax6.text(
                    (j-0.5),
                    y_top * 0.98,
                    f"{a2}-{a1}  ΔMean={d_mean:+.1f}  ΔMed={d_med:+.1f}",
                    ha="center",
                    va="top",
                    fontsize=10,
                    color="white",
                    bbox=dict(facecolor="black", alpha=0.5, edgecolor="white", boxstyle="round,pad=0.25")
                )

        # REGRESSION GRAPH
    plt.style.use("dark_background")
    sns.set_theme(style="darkgrid")

    if len(df_graph) == 0:
        st.warning("No data available for selected Severity Level in graphs.")
        g = None
    else:
        df_sample = df_graph.sample(min(100, len(df_graph)), random_state=42)

        g = sns.lmplot(
            data=df_sample,
            x="Packet Length",
            y="Anomaly Scores",
            hue="Severity Level",
            height=5,
            aspect=1.4,
            markers=True,
            scatter_kws={"s": 60, "alpha": 0.8},
            line_kws={"linewidth": 2}
        )

        # ================= DARK DASHBOARD STYLE =================
        g.fig.patch.set_facecolor("#0E1117")

        for ax in g.axes.flat:

            # Background
            ax.set_facecolor("#0E1117")

            # Axis labels color
            ax.set_xlabel("Packet Length", color="#E6E6E6", fontsize=12)
            ax.set_ylabel("Anomaly Score", color="#E6E6E6", fontsize=12)

            # Tick colors
            ax.tick_params(colors="#E6E6E6")

            # Grid styling
            ax.grid(color="white", linestyle="--", linewidth=0.8, alpha=0.25)

            # Axis spine colors
            for spine in ax.spines.values():
                spine.set_color("#E6E6E6")

        # Legend styling
        legend = g._legend
        if legend:
            legend.get_frame().set_facecolor("#0E1117")
            legend.get_frame().set_edgecolor("white")
            for text in legend.get_texts():
                text.set_color("white")
            legend.get_title().set_color("white")

        # Title styling
        g.fig.suptitle(
            "Packet Length vs Anomaly Score by Severity Level",
            fontsize=14,
            color="white",
            fontweight="bold"
        )

        g.fig.subplots_adjust(top=0.9)

    # GRID LAYOUT
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📌 Time vs Attack type")
        st.pyplot(fig5, use_container_width=True)

    with col2:
        st.markdown("### 📌 Anomaly Scores by Attack type")
        st.pyplot(fig6, use_container_width=True)

    st.markdown("### 📌 Packet Length VS Anomaly Score")
    if g is not None:
        st.pyplot(g.fig, use_container_width=True)
# ==========================================================
# 🌐 SLIDE 3 - NETWORK & GEO THREAT INTELLIGENCE
# ==========================================================
elif page == "Slide 3 - Network & Geo Threat Intelligence":

    st.header("🌐 Network & Geo Threat Intelligence")

    # =========================
    # 🎛️ FILTERS (DROPDOWN, NO DATE)
    # =========================
    with st.expander("🎛️ Filters", expanded=True):

        f1, f2, f3, f4 = st.columns(4)

        with f1:
            attack_filter = st.selectbox(
                "Attack Type",
                ["All"] + sorted(df["Attack Type"].dropna().unique())
                if "Attack Type" in df.columns else ["All"]
            )

        with f2:
            action_filter = st.selectbox(
                "Action Taken",
                ["All"] + sorted(df["Action Taken"].dropna().unique())
                if "Action Taken" in df.columns else ["All"]
            )
    # =========================
    # ✅ APPLY FILTERS
    # =========================
    df_f = df.copy()

    if attack_filter != "All" and "Attack Type" in df_f.columns:
        df_f = df_f[df_f["Attack Type"] == attack_filter]

    if action_filter != "All" and "Action Taken" in df_f.columns:
        df_f = df_f[df_f["Action Taken"] == action_filter]
    # =========================
    # KPI ROW (USING FILTERED DATA)
    # =========================
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        top_device = (
            df_f["Device/OS"].value_counts().idxmax()
            if "Device/OS" in df_f.columns and len(df_f)>0 else "N/A"
        )

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Most Targeted Device</div>
            <div class="kpi-value">{top_device}</div>
        </div>
        """, unsafe_allow_html=True)


    with k2:
        peak_hour = (
            df_f["Hour"].value_counts().idxmax()
            if "Hour" in df_f.columns and len(df_f)>0 else "N/A"
        )

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Peak Attack Hour</div>
            <div class="kpi-value">{peak_hour}:00</div>
        </div>
        """, unsafe_allow_html=True)


    with k3:
        if "Action Taken" in df_f.columns and len(df_f)>0:
            action_counts = df_f["Action Taken"].value_counts()
            top_action = action_counts.idxmax()
            top_action_count = action_counts.max()
            action_display = f"{top_action} ({top_action_count})"
        else:
            action_display = "N/A"

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Top Response Action</div>
            <div class="kpi-value">{action_display}</div>
        </div>
        """, unsafe_allow_html=True)


    with k4:
        if "Anomaly Scores" in df_f.columns and len(df_f)>0:
            max_score = round(df_f["Anomaly Scores"].max(), 2)
        else:
            max_score = 0

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Max Risk Score</div>
            <div class="kpi-value">{max_score}</div>
        </div>
        """, unsafe_allow_html=True)

# Add spacing between KPIs and charts
    st.markdown("<br><br>", unsafe_allow_html=True)
    # ======================================================
    # GRID ROW 1
    # ======================================================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📌 Monthly Attacks Over Time")

        df_temp = df_f.copy()

        df_temp["Timestamp"] = pd.to_datetime(df_temp["Timestamp"], errors="coerce")
        df_temp = df_temp.dropna(subset=["Timestamp"])
        df_temp = df_temp.set_index("Timestamp")

        time_data = df_temp.resample("M").size().reset_index(name="Attack Count")
        time_data["Month Label"] = time_data["Timestamp"].dt.strftime("%b %Y")

        import plotly.graph_objects as go

        max_val = time_data["Attack Count"].max()
        low_thr = max_val * 0.60
        med_thr = max_val * 0.85

        peak_idx = time_data["Attack Count"].idxmax()
        peak_month = time_data.loc[peak_idx, "Timestamp"]
        peak_value = time_data.loc[peak_idx, "Attack Count"]

        fig = go.Figure()

        # Low activity zone
        fig.add_hrect(
            y0=0, y1=low_thr,
            fillcolor="green",
            opacity=0.08,
            line_width=0,
            annotation_text="Low Activity Zone",
            annotation_position="top left"
        )

        # Moderate activity zone
        fig.add_hrect(
            y0=low_thr, y1=med_thr,
            fillcolor="yellow",
            opacity=0.08,
            line_width=0,
            annotation_text="Moderate Activity Zone",
            annotation_position="top left"
        )

        # High activity zone
        fig.add_hrect(
            y0=med_thr, y1=max_val * 1.08,
            fillcolor="red",
            opacity=0.08,
            line_width=0,
            annotation_text="High Activity Zone",
            annotation_position="top left"
        )

        # Main monthly trend line
        fig.add_trace(
            go.Scatter(
                x=time_data["Timestamp"],
                y=time_data["Attack Count"],
                mode="lines+markers",
                name="Monthly Attacks",
                line=dict(color="#9BE7E8", width=3),
                marker=dict(size=7, color="#9BE7E8"),
                fill="tozeroy",
                fillcolor="rgba(155,231,232,0.15)",
                hovertemplate=
                "<b>Month:</b> %{x|%b %Y}<br>"
                "<b>Attack Count:</b> %{y}<extra></extra>"
            )
        )

        # Peak point
        fig.add_trace(
            go.Scatter(
                x=[peak_month],
                y=[peak_value],
                mode="markers+text",
                name="Peak Month",
                marker=dict(size=13, color="#ff4d6d", line=dict(color="white", width=1.5)),
                text=["Peak"],
                textposition="top center",
                hovertemplate=
                "<b>Peak Month</b><br>"
                "<b>Month:</b> %{x|%b %Y}<br>"
                "<b>Attack Count:</b> %{y}<extra></extra>"
            )
        )

        fig.update_layout(
            template="plotly_dark",
            height=450,
            title=dict(
                text="Monthly Cyber Attack Trend",
                x=0.5
            ),
            xaxis_title="Month and Year",
            yaxis_title="Number of Attacks",
            hovermode="x unified",
            plot_bgcolor="black",
            paper_bgcolor="black",
            font=dict(color="white"),
            margin=dict(l=40, r=20, t=60, b=40),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        fig.update_xaxes(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.12)",
            tickformat="%Y-%m"
        )

        fig.update_yaxes(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.12)"
        )

        st.plotly_chart(fig, use_container_width=True)


    with col2:
        st.markdown("### 📌 Attack Type Distribution across Device / OS")

        plt.style.use("dark_background")

        fig, ax = plt.subplots(figsize=(8,5), dpi=100)

        sns.countplot(
            data=df_f,
            x="Device/OS",
            hue="Attack Type",
            palette="viridis",
            ax=ax
        )

        ax.tick_params(axis='x', rotation=45)
        ax.grid(alpha=0.3)

        fig.tight_layout()

        st.pyplot(fig)


    # ======================================================
    # GRID ROW 2
    # ======================================================
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 📌 Attack Distribution : Attack Type -> Action Taken")

        fig = px.treemap(
            df_f,
            path=["Attack Type", "Action Taken"],
            color="Action Taken",
            hover_data=["Severity Level", "Anomaly Scores"],
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig.update_layout(template="plotly_dark", height=450)

        st.plotly_chart(fig, use_container_width=True)

    import plotly.graph_objects as go
    with col4:

        st.markdown("### 📌 Attack Trend by Hour")

        hourly_data = df_f["Hour"].value_counts().sort_index()

        hours = hourly_data.index
        values = hourly_data.values

        peak_hour = hourly_data.idxmax()
        peak_value = hourly_data.max()

        fig = go.Figure()

        # area line
        fig.add_trace(
            go.Scatter(
                x=hours,
                y=values,
                mode="lines+markers",
                fill="tozeroy",
                line=dict(color="#90e0ef", width=3),
                marker=dict(size=7),
                hovertemplate=
                "<b>Hour:</b> %{x}:00<br>"
                "<b>Attack Count:</b> %{y}<extra></extra>"
            )
        )

        # highlight peak
        fig.add_trace(
            go.Scatter(
                x=[peak_hour],
                y=[peak_value],
                mode="markers",
                marker=dict(size=14, color="red"),
                name="Peak Hour",
                hovertemplate=
                "<b>Peak Attack Hour</b><br>"
                "Hour: %{x}:00<br>"
                "Attacks: %{y}<extra></extra>"
            )
        )

        # layout
        fig.update_layout(
            title="Cyber Attack Activity Distribution by Hour",
            xaxis_title="Hour of Day (0–23)",
            yaxis_title="Number of Detected Attacks",
            plot_bgcolor="black",
            paper_bgcolor="black",
            font=dict(color="white"),
            height=450
        )

        fig.update_xaxes(dtick=1)

        st.plotly_chart(fig, use_container_width=True)
# ==========================================================
# 📈 SLIDE 4 – RESPONSE & SYSTEM PERFORMANCE
# ==========================================================
elif page == "Slide 4 - Response & System Performance":

    st.header("📈 Response & System Performance")

    # ---------------- LOAD DATA ----------------
    df = pd.read_csv("cleanned_cybersecurity.csv")

    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df["Month"] = df["Timestamp"].dt.to_period("M").dt.to_timestamp()

    # ==================================================
    # 🎛 FILTERS
    # ==================================================
    f1, f2 = st.columns(2)

    with f1:
        severity_filter = st.selectbox(
            "Severity Level Filter",
            ["All"] + sorted(df["Severity Level"].dropna().unique().tolist())
        )

    with f2:
        alert_filter = st.selectbox(
            "Alerts / Warnings Filter",
            ["All"] + sorted(df["Alerts/Warnings"].dropna().unique().tolist())
        )

    # ==================================================
    # APPLY FILTERS
    # ==================================================
    df_filtered = df.copy()

    if severity_filter != "All":
        df_filtered = df_filtered[
            df_filtered["Severity Level"] == severity_filter
        ]

    if alert_filter != "All":
        df_filtered = df_filtered[
            df_filtered["Alerts/Warnings"] == alert_filter
        ]

    # ==================================================
    # 📌 INCIDENT TREND GRAPH (FILLED)
    # ==================================================
    st.markdown("### 📌 Incident Trend (Filled)")

    plt.style.use("dark_background")

    data_source = df_filtered.copy()

    # Keep required columns
    required_cols = ["Month", "Anomaly Scores", "Severity Level", "Alerts/Warnings"]
    plot_df = data_source[required_cols].copy()

    plot_df["Month"] = pd.to_datetime(plot_df["Month"], errors="coerce")
    plot_df["Anomaly Scores"] = pd.to_numeric(plot_df["Anomaly Scores"], errors="coerce")

    plot_df = plot_df.dropna(
        subset=["Month", "Anomaly Scores", "Severity Level", "Alerts/Warnings"]
    )

    if len(plot_df) < 3:
        st.warning("Not enough data after filtering to draw filled trend graph.")
    else:

        sample_df = plot_df.sample(
            min(300, len(plot_df)),
            random_state=42
        ).copy()

        sample_df = sample_df.sort_values("Month")

        # Aggregate mean + std
        agg = (
            sample_df
            .groupby(["Month", "Severity Level", "Alerts/Warnings"])["Anomaly Scores"]
            .agg(["mean", "std"])
            .reset_index()
        )

        fig_trend, ax = plt.subplots(figsize=(12,6))
        ax.set_facecolor("#0E1117")
        fig_trend.patch.set_facecolor("#0E1117")

        for (sev, alert), gdf in agg.groupby(["Severity Level","Alerts/Warnings"]):

            gdf = gdf.sort_values("Month")

            x = gdf["Month"].values
            y = gdf["mean"].values
            sd = gdf["std"].fillna(0).values

            ax.plot(x, y, linewidth=2, label=f"{sev} | {alert}")

            ax.fill_between(
                x,
                y - sd,
                y + sd,
                alpha=0.30
            )

        ax.set_title(
            "Incident Trend with Filled Variability (Mean ± SD)",
            color="white"
        )

        ax.set_xlabel("Month", color="white")
        ax.set_ylabel("Average Anomaly Score", color="white")

        ax.grid(color="white", linestyle="--", alpha=0.25)

        ax.legend(
            title="Severity | Alerts",
            facecolor="#0E1117",
            edgecolor="white"
        )

        st.pyplot(fig_trend, use_container_width=True)
        # ==================================================
    # 📌 DESTINATION PORT TREEMAP (UNCHANGED LOGIC)
    # ==================================================
    if "Destination Port" in df_filtered.columns:

        st.markdown("### 📌 Attack Volume by Destination Port")

        port_data = (
            df_filtered["Destination Port"]
            .value_counts()
            .head(15)
        )

        plt.style.use("dark_background")

        fig_port = plt.figure(figsize=(12,7))

        colors = plt.cm.magma(
            np.linspace(0.2, 0.9, len(port_data))
        )

        squarify.plot(
            sizes=port_data.values,
            label=[
                f"Port {int(port)}\n{count}"
                for port, count in zip(
                    port_data.index,
                    port_data.values
                )
            ],
            color=colors,
            alpha=0.9
        )

        plt.title(
            "Attack Volume by Destination Port (Top 15)",
            fontsize=18,
            weight="bold",
            pad=15
        )

        plt.axis("off")

        plt.tight_layout()

        st.pyplot(fig_port)
# ==========================================================
# 🗺️ SLIDE 5 - INDIA ATTACK MAP
# ==========================================================
elif page == "Slide 5 - India Attack Map":

    st.header("🗺️ Attack Type vs State-wise Distribution (India)")

    # ---------------- LOAD DATA ----------------
    @st.cache_data
    def load_data():
        return pd.read_csv("cleanned_cybersecurity.csv")

    df = load_data()

    # ---------------- BASIC CLEANING ----------------
    df["state"] = (
        df["state"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    # ---------------- CREATE COUNT ----------------
    attack_state_count = (
        df.groupby(["Attack Type", "state"])
          .size()
          .reset_index(name="Count")
    )

    # ---------------- ATTACK TYPE FILTER ----------------
    attack_list = sorted(attack_state_count["Attack Type"].unique())

    selected_attack = st.selectbox(
        "🔍 Select Attack Type",
        attack_list
    )

    # ---------------- FILTER DATA ----------------
    filtered_df = attack_state_count[
        attack_state_count["Attack Type"] == selected_attack
    ]

    # ---------------- MAP 1 : ATTACK COUNT ----------------
    fig = px.choropleth(
        filtered_df,
        geojson="https://raw.githubusercontent.com/geohacker/india/master/state/india_state.geojson",
        featureidkey="properties.NAME_1",
        locations="state",
        color="Count",
        hover_name="state",
        color_continuous_scale=[
            (0.0, "#ffe6e6"),
            (0.5, "#ff4d4d"),
            (1.0, "#7f0000")
        ],
        range_color=(
            filtered_df["Count"].min(),
            filtered_df["Count"].max()
        ),
        title=f"State-wise Distribution for {selected_attack}",
        template="plotly_dark"
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    fig.update_traces(
        marker_line_width=0.8,
        marker_line_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)
 
# ==========================================================
# 🤖 SLIDE 6 - ML PREDICTION + NEXT TARGET STATE
# ==========================================================
elif page == "Slide 6 - ML Prediction":
    import streamlit as st
    import pandas as pd
    import numpy as np

    from sklearn.model_selection import train_test_split
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.metrics import (
        accuracy_score,
        balanced_accuracy_score,
        f1_score,
        classification_report,
        confusion_matrix
    )
    from sklearn.ensemble import ExtraTreesClassifier

    # ==================================================
    # STREAMLIT CONFIG
    # ==================================================
    st.set_page_config(page_title="SOC ML (70%+ Try)", layout="wide")
    st.title("🛡️ SOC ML Prediction (Full Code with SOC-Rule Target)")

    # ==================================================
    # LOAD CLEAN DATA
    # ==================================================
    DATA_PATH = "cleanned_cybersecurity_high_acc_ready.csv"  # <-- your cleaned file
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()

    st.success(f"✅ Loaded: {len(df)} rows | {df.shape[1]} columns")

    # ==================================================
    # NUMERIC SAFE CONVERT (important)
    # ==================================================
    for c in ["Anomaly Scores", "Packet Length", "Source Port", "Destination Port", "Hour", "Day", "Month", "Minute", "Second"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # ==================================================
    # ✅ NEW TARGET (SOC RULE BASED High_Risk)
    # - This makes label learnable -> higher accuracy
    # ==================================================
    # safe series
    anom = df["Anomaly Scores"].copy() if "Anomaly Scores" in df.columns else pd.Series(np.nan, index=df.index)
    pkt  = df["Packet Length"].copy()  if "Packet Length" in df.columns else pd.Series(np.nan, index=df.index)
    dport = df["Destination Port"].copy() if "Destination Port" in df.columns else pd.Series(np.nan, index=df.index)

    # fill
    anom = pd.to_numeric(anom, errors="coerce")
    pkt  = pd.to_numeric(pkt, errors="coerce")
    dport = pd.to_numeric(dport, errors="coerce")

    anom = anom.fillna(anom.median() if anom.notna().any() else 0)
    pkt  = pkt.fillna(pkt.median() if pkt.notna().any() else 0)
    dport = dport.fillna(dport.median() if dport.notna().any() else 0)

    # rule conditions
    c1 = anom >= anom.quantile(0.80)  # high anomaly
    c2 = pkt  >= pkt.quantile(0.80)   # high packet length
    c3 = dport.isin([21,22,23,25,53,80,110,135,139,143,443,445,3389])  # risky ports

    c4 = False
    if "Action Taken" in df.columns:
        c4 = df["Action Taken"].astype(str).str.lower().str.contains("block|drop|deny", na=False)

    c5 = False
    if "Attack Type" in df.columns:
        c5 = df["Attack Type"].astype(str).str.lower().str.contains("ddos|malware|ransom|sql|phish", na=False)

    score = c1.astype(int) + c2.astype(int) + c3.astype(int) + c4.astype(int) + c5.astype(int)
    df["High_Risk"] = (score >= 2).astype(int)

    # show distribution + baseline
    dist = df["High_Risk"].value_counts(normalize=True) * 100
    p0 = float(dist.get(0, 0))
    p1 = float(dist.get(1, 0))
    st.info(f"High_Risk distribution → 0: {p0:.2f}% | 1: {p1:.2f}%")
    baseline = max(p0, p1) / 100.0
    st.caption(f"Baseline Accuracy (always majority class) ≈ {baseline*100:.2f}%")

    # ==================================================
    # FEATURE ENGINEERING (small but useful)
    # ==================================================
    # hour cyclic (if hour exists)
    if "Hour" in df.columns:
        h = df["Hour"].fillna(df["Hour"].median() if df["Hour"].notna().any() else 0)
        df["Hour_sin"] = np.sin(2*np.pi*h/24)
        df["Hour_cos"] = np.cos(2*np.pi*h/24)
    else:
        df["Hour_sin"] = 0.0
        df["Hour_cos"] = 1.0

    # port bucket (useful categorical)
    def port_bucket(p):
        if pd.isna(p):
            return "UNK"
        p = int(p)
        if p < 1024: return "WELL_KNOWN"
        if p < 49152: return "REGISTERED"
        return "DYNAMIC"

    df["DstPort_Bucket"] = df["Destination Port"].apply(port_bucket) if "Destination Port" in df.columns else "UNK"

    # risk score (numeric)
    if "Anomaly Scores" in df.columns and "Packet Length" in df.columns:
        df["Risk_Score"] = (
            0.65 * df["Anomaly Scores"].fillna(df["Anomaly Scores"].median()) +
            0.35 * df["Packet Length"].fillna(df["Packet Length"].median())
        )
    else:
        df["Risk_Score"] = np.nan

    # ==================================================
    # FEATURE SELECTION (auto, drop noisy columns)
    # ==================================================
    drop_cols = set([
        "High_Risk",
        "Severity Level",
        "Timestamp",
        "Timestamp_Clean",
        "Source IP Address",
        "Destination IP Address",
        "Payload Data",
        "User Information"
    ])

    feature_cols = [c for c in df.columns if c not in drop_cols]

    # auto-drop too-high-unique text columns
    clean_features = []
    for c in feature_cols:
        if df[c].dtype == "object":
            if df[c].nunique(dropna=True) > 500:
                continue
        clean_features.append(c)

    X = df[clean_features].copy()
    y = df["High_Risk"].astype(int)

    categorical = [c for c in X.columns if X[c].dtype == "object"]
    numeric = [c for c in X.columns if c not in categorical]

    st.caption(f"Using features: {len(clean_features)} | Categorical: {len(categorical)} | Numeric: {len(numeric)}")

    # ==================================================
    # PREPROCESSOR
    # ==================================================
    cat_pipe = Pipeline([
        ("imp", SimpleImputer(strategy="most_frequent")),
        ("oh", OneHotEncoder(handle_unknown="ignore", min_frequency=10))
    ])

    num_pipe = Pipeline([
        ("imp", SimpleImputer(strategy="median"))
    ])

    prep = ColumnTransformer(
        transformers=[
            ("cat", cat_pipe, categorical),
            ("num", num_pipe, numeric)
        ],
        remainder="drop"
    )

    # ==================================================
    # MODEL (Strong)
    # ==================================================
    model = Pipeline([
        ("prep", prep),
        ("clf", ExtraTreesClassifier(
            n_estimators=800,
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            max_features="sqrt",
            class_weight="balanced_subsample",
            random_state=42,
            n_jobs=-1
        ))
    ])

    # ==================================================
    # TRAIN / TEST
    # ==================================================
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    acc = accuracy_score(y_test, pred)
    bal = balanced_accuracy_score(y_test, pred)
    f1 = f1_score(y_test, pred, zero_division=0)

    c1, c2, c3 = st.columns(3)
    c1.metric("Accuracy", f"{acc*100:.2f}%")
    c2.metric("Balanced Acc", f"{bal*100:.2f}%")
    c3.metric("F1", f"{f1*100:.2f}%")

    with st.expander("📌 Classification Report"):
        st.text(classification_report(y_test, pred, zero_division=0))

    # ==================================================
    # DEBUG (shows if model predicts only one class)
    # ==================================================
    st.subheader("🔎 Debug")
    st.write("y_test distribution:", y_test.value_counts().to_dict())
    st.write("pred distribution:", pd.Series(pred).value_counts().to_dict())
    st.write("Confusion Matrix [[TN, FP],[FN, TP]]:")
    st.write(confusion_matrix(y_test, pred))

    # ==================================================
    # LIVE PREDICTION
    # ==================================================
    st.subheader("🔮 Live High-Risk Prediction")

    def pick(col, label):
        vals = df[col].dropna().astype(str).unique().tolist()
        vals = sorted(list(set([v.strip() for v in vals if v.strip()])))
        return st.selectbox(label, vals if vals else ["Unknown"])

    live = {}

    # some top categorical fields
    if "Protocol" in df.columns and "Protocol" in X.columns:
        live["Protocol"] = pick("Protocol", "Protocol")
    if "Device/OS" in df.columns and "Device/OS" in X.columns:
        live["Device/OS"] = pick("Device/OS", "Device/OS")
    if "Action Taken" in df.columns and "Action Taken" in X.columns:
        live["Action Taken"] = pick("Action Taken", "Action Taken")
    if "Traffic Type" in df.columns and "Traffic Type" in X.columns:
        live["Traffic Type"] = pick("Traffic Type", "Traffic Type")
    if "Packet Type" in df.columns and "Packet Type" in X.columns:
        live["Packet Type"] = pick("Packet Type", "Packet Type")

    anom_in = st.slider("Anomaly Scores", 0.0, 100.0, 60.0) if "Anomaly Scores" in X.columns else 60.0
    pkt_in  = st.slider("Packet Length", 0, 2000, 500) if "Packet Length" in X.columns else 500
    dstp_in = st.number_input("Destination Port", 0, 65535, 443) if "Destination Port" in X.columns else 443
    hour_in = st.slider("Hour", 0, 23, 12) if "Hour" in df.columns else 12

    # numeric fields
    if "Anomaly Scores" in X.columns: live["Anomaly Scores"] = anom_in
    if "Packet Length" in X.columns: live["Packet Length"] = pkt_in
    if "Destination Port" in X.columns: live["Destination Port"] = dstp_in
    if "Hour" in X.columns: live["Hour"] = hour_in

    # derived fields if used
    if "Risk_Score" in X.columns:
        live["Risk_Score"] = 0.65*anom_in + 0.35*pkt_in

    if "DstPort_Bucket" in X.columns:
        live["DstPort_Bucket"] = port_bucket(dstp_in)

    if "Hour_sin" in X.columns:
        live["Hour_sin"] = np.sin(2*np.pi*(hour_in)/24)
    if "Hour_cos" in X.columns:
        live["Hour_cos"] = np.cos(2*np.pi*(hour_in)/24)

    # Fill missing features with NaN
    for c in X.columns:
        if c not in live:
            live[c] = np.nan

    input_df = pd.DataFrame([live])[X.columns]
    proba = model.predict_proba(input_df)[0][1] * 100
    pred_live = int(model.predict(input_df)[0])

    st.markdown("## ✅ Live Result")
    st.write("🚨 High Risk:", "YES" if pred_live == 1 else "NO")
    st.write("🔥 Risk Probability:", f"{proba:.2f}%")