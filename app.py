import streamlit as st
import pandas as pd
import plotly.express as px
from database import init_db, add_actor, get_actors, get_actor, create_linkage, get_linkages, update_linkage_status, add_engagement, get_engagements, get_stats
from gemini_engine import find_matches, explain_linkage, suggest_programme_matches

st.set_page_config(page_title="EcoLink", page_icon="🔗", layout="wide")
init_db()

# --- Sidebar Navigation ---
st.sidebar.image("https://via.placeholder.com/200x60?text=EcoLink", use_container_width=True)
st.sidebar.title("EcoLink")
st.sidebar.caption("AI-Powered Ecosystem Relationship Engine")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Actors", "AI Matching", "Linkages", "Engagement History"],
    index=0
)

st.sidebar.divider()
st.sidebar.caption("Powered by Gemini 2.0 Flash")
st.sidebar.caption("Build With AI 2026 — MyHack")

# ============================================================
# PAGE: DASHBOARD
# ============================================================
if page == "Dashboard":
    st.title("EcoLink — Ecosystem Relationship Engine")
    st.caption("Automating Ecosystem Linkages | Cradle x Build With AI 2026")
    st.divider()

    stats = get_stats()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Actors", stats["total_actors"])
    col2.metric("Mentors", stats["mentors"])
    col3.metric("Companies", stats["companies"])
    col4.metric("Total Linkages", stats["total_linkages"])
    col5.metric("Avg Engagement Rating", f"{stats['avg_rating']}/5" if stats["avg_rating"] else "N/A")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Active Linkages")
        linkages = get_linkages()
        if linkages:
            active = [l for l in linkages if l["status"] == "active"]
            if active:
                df = pd.DataFrame(active)[["actor_a_name", "actor_b_name", "linkage_type", "match_score", "programme", "created_at"]]
                df.columns = ["Actor A", "Actor B", "Type", "Match Score", "Programme", "Created"]
                df["Match Score"] = df["Match Score"].apply(lambda x: f"{x:.0%}" if x else "N/A")
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No active linkages yet. Use AI Matching to create some!")
        else:
            st.info("No linkages yet.")

    with col_right:
        st.subheader("Ecosystem Overview")
        actors = get_actors()
        if actors:
            type_counts = pd.DataFrame(actors).groupby("type").size().reset_index(name="count")
            fig = px.pie(type_counts, values="count", names="type",
                         color_discrete_sequence=["#FF6B6B", "#4ECDC4", "#45B7D1"],
                         title="Actor Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add actors to see the ecosystem overview.")

    st.divider()
    st.subheader("AI Programme Overview")
    companies = get_actors("company")
    mentors = get_actors("mentor")
    programme = st.text_input("Programme Name (for AI analysis)", value="Cradle PEMULA 2026")
    if st.button("Generate AI Programme Insights", type="primary"):
        with st.spinner("Gemini is analyzing your ecosystem..."):
            summary = suggest_programme_matches(companies, mentors, programme)
            st.markdown(summary)


# ============================================================
# PAGE: ACTORS
# ============================================================
elif page == "Actors":
    st.title("Ecosystem Actors")
    st.caption("Manage companies, mentors, and partners in your ecosystem")
    st.divider()

    tab1, tab2 = st.tabs(["View Actors", "Add New Actor"])

    with tab1:
        filter_type = st.selectbox("Filter by type", ["All", "company", "mentor", "partner"])
        actor_type_filter = None if filter_type == "All" else filter_type
        actors = get_actors(actor_type_filter)

        if actors:
            for actor in actors:
                with st.expander(f"{'🏢' if actor['type']=='company' else '👤' if actor['type']=='mentor' else '🤝'} {actor['name']} — {actor['type'].capitalize()}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Industry:** {actor.get('industry', 'N/A')}")
                        st.write(f"**Location:** {actor.get('location', 'N/A')}")
                        st.write(f"**Skills/Expertise:** {', '.join(actor.get('skills', []))}")
                    with col2:
                        st.write(f"**Description:**")
                        st.write(actor.get("description", "N/A"))
        else:
            st.info("No actors found. Add some in the 'Add New Actor' tab.")

    with tab2:
        st.subheader("Add New Actor")
        with st.form("add_actor_form"):
            name = st.text_input("Name *")
            actor_type = st.selectbox("Type *", ["company", "mentor", "partner"])
            industry = st.text_input("Industry / Domain")
            location = st.text_input("Location")
            skills_input = st.text_input("Skills / Expertise (comma-separated)")
            description = st.text_area("Description", height=100)

            submitted = st.form_submit_button("Add Actor", type="primary")
            if submitted:
                if not name:
                    st.error("Name is required.")
                else:
                    skills = [s.strip() for s in skills_input.split(",") if s.strip()]
                    add_actor(name, actor_type, industry, description, skills, location)
                    st.success(f"Actor '{name}' added successfully!")
                    st.rerun()


# ============================================================
# PAGE: AI MATCHING
# ============================================================
elif page == "AI Matching":
    st.title("AI Matching Engine")
    st.caption("Powered by Google Gemini 2.0 Flash — finds the best ecosystem relationships")
    st.divider()

    st.info("**How it works:** Select a target actor, choose a candidate pool, and Gemini AI will rank the best matches with explanations and confidence scores.")

    actors = get_actors()
    if len(actors) < 2:
        st.warning("You need at least 2 actors to run matching. Go to the Actors page to add more.")
        st.stop()

    actor_names = {a["id"]: f"{a['name']} ({a['type']})" for a in actors}

    col1, col2 = st.columns(2)
    with col1:
        target_id = st.selectbox("Select Target Actor", options=list(actor_names.keys()), format_func=lambda x: actor_names[x])
    with col2:
        programme = st.text_input("Programme Context", value="Cradle Innovation Programme 2026")

    target_actor = get_actor(target_id)
    candidates = [a for a in actors if a["id"] != target_id]

    # Filter candidates to opposite type for smarter matching
    if target_actor["type"] == "company":
        smart_candidates = [a for a in candidates if a["type"] == "mentor"]
        st.caption(f"Matching against {len(smart_candidates)} mentors (smart filter applied)")
    elif target_actor["type"] == "mentor":
        smart_candidates = [a for a in candidates if a["type"] == "company"]
        st.caption(f"Matching against {len(smart_candidates)} companies (smart filter applied)")
    else:
        smart_candidates = candidates
        st.caption(f"Matching against {len(smart_candidates)} actors")

    if not smart_candidates:
        st.warning("No suitable candidates found. Add more actors of complementary types.")
        st.stop()

    if st.button("Find Best Matches with AI", type="primary", use_container_width=True):
        with st.spinner("Gemini is analyzing ecosystem relationships..."):
            results = find_matches(target_actor, smart_candidates, programme, top_n=5)

        if results and "error" not in results[0]:
            st.success(f"Found {len(results)} matches for **{target_actor['name']}**")
            st.divider()

            for i, match in enumerate(results):
                score = match.get("score", 0)
                confidence = match.get("confidence", "medium")
                bias_flag = match.get("bias_flag", False)

                score_color = "green" if score >= 0.7 else "orange" if score >= 0.4 else "red"
                conf_emoji = "🟢" if confidence == "high" else "🟡" if confidence == "medium" else "🔴"

                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.subheader(f"#{i+1} {match.get('name', 'Unknown')}")
                    with col2:
                        st.metric("Match Score", f"{score:.0%}")
                    with col3:
                        st.write(f"**Confidence:** {conf_emoji} {confidence.capitalize()}")

                    st.write(f"**Why this match:** {match.get('reason', 'N/A')}")

                    if bias_flag:
                        st.warning("Bias Flag: This actor appears frequently in top matches. Consider diversifying.")

                    # Create Linkage button
                    candidate_actor = next((a for a in smart_candidates if a["id"] == match.get("actor_id")), None)
                    if candidate_actor:
                        if st.button(f"Create Linkage with {match.get('name')}", key=f"link_{i}"):
                            linkage_type = f"{target_actor['type']}-{candidate_actor['type']}"
                            create_linkage(
                                target_actor["id"], candidate_actor["id"],
                                linkage_type, score, match.get("reason", ""), programme
                            )
                            st.success(f"Linkage created between {target_actor['name']} and {match.get('name')}!")
        else:
            error = results[0].get("error", "Unknown error") if results else "No results"
            st.error(f"Matching failed: {error}")


# ============================================================
# PAGE: LINKAGES
# ============================================================
elif page == "Linkages":
    st.title("Ecosystem Linkages")
    st.caption("First-class relationship entities — the core of EcoLink")
    st.divider()

    linkages = get_linkages()

    if not linkages:
        st.info("No linkages yet. Use the AI Matching page to create some!")
        st.stop()

    status_filter = st.selectbox("Filter by status", ["All", "active", "completed", "archived"])
    filtered = linkages if status_filter == "All" else [l for l in linkages if l["status"] == status_filter]

    for linkage in filtered:
        status_emoji = "🟢" if linkage["status"] == "active" else "✅" if linkage["status"] == "completed" else "📦"
        score = linkage.get("match_score", 0) or 0

        with st.expander(f"{status_emoji} {linkage['actor_a_name']} ↔ {linkage['actor_b_name']} | Score: {score:.0%} | {linkage['linkage_type']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Programme:** {linkage.get('programme', 'N/A')}")
                st.write(f"**Type:** {linkage['linkage_type']}")
                st.write(f"**Status:** {linkage['status'].capitalize()}")
                st.write(f"**Created:** {linkage['created_at'][:10]}")
            with col2:
                st.write(f"**Match Reason:**")
                st.write(linkage.get("match_reason", "N/A"))

            st.divider()

            # AI Linkage Explanation
            if st.button("Generate AI Linkage Analysis", key=f"explain_{linkage['id']}"):
                actor_a = get_actor(linkage["actor_a_id"])
                actor_b = get_actor(linkage["actor_b_id"])
                history = get_engagements(linkage["id"])
                with st.spinner("Gemini is analyzing this linkage..."):
                    explanation = explain_linkage(actor_a, actor_b, history)
                st.info(explanation)

            # Record Engagement
            st.subheader("Record Engagement Outcome")
            with st.form(f"engagement_form_{linkage['id']}"):
                outcome = st.selectbox("Outcome", ["successful", "partial", "unsuccessful"])
                rating = st.slider("Rating", 1, 5, 4)
                notes = st.text_area("Notes", height=80)
                if st.form_submit_button("Save Engagement"):
                    add_engagement(linkage["id"], outcome, notes, rating)
                    st.success("Engagement recorded!")
                    st.rerun()

            # Update Status
            new_status = st.selectbox("Update Status", ["active", "completed", "archived"], key=f"status_{linkage['id']}", index=["active", "completed", "archived"].index(linkage["status"]))
            if st.button("Update Status", key=f"update_{linkage['id']}"):
                update_linkage_status(linkage["id"], new_status)
                st.success("Status updated!")
                st.rerun()


# ============================================================
# PAGE: ENGAGEMENT HISTORY
# ============================================================
elif page == "Engagement History":
    st.title("Engagement History")
    st.caption("Historical data that feeds AI learning — no more starting from zero")
    st.divider()

    engagements = get_engagements()

    if not engagements:
        st.info("No engagement history yet. Record outcomes in the Linkages page.")
        st.stop()

    # Summary metrics
    df = pd.DataFrame(engagements)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Engagements", len(df))
    col2.metric("Avg Rating", f"{df['rating'].mean():.1f}/5")
    successful = len(df[df["outcome"] == "successful"])
    col3.metric("Success Rate", f"{successful/len(df):.0%}")

    st.divider()

    # Chart
    outcome_counts = df.groupby("outcome").size().reset_index(name="count")
    fig = px.bar(outcome_counts, x="outcome", y="count",
                 color="outcome",
                 color_discrete_map={"successful": "#4ECDC4", "partial": "#FFE66D", "unsuccessful": "#FF6B6B"},
                 title="Engagement Outcomes Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # Table
    st.subheader("All Engagement Records")
    display_df = df[["actor_a_name", "actor_b_name", "linkage_type", "outcome", "rating", "notes", "recorded_at"]].copy()
    display_df.columns = ["Actor A", "Actor B", "Type", "Outcome", "Rating", "Notes", "Date"]
    display_df["Date"] = display_df["Date"].str[:10]
    st.dataframe(display_df, use_container_width=True, hide_index=True)
